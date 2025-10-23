# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.type import date_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import report_value

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "ReportDefinition",
    },
)


class ReportDefinition(proto.Message):
    r"""The definition of how a report should be run.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        dimensions (MutableSequence[google.ads.admanager_v1.types.ReportDefinition.Dimension]):
            Required. The list of dimensions to report
            on. If empty, the report will have no
            dimensions, and any metrics will be totals.
        metrics (MutableSequence[google.ads.admanager_v1.types.ReportDefinition.Metric]):
            Required. The list of metrics to report on.
            If empty, the report will have no metrics.
        filters (MutableSequence[google.ads.admanager_v1.types.ReportDefinition.Filter]):
            Optional. The filters for this report.
        time_zone_source (google.ads.admanager_v1.types.ReportDefinition.TimeZoneSource):
            Optional. Where to get the time zone for this report.
            Defaults to using the network time zone setting (PUBLISHER).
            If source is PROVIDED, the time_zone field in the report
            definition must also set a time zone.
        time_zone (str):
            Optional. If time_zone_source is PROVIDED, this is the time
            zone to use for this report. Leave empty for any other time
            zone source. Time zone in IANA format. For example,
            "America/New_York".
        currency_code (str):
            Optional. The ISO 4217 currency code for this
            report. Defaults to publisher currency code if
            not specified.
        date_range (google.ads.admanager_v1.types.ReportDefinition.DateRange):
            Required. The primary date range of this
            report.
        comparison_date_range (google.ads.admanager_v1.types.ReportDefinition.DateRange):
            Optional. The comparison date range of this
            report. If unspecified, the report won't have
            any comparison metrics.

            This field is a member of `oneof`_ ``_comparison_date_range``.
        custom_dimension_key_ids (MutableSequence[int]):
            Optional. Custom Dimension keys that represent
            CUSTOM_DIMENSION\_\* dimensions. The index of this repeated
            field corresponds to the index on each dimension. For
            example, custom_dimension_key_ids[0] describes
            CUSTOM_DIMENSION_0_VALUE_ID and CUSTOM_DIMENSION_0_VALUE.
        line_item_custom_field_ids (MutableSequence[int]):
            Optional. Custom field IDs that represent
            LINE_ITEM_CUSTOM_FIELD\_\* dimensions. The index of this
            repeated field corresponds to the index on each dimension.
            For example, line_item_custom_field_ids[0] describes
            LINE_ITEM_CUSTOM_FIELD_0_OPTION_ID and
            LINE_ITEM_CUSTOM_FIELD_0_VALUE.
        order_custom_field_ids (MutableSequence[int]):
            Optional. Custom field IDs that represent
            ORDER_CUSTOM_FIELD\_\* dimensions. The index of this
            repeated field corresponds to the index on each dimension.
            For example, order_custom_field_ids[0] describes
            ORDER_CUSTOM_FIELD_0_OPTION_ID and
            ORDER_CUSTOM_FIELD_0_VALUE.
        creative_custom_field_ids (MutableSequence[int]):
            Optional. Custom field IDs that represent
            CREATIVE_CUSTOM_FIELD\_\* dimensions. The index of this
            repeated field corresponds to the index on each dimension.
            For example, creative_custom_field_ids[0] describes
            CREATIVE_CUSTOM_FIELD_0_OPTION_ID and
            CREATIVE_CUSTOM_FIELD_0_VALUE.
        report_type (google.ads.admanager_v1.types.ReportDefinition.ReportType):
            Required. The type of this report.
        time_period_column (google.ads.admanager_v1.types.ReportDefinition.TimePeriodColumn):
            Optional. Include a time period column to introduce
            comparison columns in the report for each generated period.
            For example, set to "QUARTERS" here to have a column for
            each quarter present in the primary date range. If "PREVIOUS
            PERIOD" is specified in comparison_date_range, then each
            quarter column will also include comparison values for its
            relative previous quarter.
        flags (MutableSequence[google.ads.admanager_v1.types.ReportDefinition.Flag]):
            Optional. List of flags for this report. Used
            to flag rows in a result set based on a set of
            defined filters.
        sorts (MutableSequence[google.ads.admanager_v1.types.ReportDefinition.Sort]):
            Optional. Default sorts to apply to this
            report.
    """

    class ReportType(proto.Enum):
        r"""Supported report types.

        Values:
            REPORT_TYPE_UNSPECIFIED (0):
                Default value. This value is unused.
            HISTORICAL (1):
                Historical.
            REACH (5):
                Reach.
            PRIVACY_AND_MESSAGING (6):
                Privacy and messaging.
            AD_SPEED (13):
                Ad speed.
        """
        REPORT_TYPE_UNSPECIFIED = 0
        HISTORICAL = 1
        REACH = 5
        PRIVACY_AND_MESSAGING = 6
        AD_SPEED = 13

    class Dimension(proto.Enum):
        r"""Reporting dimensions.

        Values:
            DIMENSION_UNSPECIFIED (0):
                Default value. This value is unused.
            ACTIVE_VIEW_MEASUREMENT_SOURCE (575):
                The measurement source of a video ad.

                Corresponds to "Active View measurement source value" in the
                Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            ACTIVE_VIEW_MEASUREMENT_SOURCE_NAME (576):
                Active View measurement source localized name.

                Corresponds to "Active View measurement source" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            ADVERTISER_CREDIT_STATUS (475):
                Advertiser credit status ENUM

                Corresponds to "Advertiser credit status value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``ENUM``
            ADVERTISER_CREDIT_STATUS_NAME (476):
                Advertiser credit status locallized name

                Corresponds to "Advertiser credit status" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            ADVERTISER_DOMAIN_NAME (242):
                The domain name of the advertiser.

                Corresponds to "Advertiser domain" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            ADVERTISER_EXTERNAL_ID (228):
                The ID used in an external system for advertiser
                identification

                Corresponds to "Advertiser external ID" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            ADVERTISER_ID (131):
                The ID of an advertiser company assigned to an order

                Corresponds to "Advertiser ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``IDENTIFIER``
            ADVERTISER_LABELS (230):
                Labels applied to the advertiser can be used for either
                competitive exclusion or ad exclusion

                Corresponds to "Advertiser labels" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING_LIST``
            ADVERTISER_LABEL_IDS (229):
                Label ids applied to the advertiser can be used for either
                competitive exclusion or ad exclusion

                Corresponds to "Advertiser label IDs" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER_LIST``
            ADVERTISER_NAME (132):
                The name of an advertiser company assigned to an order

                Corresponds to "Advertiser" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            ADVERTISER_PRIMARY_CONTACT (227):
                The name of the contact associated with an advertiser
                company

                Corresponds to "Advertiser primary contact" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            ADVERTISER_STATUS (471):
                Advertiser status ENUM

                Corresponds to "Advertiser status value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            ADVERTISER_STATUS_NAME (472):
                Advertiser status locallized name

                Corresponds to "Advertiser status" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            ADVERTISER_TYPE (473):
                Advertiser type ENUM

                Corresponds to "Advertiser type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``ENUM``
            ADVERTISER_TYPE_NAME (474):
                Advertiser type locallized name

                Corresponds to "Advertiser type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            ADVERTISER_VERTICAL (580):
                The category of an advertiser, such as Arts & Entertainment
                or Travel & Tourism.

                Corresponds to "Advertiser vertical" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            ADX_PRODUCT (499):
                Classification of different Ad Exchange products.

                Corresponds to "Ad Exchange product value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            ADX_PRODUCT_NAME (500):
                Localized name of the classification of different Ad
                Exchange products.

                Corresponds to "Ad Exchange product" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AD_EXPERIENCES_TYPE (641):
                Ad experiences type.

                Corresponds to "Ad experiences value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            AD_EXPERIENCES_TYPE_NAME (642):
                Localized name of the Ad experiences type.

                Corresponds to "Ad experiences" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AD_LOCATION (390):
                Shows an ENUM value describing whether a given piece of
                publisher inventory was above (ATF) or below the fold (BTF)
                of a page.

                Corresponds to "Ad location value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            AD_LOCATION_NAME (391):
                Shows a localized string describing whether a given piece of
                publisher inventory was above (ATF) or below the fold (BTF)
                of a page.

                Corresponds to "Ad location" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AD_TECHNOLOGY_PROVIDER_DOMAIN (620):
                The domain of the ad technology provider associated with the
                bid.

                Corresponds to "Ad technology provider domain" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AD_TECHNOLOGY_PROVIDER_ID (621):
                The ID of the ad technology provider associated with the
                bid.

                Corresponds to "Ad technology provider ID" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            AD_TECHNOLOGY_PROVIDER_NAME (622):
                The name of the ad technology provider associated with the
                bid.

                Corresponds to "Ad technology provider" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AD_TYPE (497):
                Segmentation of ad types.

                Corresponds to "Ad type value" in the Ad Manager UI (when
                showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            AD_TYPE_NAME (498):
                Localized name of the ad type.

                Corresponds to "Ad type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AD_UNIT_CODE (64):
                The code of the ad unit where the ad was requested.

                Corresponds to "Ad unit code" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``, ``REACH``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_1 (65):
                The code of the first level ad unit of the ad unit where the
                ad was requested.

                Corresponds to "Ad unit code level 1" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_10 (74):
                The code of the tenth level ad unit of the ad unit where the
                ad was requested.

                Corresponds to "Ad unit code level 10" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_11 (75):
                The code of the eleventh level ad unit of the ad unit where
                the ad was requested.

                Corresponds to "Ad unit code level 11" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_12 (76):
                The code of the twelfth level ad unit of the ad unit where
                the ad was requested.

                Corresponds to "Ad unit code level 12" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_13 (77):
                The code of the thirteenth level ad unit of the ad unit
                where the ad was requested.

                Corresponds to "Ad unit code level 13" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_14 (78):
                The code of the fourteenth level ad unit of the ad unit
                where the ad was requested.

                Corresponds to "Ad unit code level 14" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_15 (79):
                The code of the fifteenth level ad unit of the ad unit where
                the ad was requested.

                Corresponds to "Ad unit code level 15" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_16 (80):
                The code of the sixteenth level ad unit of the ad unit where
                the ad was requested.

                Corresponds to "Ad unit code level 16" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_2 (66):
                The code of the second level ad unit of the ad unit where
                the ad was requested.

                Corresponds to "Ad unit code level 2" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_3 (67):
                The code of the third level ad unit of the ad unit where the
                ad was requested.

                Corresponds to "Ad unit code level 3" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_4 (68):
                The code of the fourth level ad unit of the ad unit where
                the ad was requested.

                Corresponds to "Ad unit code level 4" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_5 (69):
                The code of the fifth level ad unit of the ad unit where the
                ad was requested.

                Corresponds to "Ad unit code level 5" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_6 (70):
                The code of the sixth level ad unit of the ad unit where the
                ad was requested.

                Corresponds to "Ad unit code level 6" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_7 (71):
                The code of the seventh level ad unit of the ad unit where
                the ad was requested.

                Corresponds to "Ad unit code level 7" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_8 (72):
                The code of the eighth level ad unit of the ad unit where
                the ad was requested.

                Corresponds to "Ad unit code level 8" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_CODE_LEVEL_9 (73):
                The code of the ninth level ad unit of the ad unit where the
                ad was requested.

                Corresponds to "Ad unit code level 9" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_ID (25):
                The ID of the ad unit where the ad was requested.

                Corresponds to "Ad unit ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``, ``REACH``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_ALL_LEVEL (27):
                The full hierarchy of ad unit IDs where the ad was
                requested, from root to leaf, excluding the root ad unit ID.

                Corresponds to "Ad unit ID (all levels)" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``, ``REACH``

                Data format: ``IDENTIFIER_LIST``
            AD_UNIT_ID_LEVEL_1 (30):
                The first level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 1" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_10 (48):
                The tenth level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 10" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_11 (50):
                The eleventh level ad unit ID of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit ID level 11" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_12 (52):
                The twelfth level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 12" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_13 (54):
                The thirteenth level ad unit ID of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit ID level 13" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_14 (56):
                The fourteenth level ad unit ID of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit ID level 14" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_15 (58):
                The fifteenth level ad unit ID of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit ID level 15" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_16 (60):
                The sixteenth level ad unit ID of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit ID level 16" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_2 (32):
                The second level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 2" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_3 (34):
                The third level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 3" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_4 (36):
                The fourth level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 4" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_5 (38):
                The fifth level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 5" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_6 (40):
                The sixth level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 6" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_7 (42):
                The seventh level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 7" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_8 (44):
                The eighth level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 8" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_LEVEL_9 (46):
                The ninth level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID level 9" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_ID_TOP_LEVEL (142):
                The top-level ad unit ID of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit ID (top level)" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            AD_UNIT_NAME (26):
                The name of the ad unit where the ad was requested.

                Corresponds to "Ad unit" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``, ``REACH``

                Data format: ``STRING``
            AD_UNIT_NAME_ALL_LEVEL (29):
                The full hierarchy of ad unit names where the ad was
                requested, from root to leaf, excluding the root ad unit
                name.

                Corresponds to "Ad unit (all levels)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``, ``REACH``

                Data format: ``STRING_LIST``
            AD_UNIT_NAME_LEVEL_1 (31):
                The first level ad unit name of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit level 1" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_10 (49):
                The tenth level ad unit name of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit level 10" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_11 (51):
                The eleventh level ad unit name of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit level 11" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_12 (53):
                The twelfth level ad unit name of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit level 12" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_13 (55):
                The thirteenth level ad unit name of the ad unit where the
                ad was requested.

                Corresponds to "Ad unit level 13" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_14 (57):
                The fourteenth level ad unit name of the ad unit where the
                ad was requested.

                Corresponds to "Ad unit level 14" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_15 (59):
                The fifteenth level ad unit name of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit level 15" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_16 (61):
                The sixteenth level ad unit name of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit level 16" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_2 (33):
                The second level ad unit name of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit level 2" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_3 (35):
                The third level ad unit name of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit level 3" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_4 (37):
                The fourth level ad unit name of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit level 4" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_5 (39):
                The fifth level ad unit name of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit level 5" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_6 (41):
                The sixth level ad unit name of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit level 6" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_7 (43):
                The seventh level ad unit name of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit level 7" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_8 (45):
                The eighth level ad unit name of the ad unit where the ad
                was requested.

                Corresponds to "Ad unit level 8" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_LEVEL_9 (47):
                The ninth level ad unit name of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit level 9" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_NAME_TOP_LEVEL (143):
                The top-level ad unit name of the ad unit where the ad was
                requested.

                Corresponds to "Ad unit (top level)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AD_UNIT_REWARD_AMOUNT (63):
                The reward amount of the ad unit where the ad was requested.

                Corresponds to "Ad unit reward amount" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``, ``REACH``

                Data format: ``INTEGER``
            AD_UNIT_REWARD_TYPE (62):
                The reward type of the ad unit where the ad was requested.

                Corresponds to "Ad unit reward type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``, ``REACH``

                Data format: ``STRING``
            AD_UNIT_STATUS (206):
                The status of the ad unit

                Corresponds to "Ad unit status value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``ENUM``
            AD_UNIT_STATUS_NAME (207):
                The name of the status of the ad unit

                Corresponds to "Ad unit status" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            AGENCY_LEVEL_1_ID (565):
                The ID of an agency at level 1 of agency hierarchy.

                Corresponds to "Agency ID (Level 1)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            AGENCY_LEVEL_1_NAME (566):
                The name of an agency at level 1 of agency hierarchy.

                Corresponds to "Agency (Level 1)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AGENCY_LEVEL_2_ID (567):
                The ID of an agency at level 2 of agency hierarchy.

                Corresponds to "Agency ID (Level 2)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            AGENCY_LEVEL_2_NAME (568):
                The name of an agency at level 2 of agency hierarchy.

                Corresponds to "Agency (Level 2)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AGENCY_LEVEL_3_ID (569):
                The ID of an agency at level 3 of agency hierarchy.

                Corresponds to "Agency ID (Level 3)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            AGENCY_LEVEL_3_NAME (570):
                The name of an agency at level 3 of agency hierarchy.

                Corresponds to "Agency (Level 3)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AGE_BRACKET (508):
                User age bracket enum.

                Corresponds to "Age bracket value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            AGE_BRACKET_NAME (582):
                Localized user age bracket returned from Google Analytics.
                For example, "18-24", "25-34", "35-44", "45-54", "55-64",
                "65+".

                Corresponds to "Age bracket" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            APP_TRACKING_TRANSPARENCY_CONSENT_STATUS (442):
                Enum value for App Tracking Transparency consent status.

                Corresponds to "App Tracking Transparency consent status
                value" in the Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            APP_TRACKING_TRANSPARENCY_CONSENT_STATUS_NAME (443):
                Localized string value for App Tracking Transparency consent
                status.

                Corresponds to "App Tracking Transparency consent status" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            APP_VERSION (392):
                The app version.

                Corresponds to "App version" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AUCTION_PACKAGE_DEAL (579):
                The name of Auction Package deal

                Corresponds to "Auction package deal" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AUCTION_PACKAGE_DEAL_ID (571):
                The ID of Auction Package deal

                Corresponds to "Auction package deal ID" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            AUDIENCE_SEGMENT_ID_TARGETED (584):
                ID of targeted audience segment, including all first-party
                and third-party segments that matched the user on the
                winning line item.

                Corresponds to "Audience segment ID (targeted)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            AUDIENCE_SEGMENT_TARGETED (585):
                Name of targeted audience segment, including all first-party
                and third-party segments that matched the user on the
                winning line item.

                Corresponds to "Audience segment (targeted)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            AUTO_REFRESHED_TRAFFIC (421):
                Enum value of Auto refreshed traffic.

                Corresponds to "Auto refreshed traffic value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            AUTO_REFRESHED_TRAFFIC_NAME (422):
                Indicates if the traffic is from auto-refreshed ad requests.

                Corresponds to "Auto refreshed traffic" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            BIDDER_ENCRYPTED_ID (493):
                The encrypted version of BIDDER_ID.

                Corresponds to "Bidder encrypted ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            BIDDER_NAME (494):
                The name of the bidder.

                Corresponds to "Bidder" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            BID_RANGE (679):
                The cpm range within which a bid falls.

                Corresponds to "Bid Range" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``BID_RANGE``
            BID_REJECTION_REASON (599):
                The reason a bid was rejected.

                Corresponds to "Bid rejection reason value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            BID_REJECTION_REASON_NAME (600):
                The localized name of the reason a bid was rejected.

                Corresponds to "Bid rejection reason" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            BRANDING_TYPE (383):
                The amount of information about the Publisher's page sent to
                the buyer who purchased the impressions.

                Corresponds to "Branding type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            BRANDING_TYPE_NAME (384):
                The localized version of branding type, the amount of
                information about the Publisher's page sent to the buyer who
                purchased the impressions.

                Corresponds to "Branding type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            BROWSER_CATEGORY (119):
                Browser category.

                Corresponds to "Browser category value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``ENUM``
            BROWSER_CATEGORY_NAME (120):
                Browser category name.

                Corresponds to "Browser category" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            BROWSER_ID (235):
                The ID of the browser.

                Corresponds to "Browser ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            BROWSER_NAME (236):
                The name of the browser.

                Corresponds to "Browser" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            BUYER_NETWORK_ID (448):
                The ID of the buyer network.

                Corresponds to "Buyer network ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            BUYER_NETWORK_NAME (449):
                The name of the buyer network.

                Corresponds to "Buyer network" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CALLOUT_STATUS_CATEGORY (588):
                The callout status category in the Ads traffic navigator
                report.

                Corresponds to "Callout status category value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types:

                Data format: ``ENUM``
            CALLOUT_STATUS_CATEGORY_NAME (589):
                The callout status category name in the Ads traffic
                navigator report.

                Corresponds to "Callout status category" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``STRING``
            CARRIER_ID (369):
                Mobile carrier ID.

                Corresponds to "Carrier ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            CARRIER_NAME (368):
                Name of the mobile carrier.

                Corresponds to "Carrier" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CHANNEL (501):
                Inventory segmentation by channel.

                Corresponds to "Channel" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CHILD_NETWORK_CODE (542):
                Child Publisher Network Code

                Corresponds to "Child network code" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CHILD_NETWORK_ID (544):
                Child Publisher Network ID

                Corresponds to "Child network ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            CHILD_PARTNER_NAME (543):
                Child Partner Network Name

                Corresponds to "Child network" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CITY_ID (459):
                The criteria ID of the city in which the ad served.

                Corresponds to "City ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            CITY_NAME (452):
                The name of the city in which the ad served.

                Corresponds to "City" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            CLASSIFIED_ADVERTISER_ID (133):
                The ID of an advertiser, classified by Google, associated
                with a creative transacted

                Corresponds to "Advertiser ID (classified)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            CLASSIFIED_ADVERTISER_NAME (134):
                The name of an advertiser, classified by Google, associated
                with a creative transacted

                Corresponds to "Advertiser (classified)" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            CLASSIFIED_BRAND_ID (243):
                ID of the brand, as classified by Google,

                Corresponds to "Brand ID (classified)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            CLASSIFIED_BRAND_NAME (244):
                Name of the brand, as classified by Google,

                Corresponds to "Brand (classified)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            CONTENT_CMS_NAME (643):
                The display name of the CMS content.

                Corresponds to "Content source name" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CONTENT_CMS_VIDEO_ID (644):
                The CMS content ID of the video content.

                Corresponds to "ID of the video in the content source" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CONTENT_ID (246):
                ID of the video content served.

                Corresponds to "Content ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            CONTENT_MAPPING_PRESENCE (731):
                Content mapping presence ENUM value

                Corresponds to "Content mapping presence value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            CONTENT_MAPPING_PRESENCE_NAME (732):
                Content mapping presence name

                Corresponds to "Content mapping presence" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CONTENT_NAME (247):
                Name of the video content served.

                Corresponds to "Content" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CONTINENT (469):
                The continent in which the ad served (derived from country).

                Corresponds to "Continent value" in the Ad Manager UI (when
                showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            CONTINENT_NAME (470):
                The name of the continent in which the ad served (derived
                from country).

                Corresponds to "Continent" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            COUNTRY_CODE (466):
                The ISO code of the country in which the ad served.

                Corresponds to "Country code" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``STRING``
            COUNTRY_ID (11):
                The criteria ID of the country in which the ad served.

                Corresponds to "Country ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``IDENTIFIER``
            COUNTRY_NAME (12):
                The name of the country in which the ad served.

                Corresponds to "Country" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``STRING``
            CREATIVE_BILLING_TYPE (366):
                Enum value of creative billing type

                Corresponds to "Creative billing type value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            CREATIVE_BILLING_TYPE_NAME (367):
                Localized string value of creative billing type

                Corresponds to "Creative billing type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CREATIVE_CLICK_THROUGH_URL (174):
                Represents the click-through URL of a creative

                Corresponds to "Creative click through url" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CREATIVE_ID (138):
                The ID of a creative

                Corresponds to "Creative ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            CREATIVE_NAME (139):
                Creative name

                Corresponds to "Creative" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            CREATIVE_POLICIES_FILTERING (711):
                Creative Policies filtering.

                Corresponds to "Creative policies filtering value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            CREATIVE_POLICIES_FILTERING_NAME (712):
                Localized name of the Creative Policies filtering.

                Corresponds to "Creative policies filtering" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CREATIVE_PROTECTIONS_FILTERING (704):
                Creative Protections filtering (Publisher Blocks
                Enforcement).

                Corresponds to "Creative protections filtering value" in the
                Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            CREATIVE_PROTECTIONS_FILTERING_NAME (705):
                Localized name of the Creative Protections filtering.

                Corresponds to "Creative protections filtering" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CREATIVE_SET_ROLE_TYPE (686):
                ENUM describing whether the creative is part of a creative
                set and if so, what its role in the creative set is.

                Corresponds to "Creative set role type value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            CREATIVE_SET_ROLE_TYPE_NAME (687):
                Localized name describing whether the creative is part of a
                creative set and if so, what its role in the creative set
                is.

                Corresponds to "Creative set role type" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CREATIVE_TECHNOLOGY (148):
                Creative technology ENUM

                Corresponds to "Creative technology value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            CREATIVE_TECHNOLOGY_NAME (149):
                Creative technology locallized name

                Corresponds to "Creative technology" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CREATIVE_THIRD_PARTY_VENDOR (361):
                Third party vendor name of a creative

                Corresponds to "Creative third party vendor" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CREATIVE_TYPE (344):
                Enum value of creative type

                Corresponds to "Creative type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``ENUM``
            CREATIVE_TYPE_NAME (345):
                Localized string name of creative type

                Corresponds to "Creative type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            CREATIVE_VENDOR_ID (706):
                Creative vendor ID.

                Corresponds to "Creative vendor ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            CREATIVE_VENDOR_NAME (707):
                Name of the Creative vendor.

                Corresponds to "Creative vendor" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CREATIVE_VIDEO_REDIRECT_THIRD_PARTY (562):
                The third party where Google Ad Manager was redirected for
                the creative, based on the domain.

                Corresponds to "Creative video redirect third party" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CURATOR_ID (572):
                The ID of a Curation partner

                Corresponds to "Curation partner ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            CURATOR_NAME (573):
                The name of a Curation partner

                Corresponds to "Curation partner" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CUSTOM_EVENT_ID (737):
                Custom event ID

                Corresponds to "Custom event id" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            CUSTOM_EVENT_NAME (735):
                Custom event name

                Corresponds to "Custom event" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CUSTOM_EVENT_TYPE (736):
                Custom event type

                Corresponds to "Custom event type value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            CUSTOM_EVENT_TYPE_NAME (738):
                Localized name of the custom event type

                Corresponds to "Custom event type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            CUSTOM_SPOT_ID (423):
                The ID of an ad spot. An ad spot can be added to an ad break
                template, as well as directly targeted by a video line item.

                Corresponds to "Custom spot ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            CUSTOM_SPOT_NAME (424):
                The name of an ad spot. An ad spot can be added to an ad
                break template, as well as directly targeted by a video line
                item.

                Corresponds to "Custom spot" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DATE (3):
                Breaks down reporting data by date.

                Corresponds to "Date" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``DATE``
            DAY_OF_WEEK (4):
                Breaks down reporting data by day of the week. Monday is 1
                and 7 is Sunday.

                Corresponds to "Day of week" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            DEAL_BUYER_ID (240):
                The ID of the buyer of a deal.

                Corresponds to "Deal buyer ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            DEAL_BUYER_NAME (241):
                The name of the buyer of a deal.

                Corresponds to "Deal buyer" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DEAL_ID (436):
                Deal ID

                Corresponds to "Deal ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DEAL_NAME (437):
                Deal name

                Corresponds to "Deal" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DELIVERED_SECURE_SIGNAL_ID (309):
                The ID of the secure signals that were sent to the bidder
                who won the impression.

                Corresponds to "Secure signal ID (delivered)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            DELIVERED_SECURE_SIGNAL_NAME (310):
                The name of the secure signals that were sent to the bidder
                who won the impression.

                Corresponds to "Secure signal name (delivered)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DEMAND_CHANNEL (9):
                Demand channel.

                Corresponds to "Demand channel value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``ENUM``
            DEMAND_CHANNEL_NAME (10):
                Demand channel name.

                Corresponds to "Demand channel" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            DEMAND_SOURCE (592):
                Demand source.

                Corresponds to "Demand source value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types:

                Data format: ``ENUM``
            DEMAND_SOURCE_NAME (593):
                Demand source name.

                Corresponds to "Demand source" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``STRING``
            DEMAND_SUBCHANNEL (22):
                Demand subchannel.

                Corresponds to "Demand subchannel value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            DEMAND_SUBCHANNEL_NAME (23):
                Demand subchannel name.

                Corresponds to "Demand subchannel" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DEVICE (226):
                The device on which an ad was served.

                Corresponds to "Device value" in the Ad Manager UI (when
                showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            DEVICE_CATEGORY (15):
                The device category to which an ad is being targeted.

                Corresponds to "Device category value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``ENUM``
            DEVICE_CATEGORY_NAME (16):
                The name of the category of device (smartphone, feature
                phone, tablet, or desktop) to which an ad is being targeted.

                Corresponds to "Device category" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``STRING``
            DEVICE_MANUFACTURER_ID (525):
                Device manufacturer ID

                Corresponds to "Device manufacturer ID" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            DEVICE_MANUFACTURER_NAME (526):
                Device manufacturer name

                Corresponds to "Device manufacturer" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DEVICE_MODEL_ID (527):
                Device model ID

                Corresponds to "Device model ID" in the Ad Manager UI (when
                showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            DEVICE_MODEL_NAME (528):
                Device model name

                Corresponds to "Device model" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DEVICE_NAME (225):
                The localized name of the device on which an ad was served.

                Corresponds to "Device" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DSP_SEAT_ID (564):
                The ID of DSP Seat

                Corresponds to "DSP seat ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            DYNAMIC_ALLOCATION_TYPE (502):
                Categorization of inventory sources based on AdX dynamic
                allocation backfill type.

                Corresponds to "Dynamic allocation value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            DYNAMIC_ALLOCATION_TYPE_NAME (503):
                Localized name of the dynamic allocation type.

                Corresponds to "Dynamic allocation" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            ESP_DELIVERY (623):
                Status of Encrypted Signals for Publishers delivery.

                Corresponds to "Secure signal delivery value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            ESP_DELIVERY_NAME (624):
                Localized name of the ESP delivery status.

                Corresponds to "Secure signal delivery" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            ESP_PRESENCE (625):
                Whether Encrypted Signals for Publishers are present on the
                ad request.

                Corresponds to "Secure signal presence value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            ESP_PRESENCE_NAME (626):
                Localized name of the ESP presence status.

                Corresponds to "Secure signal presence" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            EXCHANGE_BIDDING_DEAL_ID (715):
                Exchange bidding deal ID.

                Corresponds to "Exchange bidding deal id" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            EXCHANGE_BIDDING_DEAL_TYPE (714):
                Exchange bidding deal type.

                Corresponds to "Exchange bidding deal type value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            EXCHANGE_BIDDING_DEAL_TYPE_NAME (723):
                Localized name of the exchange bidding deal type.

                Corresponds to "Exchange bidding deal type" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            EXCHANGE_THIRD_PARTY_COMPANY_ID (185):
                ID of the yield partner as classified by Google

                Corresponds to "Yield partner ID (classified)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            EXCHANGE_THIRD_PARTY_COMPANY_NAME (186):
                Name of the yield partner as classified by Google

                Corresponds to "Yield partner (classified)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            FIRST_LOOK_PRICING_RULE_ID (248):
                The ID of the first look pricing rule.

                Corresponds to "First look pricing rule ID" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            FIRST_LOOK_PRICING_RULE_NAME (249):
                The name of the first look pricing rule.

                Corresponds to "First look pricing rule" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            FIRST_PARTY_ID_STATUS (404):
                Whether a first-party user identifier was present on a given
                ad-request.

                Corresponds to "First-party ID status value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            FIRST_PARTY_ID_STATUS_NAME (405):
                The localized name of whether a first-party user identifier
                was present on a given ad-request.

                Corresponds to "First-party ID status" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            GENDER (509):
                User gender enum value returned from Google Analytics.

                Corresponds to "Gender value" in the Ad Manager UI (when
                showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            GENDER_NAME (583):
                Localized user gender returned from Google Analytics. For
                example, "male", "female".

                Corresponds to "Gender" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            GOOGLE_ANALYTICS_STREAM_ID (519):
                The ID of a Google Analytics stream. For example, web site
                or mobile app

                Corresponds to "Google Analytics stream ID" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            GOOGLE_ANALYTICS_STREAM_NAME (520):
                The name of a Google Analytics stream. For example, web site
                or mobile app.

                Corresponds to "Google Analytics stream" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            HBT_YIELD_PARTNER_ID (659):
                The ID of the header bidding trafficking yield partner.

                Corresponds to "Yield partner ID (header bidding
                trafficking)" in the Ad Manager UI (when showing API
                fields).

                Compatible with the following report types:

                Data format: ``IDENTIFIER``
            HBT_YIELD_PARTNER_NAME (660):
                The name of the header bidding trafficking yield partner.

                Corresponds to "Yield partner (header bidding trafficking)"
                in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``STRING``
            HEADER_BIDDER_INTEGRATION_TYPE (718):
                Header Bidder integration type.

                Corresponds to "Header bidder integration type value" in the
                Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            HEADER_BIDDER_INTEGRATION_TYPE_NAME (719):
                Localized name of the Header Bidder integration type.

                Corresponds to "Header bidder integration type" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            HOUR (100):
                Breaks down reporting data by hour in one day.

                Corresponds to "Hour" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            IMPRESSION_COUNTING_METHOD (577):
                Impression Counting Method ENUM.

                Corresponds to "Impression counting method value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            IMPRESSION_COUNTING_METHOD_NAME (578):
                Localized impression counting method name.

                Corresponds to "Impression counting method" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            INTERACTION_TYPE (223):
                The interaction type of an ad.

                Corresponds to "Interaction type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            INTERACTION_TYPE_NAME (224):
                The localized name of the interaction type of an ad.

                Corresponds to "Interaction type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            INTEREST (510):
                User interest returned from Google Analytics.

                Corresponds to "Interests" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            INVENTORY_FORMAT (17):
                Inventory format. The format of the ad unit (e.g, banner)
                where the ad was requested.

                Corresponds to "Inventory format value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            INVENTORY_FORMAT_NAME (18):
                Inventory format name. The format of the ad unit (e.g,
                banner) where the ad was requested.

                Corresponds to "Inventory format" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            INVENTORY_SHARE_ASSIGNMENT_ID (648):
                The ID of the inventory share assignment.

                Corresponds to "Inventory share assignment ID" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            INVENTORY_SHARE_ASSIGNMENT_NAME (649):
                The name of the inventory share assignment.

                Corresponds to "Inventory share assignment" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            INVENTORY_SHARE_OUTCOME (603):
                The result of an inventory share.

                Corresponds to "Inventory share outcome value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            INVENTORY_SHARE_OUTCOME_NAME (604):
                The localized name of the result of an inventory share.

                Corresponds to "Inventory share outcome" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            INVENTORY_SHARE_PARTNER_AD_SERVER (652):
                The partner ad server of the inventory share.

                Corresponds to "Inventory share partner ad server value" in
                the Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            INVENTORY_SHARE_PARTNER_AD_SERVER_NAME (653):
                The localized name of the partner ad server.

                Corresponds to "Inventory share partner ad server" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            INVENTORY_SHARE_TARGET_SHARE_PERCENT (654):
                The target share percent of the inventory share assignment

                Corresponds to "Partner target share percent" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            INVENTORY_SHARE_TYPE (650):
                The type of the inventory share.

                Corresponds to "Inventory share type value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            INVENTORY_SHARE_TYPE_NAME (651):
                The localized name of the inventory share type.

                Corresponds to "Inventory share type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            INVENTORY_TYPE (19):
                Inventory type. The kind of web page or device where the ad
                was requested.

                Corresponds to "Inventory type (expanded) value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            INVENTORY_TYPE_NAME (20):
                Inventory type name. The kind of web page or device where
                the ad was requested.

                Corresponds to "Inventory type (expanded)" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            IS_ADX_DIRECT (382):
                Whether traffic is Adx Direct.

                Corresponds to "Is AdX Direct" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``BOOLEAN``
            IS_CURATION_TARGETED (574):
                If curation was targeted by the buyer when buying the
                impression

                Corresponds to "Is curation targeted" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``BOOLEAN``
            IS_DROPPED (464):
                Whether the query was dropped.

                Corresponds to "Is Dropped" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``BOOLEAN``
            IS_FIRST_LOOK_DEAL (401):
                Whether traffic is First Look.

                Corresponds to "Is First Look" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``BOOLEAN``
            KEY_VALUES_ID (214):
                The Custom Targeting Value ID

                Corresponds to "Key-values ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            KEY_VALUES_NAME (215):
                The Custom Targeting Value formatted like
                ``{keyName}={valueName}``

                Corresponds to "Key-values" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            LINE_ITEM_AGENCY (663):
                The agency of the order associated with the line item.

                Corresponds to "Line item agency" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_ARCHIVED (188):
                Whether a Line item is archived.

                Corresponds to "Line item is archived" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``BOOLEAN``
            LINE_ITEM_COMPANION_DELIVERY_OPTION (204):
                Line item comanion delivery option ENUM value.

                Corresponds to "Line item companion delivery option value"
                in the Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``ENUM``
            LINE_ITEM_COMPANION_DELIVERY_OPTION_NAME (205):
                Localized line item comanion delivery option name.

                Corresponds to "Line item companion delivery option" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_COMPUTED_STATUS (250):
                The computed status of the LineItem.

                Corresponds to "Line item computed status value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``ENUM``
            LINE_ITEM_COMPUTED_STATUS_NAME (251):
                The localized name of the computed status of the LineItem.

                Corresponds to "Line item computed status" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            LINE_ITEM_CONTRACTED_QUANTITY (92):
                The contracted units bought for the Line item.

                Corresponds to "Line item contracted quantity" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``INTEGER``
            LINE_ITEM_COST_PER_UNIT (85):
                The cost per unit of the Line item.

                Corresponds to "Line item rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``MONEY``
            LINE_ITEM_COST_TYPE (212):
                Line item cost type ENUM value.

                Corresponds to "Line item cost type value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``ENUM``
            LINE_ITEM_COST_TYPE_NAME (213):
                Localized line item cost type name.

                Corresponds to "Line item cost type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            LINE_ITEM_CREATIVE_END_DATE (176):
                Represent the end date of a creative associated with line
                item

                Corresponds to "Line item creative end date" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DATE``
            LINE_ITEM_CREATIVE_ROTATION_TYPE (189):
                The creative rotation type of the LineItem.

                Corresponds to "Line item creative rotation type value" in
                the Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``ENUM``
            LINE_ITEM_CREATIVE_ROTATION_TYPE_NAME (190):
                The localized name of the creative rotation type of the
                LineItem.

                Corresponds to "Line item creative rotation type" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_CREATIVE_START_DATE (175):
                Represent the start date of a creative associated with line
                item

                Corresponds to "Line item creative start date" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DATE``
            LINE_ITEM_CURRENCY_CODE (180):
                The 3 letter currency code of the Line Item

                Corresponds to "Line item currency code" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            LINE_ITEM_DELIVERY_INDICATOR (87):
                The progress made for the delivery of the Line item.

                Corresponds to "Line item delivery indicator" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``PERCENT``
            LINE_ITEM_DELIVERY_RATE_TYPE (191):
                The delivery rate type of the LineItem.

                Corresponds to "Line item delivery rate type value" in the
                Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``ENUM``
            LINE_ITEM_DELIVERY_RATE_TYPE_NAME (192):
                The localized name of the delivery rate type of the
                LineItem.

                Corresponds to "Line item delivery rate type" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            LINE_ITEM_DISCOUNT_ABSOLUTE (195):
                The discount of the LineItem in whole units in the
                LineItem's currency code, or if unspecified the Network's
                currency code.

                Corresponds to "Line item discount (absolute)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``MONEY``
            LINE_ITEM_DISCOUNT_PERCENTAGE (196):
                The discount of the LineItem in percentage.

                Corresponds to "Line item discount (percentage)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``WHOLE_PERCENT``
            LINE_ITEM_END_DATE (81):
                The end date of the Line item.

                Corresponds to "Line item end date" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``DATE``
            LINE_ITEM_END_DATE_TIME (83):
                The end date and time of the Line item.

                Corresponds to "Line item end time" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``TIMESTAMP``
            LINE_ITEM_ENVIRONMENT_TYPE (201):
                The ENUM value of the environment a LineItem is targeting.

                Corresponds to "Line item environment type value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``ENUM``
            LINE_ITEM_ENVIRONMENT_TYPE_NAME (202):
                The localized name of the environment a LineItem is
                targeting.

                Corresponds to "Line item environment type" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_EXTERNAL_DEAL_ID (97):
                The deal ID of the Line item. Set for Programmatic Direct
                campaigns.

                Corresponds to "Line item deal ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER``
            LINE_ITEM_EXTERNAL_ID (86):
                The external ID of the Line item.

                Corresponds to "Line item external ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_FREQUENCY_CAP (256):
                The frequency cap of the Line item (descriptive string).

                Corresponds to "Line item frequency cap" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_ID (1):
                Line item ID.

                Corresponds to "Line item ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``IDENTIFIER``
            LINE_ITEM_LABELS (667):
                Line item labels.

                Corresponds to "Line item labels" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING_LIST``
            LINE_ITEM_LABEL_IDS (665):
                Line item label IDs.

                Corresponds to "Line item label IDs" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER_LIST``
            LINE_ITEM_LAST_MODIFIED_BY_APP (181):
                The application that last modified the Line Item.

                Corresponds to "Line item last modified by app" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_LIFETIME_CLICKS (95):
                The total number of clicks delivered of the lifetime of the
                Line item.

                Corresponds to "Line item lifetime clicks" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``INTEGER``
            LINE_ITEM_LIFETIME_IMPRESSIONS (94):
                The total number of impressions delivered over the lifetime
                of the Line item.

                Corresponds to "Line item lifetime impressions" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``INTEGER``
            LINE_ITEM_LIFETIME_VIEWABLE_IMPRESSIONS (96):
                The total number of viewable impressions delivered over the
                lifetime of the Line item.

                Corresponds to "Line item lifetime viewable impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``INTEGER``
            LINE_ITEM_MAKEGOOD (89):
                Whether or not the Line item is Makegood. Makegood refers to
                free inventory offered to buyers to compensate for mistakes
                or under-delivery in the original campaigns.

                Corresponds to "Line item is makegood" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``BOOLEAN``
            LINE_ITEM_NAME (2):
                Line item Name.

                Corresponds to "Line item" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            LINE_ITEM_NON_CPD_BOOKED_REVENUE (98):
                The cost of booking for the Line item (non-CPD).

                Corresponds to "Line item booked revenue (exclude CPD)" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``MONEY``
            LINE_ITEM_OPTIMIZABLE (90):
                Whether a Line item is eligible for opitimization.

                Corresponds to "Line item is optimizable" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``BOOLEAN``
            LINE_ITEM_PO_NUMBER (669):
                The PO number of the order associated with the line item.

                Corresponds to "Line item PO number" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            LINE_ITEM_PRIMARY_GOAL_TYPE (210):
                Goal type ENUM value of the primary goal of the line item.

                Corresponds to "Line item primary goal type value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``ENUM``
            LINE_ITEM_PRIMARY_GOAL_TYPE_NAME (211):
                Localized goal type name of the primary goal of the line
                item.

                Corresponds to "Line item primary goal type" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_PRIMARY_GOAL_UNITS_ABSOLUTE (93):
                The total number of impressions or clicks that are reserved
                for a line item. For line items of type BULK or
                PRICE_PRIORITY, this represents the number of remaining
                impressions reserved. If the line item has an impression cap
                goal, this represents the number of impressions or
                conversions that the line item will stop serving at if
                reached.

                Corresponds to "Line item primary goal units (absolute)" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``INTEGER``
            LINE_ITEM_PRIMARY_GOAL_UNITS_PERCENTAGE (396):
                The percentage of impressions or clicks that are reserved
                for a line item. For line items of type SPONSORSHIP, this
                represents the percentage of available impressions reserved.
                For line items of type NETWORK or HOUSE, this represents the
                percentage of remaining impressions reserved.

                Corresponds to "Line item primary goal units (percentage)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``WHOLE_PERCENT``
            LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE (208):
                Unit type ENUM value of the primary goal of the line item.

                Corresponds to "Line item primary goal unit type value" in
                the Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``ENUM``
            LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE_NAME (209):
                Localized unit type name of the primary goal of the line
                item.

                Corresponds to "Line item primary goal unit type" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_PRIORITY (24):
                The priority of this Line item as a value between 1 and 16.
                In general, a lower priority means more serving priority for
                the Line item.

                Corresponds to "Line item priority" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``INTEGER``
            LINE_ITEM_RESERVATION_STATUS (304):
                ENUM value describing the state of inventory reservation for
                the LineItem.

                Corresponds to "Line item reservation status value" in the
                Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``ENUM``
            LINE_ITEM_RESERVATION_STATUS_NAME (305):
                Localized string describing the state of inventory
                reservation for the LineItem.

                Corresponds to "Line item reservation status" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_SALESPERSON (671):
                The sales person of the order associated with the line item.

                Corresponds to "Line item salesperson" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_SECONDARY_SALESPEOPLE (673):
                The secondary sales people of the order associated with the
                line item.

                Corresponds to "Line item secondary salespeople" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING_LIST``
            LINE_ITEM_SECONDARY_TRAFFICKERS (675):
                The secondary traffickers of the order associated with the
                line item.

                Corresponds to "Line item secondary traffickers" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING_LIST``
            LINE_ITEM_START_DATE (82):
                The start date of the Line item.

                Corresponds to "Line item start date" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``DATE``
            LINE_ITEM_START_DATE_TIME (84):
                The start date and time of the Line item.

                Corresponds to "Line item start time" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``TIMESTAMP``
            LINE_ITEM_TRAFFICKER (677):
                The trafficker of the order associated with the line item.

                Corresponds to "Line item trafficker" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            LINE_ITEM_TYPE (193):
                Line item type ENUM value.

                Corresponds to "Line item type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``ENUM``
            LINE_ITEM_TYPE_NAME (194):
                Localized line item type name.

                Corresponds to "Line item type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            LINE_ITEM_UNLIMITED_END (187):
                Whether the Line item end time and end date is set to
                effectively never end.

                Corresponds to "Line item is unlimited end time" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``BOOLEAN``
            LINE_ITEM_VALUE_COST_PER_UNIT (88):
                The artificial cost per unit used by the Ad server to help
                rank inventory.

                Corresponds to "Line item value cost per unit" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``MONEY``
            LINE_ITEM_WEB_PROPERTY_CODE (179):
                The web property code used for dynamic allocation Line
                Items.

                Corresponds to "Line item web property code" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            MASTER_COMPANION_CREATIVE_ID (140):
                The ID of creative, includes regular creatives, and master
                and companions in case of creative sets

                Corresponds to "Master and Companion creative ID" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            MASTER_COMPANION_CREATIVE_NAME (141):
                Name of creative, includes regular creatives, and master and
                companions in case of creative sets

                Corresponds to "Master and Companion creative" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            MEDIATION_TYPE (701):
                Mediation type.

                Corresponds to "Mediation type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            MEDIATION_TYPE_NAME (754):
                Localized mediation type name.

                Corresponds to "Mediation type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            MEDIATION_YIELD_PARTNER_ID (661):
                The ID of the yield partner for Mediation.

                Corresponds to "Yield partner ID (mediation)" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types:

                Data format: ``IDENTIFIER``
            MEDIATION_YIELD_PARTNER_NAME (662):
                The name of the yield partner for Mediation.

                Corresponds to "Yield partner (mediation)" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``STRING``
            METRO_ID (453):
                The criteria ID of the metro area in which the ad served.

                Corresponds to "Metro ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            METRO_NAME (454):
                The name of the metro area in which the ad served.

                Corresponds to "Metro" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            MOBILE_APP_FREE (128):
                Whether the mobile app is free.

                Corresponds to "App is free" in the Ad Manager UI (when
                showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``BOOLEAN``
            MOBILE_APP_ICON_URL (129):
                URL of app icon for the mobile app.

                Corresponds to "App icon URL" in the Ad Manager UI (when
                showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            MOBILE_APP_ID (123):
                The ID of the Mobile App.

                Corresponds to "App ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``

                Data format: ``STRING``
            MOBILE_APP_NAME (127):
                The name of the mobile app.

                Corresponds to "App" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``

                Data format: ``STRING``
            MOBILE_APP_OWNERSHIP_STATUS (311):
                Ownership status of the mobile app.

                Corresponds to "App ownership status value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            MOBILE_APP_OWNERSHIP_STATUS_NAME (312):
                Ownership status of the mobile app.

                Corresponds to "App ownership status" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            MOBILE_APP_STORE (125):
                The App Store of the mobile app.

                Corresponds to "App store value" in the Ad Manager UI (when
                showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            MOBILE_APP_STORE_NAME (245):
                The localized name of the mobile app store.

                Corresponds to "App store" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            MOBILE_INVENTORY_TYPE (99):
                Mobile inventory type. Identifies whether a mobile ad came
                from a regular web page, an AMP web page, or a mobile app.
                Values match the Inventory type dimension available in the
                Overview Home dashboard. Note: Video takes precedence over
                any other value, for example, if there is an in-stream video
                impression on a desktop device, it will be attributed to
                in-stream video and not desktop web.

                Corresponds to "Inventory type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``ENUM``
            MOBILE_INVENTORY_TYPE_NAME (21):
                Mobile inventory type name. Identifies whether a mobile ad
                came from a regular web page, an AMP web page, or a mobile
                app.

                Corresponds to "Inventory type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``STRING``
            MOBILE_RENDERING_SDK (646):
                Mobile rendering SDK.

                Corresponds to "Rendering SDK value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            MOBILE_RENDERING_SDK_NAME (647):
                Localized name of the Mobile rendering SDK.

                Corresponds to "Rendering SDK" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            MOBILE_SDK_MAJOR_VERSION (692):
                The major version of the mobile SDK.

                Corresponds to "App SDK major version" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            MOBILE_SDK_MINOR_VERSION (693):
                The minor version of the mobile SDK.

                Corresponds to "App SDK minor version" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            MOBILE_SDK_VERSION_NAME (130):
                SDK version of the mobile device.

                Corresponds to "App SDK version" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            MONTH_YEAR (6):
                Breaks down reporting data by month and year.

                Corresponds to "Month and year" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            NATIVE_AD_FORMAT_ID (255):
                Native ad format ID.

                Corresponds to "Native ad format ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            NATIVE_AD_FORMAT_NAME (254):
                Native ad format name.

                Corresponds to "Native ad format" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            NATIVE_STYLE_ID (253):
                Native style ID.

                Corresponds to "Native style ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            NATIVE_STYLE_NAME (252):
                Native style name.

                Corresponds to "Native style" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            NO_FILL_REASON_CATEGORY (586):
                No fill reason category in the Ads traffic navigator report.

                Corresponds to "No fill reason category value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types:

                Data format: ``ENUM``
            NO_FILL_REASON_CATEGORY_NAME (587):
                No fill reason category name in the Ads traffic navigator
                report.

                Corresponds to "No fill reason category" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``STRING``
            OPERATING_SYSTEM_CATEGORY (117):
                Operating system category.

                Corresponds to "Operating system category value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``ENUM``
            OPERATING_SYSTEM_CATEGORY_NAME (118):
                Operating system category name.

                Corresponds to "Operating system category" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            OPERATING_SYSTEM_VERSION_ID (238):
                ID of the operating system version.

                Corresponds to "Operating system ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            OPERATING_SYSTEM_VERSION_NAME (237):
                Details of the operating system, including version.

                Corresponds to "Operating system" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            OPTIMIZATION_TYPE (639):
                Enum value of the optimization type.

                Corresponds to "Optimization type value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            OPTIMIZATION_TYPE_NAME (640):
                Localized name of the optimization type.

                Corresponds to "Optimization type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            ORDER_AGENCY (150):
                Order agency.

                Corresponds to "Order agency" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            ORDER_AGENCY_ID (151):
                Order agency ID.

                Corresponds to "Order agency ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER``
            ORDER_BOOKED_CPC (152):
                Order booked CPC.

                Corresponds to "Order booked CPC" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``INTEGER``
            ORDER_BOOKED_CPM (153):
                Order booked CPM.

                Corresponds to "Order booked CPM" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``INTEGER``
            ORDER_DELIVERY_STATUS (231):
                Order delivery status ENUM value.

                Corresponds to "Order delivery status value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            ORDER_DELIVERY_STATUS_NAME (239):
                Order delivery status localized name.

                Corresponds to "Order delivery status" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            ORDER_END_DATE (154):
                Order end date.

                Corresponds to "Order end date" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``DATE``
            ORDER_END_DATE_TIME (155):
                Order end date and time.

                Corresponds to "Order end time" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``TIMESTAMP``
            ORDER_EXTERNAL_ID (156):
                Order external ID.

                Corresponds to "Order external ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER``
            ORDER_ID (7):
                Order ID.

                Corresponds to "Order ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``IDENTIFIER``
            ORDER_LABELS (170):
                Order labels.

                Corresponds to "Order labels" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING_LIST``
            ORDER_LABEL_IDS (171):
                Order labels IDs.

                Corresponds to "Order label IDs" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER_LIST``
            ORDER_LIFETIME_CLICKS (158):
                Order lifetime clicks.

                Corresponds to "Order lifetime clicks" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``INTEGER``
            ORDER_LIFETIME_IMPRESSIONS (159):
                Order lifetime impressions.

                Corresponds to "Order lifetime impressions" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``INTEGER``
            ORDER_NAME (8):
                Order name.

                Corresponds to "Order" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            ORDER_PO_NUMBER (160):
                Order PO number.

                Corresponds to "Order PO number" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``STRING``
            ORDER_PROGRAMMATIC (157):
                Whether the Order is programmatic.

                Corresponds to "Order is programmatic" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``BOOLEAN``
            ORDER_SALESPERSON (161):
                Order sales person.

                Corresponds to "Order salesperson" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            ORDER_SALESPERSON_ID (629):
                Order sales person ID.

                Corresponds to "Order salesperson ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER``
            ORDER_SECONDARY_SALESPEOPLE (164):
                Order secondary sales people.

                Corresponds to "Order secondary salespeople" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING_LIST``
            ORDER_SECONDARY_SALESPEOPLE_ID (165):
                Order secondary sales people ID.

                Corresponds to "Order secondary salespeople ID" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER_LIST``
            ORDER_SECONDARY_TRAFFICKERS (166):
                Order secondary traffickers.

                Corresponds to "Order secondary traffickers" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING_LIST``
            ORDER_SECONDARY_TRAFFICKERS_ID (167):
                Order secondary traffickers ID.

                Corresponds to "Order secondary trafficker IDs" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER_LIST``
            ORDER_START_DATE (168):
                Order start date.

                Corresponds to "Order start date" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``DATE``
            ORDER_START_DATE_TIME (169):
                Order start date and time.

                Corresponds to "Order start time" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``AD_SPEED``

                Data format: ``TIMESTAMP``
            ORDER_TRAFFICKER (162):
                Order trafficker.

                Corresponds to "Order trafficker" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            ORDER_TRAFFICKER_ID (163):
                Order trafficker ID.

                Corresponds to "Order trafficker ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER``
            ORDER_UNLIMITED_END (203):
                Whether the Order end time and end date is set to
                effectively never end.

                Corresponds to "Order is unlimited end time" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``BOOLEAN``
            PAGE_PATH (511):
                Page path is the part of a page URL that comes after the
                domain but before the query strings from Google Analytics.

                Corresponds to "Page path" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PAGE_TITLE_AND_SCREEN_CLASS (512):
                Page title (web) and screen class (mobile) returned from
                Google Analytics.

                Corresponds to "Page title and screen class" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PAGE_TITLE_AND_SCREEN_NAME (513):
                Page title (web) and screen name (mobile) returned from
                Google Analytics.

                Corresponds to "Page title and screen name" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PLACEMENT_ID (113):
                Placement ID

                Corresponds to "Placement ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER``
            PLACEMENT_ID_ALL (144):
                The full list of placement IDs associated with the ad unit.

                Corresponds to "Placement ID (all)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``IDENTIFIER_LIST``
            PLACEMENT_NAME (114):
                Placement name

                Corresponds to "Placement" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            PLACEMENT_NAME_ALL (145):
                The full list of placement names associated with the ad
                unit.

                Corresponds to "Placement (all)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING_LIST``
            PLACEMENT_STATUS (362):
                Placement status ENUM value

                Corresponds to "Placement status value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            PLACEMENT_STATUS_NAME (364):
                Localized placement status name.

                Corresponds to "Placement status" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PLACEMENT_STATUS_NAME_ALL (365):
                The full list of localized placement status names associated
                with the ad unit.

                Corresponds to "Placement status (all)" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING_LIST``
            POSTAL_CODE_ID (455):
                The criteria ID of the postal code in which the ad served.

                Corresponds to "Postal code ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``IDENTIFIER``
            POSTAL_CODE_NAME (456):
                The name of the postal code in which the ad served.

                Corresponds to "Postal code" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            PPID_STATUS (406):
                Indicates the valid PPID (Publisher provided identifier)
                status on a given ad request.

                Corresponds to "PPID status value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            PPID_STATUS_NAME (407):
                The localized name of that indicates the valid PPID
                (Publisher provided identifier) status on a given ad
                request.

                Corresponds to "PPID status" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PREDICTED_VIEWABILITY_BUCKET (633):
                Predicted viewability score bucket.

                Corresponds to "Predicted viewability bucket value" in the
                Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            PREDICTED_VIEWABILITY_BUCKET_NAME (634):
                The localized name of the predicted viewability score
                bucket.

                Corresponds to "Predicted viewability bucket" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PRESENTED_SECURE_SIGNAL_ID (495):
                The ID of the secure signals sent in the ad request.

                Corresponds to "Secure signal ID (presented)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            PRESENTED_SECURE_SIGNAL_NAME (496):
                The name of the secure signals sent in the ad request.

                Corresponds to "Secure signal name (presented)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PRIMARY_PERSONALIZATION_ID_TYPE (408):
                The ID type selected for personalization.

                Corresponds to "Primary personalization ID type value" in
                the Ad Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            PRIMARY_PERSONALIZATION_ID_TYPE_NAME (409):
                The localized name of the ID type selected for
                personalization.

                Corresponds to "Primary personalization ID type" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PROGRAMMATIC_BUYER_ID (240):
                Deprecated. Dimension has been renamed to ``DEAL_BUYER_ID``.
                The server will normalize any requests using this value to
                ``DEAL_BUYER_ID``. This value will be removed on or after
                October 10, 2025.
            PROGRAMMATIC_BUYER_NAME (241):
                Deprecated. Dimension has been renamed to
                ``DEAL_BUYER_NAME``. The server will normalize any requests
                using this value to ``DEAL_BUYER_NAME``. This value will be
                removed on or after October 10, 2025.
            PROGRAMMATIC_CHANNEL (13):
                Programmatic channel. The type of transaction that occurred
                in Ad Exchange.

                Corresponds to "Programmatic channel value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            PROGRAMMATIC_CHANNEL_NAME (14):
                Programmatic channel name. The type of transaction that
                occurred in Ad Exchange.

                Corresponds to "Programmatic channel" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``

                Data format: ``STRING``
            PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_EXTERNAL_CODE (410):
                External code ID of a publisher provided signal (all
                levels).

                Corresponds to "Publisher provided signals external code
                (all levels)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_IDS (546):
                The ancestor chain of IDs of a publisher provided signal
                (all levels).

                Corresponds to "Publisher provided signals ID (all levels)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER_LIST``
            PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_NAME (412):
                The ancestor chain of names of a publisher provided signal
                (all levels).

                Corresponds to "Publisher provided signals (all levels)" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING_LIST``
            PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_TIER (413):
                Tier of a publisher provided signal (all levels).

                Corresponds to "Publisher provided signals tier (all
                levels)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_TYPE (414):
                Type of a publisher provided signal (all levels).

                Corresponds to "Publisher provided signals type (all
                levels)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PUBLISHER_PROVIDED_SIGNALS_DELIVERED_EXTERNAL_CODE (425):
                External code ID of a publisher provided signal (delivered).

                Corresponds to "Publisher provided signals external code
                (delivered)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PUBLISHER_PROVIDED_SIGNALS_DELIVERED_IDS (545):
                The ancestor chain of IDs of a publisher provided signal
                (delivered).

                Corresponds to "Publisher provided signals ID (delivered)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER_LIST``
            PUBLISHER_PROVIDED_SIGNALS_DELIVERED_NAME (427):
                The ancestor chain of names of a publisher provided signal
                (delivered).

                Corresponds to "Publisher provided signals (delivered)" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING_LIST``
            PUBLISHER_PROVIDED_SIGNALS_DELIVERED_TIER (428):
                Tier of a publisher provided signal (delivered).

                Corresponds to "Publisher provided signals tier (delivered)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            PUBLISHER_PROVIDED_SIGNALS_DELIVERED_TYPE (429):
                Type of a publisher provided signal (delivered).

                Corresponds to "Publisher provided signals type (delivered)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_EXTERNAL_CODE (415):
                External code ID of a publisher provided signal (top level).

                Corresponds to "Publisher provided signals external code
                (top level)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_ID (416):
                ID of a publisher provided signal (top level).

                Corresponds to "Publisher provided signals ID (top level)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_NAME (417):
                Name of a publisher provided signal (top level).

                Corresponds to "Publisher provided signals (top level)" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING_LIST``
            PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_TIER (418):
                Tier of a publisher provided signal (top level).

                Corresponds to "Publisher provided signals tier (top level)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_TYPE (419):
                Type of a publisher provided signal (top level).

                Corresponds to "Publisher provided signals type (top level)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            PUBLISHER_PROVIDED_SIGNAL_DATA_PROVIDER_ID (136):
                Data provider ID associated with a publisher provided
                signal.

                Corresponds to "Publisher provided signals (data provider
                ID)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            PUBLISHER_PROVIDED_SIGNAL_DATA_PROVIDER_NAME (137):
                Data provider name associated with a publisher provided
                signal.

                Corresponds to "Publisher provided signals (data provider)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            REGION_ID (457):
                The criteria ID of the region (for example, US state) in
                which the ad served.

                Corresponds to "Region ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``IDENTIFIER``
            REGION_NAME (458):
                The name of the region (for example, US state) in which the
                ad served.

                Corresponds to "Region" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``, ``AD_SPEED``

                Data format: ``STRING``
            REJECTION_CLASS_CATEGORY (590):
                The rejection class category in the Ads traffic navigator
                report.

                Corresponds to "Rejection class category value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types:

                Data format: ``ENUM``
            REJECTION_CLASS_CATEGORY_NAME (591):
                The rejection class category name in the Ads traffic
                navigator report.

                Corresponds to "Rejection class category" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``STRING``
            RENDERED_CREATIVE_SIZE (343):
                The size of a rendered creative, It can differ with the
                creative's size if a creative is shown in an ad slot of a
                different size.

                Corresponds to "Rendered creative size" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            REQUESTED_AD_SIZES (352):
                Inventory Requested Ad Sizes dimension

                Corresponds to "Requested ad sizes" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            REQUEST_TYPE (146):
                Request type ENUM

                Corresponds to "Request type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``ENUM``
            REQUEST_TYPE_NAME (147):
                Request type locallized name

                Corresponds to "Request type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``AD_SPEED``

                Data format: ``STRING``
            SERVER_SIDE_UNWRAPPING_ELIGIBLE (597):
                Indicates if a request was eligible for server-side
                unwrapping.

                Corresponds to "Server-side unwrapping eligible" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``BOOLEAN``
            SERVING_RESTRICTION (631):
                The serving restriction mode for privacy.

                Corresponds to "Serving restriction value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            SERVING_RESTRICTION_NAME (632):
                The localized name of the serving restriction mode for
                privacy.

                Corresponds to "Serving restriction" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            SITE (387):
                Information about domain or subdomains.

                Corresponds to "Site" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``

                Data format: ``STRING``
            TARGETING_ID (232):
                The ID of the browser, device or other environment into
                which a line item or creative was served.

                Corresponds to "Targeting ID" in the Ad Manager UI (when
                showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            TARGETING_NAME (233):
                Information about the browser, device and other environments
                into which a line item or creative was served.

                Corresponds to "Targeting" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            TARGETING_TYPE (385):
                The way in which advertisers targeted their ads.

                Corresponds to "Targeting type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            TARGETING_TYPE_NAME (386):
                The localized name of the way in which advertisers targeted
                their ads.

                Corresponds to "Targeting type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            THIRD_PARTY_ID_STATUS (402):
                Whether a third-party cookie or device ID was present on a
                given ad request.

                Corresponds to "Third-party ID status value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            THIRD_PARTY_ID_STATUS_NAME (403):
                The localized name of whether a third-party cookie or device
                ID was present on a given ad request.

                Corresponds to "Third-party ID status" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            TOPICS_STATUS (504):
                Reports the status of Topics in the ad request.

                Corresponds to "Topics status value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            TOPICS_STATUS_NAME (505):
                The localized name of the status of Topics in the ad
                request.

                Corresponds to "Topics status" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            TOP_PRIVATE_DOMAIN (444):
                Inventory top private domain dimension

                Corresponds to "Domain" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``PRIVACY_AND_MESSAGING``

                Data format: ``STRING``
            TRAFFIC_SOURCE (388):
                Inventory Traffic source dimension

                Corresponds to "Traffic source value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            TRAFFIC_SOURCE_NAME (389):
                Inventory Traffic source dimension name

                Corresponds to "Traffic source" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            UNIFIED_PRICING_RULE_ID (393):
                Unified pricing rule ID dimension

                Corresponds to "Unified pricing rule ID" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            UNIFIED_PRICING_RULE_NAME (394):
                Unified pricing rule name dimension

                Corresponds to "Unified pricing rule" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            URL (506):
                A URL defined under a publisher's inventory.

                Corresponds to "URL" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            URL_ID (507):
                A URL defined under a publisher's inventory.

                Corresponds to "URL ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            USER_MESSAGES_ENTITLEMENT_SOURCE (635):
                Enum value for the entitlement source.

                Corresponds to "Entitlement source value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``ENUM``
            USER_MESSAGES_ENTITLEMENT_SOURCE_NAME (636):
                The localized name of the entitlement source.

                Corresponds to "Entitlement source" in the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``STRING``
            USER_MESSAGES_OPERATING_SYSTEM_CRITERIA_ID (637):
                Targeting criteria ID for the operating system group. Used
                for User Messages reports.

                Corresponds to "Operating system group ID" in the Ad Manager
                UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_OPERATING_SYSTEM_CRITERIA_NAME (638):
                The name of the operating system group. Used for User
                Messages reports.

                Corresponds to "Operating system group" in the Ad Manager
                UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``STRING``
            VAST_VERSION (554):
                The VAST version of the creative that is returned for an ad
                request.

                Corresponds to "Vast version value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VAST_VERSION_NAME (555):
                The localized name of the VAST version of the creative that
                is returned for an ad request.

                Corresponds to "Vast version" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_AD_BREAK_TYPE (556):
                The break type of a video ad request.

                Corresponds to "Video ad break type value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VIDEO_AD_BREAK_TYPE_NAME (557):
                The localized name of the break type of a video ad request.

                Corresponds to "Video ad break type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_AD_DURATION (450):
                Video ad duration

                Corresponds to "Video ad duration" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_AD_FORMATS_RULE (561):
                The name of the video ad formats rule used to control the ad
                formats eligible for your inventory.

                Corresponds to "Video ad formats rule" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_AD_FORMATS_RULE_ID (560):
                The ID of the video ad formats rule used to control the ad
                formats eligible for your inventory.

                Corresponds to "Video ad formats rule ID" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            VIDEO_AD_REQUEST_DURATION (558):
                The duration of a video ad request.

                Corresponds to "Video ad request duration value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VIDEO_AD_REQUEST_DURATION_MIDPOINT_NAME (751):
                The localized name of the midpoint of the duration of a
                video ad request.

                Corresponds to "Video ad request duration midpoint" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_AD_REQUEST_DURATION_NAME (559):
                The localized name of the duration of a video ad request.

                Corresponds to "Video ad request duration" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_AD_REQUEST_SOURCE (438):
                The video ad request source enum.

                Corresponds to "Ad request source value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VIDEO_AD_REQUEST_SOURCE_NAME (439):
                The localized name of the video ad request source.

                Corresponds to "Ad request source" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_AD_TYPE (432):
                Video ad type

                Corresponds to "Video ad type value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VIDEO_AD_TYPE_NAME (433):
                Video ad type localized name

                Corresponds to "Video ad type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_CONTINUOUS_PLAY_TYPE (721):
                The continuous play type of the video ad impression.

                Corresponds to "Video continuous play type value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VIDEO_CONTINUOUS_PLAY_TYPE_NAME (722):
                Video continuous play type localized name.

                Corresponds to "Video continuous play type" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_FALLBACK_POSITION (530):
                Fallback position of the video ad.

                Corresponds to "Fallback position" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_MEASUREMENT_SOURCE (601):
                The performance of the video ad inventory broken out by
                source.

                Corresponds to "Video measurement source value" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VIDEO_MEASUREMENT_SOURCE_NAME (602):
                Video measurement source localized name.

                Corresponds to "Video measurement source" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_PLCMT (172):
                The video placement enum as defined by ADCOM 1.0-202303.

                Corresponds to "Video placement value (new)" in the Ad
                Manager UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VIDEO_PLCMT_NAME (173):
                The localized name of the video placement as defined by
                ADCOM 1.0-202303.

                Corresponds to "Video placement (new)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_POSITION_IN_POD (538):
                The position in the video pod. For example 0, 1, 2, etc.

                Corresponds to "Position in pod" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_POSITION_OF_POD (539):
                The position of the pod in the video stream. For example
                pre-roll, mid-roll, post-roll.

                Corresponds to "Position of pod" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_SDK_VERSION (440):
                The video SDK version enum.

                Corresponds to "Video SDK version value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VIDEO_SDK_VERSION_NAME (441):
                The localized name of the video SDK version.

                Corresponds to "Video SDK version" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            VIDEO_STITCHER_TYPE (752):
                Video stitcher type.

                Corresponds to "Video stitcher type value" in the Ad Manager
                UI (when showing API fields).

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``ENUM``
            VIDEO_STITCHER_TYPE_NAME (753):
                Localized name of the video stitcher type.

                Corresponds to "Video stitcher type" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            WEEK (5):
                Breaks down reporting data by week of the year.

                Corresponds to "Week" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``,
                ``REACH``, ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            YIELD_GROUP_BUYER_NAME (184):
                Name of the company within a yield group

                Corresponds to "Yield partner" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            YIELD_GROUP_BUYER_TAG_NAME (627):
                Tag of the company within a yield group.

                Corresponds to "Yield group buyer tag" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            YIELD_GROUP_ID (182):
                ID of the group of ad networks or exchanges used for
                Mediation and Open Bidding

                Corresponds to "Yield group ID" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``IDENTIFIER``
            YIELD_GROUP_NAME (183):
                Name of the group of ad networks or exchanges used for
                Mediation and Open Bidding

                Corresponds to "Yield group" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``STRING``
            YOUTUBE_AD_DURATION_BUCKET (430):
                YouTube instream ad duration bucket.

                Corresponds to "Ad duration value" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types:

                Data format: ``ENUM``
            YOUTUBE_AD_DURATION_BUCKET_NAME (431):
                YouTube instream ad duration bucket name.

                Corresponds to "Ad duration" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``STRING``
            YOUTUBE_AD_TYPE (399):
                YouTube instream Ad Type.

                Corresponds to "YouTube ad type ID" in the Ad Manager UI
                (when showing API fields).

                Compatible with the following report types:

                Data format: ``ENUM``
            YOUTUBE_AD_TYPE_NAME (400):
                YouTube instream Ad Type locallized name.

                Corresponds to "YouTube ad type" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``STRING``
            LINE_ITEM_CUSTOM_FIELD_0_OPTION_ID (10000):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 0 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_1_OPTION_ID (10001):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 1 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_2_OPTION_ID (10002):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 2 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_3_OPTION_ID (10003):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 3 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_4_OPTION_ID (10004):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 4 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_5_OPTION_ID (10005):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 5 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_6_OPTION_ID (10006):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 6 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_7_OPTION_ID (10007):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 7 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_8_OPTION_ID (10008):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 8 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_9_OPTION_ID (10009):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 9 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_10_OPTION_ID (10010):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 10 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_11_OPTION_ID (10011):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 11 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_12_OPTION_ID (10012):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 12 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_13_OPTION_ID (10013):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 13 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_14_OPTION_ID (10014):
                Custom field option ID for Line Item with custom field ID
                equal to the ID in index 14 of
                ``ReportDefinition.line_item_custom_field_ids``.
            LINE_ITEM_CUSTOM_FIELD_0_VALUE (11000):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 0 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 0 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_1_VALUE (11001):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 1 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_2_VALUE (11002):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 2 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_3_VALUE (11003):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 3 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_4_VALUE (11004):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 4 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_5_VALUE (11005):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 5 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_6_VALUE (11006):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 6 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_7_VALUE (11007):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 7 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_8_VALUE (11008):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 8 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_9_VALUE (11009):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 9 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_10_VALUE (11010):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 10 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_11_VALUE (11011):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 11 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_12_VALUE (11012):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 12 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_13_VALUE (11013):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 13 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type ``STRING`` or ``DROPDOWN``.
            LINE_ITEM_CUSTOM_FIELD_14_VALUE (11014):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 14 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type ``STRING`` or ``DROPDOWN``.
            ORDER_CUSTOM_FIELD_0_OPTION_ID (12000):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 0 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_1_OPTION_ID (12001):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 1 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_2_OPTION_ID (12002):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 2 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_3_OPTION_ID (12003):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 3 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_4_OPTION_ID (12004):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 4 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_5_OPTION_ID (12005):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 5 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_6_OPTION_ID (12006):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 6 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_7_OPTION_ID (12007):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 7 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_8_OPTION_ID (12008):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 8 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_9_OPTION_ID (12009):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 9 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_10_OPTION_ID (12010):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 10 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_11_OPTION_ID (12011):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 11 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_12_OPTION_ID (12012):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 12 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_13_OPTION_ID (12013):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 13 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_14_OPTION_ID (12014):
                Custom field option ID for Order with custom field ID equal
                to the ID in index 14 of
                ``ReportDefinition.order_custom_field_ids``.
            ORDER_CUSTOM_FIELD_0_VALUE (13000):
                Custom field value for Order with custom field ID equal to
                the ID in index 0 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 0 is of type STRING.
            ORDER_CUSTOM_FIELD_1_VALUE (13001):
                Custom field value for Order with custom field ID equal to
                the ID in index 1 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type STRING.
            ORDER_CUSTOM_FIELD_2_VALUE (13002):
                Custom field value for Order with custom field ID equal to
                the ID in index 2 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type STRING.
            ORDER_CUSTOM_FIELD_3_VALUE (13003):
                Custom field value for Order with custom field ID equal to
                the ID in index 3 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type STRING.
            ORDER_CUSTOM_FIELD_4_VALUE (13004):
                Custom field value for Order with custom field ID equal to
                the ID in index 4 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type STRING.
            ORDER_CUSTOM_FIELD_5_VALUE (13005):
                Custom field value for Order with custom field ID equal to
                the ID in index 5 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type STRING.
            ORDER_CUSTOM_FIELD_6_VALUE (13006):
                Custom field value for Order with custom field ID equal to
                the ID in index 6 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type STRING.
            ORDER_CUSTOM_FIELD_7_VALUE (13007):
                Custom field value for Order with custom field ID equal to
                the ID in index 7 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type STRING.
            ORDER_CUSTOM_FIELD_8_VALUE (13008):
                Custom field value for Order with custom field ID equal to
                the ID in index 8 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type STRING.
            ORDER_CUSTOM_FIELD_9_VALUE (13009):
                Custom field value for Order with custom field ID equal to
                the ID in index 9 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type STRING.
            ORDER_CUSTOM_FIELD_10_VALUE (13010):
                Custom field value for Order with custom field ID equal to
                the ID in index 10 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type STRING.
            ORDER_CUSTOM_FIELD_11_VALUE (13011):
                Custom field value for Order with custom field ID equal to
                the ID in index 11 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type STRING.
            ORDER_CUSTOM_FIELD_12_VALUE (13012):
                Custom field value for Order with custom field ID equal to
                the ID in index 12 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type STRING.
            ORDER_CUSTOM_FIELD_13_VALUE (13013):
                Custom field value for Order with custom field ID equal to
                the ID in index 13 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type STRING.
            ORDER_CUSTOM_FIELD_14_VALUE (13014):
                Custom field value for Order with custom field ID equal to
                the ID in index 14 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type STRING.
            CREATIVE_CUSTOM_FIELD_0_OPTION_ID (14000):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 0 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_1_OPTION_ID (14001):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 1 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_2_OPTION_ID (14002):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 2 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_3_OPTION_ID (14003):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 3 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_4_OPTION_ID (14004):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 4 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_5_OPTION_ID (14005):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 5 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_6_OPTION_ID (14006):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 6 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_7_OPTION_ID (14007):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 7 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_8_OPTION_ID (14008):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 8 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_9_OPTION_ID (14009):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 9 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_10_OPTION_ID (14010):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 10 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_11_OPTION_ID (14011):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 11 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_12_OPTION_ID (14012):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 12 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_13_OPTION_ID (14013):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 13 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_14_OPTION_ID (14014):
                Custom field option ID for Creative with custom field ID
                equal to the ID in index 14 of
                ``ReportDefinition.creative_custom_field_ids``.
            CREATIVE_CUSTOM_FIELD_0_VALUE (15000):
                Custom field value for Creative with custom field ID equal
                to the ID in index 0 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 0 is of type STRING.
            CREATIVE_CUSTOM_FIELD_1_VALUE (15001):
                Custom field value for Creative with custom field ID equal
                to the ID in index 1 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type STRING.
            CREATIVE_CUSTOM_FIELD_2_VALUE (15002):
                Custom field value for Creative with custom field ID equal
                to the ID in index 2 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type STRING.
            CREATIVE_CUSTOM_FIELD_3_VALUE (15003):
                Custom field value for Creative with custom field ID equal
                to the ID in index 3 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type STRING.
            CREATIVE_CUSTOM_FIELD_4_VALUE (15004):
                Custom field value for Creative with custom field ID equal
                to the ID in index 4 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type STRING.
            CREATIVE_CUSTOM_FIELD_5_VALUE (15005):
                Custom field value for Creative with custom field ID equal
                to the ID in index 5 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type STRING.
            CREATIVE_CUSTOM_FIELD_6_VALUE (15006):
                Custom field value for Creative with custom field ID equal
                to the ID in index 6 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type STRING.
            CREATIVE_CUSTOM_FIELD_7_VALUE (15007):
                Custom field value for Creative with custom field ID equal
                to the ID in index 7 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type STRING.
            CREATIVE_CUSTOM_FIELD_8_VALUE (15008):
                Custom field value for Creative with custom field ID equal
                to the ID in index 8 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type STRING.
            CREATIVE_CUSTOM_FIELD_9_VALUE (15009):
                Custom field value for Creative with custom field ID equal
                to the ID in index 9 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type STRING.
            CREATIVE_CUSTOM_FIELD_10_VALUE (15010):
                Custom field value for Creative with custom field ID equal
                to the ID in index 10 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type STRING.
            CREATIVE_CUSTOM_FIELD_11_VALUE (15011):
                Custom field value for Creative with custom field ID equal
                to the ID in index 11 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type STRING.
            CREATIVE_CUSTOM_FIELD_12_VALUE (15012):
                Custom field value for Creative with custom field ID equal
                to the ID in index 12 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type STRING.
            CREATIVE_CUSTOM_FIELD_13_VALUE (15013):
                Custom field value for Creative with custom field ID equal
                to the ID in index 13 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type STRING.
            CREATIVE_CUSTOM_FIELD_14_VALUE (15014):
                Custom field value for Creative with custom field ID equal
                to the ID in index 14 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type STRING.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_0_OPTION_ID (16000):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 0 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_1_OPTION_ID (16001):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 1 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_2_OPTION_ID (16002):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 2 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_3_OPTION_ID (16003):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 3 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_4_OPTION_ID (16004):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 4 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_5_OPTION_ID (16005):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 5 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_6_OPTION_ID (16006):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 6 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_7_OPTION_ID (16007):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 7 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_8_OPTION_ID (16008):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 8 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_9_OPTION_ID (16009):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 9 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_10_OPTION_ID (16010):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 10 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_11_OPTION_ID (16011):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 11 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_12_OPTION_ID (16012):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 12 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_13_OPTION_ID (16013):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 13 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_14_OPTION_ID (16014):
                Custom field option ID for Backfill line item with custom
                field ID equal to the ID in index 14 of
                ``ReportDefinition.line_item_custom_field_ids``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_0_VALUE (17000):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 0 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 0 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_1_VALUE (17001):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 1 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_2_VALUE (17002):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 2 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_3_VALUE (17003):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 3 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_4_VALUE (17004):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 4 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_5_VALUE (17005):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 5 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_6_VALUE (17006):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 6 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_7_VALUE (17007):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 7 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_8_VALUE (17008):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 8 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_9_VALUE (17009):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 9 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_10_VALUE (17010):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 10 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_11_VALUE (17011):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 11 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_12_VALUE (17012):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 12 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_13_VALUE (17013):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 13 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_14_VALUE (17014):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 14 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_0_OPTION_ID (18000):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 0 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_1_OPTION_ID (18001):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 1 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_2_OPTION_ID (18002):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 2 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_3_OPTION_ID (18003):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 3 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_4_OPTION_ID (18004):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 4 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_5_OPTION_ID (18005):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 5 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_6_OPTION_ID (18006):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 6 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_7_OPTION_ID (18007):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 7 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_8_OPTION_ID (18008):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 8 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_9_OPTION_ID (18009):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 9 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_10_OPTION_ID (18010):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 10 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_11_OPTION_ID (18011):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 11 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_12_OPTION_ID (18012):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 12 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_13_OPTION_ID (18013):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 13 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_14_OPTION_ID (18014):
                Custom field option ID for Backfill order with custom field
                ID equal to the ID in index 14 of
                ``ReportDefinition.order_custom_field_ids``.
            BACKFILL_ORDER_CUSTOM_FIELD_0_VALUE (19000):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 0 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 0 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_1_VALUE (19001):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 1 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_2_VALUE (19002):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 2 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_3_VALUE (19003):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 3 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_4_VALUE (19004):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 4 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_5_VALUE (19005):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 5 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_6_VALUE (19006):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 6 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_7_VALUE (19007):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 7 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_8_VALUE (19008):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 8 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_9_VALUE (19009):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 9 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_10_VALUE (19010):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 10 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_11_VALUE (19011):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 11 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_12_VALUE (19012):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 12 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_13_VALUE (19013):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 13 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_ORDER_CUSTOM_FIELD_14_VALUE (19014):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 14 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_0_OPTION_ID (20000):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 0 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_1_OPTION_ID (20001):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 1 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_2_OPTION_ID (20002):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 2 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_3_OPTION_ID (20003):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 3 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_4_OPTION_ID (20004):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 4 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_5_OPTION_ID (20005):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 5 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_6_OPTION_ID (20006):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 6 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_7_OPTION_ID (20007):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 7 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_8_OPTION_ID (20008):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 8 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_9_OPTION_ID (20009):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 9 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_10_OPTION_ID (20010):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 10 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_11_OPTION_ID (20011):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 11 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_12_OPTION_ID (20012):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 12 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_13_OPTION_ID (20013):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 13 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_14_OPTION_ID (20014):
                Custom field option ID for Backfill creative with custom
                field ID equal to the ID in index 14 of
                ``ReportDefinition.creative_custom_field_ids``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_0_VALUE (21000):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 0 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 0 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_1_VALUE (21001):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 1 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_2_VALUE (21002):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 2 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_3_VALUE (21003):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 3 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_4_VALUE (21004):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 4 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_5_VALUE (21005):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 5 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_6_VALUE (21006):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 6 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_7_VALUE (21007):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 7 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_8_VALUE (21008):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 8 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_9_VALUE (21009):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 9 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_10_VALUE (21010):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 10 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_11_VALUE (21011):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 11 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_12_VALUE (21012):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 12 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_13_VALUE (21013):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 13 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type ``STRING`` or ``DROPDOWN``.
            BACKFILL_CREATIVE_CUSTOM_FIELD_14_VALUE (21014):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 14 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type ``STRING`` or ``DROPDOWN``.
            CUSTOM_DIMENSION_0_VALUE_ID (100000):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 0 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_1_VALUE_ID (100001):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 1 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_2_VALUE_ID (100002):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 2 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_3_VALUE_ID (100003):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 3 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_4_VALUE_ID (100004):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 4 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_5_VALUE_ID (100005):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 5 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_6_VALUE_ID (100006):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 6 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_7_VALUE_ID (100007):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 9 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_8_VALUE_ID (100008):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 8 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_9_VALUE_ID (100009):
                Custom Dimension Value ID for Custom Dimension with key
                equal to the key in index 9 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_0_VALUE (101000):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 0 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_1_VALUE (101001):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 1 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_2_VALUE (101002):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 2 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_3_VALUE (101003):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 3 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_4_VALUE (101004):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 4 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_5_VALUE (101005):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 5 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_6_VALUE (101006):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 6 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_7_VALUE (101007):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 7 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_8_VALUE (101008):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 8 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_9_VALUE (101009):
                Custom Dimension Value name for Custom Dimension with key
                equal to the ID in index 9 of
                ``ReportDefinition.custom_dimension_key_ids``.
        """
        _pb_options = {"allow_alias": True}
        DIMENSION_UNSPECIFIED = 0
        ACTIVE_VIEW_MEASUREMENT_SOURCE = 575
        ACTIVE_VIEW_MEASUREMENT_SOURCE_NAME = 576
        ADVERTISER_CREDIT_STATUS = 475
        ADVERTISER_CREDIT_STATUS_NAME = 476
        ADVERTISER_DOMAIN_NAME = 242
        ADVERTISER_EXTERNAL_ID = 228
        ADVERTISER_ID = 131
        ADVERTISER_LABELS = 230
        ADVERTISER_LABEL_IDS = 229
        ADVERTISER_NAME = 132
        ADVERTISER_PRIMARY_CONTACT = 227
        ADVERTISER_STATUS = 471
        ADVERTISER_STATUS_NAME = 472
        ADVERTISER_TYPE = 473
        ADVERTISER_TYPE_NAME = 474
        ADVERTISER_VERTICAL = 580
        ADX_PRODUCT = 499
        ADX_PRODUCT_NAME = 500
        AD_EXPERIENCES_TYPE = 641
        AD_EXPERIENCES_TYPE_NAME = 642
        AD_LOCATION = 390
        AD_LOCATION_NAME = 391
        AD_TECHNOLOGY_PROVIDER_DOMAIN = 620
        AD_TECHNOLOGY_PROVIDER_ID = 621
        AD_TECHNOLOGY_PROVIDER_NAME = 622
        AD_TYPE = 497
        AD_TYPE_NAME = 498
        AD_UNIT_CODE = 64
        AD_UNIT_CODE_LEVEL_1 = 65
        AD_UNIT_CODE_LEVEL_10 = 74
        AD_UNIT_CODE_LEVEL_11 = 75
        AD_UNIT_CODE_LEVEL_12 = 76
        AD_UNIT_CODE_LEVEL_13 = 77
        AD_UNIT_CODE_LEVEL_14 = 78
        AD_UNIT_CODE_LEVEL_15 = 79
        AD_UNIT_CODE_LEVEL_16 = 80
        AD_UNIT_CODE_LEVEL_2 = 66
        AD_UNIT_CODE_LEVEL_3 = 67
        AD_UNIT_CODE_LEVEL_4 = 68
        AD_UNIT_CODE_LEVEL_5 = 69
        AD_UNIT_CODE_LEVEL_6 = 70
        AD_UNIT_CODE_LEVEL_7 = 71
        AD_UNIT_CODE_LEVEL_8 = 72
        AD_UNIT_CODE_LEVEL_9 = 73
        AD_UNIT_ID = 25
        AD_UNIT_ID_ALL_LEVEL = 27
        AD_UNIT_ID_LEVEL_1 = 30
        AD_UNIT_ID_LEVEL_10 = 48
        AD_UNIT_ID_LEVEL_11 = 50
        AD_UNIT_ID_LEVEL_12 = 52
        AD_UNIT_ID_LEVEL_13 = 54
        AD_UNIT_ID_LEVEL_14 = 56
        AD_UNIT_ID_LEVEL_15 = 58
        AD_UNIT_ID_LEVEL_16 = 60
        AD_UNIT_ID_LEVEL_2 = 32
        AD_UNIT_ID_LEVEL_3 = 34
        AD_UNIT_ID_LEVEL_4 = 36
        AD_UNIT_ID_LEVEL_5 = 38
        AD_UNIT_ID_LEVEL_6 = 40
        AD_UNIT_ID_LEVEL_7 = 42
        AD_UNIT_ID_LEVEL_8 = 44
        AD_UNIT_ID_LEVEL_9 = 46
        AD_UNIT_ID_TOP_LEVEL = 142
        AD_UNIT_NAME = 26
        AD_UNIT_NAME_ALL_LEVEL = 29
        AD_UNIT_NAME_LEVEL_1 = 31
        AD_UNIT_NAME_LEVEL_10 = 49
        AD_UNIT_NAME_LEVEL_11 = 51
        AD_UNIT_NAME_LEVEL_12 = 53
        AD_UNIT_NAME_LEVEL_13 = 55
        AD_UNIT_NAME_LEVEL_14 = 57
        AD_UNIT_NAME_LEVEL_15 = 59
        AD_UNIT_NAME_LEVEL_16 = 61
        AD_UNIT_NAME_LEVEL_2 = 33
        AD_UNIT_NAME_LEVEL_3 = 35
        AD_UNIT_NAME_LEVEL_4 = 37
        AD_UNIT_NAME_LEVEL_5 = 39
        AD_UNIT_NAME_LEVEL_6 = 41
        AD_UNIT_NAME_LEVEL_7 = 43
        AD_UNIT_NAME_LEVEL_8 = 45
        AD_UNIT_NAME_LEVEL_9 = 47
        AD_UNIT_NAME_TOP_LEVEL = 143
        AD_UNIT_REWARD_AMOUNT = 63
        AD_UNIT_REWARD_TYPE = 62
        AD_UNIT_STATUS = 206
        AD_UNIT_STATUS_NAME = 207
        AGENCY_LEVEL_1_ID = 565
        AGENCY_LEVEL_1_NAME = 566
        AGENCY_LEVEL_2_ID = 567
        AGENCY_LEVEL_2_NAME = 568
        AGENCY_LEVEL_3_ID = 569
        AGENCY_LEVEL_3_NAME = 570
        AGE_BRACKET = 508
        AGE_BRACKET_NAME = 582
        APP_TRACKING_TRANSPARENCY_CONSENT_STATUS = 442
        APP_TRACKING_TRANSPARENCY_CONSENT_STATUS_NAME = 443
        APP_VERSION = 392
        AUCTION_PACKAGE_DEAL = 579
        AUCTION_PACKAGE_DEAL_ID = 571
        AUDIENCE_SEGMENT_ID_TARGETED = 584
        AUDIENCE_SEGMENT_TARGETED = 585
        AUTO_REFRESHED_TRAFFIC = 421
        AUTO_REFRESHED_TRAFFIC_NAME = 422
        BIDDER_ENCRYPTED_ID = 493
        BIDDER_NAME = 494
        BID_RANGE = 679
        BID_REJECTION_REASON = 599
        BID_REJECTION_REASON_NAME = 600
        BRANDING_TYPE = 383
        BRANDING_TYPE_NAME = 384
        BROWSER_CATEGORY = 119
        BROWSER_CATEGORY_NAME = 120
        BROWSER_ID = 235
        BROWSER_NAME = 236
        BUYER_NETWORK_ID = 448
        BUYER_NETWORK_NAME = 449
        CALLOUT_STATUS_CATEGORY = 588
        CALLOUT_STATUS_CATEGORY_NAME = 589
        CARRIER_ID = 369
        CARRIER_NAME = 368
        CHANNEL = 501
        CHILD_NETWORK_CODE = 542
        CHILD_NETWORK_ID = 544
        CHILD_PARTNER_NAME = 543
        CITY_ID = 459
        CITY_NAME = 452
        CLASSIFIED_ADVERTISER_ID = 133
        CLASSIFIED_ADVERTISER_NAME = 134
        CLASSIFIED_BRAND_ID = 243
        CLASSIFIED_BRAND_NAME = 244
        CONTENT_CMS_NAME = 643
        CONTENT_CMS_VIDEO_ID = 644
        CONTENT_ID = 246
        CONTENT_MAPPING_PRESENCE = 731
        CONTENT_MAPPING_PRESENCE_NAME = 732
        CONTENT_NAME = 247
        CONTINENT = 469
        CONTINENT_NAME = 470
        COUNTRY_CODE = 466
        COUNTRY_ID = 11
        COUNTRY_NAME = 12
        CREATIVE_BILLING_TYPE = 366
        CREATIVE_BILLING_TYPE_NAME = 367
        CREATIVE_CLICK_THROUGH_URL = 174
        CREATIVE_ID = 138
        CREATIVE_NAME = 139
        CREATIVE_POLICIES_FILTERING = 711
        CREATIVE_POLICIES_FILTERING_NAME = 712
        CREATIVE_PROTECTIONS_FILTERING = 704
        CREATIVE_PROTECTIONS_FILTERING_NAME = 705
        CREATIVE_SET_ROLE_TYPE = 686
        CREATIVE_SET_ROLE_TYPE_NAME = 687
        CREATIVE_TECHNOLOGY = 148
        CREATIVE_TECHNOLOGY_NAME = 149
        CREATIVE_THIRD_PARTY_VENDOR = 361
        CREATIVE_TYPE = 344
        CREATIVE_TYPE_NAME = 345
        CREATIVE_VENDOR_ID = 706
        CREATIVE_VENDOR_NAME = 707
        CREATIVE_VIDEO_REDIRECT_THIRD_PARTY = 562
        CURATOR_ID = 572
        CURATOR_NAME = 573
        CUSTOM_EVENT_ID = 737
        CUSTOM_EVENT_NAME = 735
        CUSTOM_EVENT_TYPE = 736
        CUSTOM_EVENT_TYPE_NAME = 738
        CUSTOM_SPOT_ID = 423
        CUSTOM_SPOT_NAME = 424
        DATE = 3
        DAY_OF_WEEK = 4
        DEAL_BUYER_ID = 240
        DEAL_BUYER_NAME = 241
        DEAL_ID = 436
        DEAL_NAME = 437
        DELIVERED_SECURE_SIGNAL_ID = 309
        DELIVERED_SECURE_SIGNAL_NAME = 310
        DEMAND_CHANNEL = 9
        DEMAND_CHANNEL_NAME = 10
        DEMAND_SOURCE = 592
        DEMAND_SOURCE_NAME = 593
        DEMAND_SUBCHANNEL = 22
        DEMAND_SUBCHANNEL_NAME = 23
        DEVICE = 226
        DEVICE_CATEGORY = 15
        DEVICE_CATEGORY_NAME = 16
        DEVICE_MANUFACTURER_ID = 525
        DEVICE_MANUFACTURER_NAME = 526
        DEVICE_MODEL_ID = 527
        DEVICE_MODEL_NAME = 528
        DEVICE_NAME = 225
        DSP_SEAT_ID = 564
        DYNAMIC_ALLOCATION_TYPE = 502
        DYNAMIC_ALLOCATION_TYPE_NAME = 503
        ESP_DELIVERY = 623
        ESP_DELIVERY_NAME = 624
        ESP_PRESENCE = 625
        ESP_PRESENCE_NAME = 626
        EXCHANGE_BIDDING_DEAL_ID = 715
        EXCHANGE_BIDDING_DEAL_TYPE = 714
        EXCHANGE_BIDDING_DEAL_TYPE_NAME = 723
        EXCHANGE_THIRD_PARTY_COMPANY_ID = 185
        EXCHANGE_THIRD_PARTY_COMPANY_NAME = 186
        FIRST_LOOK_PRICING_RULE_ID = 248
        FIRST_LOOK_PRICING_RULE_NAME = 249
        FIRST_PARTY_ID_STATUS = 404
        FIRST_PARTY_ID_STATUS_NAME = 405
        GENDER = 509
        GENDER_NAME = 583
        GOOGLE_ANALYTICS_STREAM_ID = 519
        GOOGLE_ANALYTICS_STREAM_NAME = 520
        HBT_YIELD_PARTNER_ID = 659
        HBT_YIELD_PARTNER_NAME = 660
        HEADER_BIDDER_INTEGRATION_TYPE = 718
        HEADER_BIDDER_INTEGRATION_TYPE_NAME = 719
        HOUR = 100
        IMPRESSION_COUNTING_METHOD = 577
        IMPRESSION_COUNTING_METHOD_NAME = 578
        INTERACTION_TYPE = 223
        INTERACTION_TYPE_NAME = 224
        INTEREST = 510
        INVENTORY_FORMAT = 17
        INVENTORY_FORMAT_NAME = 18
        INVENTORY_SHARE_ASSIGNMENT_ID = 648
        INVENTORY_SHARE_ASSIGNMENT_NAME = 649
        INVENTORY_SHARE_OUTCOME = 603
        INVENTORY_SHARE_OUTCOME_NAME = 604
        INVENTORY_SHARE_PARTNER_AD_SERVER = 652
        INVENTORY_SHARE_PARTNER_AD_SERVER_NAME = 653
        INVENTORY_SHARE_TARGET_SHARE_PERCENT = 654
        INVENTORY_SHARE_TYPE = 650
        INVENTORY_SHARE_TYPE_NAME = 651
        INVENTORY_TYPE = 19
        INVENTORY_TYPE_NAME = 20
        IS_ADX_DIRECT = 382
        IS_CURATION_TARGETED = 574
        IS_DROPPED = 464
        IS_FIRST_LOOK_DEAL = 401
        KEY_VALUES_ID = 214
        KEY_VALUES_NAME = 215
        LINE_ITEM_AGENCY = 663
        LINE_ITEM_ARCHIVED = 188
        LINE_ITEM_COMPANION_DELIVERY_OPTION = 204
        LINE_ITEM_COMPANION_DELIVERY_OPTION_NAME = 205
        LINE_ITEM_COMPUTED_STATUS = 250
        LINE_ITEM_COMPUTED_STATUS_NAME = 251
        LINE_ITEM_CONTRACTED_QUANTITY = 92
        LINE_ITEM_COST_PER_UNIT = 85
        LINE_ITEM_COST_TYPE = 212
        LINE_ITEM_COST_TYPE_NAME = 213
        LINE_ITEM_CREATIVE_END_DATE = 176
        LINE_ITEM_CREATIVE_ROTATION_TYPE = 189
        LINE_ITEM_CREATIVE_ROTATION_TYPE_NAME = 190
        LINE_ITEM_CREATIVE_START_DATE = 175
        LINE_ITEM_CURRENCY_CODE = 180
        LINE_ITEM_DELIVERY_INDICATOR = 87
        LINE_ITEM_DELIVERY_RATE_TYPE = 191
        LINE_ITEM_DELIVERY_RATE_TYPE_NAME = 192
        LINE_ITEM_DISCOUNT_ABSOLUTE = 195
        LINE_ITEM_DISCOUNT_PERCENTAGE = 196
        LINE_ITEM_END_DATE = 81
        LINE_ITEM_END_DATE_TIME = 83
        LINE_ITEM_ENVIRONMENT_TYPE = 201
        LINE_ITEM_ENVIRONMENT_TYPE_NAME = 202
        LINE_ITEM_EXTERNAL_DEAL_ID = 97
        LINE_ITEM_EXTERNAL_ID = 86
        LINE_ITEM_FREQUENCY_CAP = 256
        LINE_ITEM_ID = 1
        LINE_ITEM_LABELS = 667
        LINE_ITEM_LABEL_IDS = 665
        LINE_ITEM_LAST_MODIFIED_BY_APP = 181
        LINE_ITEM_LIFETIME_CLICKS = 95
        LINE_ITEM_LIFETIME_IMPRESSIONS = 94
        LINE_ITEM_LIFETIME_VIEWABLE_IMPRESSIONS = 96
        LINE_ITEM_MAKEGOOD = 89
        LINE_ITEM_NAME = 2
        LINE_ITEM_NON_CPD_BOOKED_REVENUE = 98
        LINE_ITEM_OPTIMIZABLE = 90
        LINE_ITEM_PO_NUMBER = 669
        LINE_ITEM_PRIMARY_GOAL_TYPE = 210
        LINE_ITEM_PRIMARY_GOAL_TYPE_NAME = 211
        LINE_ITEM_PRIMARY_GOAL_UNITS_ABSOLUTE = 93
        LINE_ITEM_PRIMARY_GOAL_UNITS_PERCENTAGE = 396
        LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE = 208
        LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE_NAME = 209
        LINE_ITEM_PRIORITY = 24
        LINE_ITEM_RESERVATION_STATUS = 304
        LINE_ITEM_RESERVATION_STATUS_NAME = 305
        LINE_ITEM_SALESPERSON = 671
        LINE_ITEM_SECONDARY_SALESPEOPLE = 673
        LINE_ITEM_SECONDARY_TRAFFICKERS = 675
        LINE_ITEM_START_DATE = 82
        LINE_ITEM_START_DATE_TIME = 84
        LINE_ITEM_TRAFFICKER = 677
        LINE_ITEM_TYPE = 193
        LINE_ITEM_TYPE_NAME = 194
        LINE_ITEM_UNLIMITED_END = 187
        LINE_ITEM_VALUE_COST_PER_UNIT = 88
        LINE_ITEM_WEB_PROPERTY_CODE = 179
        MASTER_COMPANION_CREATIVE_ID = 140
        MASTER_COMPANION_CREATIVE_NAME = 141
        MEDIATION_TYPE = 701
        MEDIATION_TYPE_NAME = 754
        MEDIATION_YIELD_PARTNER_ID = 661
        MEDIATION_YIELD_PARTNER_NAME = 662
        METRO_ID = 453
        METRO_NAME = 454
        MOBILE_APP_FREE = 128
        MOBILE_APP_ICON_URL = 129
        MOBILE_APP_ID = 123
        MOBILE_APP_NAME = 127
        MOBILE_APP_OWNERSHIP_STATUS = 311
        MOBILE_APP_OWNERSHIP_STATUS_NAME = 312
        MOBILE_APP_STORE = 125
        MOBILE_APP_STORE_NAME = 245
        MOBILE_INVENTORY_TYPE = 99
        MOBILE_INVENTORY_TYPE_NAME = 21
        MOBILE_RENDERING_SDK = 646
        MOBILE_RENDERING_SDK_NAME = 647
        MOBILE_SDK_MAJOR_VERSION = 692
        MOBILE_SDK_MINOR_VERSION = 693
        MOBILE_SDK_VERSION_NAME = 130
        MONTH_YEAR = 6
        NATIVE_AD_FORMAT_ID = 255
        NATIVE_AD_FORMAT_NAME = 254
        NATIVE_STYLE_ID = 253
        NATIVE_STYLE_NAME = 252
        NO_FILL_REASON_CATEGORY = 586
        NO_FILL_REASON_CATEGORY_NAME = 587
        OPERATING_SYSTEM_CATEGORY = 117
        OPERATING_SYSTEM_CATEGORY_NAME = 118
        OPERATING_SYSTEM_VERSION_ID = 238
        OPERATING_SYSTEM_VERSION_NAME = 237
        OPTIMIZATION_TYPE = 639
        OPTIMIZATION_TYPE_NAME = 640
        ORDER_AGENCY = 150
        ORDER_AGENCY_ID = 151
        ORDER_BOOKED_CPC = 152
        ORDER_BOOKED_CPM = 153
        ORDER_DELIVERY_STATUS = 231
        ORDER_DELIVERY_STATUS_NAME = 239
        ORDER_END_DATE = 154
        ORDER_END_DATE_TIME = 155
        ORDER_EXTERNAL_ID = 156
        ORDER_ID = 7
        ORDER_LABELS = 170
        ORDER_LABEL_IDS = 171
        ORDER_LIFETIME_CLICKS = 158
        ORDER_LIFETIME_IMPRESSIONS = 159
        ORDER_NAME = 8
        ORDER_PO_NUMBER = 160
        ORDER_PROGRAMMATIC = 157
        ORDER_SALESPERSON = 161
        ORDER_SALESPERSON_ID = 629
        ORDER_SECONDARY_SALESPEOPLE = 164
        ORDER_SECONDARY_SALESPEOPLE_ID = 165
        ORDER_SECONDARY_TRAFFICKERS = 166
        ORDER_SECONDARY_TRAFFICKERS_ID = 167
        ORDER_START_DATE = 168
        ORDER_START_DATE_TIME = 169
        ORDER_TRAFFICKER = 162
        ORDER_TRAFFICKER_ID = 163
        ORDER_UNLIMITED_END = 203
        PAGE_PATH = 511
        PAGE_TITLE_AND_SCREEN_CLASS = 512
        PAGE_TITLE_AND_SCREEN_NAME = 513
        PLACEMENT_ID = 113
        PLACEMENT_ID_ALL = 144
        PLACEMENT_NAME = 114
        PLACEMENT_NAME_ALL = 145
        PLACEMENT_STATUS = 362
        PLACEMENT_STATUS_NAME = 364
        PLACEMENT_STATUS_NAME_ALL = 365
        POSTAL_CODE_ID = 455
        POSTAL_CODE_NAME = 456
        PPID_STATUS = 406
        PPID_STATUS_NAME = 407
        PREDICTED_VIEWABILITY_BUCKET = 633
        PREDICTED_VIEWABILITY_BUCKET_NAME = 634
        PRESENTED_SECURE_SIGNAL_ID = 495
        PRESENTED_SECURE_SIGNAL_NAME = 496
        PRIMARY_PERSONALIZATION_ID_TYPE = 408
        PRIMARY_PERSONALIZATION_ID_TYPE_NAME = 409
        PROGRAMMATIC_BUYER_ID = 240
        PROGRAMMATIC_BUYER_NAME = 241
        PROGRAMMATIC_CHANNEL = 13
        PROGRAMMATIC_CHANNEL_NAME = 14
        PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_EXTERNAL_CODE = 410
        PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_IDS = 546
        PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_NAME = 412
        PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_TIER = 413
        PUBLISHER_PROVIDED_SIGNALS_ALL_LEVELS_TYPE = 414
        PUBLISHER_PROVIDED_SIGNALS_DELIVERED_EXTERNAL_CODE = 425
        PUBLISHER_PROVIDED_SIGNALS_DELIVERED_IDS = 545
        PUBLISHER_PROVIDED_SIGNALS_DELIVERED_NAME = 427
        PUBLISHER_PROVIDED_SIGNALS_DELIVERED_TIER = 428
        PUBLISHER_PROVIDED_SIGNALS_DELIVERED_TYPE = 429
        PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_EXTERNAL_CODE = 415
        PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_ID = 416
        PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_NAME = 417
        PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_TIER = 418
        PUBLISHER_PROVIDED_SIGNALS_TOP_LEVEL_TYPE = 419
        PUBLISHER_PROVIDED_SIGNAL_DATA_PROVIDER_ID = 136
        PUBLISHER_PROVIDED_SIGNAL_DATA_PROVIDER_NAME = 137
        REGION_ID = 457
        REGION_NAME = 458
        REJECTION_CLASS_CATEGORY = 590
        REJECTION_CLASS_CATEGORY_NAME = 591
        RENDERED_CREATIVE_SIZE = 343
        REQUESTED_AD_SIZES = 352
        REQUEST_TYPE = 146
        REQUEST_TYPE_NAME = 147
        SERVER_SIDE_UNWRAPPING_ELIGIBLE = 597
        SERVING_RESTRICTION = 631
        SERVING_RESTRICTION_NAME = 632
        SITE = 387
        TARGETING_ID = 232
        TARGETING_NAME = 233
        TARGETING_TYPE = 385
        TARGETING_TYPE_NAME = 386
        THIRD_PARTY_ID_STATUS = 402
        THIRD_PARTY_ID_STATUS_NAME = 403
        TOPICS_STATUS = 504
        TOPICS_STATUS_NAME = 505
        TOP_PRIVATE_DOMAIN = 444
        TRAFFIC_SOURCE = 388
        TRAFFIC_SOURCE_NAME = 389
        UNIFIED_PRICING_RULE_ID = 393
        UNIFIED_PRICING_RULE_NAME = 394
        URL = 506
        URL_ID = 507
        USER_MESSAGES_ENTITLEMENT_SOURCE = 635
        USER_MESSAGES_ENTITLEMENT_SOURCE_NAME = 636
        USER_MESSAGES_OPERATING_SYSTEM_CRITERIA_ID = 637
        USER_MESSAGES_OPERATING_SYSTEM_CRITERIA_NAME = 638
        VAST_VERSION = 554
        VAST_VERSION_NAME = 555
        VIDEO_AD_BREAK_TYPE = 556
        VIDEO_AD_BREAK_TYPE_NAME = 557
        VIDEO_AD_DURATION = 450
        VIDEO_AD_FORMATS_RULE = 561
        VIDEO_AD_FORMATS_RULE_ID = 560
        VIDEO_AD_REQUEST_DURATION = 558
        VIDEO_AD_REQUEST_DURATION_MIDPOINT_NAME = 751
        VIDEO_AD_REQUEST_DURATION_NAME = 559
        VIDEO_AD_REQUEST_SOURCE = 438
        VIDEO_AD_REQUEST_SOURCE_NAME = 439
        VIDEO_AD_TYPE = 432
        VIDEO_AD_TYPE_NAME = 433
        VIDEO_CONTINUOUS_PLAY_TYPE = 721
        VIDEO_CONTINUOUS_PLAY_TYPE_NAME = 722
        VIDEO_FALLBACK_POSITION = 530
        VIDEO_MEASUREMENT_SOURCE = 601
        VIDEO_MEASUREMENT_SOURCE_NAME = 602
        VIDEO_PLCMT = 172
        VIDEO_PLCMT_NAME = 173
        VIDEO_POSITION_IN_POD = 538
        VIDEO_POSITION_OF_POD = 539
        VIDEO_SDK_VERSION = 440
        VIDEO_SDK_VERSION_NAME = 441
        VIDEO_STITCHER_TYPE = 752
        VIDEO_STITCHER_TYPE_NAME = 753
        WEEK = 5
        YIELD_GROUP_BUYER_NAME = 184
        YIELD_GROUP_BUYER_TAG_NAME = 627
        YIELD_GROUP_ID = 182
        YIELD_GROUP_NAME = 183
        YOUTUBE_AD_DURATION_BUCKET = 430
        YOUTUBE_AD_DURATION_BUCKET_NAME = 431
        YOUTUBE_AD_TYPE = 399
        YOUTUBE_AD_TYPE_NAME = 400
        LINE_ITEM_CUSTOM_FIELD_0_OPTION_ID = 10000
        LINE_ITEM_CUSTOM_FIELD_1_OPTION_ID = 10001
        LINE_ITEM_CUSTOM_FIELD_2_OPTION_ID = 10002
        LINE_ITEM_CUSTOM_FIELD_3_OPTION_ID = 10003
        LINE_ITEM_CUSTOM_FIELD_4_OPTION_ID = 10004
        LINE_ITEM_CUSTOM_FIELD_5_OPTION_ID = 10005
        LINE_ITEM_CUSTOM_FIELD_6_OPTION_ID = 10006
        LINE_ITEM_CUSTOM_FIELD_7_OPTION_ID = 10007
        LINE_ITEM_CUSTOM_FIELD_8_OPTION_ID = 10008
        LINE_ITEM_CUSTOM_FIELD_9_OPTION_ID = 10009
        LINE_ITEM_CUSTOM_FIELD_10_OPTION_ID = 10010
        LINE_ITEM_CUSTOM_FIELD_11_OPTION_ID = 10011
        LINE_ITEM_CUSTOM_FIELD_12_OPTION_ID = 10012
        LINE_ITEM_CUSTOM_FIELD_13_OPTION_ID = 10013
        LINE_ITEM_CUSTOM_FIELD_14_OPTION_ID = 10014
        LINE_ITEM_CUSTOM_FIELD_0_VALUE = 11000
        LINE_ITEM_CUSTOM_FIELD_1_VALUE = 11001
        LINE_ITEM_CUSTOM_FIELD_2_VALUE = 11002
        LINE_ITEM_CUSTOM_FIELD_3_VALUE = 11003
        LINE_ITEM_CUSTOM_FIELD_4_VALUE = 11004
        LINE_ITEM_CUSTOM_FIELD_5_VALUE = 11005
        LINE_ITEM_CUSTOM_FIELD_6_VALUE = 11006
        LINE_ITEM_CUSTOM_FIELD_7_VALUE = 11007
        LINE_ITEM_CUSTOM_FIELD_8_VALUE = 11008
        LINE_ITEM_CUSTOM_FIELD_9_VALUE = 11009
        LINE_ITEM_CUSTOM_FIELD_10_VALUE = 11010
        LINE_ITEM_CUSTOM_FIELD_11_VALUE = 11011
        LINE_ITEM_CUSTOM_FIELD_12_VALUE = 11012
        LINE_ITEM_CUSTOM_FIELD_13_VALUE = 11013
        LINE_ITEM_CUSTOM_FIELD_14_VALUE = 11014
        ORDER_CUSTOM_FIELD_0_OPTION_ID = 12000
        ORDER_CUSTOM_FIELD_1_OPTION_ID = 12001
        ORDER_CUSTOM_FIELD_2_OPTION_ID = 12002
        ORDER_CUSTOM_FIELD_3_OPTION_ID = 12003
        ORDER_CUSTOM_FIELD_4_OPTION_ID = 12004
        ORDER_CUSTOM_FIELD_5_OPTION_ID = 12005
        ORDER_CUSTOM_FIELD_6_OPTION_ID = 12006
        ORDER_CUSTOM_FIELD_7_OPTION_ID = 12007
        ORDER_CUSTOM_FIELD_8_OPTION_ID = 12008
        ORDER_CUSTOM_FIELD_9_OPTION_ID = 12009
        ORDER_CUSTOM_FIELD_10_OPTION_ID = 12010
        ORDER_CUSTOM_FIELD_11_OPTION_ID = 12011
        ORDER_CUSTOM_FIELD_12_OPTION_ID = 12012
        ORDER_CUSTOM_FIELD_13_OPTION_ID = 12013
        ORDER_CUSTOM_FIELD_14_OPTION_ID = 12014
        ORDER_CUSTOM_FIELD_0_VALUE = 13000
        ORDER_CUSTOM_FIELD_1_VALUE = 13001
        ORDER_CUSTOM_FIELD_2_VALUE = 13002
        ORDER_CUSTOM_FIELD_3_VALUE = 13003
        ORDER_CUSTOM_FIELD_4_VALUE = 13004
        ORDER_CUSTOM_FIELD_5_VALUE = 13005
        ORDER_CUSTOM_FIELD_6_VALUE = 13006
        ORDER_CUSTOM_FIELD_7_VALUE = 13007
        ORDER_CUSTOM_FIELD_8_VALUE = 13008
        ORDER_CUSTOM_FIELD_9_VALUE = 13009
        ORDER_CUSTOM_FIELD_10_VALUE = 13010
        ORDER_CUSTOM_FIELD_11_VALUE = 13011
        ORDER_CUSTOM_FIELD_12_VALUE = 13012
        ORDER_CUSTOM_FIELD_13_VALUE = 13013
        ORDER_CUSTOM_FIELD_14_VALUE = 13014
        CREATIVE_CUSTOM_FIELD_0_OPTION_ID = 14000
        CREATIVE_CUSTOM_FIELD_1_OPTION_ID = 14001
        CREATIVE_CUSTOM_FIELD_2_OPTION_ID = 14002
        CREATIVE_CUSTOM_FIELD_3_OPTION_ID = 14003
        CREATIVE_CUSTOM_FIELD_4_OPTION_ID = 14004
        CREATIVE_CUSTOM_FIELD_5_OPTION_ID = 14005
        CREATIVE_CUSTOM_FIELD_6_OPTION_ID = 14006
        CREATIVE_CUSTOM_FIELD_7_OPTION_ID = 14007
        CREATIVE_CUSTOM_FIELD_8_OPTION_ID = 14008
        CREATIVE_CUSTOM_FIELD_9_OPTION_ID = 14009
        CREATIVE_CUSTOM_FIELD_10_OPTION_ID = 14010
        CREATIVE_CUSTOM_FIELD_11_OPTION_ID = 14011
        CREATIVE_CUSTOM_FIELD_12_OPTION_ID = 14012
        CREATIVE_CUSTOM_FIELD_13_OPTION_ID = 14013
        CREATIVE_CUSTOM_FIELD_14_OPTION_ID = 14014
        CREATIVE_CUSTOM_FIELD_0_VALUE = 15000
        CREATIVE_CUSTOM_FIELD_1_VALUE = 15001
        CREATIVE_CUSTOM_FIELD_2_VALUE = 15002
        CREATIVE_CUSTOM_FIELD_3_VALUE = 15003
        CREATIVE_CUSTOM_FIELD_4_VALUE = 15004
        CREATIVE_CUSTOM_FIELD_5_VALUE = 15005
        CREATIVE_CUSTOM_FIELD_6_VALUE = 15006
        CREATIVE_CUSTOM_FIELD_7_VALUE = 15007
        CREATIVE_CUSTOM_FIELD_8_VALUE = 15008
        CREATIVE_CUSTOM_FIELD_9_VALUE = 15009
        CREATIVE_CUSTOM_FIELD_10_VALUE = 15010
        CREATIVE_CUSTOM_FIELD_11_VALUE = 15011
        CREATIVE_CUSTOM_FIELD_12_VALUE = 15012
        CREATIVE_CUSTOM_FIELD_13_VALUE = 15013
        CREATIVE_CUSTOM_FIELD_14_VALUE = 15014
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_0_OPTION_ID = 16000
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_1_OPTION_ID = 16001
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_2_OPTION_ID = 16002
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_3_OPTION_ID = 16003
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_4_OPTION_ID = 16004
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_5_OPTION_ID = 16005
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_6_OPTION_ID = 16006
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_7_OPTION_ID = 16007
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_8_OPTION_ID = 16008
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_9_OPTION_ID = 16009
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_10_OPTION_ID = 16010
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_11_OPTION_ID = 16011
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_12_OPTION_ID = 16012
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_13_OPTION_ID = 16013
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_14_OPTION_ID = 16014
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_0_VALUE = 17000
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_1_VALUE = 17001
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_2_VALUE = 17002
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_3_VALUE = 17003
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_4_VALUE = 17004
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_5_VALUE = 17005
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_6_VALUE = 17006
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_7_VALUE = 17007
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_8_VALUE = 17008
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_9_VALUE = 17009
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_10_VALUE = 17010
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_11_VALUE = 17011
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_12_VALUE = 17012
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_13_VALUE = 17013
        BACKFILL_LINE_ITEM_CUSTOM_FIELD_14_VALUE = 17014
        BACKFILL_ORDER_CUSTOM_FIELD_0_OPTION_ID = 18000
        BACKFILL_ORDER_CUSTOM_FIELD_1_OPTION_ID = 18001
        BACKFILL_ORDER_CUSTOM_FIELD_2_OPTION_ID = 18002
        BACKFILL_ORDER_CUSTOM_FIELD_3_OPTION_ID = 18003
        BACKFILL_ORDER_CUSTOM_FIELD_4_OPTION_ID = 18004
        BACKFILL_ORDER_CUSTOM_FIELD_5_OPTION_ID = 18005
        BACKFILL_ORDER_CUSTOM_FIELD_6_OPTION_ID = 18006
        BACKFILL_ORDER_CUSTOM_FIELD_7_OPTION_ID = 18007
        BACKFILL_ORDER_CUSTOM_FIELD_8_OPTION_ID = 18008
        BACKFILL_ORDER_CUSTOM_FIELD_9_OPTION_ID = 18009
        BACKFILL_ORDER_CUSTOM_FIELD_10_OPTION_ID = 18010
        BACKFILL_ORDER_CUSTOM_FIELD_11_OPTION_ID = 18011
        BACKFILL_ORDER_CUSTOM_FIELD_12_OPTION_ID = 18012
        BACKFILL_ORDER_CUSTOM_FIELD_13_OPTION_ID = 18013
        BACKFILL_ORDER_CUSTOM_FIELD_14_OPTION_ID = 18014
        BACKFILL_ORDER_CUSTOM_FIELD_0_VALUE = 19000
        BACKFILL_ORDER_CUSTOM_FIELD_1_VALUE = 19001
        BACKFILL_ORDER_CUSTOM_FIELD_2_VALUE = 19002
        BACKFILL_ORDER_CUSTOM_FIELD_3_VALUE = 19003
        BACKFILL_ORDER_CUSTOM_FIELD_4_VALUE = 19004
        BACKFILL_ORDER_CUSTOM_FIELD_5_VALUE = 19005
        BACKFILL_ORDER_CUSTOM_FIELD_6_VALUE = 19006
        BACKFILL_ORDER_CUSTOM_FIELD_7_VALUE = 19007
        BACKFILL_ORDER_CUSTOM_FIELD_8_VALUE = 19008
        BACKFILL_ORDER_CUSTOM_FIELD_9_VALUE = 19009
        BACKFILL_ORDER_CUSTOM_FIELD_10_VALUE = 19010
        BACKFILL_ORDER_CUSTOM_FIELD_11_VALUE = 19011
        BACKFILL_ORDER_CUSTOM_FIELD_12_VALUE = 19012
        BACKFILL_ORDER_CUSTOM_FIELD_13_VALUE = 19013
        BACKFILL_ORDER_CUSTOM_FIELD_14_VALUE = 19014
        BACKFILL_CREATIVE_CUSTOM_FIELD_0_OPTION_ID = 20000
        BACKFILL_CREATIVE_CUSTOM_FIELD_1_OPTION_ID = 20001
        BACKFILL_CREATIVE_CUSTOM_FIELD_2_OPTION_ID = 20002
        BACKFILL_CREATIVE_CUSTOM_FIELD_3_OPTION_ID = 20003
        BACKFILL_CREATIVE_CUSTOM_FIELD_4_OPTION_ID = 20004
        BACKFILL_CREATIVE_CUSTOM_FIELD_5_OPTION_ID = 20005
        BACKFILL_CREATIVE_CUSTOM_FIELD_6_OPTION_ID = 20006
        BACKFILL_CREATIVE_CUSTOM_FIELD_7_OPTION_ID = 20007
        BACKFILL_CREATIVE_CUSTOM_FIELD_8_OPTION_ID = 20008
        BACKFILL_CREATIVE_CUSTOM_FIELD_9_OPTION_ID = 20009
        BACKFILL_CREATIVE_CUSTOM_FIELD_10_OPTION_ID = 20010
        BACKFILL_CREATIVE_CUSTOM_FIELD_11_OPTION_ID = 20011
        BACKFILL_CREATIVE_CUSTOM_FIELD_12_OPTION_ID = 20012
        BACKFILL_CREATIVE_CUSTOM_FIELD_13_OPTION_ID = 20013
        BACKFILL_CREATIVE_CUSTOM_FIELD_14_OPTION_ID = 20014
        BACKFILL_CREATIVE_CUSTOM_FIELD_0_VALUE = 21000
        BACKFILL_CREATIVE_CUSTOM_FIELD_1_VALUE = 21001
        BACKFILL_CREATIVE_CUSTOM_FIELD_2_VALUE = 21002
        BACKFILL_CREATIVE_CUSTOM_FIELD_3_VALUE = 21003
        BACKFILL_CREATIVE_CUSTOM_FIELD_4_VALUE = 21004
        BACKFILL_CREATIVE_CUSTOM_FIELD_5_VALUE = 21005
        BACKFILL_CREATIVE_CUSTOM_FIELD_6_VALUE = 21006
        BACKFILL_CREATIVE_CUSTOM_FIELD_7_VALUE = 21007
        BACKFILL_CREATIVE_CUSTOM_FIELD_8_VALUE = 21008
        BACKFILL_CREATIVE_CUSTOM_FIELD_9_VALUE = 21009
        BACKFILL_CREATIVE_CUSTOM_FIELD_10_VALUE = 21010
        BACKFILL_CREATIVE_CUSTOM_FIELD_11_VALUE = 21011
        BACKFILL_CREATIVE_CUSTOM_FIELD_12_VALUE = 21012
        BACKFILL_CREATIVE_CUSTOM_FIELD_13_VALUE = 21013
        BACKFILL_CREATIVE_CUSTOM_FIELD_14_VALUE = 21014
        CUSTOM_DIMENSION_0_VALUE_ID = 100000
        CUSTOM_DIMENSION_1_VALUE_ID = 100001
        CUSTOM_DIMENSION_2_VALUE_ID = 100002
        CUSTOM_DIMENSION_3_VALUE_ID = 100003
        CUSTOM_DIMENSION_4_VALUE_ID = 100004
        CUSTOM_DIMENSION_5_VALUE_ID = 100005
        CUSTOM_DIMENSION_6_VALUE_ID = 100006
        CUSTOM_DIMENSION_7_VALUE_ID = 100007
        CUSTOM_DIMENSION_8_VALUE_ID = 100008
        CUSTOM_DIMENSION_9_VALUE_ID = 100009
        CUSTOM_DIMENSION_0_VALUE = 101000
        CUSTOM_DIMENSION_1_VALUE = 101001
        CUSTOM_DIMENSION_2_VALUE = 101002
        CUSTOM_DIMENSION_3_VALUE = 101003
        CUSTOM_DIMENSION_4_VALUE = 101004
        CUSTOM_DIMENSION_5_VALUE = 101005
        CUSTOM_DIMENSION_6_VALUE = 101006
        CUSTOM_DIMENSION_7_VALUE = 101007
        CUSTOM_DIMENSION_8_VALUE = 101008
        CUSTOM_DIMENSION_9_VALUE = 101009

    class Metric(proto.Enum):
        r"""Reporting metrics.

        Values:
            METRIC_UNSPECIFIED (0):
                Default value. This value is unused.
            ACTIVE_USERS (223):
                The number of people who engaged with your site or app in
                the specified date range from Google Analytics.

                Corresponds to "Active users" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_AUDIBLE_AT_START_PERCENT (445):
                Number of impressions with unmuted playback at start.

                Corresponds to "Active View % audible at start" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_AUDIBLE_IMPRESSIONS (659):
                Total Active View audible impressions

                Corresponds to "Total Active View audible impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_AUDIBLE_THROUGH_COMPLETION_PERCENT (446):
                Number of impressions with unmuted playback through the
                entire stream.

                Corresponds to "Active View % audible through completion" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_AUDIBLE_THROUGH_FIRST_QUARTILE_PERCENT (447):
                Number of impressions with unmuted playback through at least
                25%.

                Corresponds to "Active View % audible through first
                quartile" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_AUDIBLE_THROUGH_MIDPOINT_PERCENT (448):
                Number of impressions with unmuted playback through at least
                50%.

                Corresponds to "Active View % audible through midpoint" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_AUDIBLE_THROUGH_THIRD_QUARTILE_PERCENT (449):
                Number of impressions with unmuted playback through at least
                75%.

                Corresponds to "Active View % audible through third
                quartile" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_AUDIO_ENABLED_IMPRESSIONS (660):
                Total Active View audio enabled impressions

                Corresponds to "Total Active View audio eligible
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_AUDIO_MEASURABLE_IMPRESSIONS (661):
                Total Active View audio measurable impressions

                Corresponds to "Total Active View audio measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME (61):
                Active View total average time in seconds that specific
                impressions are reported as being viewable.

                Corresponds to "Total Active View average viewable time
                (seconds)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS (58):
                Total number of impressions that were eligible to measure
                viewability.

                Corresponds to "Total Active View eligible impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_EVER_AUDIBLE_BACKGROUNDED_PERCENT (450):
                Number of impressions where the ad player is in the
                background at any point during playback with volume > 0.

                Corresponds to "Active View % ever audible while
                backgrounded" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_EVER_AUDIBLE_PERCENT (451):
                Number of impressions where volume > 0 at any point.

                Corresponds to "Active View % ever audible" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_EVER_BACKGROUNDED_PERCENT (452):
                Number of impressions where the ad player is in the
                background at any point during playback.

                Corresponds to "Active View % ever backgrounded" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_EVER_MUTED_PERCENT (453):
                Number of impressions where volume = 0 at any point.

                Corresponds to "Active View % ever muted" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_IMPRESSIONS_AUDIBLE_AND_VISIBLIE_AT_COMPLETION (411):
                The number of measurable impressions that were played to
                video completion, and also audible and visible at the time
                of completion.

                Corresponds to "Total Active View impressions audible and
                visible at completion" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_MEASURABLE_IMPRESSIONS (57):
                The total number of impressions that were sampled and
                measured by active view.

                Corresponds to "Total Active View measurable impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE (60):
                The percentage of total impressions that were measurable by
                active view (out of all the total impressions sampled for
                active view).

                Corresponds to "Total Active View % measurable impressions"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_NON_MEASURABLE_IMPRESSIONS (662):
                Total Active View non-measurable impressions

                Corresponds to "Total Active View non-measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS (663):
                Total Active View non-viewable impressions

                Corresponds to "Total Active View non-viewable impressions"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS_DISTRIBUTION (664):
                Total Active View non-viewable impressions distribution

                Corresponds to "Total Active View non-viewable impression
                distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_PERCENT_AUDIBLE_IMPRESSIONS (665):
                Total Active View percent audible impressions

                Corresponds to "Total Active View % audible impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_PLUS_MEASURABLE_COUNT (454):
                Number of impressions where we were able to collect Active
                View+ signals.

                Corresponds to "Active View+ measurable impressions" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_REVENUE (414):
                Revenue generated from Active View impressions.

                Corresponds to "Total Active View revenue" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            ACTIVE_VIEW_UNDETERMINED_IMPRESSIONS_DISTRIBUTION (666):
                Total Active View undetermined impressions distribution

                Corresponds to "Total Active View undetermined impression
                distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_VIEWABLE_IMPRESSIONS (56):
                The total number of impressions viewed on the user's screen.

                Corresponds to "Total Active View viewable impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_DISTRIBUTION (667):
                Total Active View viewable impressions distribution

                Corresponds to "Total Active View viewable impression
                distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE (59):
                The percentage of total impressions viewed on the user's
                screen (out of the total impressions measurable by active
                view).

                Corresponds to "Total Active View % viewable impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME (73):
                Active View AdSense average time in seconds that specific
                impressions are reported as being viewable.

                Corresponds to "AdSense Active View average viewable time
                (seconds)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            ADSENSE_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS (70):
                Total number of impressions delivered by AdSense that were
                eligible to measure viewability.

                Corresponds to "AdSense Active View eligible impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ADSENSE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS (69):
                The number of impressions delivered by AdSense that were
                sampled, and measurable by active view.

                Corresponds to "AdSense Active View measurable impressions"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ADSENSE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE (72):
                The percentage of impressions delivered by AdSense that were
                measurable by active view (out of all AdSense impressions
                sampled for active view).

                Corresponds to "AdSense Active View % measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_ACTIVE_VIEW_NON_MEASURABLE_IMPRESSIONS (642):
                AdSense Active View non-measurable impressions

                Corresponds to "AdSense Active View non-measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ADSENSE_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS (643):
                AdSense Active View non-viewable impressions

                Corresponds to "AdSense Active View non-viewable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ADSENSE_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS_DISTRIBUTION (644):
                AdSense Active View non-viewable impressions distribution

                Corresponds to "AdSense Active View non-viewable impression
                distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_ACTIVE_VIEW_UNDETERMINED_IMPRESSIONS_DISTRIBUTION (645):
                AdSense Active View undetermined impressions distribution

                Corresponds to "AdSense Active View undetermined impression
                distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS (68):
                The number of impressions delivered by AdSense viewed on the
                user's screen.

                Corresponds to "AdSense Active View viewable impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ADSENSE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_DISTRIBUTION (646):
                AdSense Active View viewable impressions distribution

                Corresponds to "AdSense Active View viewable impression
                distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE (71):
                The percentage of impressions delivered by AdSense viewed on
                the user's screen (out of AdSense impressions measurable by
                active view).

                Corresponds to "AdSense Active View % viewable impressions"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_AVERAGE_ECPM (26):
                The average effective cost-per-thousand-impressions earned
                from the ads delivered by AdSense through line item dynamic
                allocation.

                Corresponds to "AdSense average eCPM" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            ADSENSE_CLICKS (23):
                Number of clicks delivered by AdSense demand channel.

                Corresponds to "AdSense clicks" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ADSENSE_CTR (24):
                The ratio of impressions served by AdSense that resulted in
                users clicking on an ad. The clickthrough rate (CTR) is
                updated nightly. The AdSense CTR is calculated as: (AdSense
                clicks / AdSense impressions).

                Corresponds to "AdSense CTR" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_IMPRESSIONS (22):
                Total impressions delivered by AdSense.

                Corresponds to "AdSense impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ADSENSE_PERCENT_CLICKS (28):
                Ratio of clicks delivered by AdSense through line item
                dynamic allocation in relation to the total clicks
                delivered.

                Corresponds to "AdSense clicks (%)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_PERCENT_IMPRESSIONS (27):
                Ratio of impressions delivered by AdSense through line item
                dynamic allocation in relation to the total impressions
                delivered.

                Corresponds to "AdSense impressions (%)" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_PERCENT_REVENUE (29):
                Ratio of revenue generated by AdSense through line item
                dynamic allocation in relation to the total revenue.

                Corresponds to "AdSense revenue (%)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_PERCENT_REVENUE_WITHOUT_CPD (30):
                Ratio of revenue generated by AdSense through line item
                dynamic allocation in relation to the total revenue
                (excluding CPD).

                Corresponds to "AdSense revenue w/o CPD (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ADSENSE_RESPONSES_SERVED (41):
                The total number of times that an AdSense ad is delivered.

                Corresponds to "AdSense responses served" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ADSENSE_REVENUE (25):
                Revenue generated from AdSense through line item dynamic
                allocation, calculated in the network's currency and time
                zone.

                Corresponds to "AdSense revenue" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXCHANGE_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME (79):
                Active View AdExchange average time in seconds that specific
                impressions are reported as being viewable.

                Corresponds to "Ad Exchange Active View average viewable
                time (seconds)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            AD_EXCHANGE_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS (76):
                Total number of impressions delivered by Ad Exchange that
                were eligible to measure viewability.

                Corresponds to "Ad Exchange Active View eligible
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS (75):
                The number of impressions delivered by Ad Exchange that were
                sampled, and measurable by active view.

                Corresponds to "Ad Exchange Active View measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE (78):
                The percentage of impressions delivered by Ad Exchange that
                were measurable by active view (out of all Ad Exchange
                impressions sampled for active view).

                Corresponds to "Ad Exchange Active View % measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_ACTIVE_VIEW_NON_MEASURABLE_IMPRESSIONS (654):
                Ad Exchange Active View non-measurable impressions

                Corresponds to "Ad Exchange Active View non-measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS (655):
                Ad Exchange Active View non-viewable impressions

                Corresponds to "Ad Exchange Active View non-viewable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS_DISTRIBUTION (656):
                Ad Exchange Active View non-viewable impressions
                distribution

                Corresponds to "Ad Exchange Active View non-viewable
                impression distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_ACTIVE_VIEW_UNDETERMINED_IMPRESSIONS_DISTRIBUTION (657):
                Ad Exchange Active View undetermined impressions
                distribution

                Corresponds to "Ad Exchange Active View undetermined
                impression distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS (74):
                The number of impressions delivered by Ad Exchange viewed on
                the user's screen.

                Corresponds to "Ad Exchange Active View viewable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_DISTRIBUTION (658):
                Ad Exchange Active View viewable impressions distribution

                Corresponds to "Ad Exchange Active View viewable impression
                distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE (77):
                The percentage of impressions delivered by Ad Exchange
                viewed on the user's screen (out of Ad Exchange impressions
                measurable by active view).

                Corresponds to "Ad Exchange Active View % viewable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_AVERAGE_ECPM (18):
                The average effective cost-per-thousand-impressions earned
                from the ads delivered by Ad Exchange through line item
                dynamic allocation.

                Corresponds to "Ad Exchange average eCPM" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXCHANGE_CLICKS (15):
                Number of clicks delivered by the Ad Exchange.

                Corresponds to "Ad Exchange clicks" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_CPC (244):
                The average effective cost-per-click earned from the ads
                delivered by Ad Exchange through line item dynamic
                allocation.

                Corresponds to "Ad Exchange CPC" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXCHANGE_CTR (16):
                The ratio of impressions served by the Ad Exchange that
                resulted in users clicking on an ad. The clickthrough rate
                (CTR) is updated nightly. Ad Exchange CTR is calculated as:
                (Ad Exchange clicks / Ad Exchange impressions).

                Corresponds to "Ad Exchange CTR" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_DELIVERY_RATE (245):
                Ratio of impressions delivered by Ad Exchange through line
                item dynamic allocation to ad requests.

                Corresponds to "Ad Exchange delivery rate" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_IMPRESSIONS (14):
                Total impressions delivered by the Ad Exchange.

                Corresponds to "Ad Exchange impressions" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_IMPRESSIONS_PER_AD_VIEWER (427):
                The total number of impressions based on the number of ad
                viewers.

                Corresponds to "Ad Exchange impressions per ad viewer" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            AD_EXCHANGE_IMPRESSIONS_PER_SESSION (428):
                The total number of impressions based on the number of
                sessions.

                Corresponds to "Ad Exchange impressions per session" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            AD_EXCHANGE_LIFT (246):
                The increase in revenue gained for won impressions over the
                applicable third party price (the minimum CPM or the best
                price specified during dynamic allocation),

                Corresponds to "Ad Exchange lift earnings" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_MATCHED_REQUEST_CTR (247):
                The ratio of matched ad requests served by the Ad Exchange
                that resulted in users clicking on an ad. The clickthrough
                rate (CTR) is updated nightly. Ad Exchange Matched Request
                CTR is calculated as: (Ad Exchange clicks / Ad Exchange
                Macthed Ad Requests).

                Corresponds to "Ad Exchange matched request CTR" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_MATCHED_REQUEST_ECPM (248):
                The average effective cost per thousand matched ad requests
                earned from the ads delivered by Ad Exchange through line
                item dynamic allocation.

                Corresponds to "Ad Exchange matched request eCPM" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXCHANGE_MATCH_RATE (249):
                The number of responses served divided by the number of
                queries eligible in ad exchange.

                Corresponds to "Ad Exchange match rate" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_OPPORTUNITIES_FROM_ERRORS (250):
                Total opportunities from video VAST error within the
                waterfall for backfill ads.

                Corresponds to "Ad Exchange opportunities from errors" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_OPPORTUNITIES_FROM_IMPRESSIONS (251):
                Number of opportunities from impressions within the
                waterfall for backfill ads.

                Corresponds to "Ad Exchange opportunities from impressions"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_PERCENT_CLICKS (20):
                Ratio of clicks delivered by Ad Exchange through line item
                dynamic allocation in relation to the total clicks
                delivered.

                Corresponds to "Ad Exchange clicks (%)" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_PERCENT_IMPRESSIONS (19):
                Ratio of impressions delivered by Ad Exchange through line
                item dynamic allocation in relation to the total impressions
                delivered.

                Corresponds to "Ad Exchange impressions (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_PERCENT_REVENUE (21):
                Ratio of revenue generated by Ad Exchange through line item
                dynamic allocation in relation to the total revenue.

                Corresponds to "Ad Exchange revenue (%)" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_PERCENT_REVENUE_WITHOUT_CPD (31):
                Ratio of revenue generated by Ad Exchange through line item
                dynamic allocation in relation to the total revenue
                (excluding CPD).

                Corresponds to "Ad Exchange revenue w/o CPD (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_PLUS_YIELD_GROUP_ECPM (252):
                The average effective cost-per-thousand-impressions earned
                from the ads delivered by Ad Exchange through line item
                dynamic allocation and yield group partners.

                Corresponds to "Ad Exchange plus yield group eCPM" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXCHANGE_PLUS_YIELD_GROUP_IMPRESSIONS (253):
                Total impressions delivered by the Ad Exchange and
                third-party networks.

                Corresponds to "Ad Exchange plus yield group impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_PLUS_YIELD_GROUP_REVENUE (254):
                Revenue generated from the Ad Exchange and Yield Group,
                calculated in your network's currency and time zone.

                Corresponds to "Ad Exchange plus yield group revenue" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXCHANGE_RESPONSES_SERVED (42):
                The total number of times that an Ad Exchange ad is
                delivered.

                Corresponds to "Ad Exchange responses served" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_REVENUE (17):
                Revenue generated from the Ad Exchange through line item
                dynamic allocation, calculated in your network's currency
                and time zone.

                Corresponds to "Ad Exchange revenue" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXCHANGE_REVENUE_PAID_THROUGH_MCM_AUTOPAYMENT (212):
                The Ad Exchange revenue accrued in the child network's own
                account but paid to their parent network through
                auto-payment. This metric is only relevant for a "Manage
                Account" child network.

                Corresponds to "Ad Exchange revenue paid through MCM
                auto-payment" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXCHANGE_REVENUE_PER_AD_VIEWER (429):
                The total amount of Ad Exchange revenue based on the number
                of ad viewers.

                Corresponds to "Ad Exchange revenue per ad viewer" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXCHANGE_TOTAL_REQUESTS (255):
                The number of programmatic eligible queries in Ad Exchange.

                Corresponds to "Ad Exchange total requests" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_EXCHANGE_TOTAL_REQUEST_CTR (256):
                The ratio of total ad requests served by the Ad Exchange
                that resulted in users clicking on an ad. The clickthrough
                rate (CTR) is updated nightly. Ad Exchange Total Request CTR
                is calculated as: (Ad Exchange clicks / Ad Exchange Total Ad
                Requests).

                Corresponds to "Ad Exchange total request CTR" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_EXCHANGE_TOTAL_REQUEST_ECPM (257):
                The average effective cost per thousand ad requests earned
                from the ads delivered by Ad Exchange through line item
                dynamic allocation and yield group partners.

                Corresponds to "Ad Exchange total request eCPM" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_EXPOSURE_SECONDS (241):
                Length of time in seconds that an ad is visible on the
                user's screen from Google Analytics.

                Corresponds to "Ad exposure (seconds)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            AD_REQUESTS (38):
                The total number of times that an ad request is sent to the
                ad server including dynamic allocation.

                Corresponds to "Total ad requests" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME (67):
                Active View ad server average time in seconds that specific
                impressions are reported as being viewable.

                Corresponds to "Ad server Active View average viewable time
                (seconds)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            AD_SERVER_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS (64):
                Total number of impressions delivered by the ad server that
                were eligible to measure viewability.

                Corresponds to "Ad server Active View eligible impressions"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS (63):
                The number of impressions delivered by the ad server that
                were sampled, and measurable by active view.

                Corresponds to "Ad server Active View measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE (66):
                The percentage of impressions delivered by the ad server
                that were measurable by active view (out of all the ad
                server impressions sampled for active view).

                Corresponds to "Ad server Active View % measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_ACTIVE_VIEW_NON_MEASURABLE_IMPRESSIONS (332):
                The number of impressions delivered by Ad Server that were
                not measured. For example, impressions where measurement was
                attempted but failed.

                Corresponds to "Ad server Active View non-measurable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS (331):
                The number of impressions delivered by Ad Server that were
                measured by active view, but deemed not viewable.

                Corresponds to "Ad server Active View non-viewable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS_DISTRIBUTION (334):
                The fraction of non-viewable impressions among eligible
                impressions from Ad Server in Active View reporting."

                Corresponds to "Ad server Active View non-viewable
                impression distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_ACTIVE_VIEW_UNDETERMINED_IMPRESSIONS_DISTRIBUTION (335):
                The fraction of non-eligible impressions among eligible
                impressions from Ad Server in Active View reporting."

                Corresponds to "Ad server Active View undetermined
                impression distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS (62):
                The number of impressions delivered by the ad server viewed
                on the user's screen.

                Corresponds to "Ad server Active View viewable impressions"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_DISTRIBUTION (333):
                The fraction of viewable impressions among eligible
                impressions from Ad Server in Active View reporting.

                Corresponds to "Ad server Active View viewable impression
                distribution" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE (65):
                The percentage of impressions delivered by the ad server
                viewed on the user's screen (out of the ad server
                impressions measurable by active view).

                Corresponds to "Ad server Active View % viewable
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_AVERAGE_ECPM (34):
                Average effective cost-per-thousand-impressions earned from
                the ads delivered by the Google Ad Manager server.

                Corresponds to "Ad server average eCPM" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_SERVER_AVERAGE_ECPM_WITHOUT_CPD (10):
                Average effective cost-per-thousand-impressions earned from
                the ads delivered by the Google Ad Manager server, excluding
                CPD value.

                Corresponds to "Ad server average eCPM w/o CPD" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_SERVER_BEGIN_TO_RENDER_IMPRESSIONS (262):
                Total raw impressions counted when creative begins to render
                or the first frame of a video is shown.

                Corresponds to "Ad server begin to render impressions" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_CLICKS (7):
                Total clicks served by the Google Ad Manager server. It
                usually takes about 30 minutes for new clicks to be recorded
                and added to the total displayed in reporting.

                Corresponds to "Ad server clicks" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_COMPLETED_VIEWS (431):
                The number of completed views for ad server.

                Corresponds to "Ad server completed views" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_COVIEWED_IMPRESSIONS (554):
                Total coviewed impressions delivered by the Ad Server.

                Corresponds to "Ad server impressions (co-viewed)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_CPD_REVENUE (32):
                CPD revenue earned, calculated in your network's currency,
                for the ads delivered by the Google Ad Manager server. Sum
                of all booked revenue.

                Corresponds to "Ad server CPD revenue" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_SERVER_CTR (8):
                Ratio of impressions served by the Google Ad Manager server
                that resulted in users clicking on an ad. The clickthrough
                rate (CTR) is updated nightly. The ad server CTR is
                calculated as: (Ad server clicks / Ad server impressions).

                Corresponds to "Ad server CTR" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_GROSS_REVENUE (483):
                Gross revenue earned, calculated in your network's currency,
                for the ads delivered by the Google Ad Manager server. This
                includes pre-rev-share revenue for Programmatic traffic.
                This metric is to help with the transition from gross to net
                revenue reporting.

                Corresponds to "Ad server total revenue (gross)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_SERVER_GROSS_REVENUE_WITHOUT_CPD (484):
                Gross revenue earned, calculated in your network's currency,
                for the ads delivered by the Google Ad Manager server,
                excluding CPD revenue. This includes pre-rev-share revenue
                for Programmatic traffic. This metric is to help with the
                transition from gross to net revenue reporting.

                Corresponds to "Ad server CPM and CPC revenue (gross)" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_SERVER_IMPRESSIONS (6):
                Total impressions delivered by the Ad Server.

                Corresponds to "Ad server impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_IMPRESSIONS_WITH_COMPANION (222):
                Total impressions delivered by the Ad Server with companion
                impressions.

                Corresponds to "Ad server impressions with companion" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_INACTIVE_BEGIN_TO_RENDER_IMPRESSIONS (338):
                Impressions (via begin to render methodology) delivered by
                the Google Ad Manager server considered inactive, as defined
                by served to a device receiving ad or bid requests
                continuously for a session of greater than 16 hours without
                a "reset" event.

                Corresponds to "Ad server inactive begin to render
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_PERCENT_CLICKS (12):
                Ratio of clicks delivered by the Google Ad Manager server in
                relation to the total clicks delivered.

                Corresponds to "Ad server clicks (%)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_PERCENT_IMPRESSIONS (11):
                Ratio of impressions delivered by the Google Ad Manager
                server in relation to the total impressions delivered.

                Corresponds to "Ad server impressions (%)" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_PERCENT_REVENUE (35):
                Ratio of revenue generated by the Google Ad Manager server
                in relation to the total revenue.

                Corresponds to "Ad server revenue (%)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_PERCENT_REVENUE_WITHOUT_CPD (13):
                Ratio of revenue generated by the Google Ad Manager server
                (excluding CPD) in relation to the total revenue.

                Corresponds to "Ad server revenue w/o CPD (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            AD_SERVER_RESPONSES_SERVED (40):
                The total number of times that an ad is served by the ad
                server.

                Corresponds to "Ad server responses served" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_REVENUE (33):
                All CPM, CPC, and CPD revenue earned, calculated in your
                network's currency, for the ads delivered by the Google Ad
                Manager server. Sum of all booked revenue.

                Corresponds to "Ad server total revenue" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_SERVER_REVENUE_PAID_THROUGH_MCM_AUTOPAYMENT (213):
                The Google Ad Manager server revenue accrued in the child
                network's own account but paid to their parent network
                through auto-payment. This metric is only relevant for a
                "Manage Account" child network.

                Corresponds to "Ad server revenue paid through MCM
                auto-payment" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_SERVER_REVENUE_WITHOUT_CPD (9):
                Revenue (excluding CPD) earned, calculated in your network's
                currency, for the ads delivered by the Google Ad Manager
                server. Sum of all booked revenue.

                Corresponds to "Ad server CPM and CPC revenue" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AD_SERVER_TARGETED_CLICKS (274):
                The number of clicks delivered by the ad server by explicit
                custom criteria targeting.

                Corresponds to "Ad server targeted clicks" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_TARGETED_IMPRESSIONS (275):
                The number of impressions delivered by the ad server by
                explicit custom criteria targeting.

                Corresponds to "Ad server targeted impressions" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_TRACKED_ADS (264):
                The number of tracked ads delivered by the ad server.

                Corresponds to "Ad server tracked ads" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_UNFILTERED_BEGIN_TO_RENDER_IMPRESSIONS (261):
                Total raw impressions counted when creative begins to render
                or the first frame of a video is shown, before invalid
                traffic filtrations by Ad Server.

                Corresponds to "Ad server unfiltered begin to render
                impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_UNFILTERED_CLICKS (259):
                Total clicks delivered by the Ad Server before spam
                filtering.

                Corresponds to "Ad server unfiltered clicks" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_UNFILTERED_DOWNLOADED_IMPRESSIONS (260):
                Total downloaded impressions delivered by the Ad Server
                before spam filtering.

                Corresponds to "Ad server unfiltered downloaded impressions"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_SERVER_UNFILTERED_IMPRESSIONS (260):
                Deprecated. This metric has been renamed to
                ``AD_SERVER_UNFILTERED_DOWNLOADED_IMPRESSIONS``. The server
                will normalize any requests using this value to
                ``AD_SERVER_UNFILTERED_DOWNLOADED_IMPRESSIONS``. This value
                will be removed on or after October 1, 2025.
            AD_SERVER_UNFILTERED_TRACKED_ADS (263):
                The number of tracked ads delivered by the ad server before
                invalid traffic filtrations.

                Corresponds to "Ad server unfiltered tracked ads" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            AD_UNIT_EXPOSURE_SECONDS (242):
                Length of time in seconds that an ad unit is visible on the
                user's screen from Google Analytics.

                Corresponds to "Ad unit exposure (seconds)" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            AD_VIEWERS (425):
                The number of users who viewed an ads on your site or app in
                the specified date range from Google Analytics.

                Corresponds to "Ad viewers" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ATN_ADS_FAILED_TO_RENDER (430):
                Number of ads that Ad Manager failed to render in the Ads
                traffic navigator report.

                Corresponds to "Ads failed to render" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_ELIGIBLE_LINE_ITEMS (342):
                Number of line items that matched an ad request in the Ads
                traffic navigator report.

                Corresponds to "Eligible line items" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_ELIGIBLE_LINE_ITEMS_AD_REQUESTS (343):
                Number of ad requests that contain eligible line items for
                the auction in the Ads traffic navigator report.

                Corresponds to "Ad requests with eligible line items" in the
                Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_HBT_ALLOWED_AD_REQUESTS (344):
                Number of ad requests that have header bidding trafficking
                demand in the Ads traffic navigator report.

                Corresponds to "Ad requests allowing header bidding
                trafficking" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_HBT_BIDS_IN_AUCTION (345):
                Number of header bidding trafficking bids that are able to
                match an ad request and enter the auction in the Ads traffic
                navigator report.

                Corresponds to "Competing header bidding trafficking bids"
                in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_HBT_BIDS_IN_AUCTION_AD_REQUESTS (346):
                Number of header bidding trafficking ad requests with bids
                in auction in the Ads traffic navigator report.

                Corresponds to "Ad requests with competing header bidding
                trafficking bids" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_HBT_CANDIDATE_BIDS (347):
                Number of header bidding trafficking candidate bids that
                match an ad request in the Ads traffic navigator report.

                Corresponds to "Header bidding trafficking bids" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_HBT_INVALID_AD_REQUESTS (348):
                Number of invalid header bidding trafficking ad requests in
                the Ads traffic navigator report.

                Corresponds to "Invalid ad requests allowing header bidding
                trafficking" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_HBT_NO_BIDS_AD_REQUESTS (472):
                Number of header bidding trafficking ad requests with no
                bids in the Ads traffic navigator report.

                Corresponds to "Header bidding trafficking ad requests with
                no bids" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_HBT_REJECTED_BIDS (349):
                Number of header bidding trafficking bids that didn't match
                the ad request in the Ads traffic navigator report.

                Corresponds to "Rejected header bidding trafficking bids" in
                the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_HBT_VALID_AD_REQUESTS (350):
                Number of ad requests with the header bidding trafficking
                demand that are valid in the Ads traffic navigator report.

                Corresponds to "Valid header bidding trafficking ad
                requests" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_HBT_WITH_BIDS_AD_REQUESTS (473):
                Number of header bidding trafficking ad requests with bids
                in the Ads traffic navigator report.

                Corresponds to "Header bidding trafficking ad requests with
                bids" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_INVALID_AD_REQUESTS (351):
                Ad requests that are not valid in the Ads traffic navigator
                report.

                Corresponds to "Invalid ad requests" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_LINE_ITEMS_CREATIVE_NOT_RETRIEVED (476):
                Number of line items with no creative retrieved in the Ads
                traffic navigator report.

                Corresponds to "Creative not retrieved" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_LINE_ITEMS_IN_AUCTION (352):
                Number of line items that matched an ad request and entered
                in auction in the Ads traffic navigator report.

                Corresponds to "Competing line items" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_LINE_ITEMS_NOT_COMPETING (515):
                Number of line items that were ranked but did not compete in
                auction in the Ads traffic navigator report.

                Corresponds to "Non-competing line items" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_LINE_ITEMS_NOT_SELECTED (353):
                Number of line items that matched an ad request but were not
                selected to compete in the auction in the Ads traffic
                navigator report.

                Corresponds to "Not selected to compete" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_LINE_ITEM_IN_AUCTION_AD_REQUESTS (354):
                Number of line item ad requests in auction in the Ads
                traffic navigator report.

                Corresponds to "Ad requests with competing line items" in
                the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_LINE_ITEM_TARGETED_AD_REQUESTS (355):
                Number of line item targeted ad requests in the Ads traffic
                navigator report.

                Corresponds to "Ad requests with targeted line items" in the
                Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_ALLOWED_AD_REQUESTS (356):
                Number of ad requests with the mediation demand in the Ads
                traffic navigator report.

                Corresponds to "Ad requests allowing mediation" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_INVALID_AD_REQUESTS (357):
                Number of invalid mediation ad requests in the Ads traffic
                navigator report.

                Corresponds to "Invalid ad requests allowing mediation" in
                the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_LOADED_ADS_FROM_CHAINS (358):
                Number of times the Yield Partner's ad was loaded in the Ads
                traffic navigator report.

                Corresponds to "Loaded ads from chains" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_NO_PARTNER_AD_REQUESTS (474):
                Number of ad requests with mediation demand having no
                partners in the Ads traffic navigator report.

                Corresponds to "Mediation requests with no partners" in the
                Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_PARTNERS_IN_AUCTION (359):
                Number of mediation yield partners in auction in the Ads
                traffic navigator report.

                Corresponds to "Competing mediation partners" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_PARTNERS_IN_AUCTION_AD_REQUESTS (360):
                Number of ad requests in auction that serve mediation chains
                in the Ads traffic navigator report.

                Corresponds to "Ad requests with competing mediation
                partners" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_REJECTED_PARTNERS (361):
                Number of mediation partners that didn't match an ad request
                in the Ads traffic navigator report.

                Corresponds to "Rejected partners" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_TARGETED_PARTNERS (362):
                Number of mediation partners that have targeted an ad
                request and are able to match it in the Ads traffic
                navigator report.

                Corresponds to "Targeted mediation partners" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_TOTAL_YIELD_PARTNERS (442):
                Number of partners on served mediation chains in the Ads
                traffic navigator report.

                Corresponds to "Total yield partners" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_UNLOADED_ADS_FROM_CHAINS (363):
                Number of ads from mediation chains that Ad Manager won't
                serve in the Ads traffic navigator report.

                Corresponds to "Unloaded ads from chains" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_UNUSED_BIDS_OR_PARTNERS (364):
                Number of times the Yield Partner's mediation chain ad was
                not reached in the Ads traffic navigator report.

                Corresponds to "Unused bids or partners" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_VALID_AD_REQUESTS (365):
                Number of ad requests that have mediation demand in the Ads
                traffic navigator report.

                Corresponds to "Valid mediation ad requests" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_MEDIATION_WITH_PARTNERS_AD_REQUESTS (475):
                Number of ad requests with mediation demand having partners
                in the Ads traffic navigator report.

                Corresponds to "Ad requests with targeted mediation
                partners" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_AD_REQUESTS_WITH_BIDS (366):
                Number of ad requests with programmatic demand that have
                received a bid in the Ads traffic navigator report.

                Corresponds to "Ad requests with bids" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_AD_REQUESTS_WITH_BID_REQUESTS_SENT (367):
                Number of ad requests with programmatic demand that have
                sent a bid to at least one buyer in the Ads traffic
                navigator report.

                Corresponds to "Ad requests with bid requests sent" in the
                Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_ALLOWED_AD_REQUESTS (368):
                Number of ad requests with programmatic demand in the Ads
                traffic navigator report.

                Corresponds to "Ad requests allowing programmatic" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_BIDS_IN_AUCTION (369):
                Number of ads with programmatic bids that entered the
                auction in the Ads traffic navigator report.

                Corresponds to "Competing programmatic bids" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_BID_IN_AUCTION_AD_REQUESTS (370):
                Number of ad requests that have received eligible
                programmatic bids to compete in the auction in the Ads
                traffic navigator report.

                Corresponds to "Ad requests with competing programmatic
                bids" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_BID_REQUESTS_SENT (371):
                Number of programmatic callout bid requests sent to buyers
                in the Ads traffic navigator report.

                Corresponds to "Bid requests sent" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_BID_REQUESTS_WITH_RESPONSE (372):
                Number of programmatic callout bid requests that resulted
                with a response in the Ads traffic navigator report.

                Corresponds to "Bid requests with response" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_BID_REQUEST_CANDIDATES (373):
                All buyers that Ad Manager could potentially send a
                programmatic bid request to in the Ads traffic navigator
                report.

                Corresponds to "Bid request candidates" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_BID_REQUEST_ERRORS (374):
                Number of programmatic callout bid requests with errors in
                the Ads traffic navigator report.

                Corresponds to "Bid request errors" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_INELIGIBLE_AD_REQUESTS (375):
                Number of ad requests that are ineligible for programmatic
                in the Ads traffic navigator report.

                Corresponds to "Invalid ad requests allowing programmatic"
                in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_REJECTED_BIDS (376):
                Number of programmatic callout bids rejected in the Ads
                traffic navigator report.

                Corresponds to "Rejected bids" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_SKIPPED_BID_REQUESTS (377):
                Number of programmatic callout bid requests Ad Manager won't
                send to buyers in the Ads traffic navigator report.

                Corresponds to "Skipped bid requests" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_TOTAL_BIDS (378):
                Number of programmatic bids that Ad Manager received from
                buyers in the Ads traffic navigator report.

                Corresponds to "Total programmatic bids" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_PROGRAMMATIC_VALID_AD_REQUESTS (379):
                Number of ad requests that allow programmatic in the Ads
                traffic navigator report.

                Corresponds to "Valid ad requests allowing programmatic" in
                the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_REJECTED_LINE_ITEMS (380):
                Number of line items targeted that didn't match an ad
                request in the Ads traffic navigator report.

                Corresponds to "Rejected line items" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_SERVED_MEDIATION_CHAINS (381):
                Number of mediation chains Ad Manager serves in the Ads
                traffic navigator report.

                Corresponds to "Served mediation chains" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_SERVED_SINGLE_ADS (382):
                Number of single ads served in the Ads traffic navigator
                report.

                Corresponds to "Served single ads" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_TARGETED_LINE_ITEMS (383):
                Number of line items with targeting that matches an ad
                request in the Ads traffic navigator report.

                Corresponds to "Targeted line items" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_TOTAL_AD_REQUESTS (384):
                Total number of ad requests which counts optimized pod
                request as a single request in the Ads traffic navigator
                report.

                Corresponds to "Total ad requests (ATN)" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_TOTAL_COMPETING_ADS_IN_AUCTION (385):
                Number of competing ads in auction in the Ads traffic
                navigator report.

                Corresponds to "Total competing ads" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_TOTAL_LOADED_ADS (387):
                Total number of ads loaded in the Ads traffic navigator
                report.

                Corresponds to "Total loaded ads" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_VALID_AD_REQUESTS (389):
                Ad requests that are valid in the Ads traffic navigator
                report.

                Corresponds to "Valid ad requests" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            ATN_YIELD_GROUP_MEDIATION_PASSBACKS (390):
                Number of times the Yield Partner passed-back on a Mediation
                chain ad in the Ads traffic navigator report.

                Corresponds to "Yield group mediation passbacks" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            AVERAGE_ECPM (37):
                eCPM averaged across the Google Ad Manager server, AdSense,
                and Ad Exchange.

                Corresponds to "Total average eCPM" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AVERAGE_ECPM_WITHOUT_CPD (5):
                eCPM averaged across the Google Ad Manager server (excluding
                CPD), AdSense, and Ad Exchange.

                Corresponds to "Total average eCPM w/o CPD" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AVERAGE_ENGAGEMENT_SECONDS_PER_SESSION (224):
                Average user engagement seconds per session in Google
                Analytics.

                Corresponds to "Average engagement time per session
                (seconds)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            AVERAGE_ENGAGEMENT_SECONDS_PER_USER (225):
                Average user engagement seconds per user in Google
                Analytics.

                Corresponds to "Average engagement time per user (seconds)"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            AVERAGE_IMPRESSIONS_PER_UNIQUE_VISITOR (418):
                The average number of unique users reached per ad
                impression.

                Corresponds to "Average impressions/unique visitor" in the
                Ad Manager UI.

                Compatible with the following report types: ``REACH``

                Data format: ``DOUBLE``
            AVERAGE_PURCHASE_REVENUE_PER_PAYING_USER (226):
                Average total purchase revenue per user in Google Analytics.

                Corresponds to "ARPPU" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AVERAGE_REVENUE_PER_USER (227):
                Average revenue earned from each active user in Google
                Analytics.

                Corresponds to "ARPU" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            AVERAGE_SESSION_SECONDS (228):
                Average length of a session in Google Analytics.

                Corresponds to "Average session duration (seconds)" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            BIDS (443):
                The number of bids.

                Corresponds to "Bids" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            BID_AVERAGE_CPM (444):
                The average CPM of the bids submitted by bidders.

                Corresponds to "Average bid CPM" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            BOUNCE_RATE (433):
                The ratio of (sessions - engaged sessions) / sessions.

                Corresponds to "Bounce rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            CLICKS (2):
                The number of times a user clicked on an ad.

                Corresponds to "Total clicks" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            CODE_SERVED_COUNT (44):
                The total number of times that the code for an ad is served
                by the ad server including dynamic allocation.

                Corresponds to "Total code served count" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            CPC_REVENUE (440):
                Total amount of CPC revenue.

                Corresponds to "CPC revenue" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``MONEY``
            CPM_REVENUE (441):
                Total amount of CPM revenue.

                Corresponds to "CPM revenue" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``MONEY``
            CREATIVE_LOAD_TIME_0_500_PERCENT (324):
                Percent of creatives whose load time is between [0, 500ms).

                Corresponds to "Creative load time 0 - 500ms (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            CREATIVE_LOAD_TIME_1000_2000_PERCENT (326):
                Percent of creatives whose load time is between [1000,
                2000ms).

                Corresponds to "Creative load time 1s - 2s (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            CREATIVE_LOAD_TIME_2000_4000_PERCENT (327):
                Percent of creatives whose load time is between [2000,
                4000ms).

                Corresponds to "Creative load time 2s - 4s (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            CREATIVE_LOAD_TIME_4000_8000_PERCENT (328):
                Percent of creatives whose load time is between [4000,
                8000ms).

                Corresponds to "Creative load time 4s - 8s (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            CREATIVE_LOAD_TIME_500_1000_PERCENT (325):
                Percent of creatives whose load time is between [500,
                1000ms).

                Corresponds to "Creative load time 500ms - 1s (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            CREATIVE_LOAD_TIME_GT_8000_PERCENT (329):
                Percent of creatives load time is greater than 8000ms.

                Corresponds to "Creative load time >8s (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            CTR (3):
                For standard ads, your ad clickthrough rate (CTR) is the
                number of ad clicks divided by the number of individual ad
                impressions expressed as a fraction. Ad CTR = Clicks / Ad
                impressions.

                Corresponds to "Total CTR" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            DEALS_BIDS (542):
                Number of bids received for a deal.

                Corresponds to "Deals bids" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            DEALS_BID_RATE (543):
                Bid rate for a deal.

                Corresponds to "Deals bid rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            DEALS_BID_REQUESTS (544):
                Number of bid requests sent for a deal.

                Corresponds to "Deals bid requests" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            DEALS_WINNING_BIDS (545):
                Number of winning bids for a deal.

                Corresponds to "Deals winning bids" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            DEALS_WIN_RATE (546):
                Bid win rate for a deal.

                Corresponds to "Deals win rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            DOM_LOAD_TO_FIRST_AD_REQUEST_0_500_PERCENT (521):
                Percent of dom load time to 1st ad request in [0, 500ms)
                range.

                Corresponds to "Page navigation to first ad request time 0 -
                500ms (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_FIRST_AD_REQUEST_1000_2000_PERCENT (522):
                Percent of dom load time to 1st ad request in [1000ms,
                2000ms) range.

                Corresponds to "Page navigation to first ad request time 1s
                - 2s (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_FIRST_AD_REQUEST_2000_4000_PERCENT (523):
                Percent of dom load time to 1st ad request in [2000ms,
                4000ms) range.

                Corresponds to "Page navigation to first ad request time 2s
                - 4s (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_FIRST_AD_REQUEST_4000_8000_PERCENT (524):
                Percent of dom load time to 1st ad request in [4000ms,
                8000ms) range.

                Corresponds to "Page navigation to first ad request time 4s
                - 8s (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_FIRST_AD_REQUEST_500_1000_PERCENT (525):
                Percent of dom load time to 1st ad request in [500ms,
                1000ms) range.

                Corresponds to "Page navigation to first ad request time
                500ms - 1s (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_FIRST_AD_REQUEST_GT_8000_PERCENT (520):
                Percent of dom load time to 1st ad request in [8000ms, +inf)
                range.

                Corresponds to "Page navigation to first ad request time >8s
                (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_TAG_LOAD_TIME_0_500_PERCENT (526):
                Percent of dom load time to tag load time in [0, 500ms)
                range.

                Corresponds to "Page navigation to tag loaded time 0 - 500ms
                (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_TAG_LOAD_TIME_1000_2000_PERCENT (527):
                Percent of dom load time to tag load time in [1000ms,
                2000ms) range.

                Corresponds to "Page navigation to tag loaded time 1s - 2s
                (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_TAG_LOAD_TIME_2000_4000_PERCENT (528):
                Percent of dom load time to tag load time in [2000ms,
                4000ms) range.

                Corresponds to "Page navigation to tag loaded time 2s - 4s
                (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_TAG_LOAD_TIME_4000_8000_PERCENT (529):
                Percent of dom load time to tag load time in [4000ms,
                8000ms) range.

                Corresponds to "Page navigation to tag loaded time 4s - 8s
                (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_TAG_LOAD_TIME_500_1000_PERCENT (531):
                Percent of dom load time to tag load time in [500ms, 1000ms)
                range.

                Corresponds to "Page navigation to tag loaded time 500ms -
                1s (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DOM_LOAD_TO_TAG_LOAD_TIME_GT_8000_PERCENT (530):
                Percent of dom load time to tag load time in [8000ms, +inf)
                range.

                Corresponds to "Page navigation to tag loaded time >8s (%)"
                in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            DROPOFF_RATE (415):
                Percentage of ad responses that didn't result in an
                impression.

                Corresponds to "Drop-off rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            ENGAGED_SESSIONS (229):
                Engaged session count from Google Analytics.

                Corresponds to "Engaged sessions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            ENGAGED_SESSIONS_PER_USER (230):
                Engaged sessions per user from Google Analytics.

                Corresponds to "Engaged sessions per user" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            ENGAGEMENT_RATE (426):
                The ratio of engaged sessions to sessions.

                Corresponds to "Engagement rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            EUROPEAN_REGULATIONS_CONSENT_RATE (270):
                Percentage of European regulations messages where the user
                consented to all of the purposes and vendors.

                Corresponds to "European regulations consent rate" in the Ad
                Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``PERCENT``
            EUROPEAN_REGULATIONS_CUSTOM_CONSENT_RATE (271):
                Percentage of European regulations messages where users made
                a consent choice after selecting "Manage options".

                Corresponds to "European regulations custom consent rate" in
                the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``PERCENT``
            EUROPEAN_REGULATIONS_MESSAGES_SHOWN (272):
                Number of times a European regulations message was shown to
                users.

                Corresponds to "European regulations messages shown" in the
                Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            EUROPEAN_REGULATIONS_NO_CONSENT_RATE (273):
                Percentage of European regulations messages where the user
                rejected all purposes and vendors.

                Corresponds to "European regulations no consent rate" in the
                Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``PERCENT``
            FILL_RATE (258):
                The rate at which an ad request is filled by the ad server
                including dynamic allocation.

                Corresponds to "Total fill rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            GOOGLE_ANALYTICS_CLICKS (231):
                The number of clicks joined with Google Analytics data.

                Corresponds to "Google Analytics clicks" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            GOOGLE_ANALYTICS_CTR (232):
                The click-through rate from Google Analytics data.

                Corresponds to "Google Analytics CTR" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            GOOGLE_ANALYTICS_ECPM (233):
                The eCPM revenue data from Google Analytics.

                Corresponds to "Google Analytics eCPM" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            GOOGLE_ANALYTICS_IMPRESSIONS (234):
                The number of impressions joined with Google Analytics data.

                Corresponds to "Google Analytics impressions" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            GOOGLE_ANALYTICS_REVENUE (235):
                The amount of revenue joined with Google Analytics data.

                Corresponds to "Google Analytics revenue" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            GOOGLE_ANALYTICS_VIEWS (236):
                Number of views of a web site or mobile screen from Google
                Analytics.

                Corresponds to "Views" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            GOOGLE_ANALYTICS_VIEWS_PER_USER (237):
                Number of views per user from Google Analytics.

                Corresponds to "Views per user" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            GOOGLE_SOLD_AUCTION_COVIEWED_IMPRESSIONS (129):
                The number of coviewed impressions sold by Google in partner
                sales.

                Corresponds to "Google-sold auction impressions (co-viewed)"
                in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            GOOGLE_SOLD_AUCTION_IMPRESSIONS (128):
                The number of auction impressions sold by Google in partner
                sales.

                Corresponds to "Google-sold auction impressions" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            GOOGLE_SOLD_COVIEWED_IMPRESSIONS (131):
                The number of coviewed impressions sold by Google in partner
                sales.

                Corresponds to "Google-sold impressions (co-viewed)" in the
                Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            GOOGLE_SOLD_IMPRESSIONS (130):
                The number of impressions sold by Google in partner sales.

                Corresponds to "Google-sold impressions" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            GOOGLE_SOLD_RESERVATION_COVIEWED_IMPRESSIONS (127):
                The number of coviewed impressions sold by Google in partner
                sales.

                Corresponds to "Google-sold reservation impressions
                (co-viewed)" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            GOOGLE_SOLD_RESERVATION_IMPRESSIONS (126):
                The number of reservation impressions sold by Google in
                partner sales.

                Corresponds to "Google-sold reservation impressions" in the
                Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            IMPRESSIONS (1):
                Total impressions from the Google Ad Manager server,
                AdSense, Ad Exchange, and yield group partners.

                Corresponds to "Total impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            INACTIVE_BEGIN_TO_RENDER_IMPRESSIONS (407):
                The number of impressions (via begin to render methodology)
                considered inactive, as defined by served to a device
                receiving ad or bid requests continuously for a session of
                greater than 16 hours without a "reset" event. Only applied
                to CTV ads.

                Corresponds to "Inactive begin to render impressions" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            INVENTORY_SHARES (547):
                The total number of inventory shares

                Corresponds to "Inventory shares" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            INVENTORY_SHARE_PARTNER_UNFILLED_OPPORTUNITIES (548):
                The total number of partner unfilled opportunities from an
                inventory share

                Corresponds to "Inventory share partner unfilled
                opportunities" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            INVOICED_IMPRESSIONS (404):
                The number of invoiced impressions.

                Corresponds to "Invoiced impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            INVOICED_UNFILLED_IMPRESSIONS (405):
                The number of invoiced unfilled impressions.

                Corresponds to "Invoiced unfilled impressions" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            MEDIATION_CHAINS_FILLED (584):
                The number of mediation chains that were filled.

                Corresponds to "Mediation chains filled" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            MUTED_IMPRESSIONS (412):
                The number of impressions where the user chose to mute the
                ad.

                Corresponds to "Total muted impressions" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            MUTE_ELIGIBLE_IMPRESSIONS (409):
                The number of impressions that had the "Mute This Ad"
                overlay applied.

                Corresponds to "Total mute eligible impressions" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            OPPORTUNITIES (463):
                The total number of opportunities from impressions and
                errors.

                Corresponds to "Total opportunities" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            OVERDELIVERED_IMPRESSIONS (432):
                The number of impressions that were overdelivered.

                Corresponds to "Total overdelivered impressions" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            PARTNER_SALES_FILLED_POD_REQUESTS (135):
                The number of filled pod requests (filled by partner or
                Google) in partner sales.

                Corresponds to "Filled pod requests" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            PARTNER_SALES_FILL_RATE (136):
                The percent of filled requests to total ad requests in
                partner sales.

                Corresponds to "Fill rate" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``PERCENT``
            PARTNER_SALES_PARTNER_MATCH_RATE (137):
                The percent of partner filled requests to total ad requests
                in partner sales.

                Corresponds to "Partner match rate" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``PERCENT``
            PARTNER_SALES_QUERIES (132):
                The number of queries eligible for partner sales.

                Corresponds to "Total partner sales ad requests" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            PARTNER_SALES_UNFILLED_IMPRESSIONS (133):
                The number of partner unfilled impressions in partner sales.
                If a pod request is not filled by partner but filled by
                Google, this metric will still count 1.

                Corresponds to "Partner unfilled impressions" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            PARTNER_SALES_UNMATCHED_QUERIES (134):
                The number of partner unmatched queries in partner sales. If
                an ad request is not filled by partner but filled by Google,
                this metric will still count 1.

                Corresponds to "Partner unmatched ad requests" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            PARTNER_SOLD_CODE_SERVED (125):
                The number of code served sold by partner in partner sales.

                Corresponds to "Partner-sold code served count" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            PARTNER_SOLD_COVIEWED_IMPRESSIONS (124):
                The number of coviewed impressions sold by partner in
                partner sales.

                Corresponds to "Partner-sold impressions (co-viewed)" in the
                Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            PARTNER_SOLD_IMPRESSIONS (123):
                The number of impressions sold by partner in partner sales.

                Corresponds to "Partner-sold impressions" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            PROGRAMMATIC_ELIGIBLE_AD_REQUESTS (177):
                The total number of ad requests eligible for programmatic
                inventory, including Programmatic Guaranteed, Preferred
                Deals, backfill, and open auction.

                Corresponds to "Programmatic eligible ad requests" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            PROGRAMMATIC_MATCH_RATE (178):
                The number of programmatic responses served divided by the
                number of programmatic eligible ad requests. Includes Ad
                Exchange, Open Bidding, and Preferred Deals.

                Corresponds to "Programmatic match rate" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            PROGRAMMATIC_RESPONSES_SERVED (176):
                Total number of ad responses served from programmatic demand
                sources. Includes Ad Exchange, Open Bidding, and Preferred
                Deals.

                Differs from AD_EXCHANGE_RESPONSES_SERVED, which doesn't
                include Open Bidding ad requests.

                Corresponds to "Programmatic responses served" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            REACH_IMPRESSIONS (416):
                Number of impressions for reach reports.

                Corresponds to "Total reach impressions" in the Ad Manager
                UI.

                Compatible with the following report types: ``REACH``

                Data format: ``INTEGER``
            RESPONSES_SERVED (39):
                The total number of times that an ad is served by the ad
                server including dynamic allocation.

                Corresponds to "Total responses served" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RETENTION (238):
                Retention of users in Google Analytics

                Corresponds to "Retention" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            REVENUE (36):
                Total amount of CPM, CPC, and CPD revenue based on the
                number of units served by the Google Ad Manager server,
                AdSense, Ad Exchange, and third-party Mediation networks.

                Corresponds to "Total revenue" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            REVENUE_PAID_THROUGH_MCM_AUTOPAYMENT (214):
                The total revenue accrued in the child network's own account
                but paid to their parent network through auto-payment. This
                metric is only relevant for a "Manage Account" child
                network.

                Corresponds to "Total revenue paid through MCM auto-payment"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            REVENUE_WITHOUT_CPD (4):
                Total amount of revenue (excluding CPD) based on the number
                of units served by the Google Ad Manager server, AdSense, Ad
                Exchange, and third-party Mediation networks.

                Corresponds to "Total CPM and CPC revenue" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            REWARDS_GRANTED (413):
                The number of rewards granted to users from watching ads.

                Corresponds to "Total rewards granted" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_AVERAGE_DISPLAY_TIME (587):
                The average amount of time (in seconds) that each rich media
                ad is displayed to users.

                Corresponds to "Average display time" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            RICH_MEDIA_AVERAGE_INTERACTION_TIME (588):
                The average amount of time (in seconds) that a user
                interacts with a rich media ad.

                Corresponds to "Average interaction time" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            RICH_MEDIA_BACKUP_IMAGES (589):
                The total number of times a backup image is served in place
                of a rich media ad.

                Corresponds to "Backup image impressions" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_CUSTOM_EVENT_COUNT (599):
                The number of times a user interacts with a specific part of
                a rich media ad.

                Corresponds to "Custom event - count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_CUSTOM_EVENT_TIME (600):
                The amount of time (in seconds) that a user interacts with a
                specific part of a rich media ad.

                Corresponds to "Custom event - time" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            RICH_MEDIA_DISPLAY_TIME (590):
                The amount of time (in seconds) that each rich media ad is
                displayed to users.

                Corresponds to "Total display time" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            RICH_MEDIA_EXPANDING_TIME (591):
                The average amount of time (in seconds) that an expanding ad
                is viewed in an expanded state.

                Corresponds to "Average expanding time" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            RICH_MEDIA_EXPANSIONS (592):
                The number of times an expanding ad was expanded.

                Corresponds to "Total expansions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_FULL_SCREEN_IMPRESSIONS (593):
                The number of times a user opens a rich media ad in full
                screen mode.

                Corresponds to "Full-screen impressions" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_INTERACTION_COUNT (594):
                The number of times that a user interacts with a rich media
                ad.

                Corresponds to "Total interactions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_INTERACTION_RATE (595):
                The ratio of rich media ad interactions to the number of
                times the ad was displayed.

                Corresponds to "Interaction rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            RICH_MEDIA_INTERACTION_TIME (596):
                The total amount of time (in seconds) that a user interacts
                with a rich media ad.

                Corresponds to "Interaction time" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            RICH_MEDIA_INTERACTIVE_IMPRESSIONS (597):
                The number of impressions where a user interacted with a
                rich media ad.

                Corresponds to "Interactive impressions" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_MANUAL_CLOSES (598):
                The number of times that a user manually closes a rich media
                ad.

                Corresponds to "Manual closes" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_COMPLETES (503):
                The number of times a rich media video was fully played.

                Corresponds to "Rich media video completes" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_INTERACTIONS (505):
                The number of times a user clicked on the graphical controls
                of a video player.

                Corresponds to "Rich media total video interactions" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_INTERACTION_RATE (504):
                The ratio of video interactions to video plays. Represented
                as a percentage.

                Corresponds to "Rich media video interaction rate" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            RICH_MEDIA_VIDEO_MIDPOINTS (506):
                The number of times a rich media video was played up to
                midpoint.

                Corresponds to "Rich media video midpoints" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_MUTES (507):
                The number of times a rich media video was muted.

                Corresponds to "Rich media video mutes" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_PAUSES (508):
                The number of times a rich media video was paused.

                Corresponds to "Rich media video pauses" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_PLAYS (509):
                The number of times a rich media video was played.

                Corresponds to "Rich media video plays" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_REPLAYS (510):
                The number of times a rich media video was restarted.

                Corresponds to "Rich media video replays" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_STOPS (511):
                The number of times a rich media video was stopped.

                Corresponds to "Rich media video stops" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_UNMUTES (512):
                The number of times a rich media video was unmuted.

                Corresponds to "Rich media video unmutes" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            RICH_MEDIA_VIDEO_VIEW_RATE (513):
                The percentage of a video watched by a user.

                Corresponds to "Rich media video view rate" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            RICH_MEDIA_VIDEO_VIEW_TIME (514):
                The average amount of time(seconds) that a rich media video
                was viewed per view.

                Corresponds to "Rich media video average view time" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            SELL_THROUGH_AVAILABLE_IMPRESSIONS (477):
                The number of forecasted impressions not reserved by any
                line item.

                Corresponds to "Available impressions" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            SELL_THROUGH_FORECASTED_IMPRESSIONS (478):
                The total number of forecasted impressions.

                Corresponds to "Forecasted impressions" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            SELL_THROUGH_RESERVED_IMPRESSIONS (479):
                The number of forecasted impressions reserved by line items.

                Corresponds to "Reserved impressions" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            SELL_THROUGH_SELL_THROUGH_RATE (480):
                The fraction of forecasted impressions reserved by line
                items.

                Corresponds to "Sell-through rate" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``PERCENT``
            SERVER_SIDE_UNWRAPPING_AVERAGE_LATENCY_MS (434):
                The average latency in milliseconds across all server-side
                unwrapping callout requests. There is no special handling
                for error or timeout responses. This reflects the entire
                chain of a parent callout request, which may result in
                multiple child callouts. This metric is not sliced by child
                callout dimensions.

                Corresponds to "Server-side unwrapping average latency
                (milliseconds)" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            SERVER_SIDE_UNWRAPPING_CALLOUTS (435):
                The total number of server-side unwrapping callout requests.

                Corresponds to "Server-side unwrapping callouts" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            SERVER_SIDE_UNWRAPPING_EMPTY_RESPONSES (436):
                The total number of server-side unwrapping callouts that
                returned an empty response. Timeouts are not considered
                empty responses.

                Corresponds to "Server-side unwrapping empty responses" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            SERVER_SIDE_UNWRAPPING_ERROR_RESPONSES (437):
                The total number of server-side unwrapping callouts that
                returned an error response. Timeouts and empty responses are
                not considered errors.

                Corresponds to "Server-side unwrapping error responses" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            SERVER_SIDE_UNWRAPPING_SUCCESSFUL_RESPONSES (438):
                The total number of successfully unwrapped, non-empty
                server-side wrapping callouts. Successful unwrapping does
                not indicate that the resulting creative was served.

                Corresponds to "Server-side unwrapping successful responses"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            SERVER_SIDE_UNWRAPPING_TIMEOUTS (439):
                The total number of server-side unwrapping callouts that
                timed out before returning a response.

                Corresponds to "Server-side unwrapping timeouts" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            SESSIONS (239):
                Count of sessions from Google Analytics.

                Corresponds to "Sessions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            TAG_LOAD_TO_FIRST_AD_REQUEST_0_500_PERCENT (455):
                Percent of tag load time to 1st ad request in [0, 500ms)
                range.

                Corresponds to "Tag loaded to first ad request time 0 -
                500ms (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            TAG_LOAD_TO_FIRST_AD_REQUEST_1000_2000_PERCENT (457):
                Percent of tag load time to 1st ad request in [1000ms,
                2000ms) range.

                Corresponds to "Tag loaded to first ad request time 1s - 2s
                (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            TAG_LOAD_TO_FIRST_AD_REQUEST_2000_4000_PERCENT (458):
                Percent of tag load time to 1st ad request in [2000ms,
                4000ms) range.

                Corresponds to "Tag loaded to first ad request time 2s - 4s
                (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            TAG_LOAD_TO_FIRST_AD_REQUEST_4000_8000_PERCENT (459):
                Percent of tag load time to 1st ad request in [4000ms,
                8000ms) range.

                Corresponds to "Tag loaded to first ad request time 4s - 8s
                (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            TAG_LOAD_TO_FIRST_AD_REQUEST_500_1000_PERCENT (456):
                Percent of tag load time to 1st ad request in [500ms,
                1000ms) range.

                Corresponds to "Tag loaded to first ad request time 500ms -
                1s (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            TAG_LOAD_TO_FIRST_AD_REQUEST_GT_8000_PERCENT (460):
                Percent of tag load time to 1st ad request in [8000ms, +inf)
                range.

                Corresponds to "Tag loaded to first ad request time >8s (%)"
                in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            TARGETED_CLICKS (276):
                The total number of clicks delivered including line
                item-level dynamic allocation by explicit custom criteria
                targeting.

                Corresponds to "Total targeted clicks" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            TARGETED_IMPRESSIONS (277):
                The total number of impressions delivered including line
                item-level dynamic allocation by explicit custom criteria
                targeting.

                Corresponds to "Total targeted impressions" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            UNFILLED_IMPRESSIONS (45):
                The total number of missed impressions due to the ad
                servers' inability to find ads to serve including dynamic
                allocation.

                Corresponds to "Unfilled impressions" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            UNIQUE_VISITORS (417):
                The total number of unique users who viewed the ad.

                Corresponds to "Total unique visitors" in the Ad Manager UI.

                Compatible with the following report types: ``REACH``

                Data format: ``INTEGER``
            UNLOADED_IMPRESSIONS_DUE_TO_CPU (408):
                The number of impressions impacted by Chrome Ads
                Intervention due to CPU usage.

                Corresponds to "Total unloaded impressions due to CPU" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            UNLOADED_IMPRESSIONS_DUE_TO_NETWORK (406):
                The number of impressions impacted by Chrome Ads
                Intervention due to network usage.

                Corresponds to "Total unloaded impressions due to Network"
                in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            UNMATCHED_AD_REQUESTS (43):
                The total number of times that an ad is not returned by the
                ad server.

                Corresponds to "Total unmatched ad requests" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            UNVIEWED_REASON_OTHER_PERCENT (550):
                The percentage of unviewed impressions due to other reasons.

                Corresponds to "Other non-viewable impression reasons (%)"
                in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            UNVIEWED_REASON_SLOT_NEVER_ENTERED_VIEWPORT_PERCENT (553):
                The percentage of unviewed impressions due to slot never
                entered viewport.

                Corresponds to "Slot never entered viewport (%)" in the Ad
                Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            UNVIEWED_REASON_USER_SCROLLED_BEFORE_AD_FILLED_PERCENT (551):
                The percentage of unviewed impressions due to scrolled past
                before ad filled.

                Corresponds to "User scrolled before ad filled (%)" in the
                Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            UNVIEWED_REASON_USER_SCROLLED_BEFORE_AD_LOADED_PERCENT (552):
                The percentage of unviewed impressions due to scrolled past
                before ad loaded.

                Corresponds to "User scrolled/navigated before ad loaded
                (%)" in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            UNVIEWED_REASON_USER_SCROLLED_BEFORE_ONE_SECOND_PERCENT (549):
                The percentage of unviewed impressions due to insufficient
                time on screen.

                Corresponds to "User scrolled/navigated before 1 second (%)"
                in the Ad Manager UI.

                Compatible with the following report types: ``AD_SPEED``

                Data format: ``PERCENT``
            USER_ENGAGEMENT_DURATION_IN_SECONDS (240):
                Time of users interacting with web site or mobile app from
                Google Analytics in seconds.

                Corresponds to "User engagement duration (seconds)" in the
                Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            USER_MESSAGES_AD_BLOCKING_EXTENSION_RATE (486):
                Fraction of page views where users had ad blocker extensions
                installed. Includes only Desktop page views.

                Corresponds to "Ad blocking extension rate" in the Ad
                Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``PERCENT``
            USER_MESSAGES_AD_BLOCKING_RECOVERY_ALLOWLISTED_COUNT (487):
                Number of ad-blocking messages shown in the selected date
                range that resulted in users adding the site to their
                allowlist to view ads

                Corresponds to "Ad blocking recovery message conversions" in
                the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_AD_BLOCKING_RECOVERY_MESSAGES_SHOWN (488):
                Number of times an ad blocking recovery message was shown to
                users.

                Corresponds to "Ad blocking recovery messages shown" in the
                Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_ALLOW_ADS_PAGEVIEWS (489):
                The number of page views generated by users with an ad
                blocking extension installed who were shown the ad blocking
                recovery message and later allowed ads.

                Corresponds to "Allow-ads page views" in the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_CCPA_MESSAGES_SHOWN (490):
                Number of times a US state regulations message was shown to
                users.

                Corresponds to "US states messages shown" in the Ad Manager
                UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_IDFA_ATT_ALERTS_SHOWN (491):
                Number of iOS ATT alerts that were triggered by an IDFA
                message (IDFA messages can be IDFA explainers or GDPR
                messages).

                Corresponds to "IDFA ATT alerts shown" in the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_IDFA_ATT_CONSENT (492):
                Number of iOS ATT alerts triggered by the IDFA message where
                the user chose to allow tracking.

                Corresponds to "IDFA ATT consent" in the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_IDFA_ATT_CONSENT_RATE (493):
                Percentage of iOS ATT alerts triggered by the IDFA message
                where the outcome was to allow tracking.

                Corresponds to "IDFA ATT consent rate" in the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``PERCENT``
            USER_MESSAGES_IDFA_ATT_DECLINE_CONSENT (494):
                Number of iOS ATT alerts triggered by the IDFA message where
                the user chose to deny tracking.

                Corresponds to "IDFA ATT decline consent" in the Ad Manager
                UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_IDFA_ATT_DECLINE_RATE (495):
                Percentage of iOS ATT alerts triggered by the IDFA message
                where the user chose to deny tracking.

                Corresponds to "IDFA ATT decline rate" in the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``PERCENT``
            USER_MESSAGES_IDFA_EXPLAINERS_SHOWN (496):
                Number of times an IDFA explainer message was shown to
                users.

                Corresponds to "IDFA explainers shown" in the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_IDFA_IAB_MESSAGES_SHOWN (497):
                Number of times a European regulations message was shown
                immediately before the iOS ATT alert.

                Corresponds to "IDFA IAB messages shown" in the Ad Manager
                UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_IDFA_NO_DECISION (498):
                Number of IDFA explainer messages where the user didn't
                choose anything.

                Corresponds to "IDFA no decision" in the Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_OFFERWALL_MESSAGES_SHOWN (121):
                Number of times an Offerwall message was shown to users.

                Corresponds to "Offerwall messages shown" in the Ad Manager
                UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_OFFERWALL_SUCCESSFUL_ENGAGEMENTS (122):
                The number of messages where the user gained an entitlement.

                Corresponds to "Monetized Offerwall engagements" in the Ad
                Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_POST_OFFERWALL_PAGEVIEWS (499):
                The number of pages viewed by users after gaining an
                entitlement. Only counts pages included for Offerwall.

                Corresponds to "Post-offerwall page views" in the Ad Manager
                UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_TOTAL_ESTIMATED_REVENUE (500):
                Revenue earned through Offerwall, including Rewarded ad
                revenue and third-party integrations.

                Corresponds to "Estimated Offerwall revenue" in the Ad
                Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``MONEY``
            USER_MESSAGES_UPTC_MESSAGES_SHOWN (501):
                Number of times an ads personalization controls message was
                shown to users.

                Corresponds to "Ads personalization messages shown" in the
                Ad Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``INTEGER``
            USER_MESSAGES_UPTC_PERSONALIZATION_OPT_OUT_RATIO (502):
                Percentage of ads personalization controls messages where
                users chose the opt-out option.

                Corresponds to "Personalization opt-out ratio" in the Ad
                Manager UI.

                Compatible with the following report types:
                ``PRIVACY_AND_MESSAGING``

                Data format: ``PERCENT``
            VIDEO_ERROR_100_COUNT (180):
                The number of errors of type 100 in reporting.

                Corresponds to "VAST error 100 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_101_COUNT (181):
                The number of errors of type 101 in reporting.

                Corresponds to "VAST error 101 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_102_COUNT (182):
                The number of errors of type 102 in reporting.

                Corresponds to "VAST error 102 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_200_COUNT (183):
                The number of errors of type 200 in reporting.

                Corresponds to "VAST error 200 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_201_COUNT (184):
                The number of errors of type 201 in reporting.

                Corresponds to "VAST error 201 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_202_COUNT (185):
                The number of errors of type 202 in reporting.

                Corresponds to "VAST error 202 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_203_COUNT (186):
                The number of errors of type 203 in reporting.

                Corresponds to "VAST error 203 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_300_COUNT (187):
                The number of errors of type 300 in reporting.

                Corresponds to "VAST error 300 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_301_COUNT (188):
                The number of errors of type 301 in reporting.

                Corresponds to "VAST error 301 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_302_COUNT (189):
                The number of errors of type 302 in reporting.

                Corresponds to "VAST error 302 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_303_COUNT (190):
                The number of errors of type 303 in reporting.

                Corresponds to "VAST error 303 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_400_COUNT (191):
                The number of errors of type 400 in reporting.

                Corresponds to "VAST error 400 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_401_COUNT (192):
                The number of errors of type 401 in reporting.

                Corresponds to "VAST error 401 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_402_COUNT (193):
                The number of errors of type 402 in reporting.

                Corresponds to "VAST error 402 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_403_COUNT (194):
                The number of errors of type 403 in reporting.

                Corresponds to "VAST error 403 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_405_COUNT (195):
                The number of errors of type 405 in reporting.

                Corresponds to "VAST error 405 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_406_COUNT (196):
                The number of errors of type 406 in reporting.

                Corresponds to "VAST error 406 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_407_COUNT (197):
                The number of errors of type 407 in reporting.

                Corresponds to "VAST error 407 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_408_COUNT (198):
                The number of errors of type 408 in reporting.

                Corresponds to "VAST error 408 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_409_COUNT (199):
                The number of errors of type 409 in reporting.

                Corresponds to "VAST error 409 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_410_COUNT (200):
                The number of errors of type 410 in reporting.

                Corresponds to "VAST error 410 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_500_COUNT (201):
                The number of errors of type 500 in reporting.

                Corresponds to "VAST error 500 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_501_COUNT (202):
                The number of errors of type 501 in reporting.

                Corresponds to "VAST error 501 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_502_COUNT (203):
                The number of errors of type 502 in reporting.

                Corresponds to "VAST error 502 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_503_COUNT (204):
                The number of errors of type 503 in reporting.

                Corresponds to "VAST error 503 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_600_COUNT (205):
                The number of errors of type 600 in reporting.

                Corresponds to "VAST error 600 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_601_COUNT (206):
                The number of errors of type 601 in reporting.

                Corresponds to "VAST error 601 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_602_COUNT (207):
                The number of errors of type 602 in reporting.

                Corresponds to "VAST error 602 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_603_COUNT (208):
                The number of errors of type 603 in reporting.

                Corresponds to "VAST error 603 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_604_COUNT (209):
                The number of errors of type 604 in reporting.

                Corresponds to "VAST error 604 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_900_COUNT (210):
                The number of errors of type 900 in reporting.

                Corresponds to "VAST error 900 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_ERROR_901_COUNT (211):
                The number of errors of type 901 in reporting.

                Corresponds to "VAST error 901 count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_INTERACTION_AVERAGE_INTERACTION_RATE (92):
                The number of user interactions with a video, on average,
                such as pause, full screen, mute, etc.

                Corresponds to "Average interaction rate" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            VIDEO_INTERACTION_COLLAPSES (93):
                The number of times a user collapses a video, either to its
                original size or to a different size.

                Corresponds to "Collapses" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_INTERACTION_EXPANDS (95):
                The number of times a user expands a video.

                Corresponds to "Expands" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_INTERACTION_FULL_SCREENS (96):
                The number of times ad clip played in full screen mode.

                Corresponds to "Full screens" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_INTERACTION_MUTES (97):
                The number of times video player was in mute state during
                play of ad clip.

                Corresponds to "Mutes" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_INTERACTION_PAUSES (98):
                The number of times user paused ad clip.

                Corresponds to "Pauses" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_INTERACTION_RESUMES (99):
                The number of times the user unpaused the video.

                Corresponds to "Resumes" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_INTERACTION_REWINDS (100):
                The number of times a user rewinds the video.

                Corresponds to "Rewinds" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_INTERACTION_UNMUTES (101):
                The number of times a user unmutes the video.

                Corresponds to "Unmutes" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_INTERACTION_VIDEO_SKIPS (102):
                The number of times a skippable video is skipped.

                Corresponds to "Skips" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_MONETIZABLE_CONTENT_VIEWS (601):
                The number of views for monetizable video content.

                Corresponds to "Monetizable content views" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_CREATIVE_SERVES (139):
                The number of total creative serves in video realtime
                reporting.

                Corresponds to "Total creative serves" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_100_COUNT (143):
                The number of errors of type 100 in video realtime
                reporting.

                Corresponds to "VAST error 100 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_101_COUNT (144):
                The number of errors of type 101 in video realtime
                reporting.

                Corresponds to "VAST error 101 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_102_COUNT (145):
                The number of errors of type 102 in video realtime
                reporting.

                Corresponds to "VAST error 102 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_200_COUNT (146):
                The number of errors of type 200 in video realtime
                reporting.

                Corresponds to "VAST error 200 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_201_COUNT (147):
                The number of errors of type 201 in video realtime
                reporting.

                Corresponds to "VAST error 201 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_202_COUNT (148):
                The number of errors of type 202 in video realtime
                reporting.

                Corresponds to "VAST error 202 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_203_COUNT (149):
                The number of errors of type 203 in video realtime
                reporting.

                Corresponds to "VAST error 203 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_300_COUNT (150):
                The number of errors of type 300 in video realtime
                reporting.

                Corresponds to "VAST error 300 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_301_COUNT (151):
                The number of errors of type 301 in video realtime
                reporting.

                Corresponds to "VAST error 301 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_302_COUNT (152):
                The number of errors of type 302 in video realtime
                reporting.

                Corresponds to "VAST error 302 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_303_COUNT (153):
                The number of errors of type 303 in video realtime
                reporting.

                Corresponds to "VAST error 303 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_400_COUNT (154):
                The number of errors of type 400 in video realtime
                reporting.

                Corresponds to "VAST error 400 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_401_COUNT (155):
                The number of errors of type 401 in video realtime
                reporting.

                Corresponds to "VAST error 401 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_402_COUNT (156):
                The number of errors of type 402 in video realtime
                reporting.

                Corresponds to "VAST error 402 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_403_COUNT (157):
                The number of errors of type 403 in video realtime
                reporting.

                Corresponds to "VAST error 403 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_405_COUNT (158):
                The number of errors of type 405 in video realtime
                reporting.

                Corresponds to "VAST error 405 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_406_COUNT (159):
                The number of errors of type 406 in video realtime
                reporting.

                Corresponds to "VAST error 406 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_407_COUNT (160):
                The number of errors of type 407 in video realtime
                reporting.

                Corresponds to "VAST error 407 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_408_COUNT (161):
                The number of errors of type 408 in video realtime
                reporting.

                Corresponds to "VAST error 408 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_409_COUNT (162):
                The number of errors of type 409 in video realtime
                reporting.

                Corresponds to "VAST error 409 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_410_COUNT (163):
                The number of errors of type 410 in video realtime
                reporting.

                Corresponds to "VAST error 410 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_500_COUNT (164):
                The number of errors of type 500 in video realtime
                reporting.

                Corresponds to "VAST error 500 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_501_COUNT (165):
                The number of errors of type 501 in video realtime
                reporting.

                Corresponds to "VAST error 501 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_502_COUNT (166):
                The number of errors of type 502 in video realtime
                reporting.

                Corresponds to "VAST error 502 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_503_COUNT (167):
                The number of errors of type 503 in video realtime
                reporting.

                Corresponds to "VAST error 503 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_600_COUNT (168):
                The number of errors of type 600 in video realtime
                reporting.

                Corresponds to "VAST error 600 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_601_COUNT (169):
                The number of errors of type 601 in video realtime
                reporting.

                Corresponds to "VAST error 601 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_602_COUNT (170):
                The number of errors of type 602 in video realtime
                reporting.

                Corresponds to "VAST error 602 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_603_COUNT (171):
                The number of errors of type 603 in video realtime
                reporting.

                Corresponds to "VAST error 603 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_604_COUNT (172):
                The number of errors of type 604 in video realtime
                reporting.

                Corresponds to "VAST error 604 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_900_COUNT (173):
                The number of errors of type 900 in video realtime
                reporting.

                Corresponds to "VAST error 900 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_ERROR_901_COUNT (174):
                The number of errors of type 901 in video realtime
                reporting.

                Corresponds to "VAST error 901 count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_IMPRESSIONS (138):
                The number of total impressions in video realtime reporting.

                Corresponds to "Total impressions" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_MATCHED_QUERIES (140):
                The number of matched queries in video realtime reporting.

                Corresponds to "Total responses served" in the Ad Manager
                UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_TOTAL_ERROR_COUNT (175):
                The number of all errors in video realtime reporting.

                Corresponds to "Total error count" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_TOTAL_QUERIES (142):
                The number of total queries in video realtime reporting.

                Corresponds to "Total ad requests" in the Ad Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_REAL_TIME_UNMATCHED_QUERIES (141):
                The number of unmatched queries in video realtime reporting.

                Corresponds to "Total unmatched ad requests" in the Ad
                Manager UI.

                Compatible with the following report types:

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_AUTO_PLAYS (103):
                Number of times that the publisher specified a video ad
                played automatically.

                Corresponds to "Auto-plays" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_AVERAGE_VIEW_RATE (104):
                Average percentage of the video watched by users.

                Corresponds to "Average view rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            VIDEO_VIEWERSHIP_AVERAGE_VIEW_TIME (105):
                Average time(seconds) users watched the video.

                Corresponds to "Average view time" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            VIDEO_VIEWERSHIP_CLICK_TO_PLAYS (106):
                Number of times that the publisher specified a video ad was
                clicked to play.

                Corresponds to "Click-to-plays" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_COMPLETES (107):
                The number of times the video played to completion.

                Corresponds to "Completes" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_COMPLETION_RATE (108):
                Percentage of times the video played to the end.

                Corresponds to "Completion rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            VIDEO_VIEWERSHIP_ENGAGED_VIEWS (109):
                The number of engaged views: ad is viewed to completion or
                for 30s, whichever comes first.

                Corresponds to "Engaged views" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_FIRST_QUARTILES (110):
                The number of times the video played to 25% of its length.

                Corresponds to "First quartiles" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_MIDPOINTS (111):
                The number of times the video reached its midpoint during
                play.

                Corresponds to "Midpoints" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_SKIP_BUTTONS_SHOWN (112):
                The number of times a skip button is shown in video.

                Corresponds to "Skip buttons shown" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_STARTS (113):
                The number of impressions where the video was played.

                Corresponds to "Starts" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_THIRD_QUARTILES (114):
                The number of times the video played to 75% of its length.

                Corresponds to "Third quartiles" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_TOTAL_ERROR_COUNT (115):
                The number of times an error occurred, such as a VAST
                redirect error, a video playback error, or an invalid
                response error.

                Corresponds to "Total error count" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            VIDEO_VIEWERSHIP_TOTAL_ERROR_RATE (94):
                The percentage of video error count.

                Corresponds to "Total error rate" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            VIDEO_VIEWERSHIP_VIDEO_LENGTH (116):
                Duration of the video creative.

                Corresponds to "Video length" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            VIDEO_VIEWERSHIP_VIEW_THROUGH_RATE (117):
                View-through rate represented as a percentage.

                Corresponds to "Video view through rate" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``PERCENT``
            YIELD_GROUP_AUCTIONS_WON (80):
                Number of winning bids received from Open Bidding buyers,
                even when the winning bid is placed at the end of a
                mediation for mobile apps chain.

                Corresponds to "Yield group auctions won" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            YIELD_GROUP_BIDS (81):
                Number of bids received from Open Bidding buyers, regardless
                of whether the returned bid competes in an auction.

                Corresponds to "Yield group bids" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            YIELD_GROUP_BIDS_IN_AUCTION (82):
                Number of bids received from Open Bidding buyers that
                competed in the auction.

                Corresponds to "Yield group bids in auction" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            YIELD_GROUP_CALLOUTS (83):
                Number of times a yield partner is asked to return bid to
                fill a yield group request.

                Corresponds to "Yield group callouts" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            YIELD_GROUP_ESTIMATED_CPM (88):
                The estimated net rate for yield groups or individual yield
                group partners.

                Corresponds to "Yield group estimated CPM" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            YIELD_GROUP_ESTIMATED_REVENUE (87):
                Total net revenue earned by a yield group, based upon the
                yield group estimated CPM and yield group impressions
                recorded.

                Corresponds to "Yield group estimated revenue" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            YIELD_GROUP_IMPRESSIONS (85):
                Number of matched yield group requests where a yield partner
                delivered their ad to publisher inventory.

                Corresponds to "Yield group impressions" in the Ad Manager
                UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            YIELD_GROUP_MEDIATION_FILL_RATE (89):
                Yield group Mediation fill rate indicating how often a
                network fills an ad request.

                Corresponds to "Yield group mediation fill rate" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            YIELD_GROUP_MEDIATION_MATCHED_QUERIES (86):
                Total requests where a Mediation chain was served.

                Corresponds to "Yield group mediation matched queries" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            YIELD_GROUP_MEDIATION_PASSBACKS (118):
                The number of mediation chain passback across all channels.

                Corresponds to "Yield group mediation passbacks" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
            YIELD_GROUP_MEDIATION_THIRD_PARTY_ECPM (90):
                Revenue per thousand impressions based on data collected by
                Ad Manager from third-party ad network reports.

                Corresponds to "Yield group mediation third party ECPM" in
                the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``DOUBLE``
            YIELD_GROUP_REVENUE_PAID_THROUGH_MCM_AUTOPAYMENT (215):
                The yield group revenue accrued in the child network's own
                account but paid to their parent network through
                auto-payment. This metric is only relevant for a "Manage
                Account" child network.

                Corresponds to "Yield group revenue paid through MCM
                auto-payment" in the Ad Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``MONEY``
            YIELD_GROUP_SUCCESSFUL_RESPONSES (84):
                Number of times a yield group buyer successfully returned a
                bid in response to a yield group callout.

                Corresponds to "Yield group successful responses" in the Ad
                Manager UI.

                Compatible with the following report types: ``HISTORICAL``

                Data format: ``INTEGER``
        """
        _pb_options = {"allow_alias": True}
        METRIC_UNSPECIFIED = 0
        ACTIVE_USERS = 223
        ACTIVE_VIEW_AUDIBLE_AT_START_PERCENT = 445
        ACTIVE_VIEW_AUDIBLE_IMPRESSIONS = 659
        ACTIVE_VIEW_AUDIBLE_THROUGH_COMPLETION_PERCENT = 446
        ACTIVE_VIEW_AUDIBLE_THROUGH_FIRST_QUARTILE_PERCENT = 447
        ACTIVE_VIEW_AUDIBLE_THROUGH_MIDPOINT_PERCENT = 448
        ACTIVE_VIEW_AUDIBLE_THROUGH_THIRD_QUARTILE_PERCENT = 449
        ACTIVE_VIEW_AUDIO_ENABLED_IMPRESSIONS = 660
        ACTIVE_VIEW_AUDIO_MEASURABLE_IMPRESSIONS = 661
        ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME = 61
        ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS = 58
        ACTIVE_VIEW_EVER_AUDIBLE_BACKGROUNDED_PERCENT = 450
        ACTIVE_VIEW_EVER_AUDIBLE_PERCENT = 451
        ACTIVE_VIEW_EVER_BACKGROUNDED_PERCENT = 452
        ACTIVE_VIEW_EVER_MUTED_PERCENT = 453
        ACTIVE_VIEW_IMPRESSIONS_AUDIBLE_AND_VISIBLIE_AT_COMPLETION = 411
        ACTIVE_VIEW_MEASURABLE_IMPRESSIONS = 57
        ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE = 60
        ACTIVE_VIEW_NON_MEASURABLE_IMPRESSIONS = 662
        ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS = 663
        ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS_DISTRIBUTION = 664
        ACTIVE_VIEW_PERCENT_AUDIBLE_IMPRESSIONS = 665
        ACTIVE_VIEW_PLUS_MEASURABLE_COUNT = 454
        ACTIVE_VIEW_REVENUE = 414
        ACTIVE_VIEW_UNDETERMINED_IMPRESSIONS_DISTRIBUTION = 666
        ACTIVE_VIEW_VIEWABLE_IMPRESSIONS = 56
        ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_DISTRIBUTION = 667
        ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE = 59
        ADSENSE_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME = 73
        ADSENSE_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS = 70
        ADSENSE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS = 69
        ADSENSE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE = 72
        ADSENSE_ACTIVE_VIEW_NON_MEASURABLE_IMPRESSIONS = 642
        ADSENSE_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS = 643
        ADSENSE_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS_DISTRIBUTION = 644
        ADSENSE_ACTIVE_VIEW_UNDETERMINED_IMPRESSIONS_DISTRIBUTION = 645
        ADSENSE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS = 68
        ADSENSE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_DISTRIBUTION = 646
        ADSENSE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE = 71
        ADSENSE_AVERAGE_ECPM = 26
        ADSENSE_CLICKS = 23
        ADSENSE_CTR = 24
        ADSENSE_IMPRESSIONS = 22
        ADSENSE_PERCENT_CLICKS = 28
        ADSENSE_PERCENT_IMPRESSIONS = 27
        ADSENSE_PERCENT_REVENUE = 29
        ADSENSE_PERCENT_REVENUE_WITHOUT_CPD = 30
        ADSENSE_RESPONSES_SERVED = 41
        ADSENSE_REVENUE = 25
        AD_EXCHANGE_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME = 79
        AD_EXCHANGE_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS = 76
        AD_EXCHANGE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS = 75
        AD_EXCHANGE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE = 78
        AD_EXCHANGE_ACTIVE_VIEW_NON_MEASURABLE_IMPRESSIONS = 654
        AD_EXCHANGE_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS = 655
        AD_EXCHANGE_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS_DISTRIBUTION = 656
        AD_EXCHANGE_ACTIVE_VIEW_UNDETERMINED_IMPRESSIONS_DISTRIBUTION = 657
        AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS = 74
        AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_DISTRIBUTION = 658
        AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE = 77
        AD_EXCHANGE_AVERAGE_ECPM = 18
        AD_EXCHANGE_CLICKS = 15
        AD_EXCHANGE_CPC = 244
        AD_EXCHANGE_CTR = 16
        AD_EXCHANGE_DELIVERY_RATE = 245
        AD_EXCHANGE_IMPRESSIONS = 14
        AD_EXCHANGE_IMPRESSIONS_PER_AD_VIEWER = 427
        AD_EXCHANGE_IMPRESSIONS_PER_SESSION = 428
        AD_EXCHANGE_LIFT = 246
        AD_EXCHANGE_MATCHED_REQUEST_CTR = 247
        AD_EXCHANGE_MATCHED_REQUEST_ECPM = 248
        AD_EXCHANGE_MATCH_RATE = 249
        AD_EXCHANGE_OPPORTUNITIES_FROM_ERRORS = 250
        AD_EXCHANGE_OPPORTUNITIES_FROM_IMPRESSIONS = 251
        AD_EXCHANGE_PERCENT_CLICKS = 20
        AD_EXCHANGE_PERCENT_IMPRESSIONS = 19
        AD_EXCHANGE_PERCENT_REVENUE = 21
        AD_EXCHANGE_PERCENT_REVENUE_WITHOUT_CPD = 31
        AD_EXCHANGE_PLUS_YIELD_GROUP_ECPM = 252
        AD_EXCHANGE_PLUS_YIELD_GROUP_IMPRESSIONS = 253
        AD_EXCHANGE_PLUS_YIELD_GROUP_REVENUE = 254
        AD_EXCHANGE_RESPONSES_SERVED = 42
        AD_EXCHANGE_REVENUE = 17
        AD_EXCHANGE_REVENUE_PAID_THROUGH_MCM_AUTOPAYMENT = 212
        AD_EXCHANGE_REVENUE_PER_AD_VIEWER = 429
        AD_EXCHANGE_TOTAL_REQUESTS = 255
        AD_EXCHANGE_TOTAL_REQUEST_CTR = 256
        AD_EXCHANGE_TOTAL_REQUEST_ECPM = 257
        AD_EXPOSURE_SECONDS = 241
        AD_REQUESTS = 38
        AD_SERVER_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME = 67
        AD_SERVER_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS = 64
        AD_SERVER_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS = 63
        AD_SERVER_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE = 66
        AD_SERVER_ACTIVE_VIEW_NON_MEASURABLE_IMPRESSIONS = 332
        AD_SERVER_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS = 331
        AD_SERVER_ACTIVE_VIEW_NON_VIEWABLE_IMPRESSIONS_DISTRIBUTION = 334
        AD_SERVER_ACTIVE_VIEW_UNDETERMINED_IMPRESSIONS_DISTRIBUTION = 335
        AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS = 62
        AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_DISTRIBUTION = 333
        AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE = 65
        AD_SERVER_AVERAGE_ECPM = 34
        AD_SERVER_AVERAGE_ECPM_WITHOUT_CPD = 10
        AD_SERVER_BEGIN_TO_RENDER_IMPRESSIONS = 262
        AD_SERVER_CLICKS = 7
        AD_SERVER_COMPLETED_VIEWS = 431
        AD_SERVER_COVIEWED_IMPRESSIONS = 554
        AD_SERVER_CPD_REVENUE = 32
        AD_SERVER_CTR = 8
        AD_SERVER_GROSS_REVENUE = 483
        AD_SERVER_GROSS_REVENUE_WITHOUT_CPD = 484
        AD_SERVER_IMPRESSIONS = 6
        AD_SERVER_IMPRESSIONS_WITH_COMPANION = 222
        AD_SERVER_INACTIVE_BEGIN_TO_RENDER_IMPRESSIONS = 338
        AD_SERVER_PERCENT_CLICKS = 12
        AD_SERVER_PERCENT_IMPRESSIONS = 11
        AD_SERVER_PERCENT_REVENUE = 35
        AD_SERVER_PERCENT_REVENUE_WITHOUT_CPD = 13
        AD_SERVER_RESPONSES_SERVED = 40
        AD_SERVER_REVENUE = 33
        AD_SERVER_REVENUE_PAID_THROUGH_MCM_AUTOPAYMENT = 213
        AD_SERVER_REVENUE_WITHOUT_CPD = 9
        AD_SERVER_TARGETED_CLICKS = 274
        AD_SERVER_TARGETED_IMPRESSIONS = 275
        AD_SERVER_TRACKED_ADS = 264
        AD_SERVER_UNFILTERED_BEGIN_TO_RENDER_IMPRESSIONS = 261
        AD_SERVER_UNFILTERED_CLICKS = 259
        AD_SERVER_UNFILTERED_DOWNLOADED_IMPRESSIONS = 260
        AD_SERVER_UNFILTERED_IMPRESSIONS = 260
        AD_SERVER_UNFILTERED_TRACKED_ADS = 263
        AD_UNIT_EXPOSURE_SECONDS = 242
        AD_VIEWERS = 425
        ATN_ADS_FAILED_TO_RENDER = 430
        ATN_ELIGIBLE_LINE_ITEMS = 342
        ATN_ELIGIBLE_LINE_ITEMS_AD_REQUESTS = 343
        ATN_HBT_ALLOWED_AD_REQUESTS = 344
        ATN_HBT_BIDS_IN_AUCTION = 345
        ATN_HBT_BIDS_IN_AUCTION_AD_REQUESTS = 346
        ATN_HBT_CANDIDATE_BIDS = 347
        ATN_HBT_INVALID_AD_REQUESTS = 348
        ATN_HBT_NO_BIDS_AD_REQUESTS = 472
        ATN_HBT_REJECTED_BIDS = 349
        ATN_HBT_VALID_AD_REQUESTS = 350
        ATN_HBT_WITH_BIDS_AD_REQUESTS = 473
        ATN_INVALID_AD_REQUESTS = 351
        ATN_LINE_ITEMS_CREATIVE_NOT_RETRIEVED = 476
        ATN_LINE_ITEMS_IN_AUCTION = 352
        ATN_LINE_ITEMS_NOT_COMPETING = 515
        ATN_LINE_ITEMS_NOT_SELECTED = 353
        ATN_LINE_ITEM_IN_AUCTION_AD_REQUESTS = 354
        ATN_LINE_ITEM_TARGETED_AD_REQUESTS = 355
        ATN_MEDIATION_ALLOWED_AD_REQUESTS = 356
        ATN_MEDIATION_INVALID_AD_REQUESTS = 357
        ATN_MEDIATION_LOADED_ADS_FROM_CHAINS = 358
        ATN_MEDIATION_NO_PARTNER_AD_REQUESTS = 474
        ATN_MEDIATION_PARTNERS_IN_AUCTION = 359
        ATN_MEDIATION_PARTNERS_IN_AUCTION_AD_REQUESTS = 360
        ATN_MEDIATION_REJECTED_PARTNERS = 361
        ATN_MEDIATION_TARGETED_PARTNERS = 362
        ATN_MEDIATION_TOTAL_YIELD_PARTNERS = 442
        ATN_MEDIATION_UNLOADED_ADS_FROM_CHAINS = 363
        ATN_MEDIATION_UNUSED_BIDS_OR_PARTNERS = 364
        ATN_MEDIATION_VALID_AD_REQUESTS = 365
        ATN_MEDIATION_WITH_PARTNERS_AD_REQUESTS = 475
        ATN_PROGRAMMATIC_AD_REQUESTS_WITH_BIDS = 366
        ATN_PROGRAMMATIC_AD_REQUESTS_WITH_BID_REQUESTS_SENT = 367
        ATN_PROGRAMMATIC_ALLOWED_AD_REQUESTS = 368
        ATN_PROGRAMMATIC_BIDS_IN_AUCTION = 369
        ATN_PROGRAMMATIC_BID_IN_AUCTION_AD_REQUESTS = 370
        ATN_PROGRAMMATIC_BID_REQUESTS_SENT = 371
        ATN_PROGRAMMATIC_BID_REQUESTS_WITH_RESPONSE = 372
        ATN_PROGRAMMATIC_BID_REQUEST_CANDIDATES = 373
        ATN_PROGRAMMATIC_BID_REQUEST_ERRORS = 374
        ATN_PROGRAMMATIC_INELIGIBLE_AD_REQUESTS = 375
        ATN_PROGRAMMATIC_REJECTED_BIDS = 376
        ATN_PROGRAMMATIC_SKIPPED_BID_REQUESTS = 377
        ATN_PROGRAMMATIC_TOTAL_BIDS = 378
        ATN_PROGRAMMATIC_VALID_AD_REQUESTS = 379
        ATN_REJECTED_LINE_ITEMS = 380
        ATN_SERVED_MEDIATION_CHAINS = 381
        ATN_SERVED_SINGLE_ADS = 382
        ATN_TARGETED_LINE_ITEMS = 383
        ATN_TOTAL_AD_REQUESTS = 384
        ATN_TOTAL_COMPETING_ADS_IN_AUCTION = 385
        ATN_TOTAL_LOADED_ADS = 387
        ATN_VALID_AD_REQUESTS = 389
        ATN_YIELD_GROUP_MEDIATION_PASSBACKS = 390
        AVERAGE_ECPM = 37
        AVERAGE_ECPM_WITHOUT_CPD = 5
        AVERAGE_ENGAGEMENT_SECONDS_PER_SESSION = 224
        AVERAGE_ENGAGEMENT_SECONDS_PER_USER = 225
        AVERAGE_IMPRESSIONS_PER_UNIQUE_VISITOR = 418
        AVERAGE_PURCHASE_REVENUE_PER_PAYING_USER = 226
        AVERAGE_REVENUE_PER_USER = 227
        AVERAGE_SESSION_SECONDS = 228
        BIDS = 443
        BID_AVERAGE_CPM = 444
        BOUNCE_RATE = 433
        CLICKS = 2
        CODE_SERVED_COUNT = 44
        CPC_REVENUE = 440
        CPM_REVENUE = 441
        CREATIVE_LOAD_TIME_0_500_PERCENT = 324
        CREATIVE_LOAD_TIME_1000_2000_PERCENT = 326
        CREATIVE_LOAD_TIME_2000_4000_PERCENT = 327
        CREATIVE_LOAD_TIME_4000_8000_PERCENT = 328
        CREATIVE_LOAD_TIME_500_1000_PERCENT = 325
        CREATIVE_LOAD_TIME_GT_8000_PERCENT = 329
        CTR = 3
        DEALS_BIDS = 542
        DEALS_BID_RATE = 543
        DEALS_BID_REQUESTS = 544
        DEALS_WINNING_BIDS = 545
        DEALS_WIN_RATE = 546
        DOM_LOAD_TO_FIRST_AD_REQUEST_0_500_PERCENT = 521
        DOM_LOAD_TO_FIRST_AD_REQUEST_1000_2000_PERCENT = 522
        DOM_LOAD_TO_FIRST_AD_REQUEST_2000_4000_PERCENT = 523
        DOM_LOAD_TO_FIRST_AD_REQUEST_4000_8000_PERCENT = 524
        DOM_LOAD_TO_FIRST_AD_REQUEST_500_1000_PERCENT = 525
        DOM_LOAD_TO_FIRST_AD_REQUEST_GT_8000_PERCENT = 520
        DOM_LOAD_TO_TAG_LOAD_TIME_0_500_PERCENT = 526
        DOM_LOAD_TO_TAG_LOAD_TIME_1000_2000_PERCENT = 527
        DOM_LOAD_TO_TAG_LOAD_TIME_2000_4000_PERCENT = 528
        DOM_LOAD_TO_TAG_LOAD_TIME_4000_8000_PERCENT = 529
        DOM_LOAD_TO_TAG_LOAD_TIME_500_1000_PERCENT = 531
        DOM_LOAD_TO_TAG_LOAD_TIME_GT_8000_PERCENT = 530
        DROPOFF_RATE = 415
        ENGAGED_SESSIONS = 229
        ENGAGED_SESSIONS_PER_USER = 230
        ENGAGEMENT_RATE = 426
        EUROPEAN_REGULATIONS_CONSENT_RATE = 270
        EUROPEAN_REGULATIONS_CUSTOM_CONSENT_RATE = 271
        EUROPEAN_REGULATIONS_MESSAGES_SHOWN = 272
        EUROPEAN_REGULATIONS_NO_CONSENT_RATE = 273
        FILL_RATE = 258
        GOOGLE_ANALYTICS_CLICKS = 231
        GOOGLE_ANALYTICS_CTR = 232
        GOOGLE_ANALYTICS_ECPM = 233
        GOOGLE_ANALYTICS_IMPRESSIONS = 234
        GOOGLE_ANALYTICS_REVENUE = 235
        GOOGLE_ANALYTICS_VIEWS = 236
        GOOGLE_ANALYTICS_VIEWS_PER_USER = 237
        GOOGLE_SOLD_AUCTION_COVIEWED_IMPRESSIONS = 129
        GOOGLE_SOLD_AUCTION_IMPRESSIONS = 128
        GOOGLE_SOLD_COVIEWED_IMPRESSIONS = 131
        GOOGLE_SOLD_IMPRESSIONS = 130
        GOOGLE_SOLD_RESERVATION_COVIEWED_IMPRESSIONS = 127
        GOOGLE_SOLD_RESERVATION_IMPRESSIONS = 126
        IMPRESSIONS = 1
        INACTIVE_BEGIN_TO_RENDER_IMPRESSIONS = 407
        INVENTORY_SHARES = 547
        INVENTORY_SHARE_PARTNER_UNFILLED_OPPORTUNITIES = 548
        INVOICED_IMPRESSIONS = 404
        INVOICED_UNFILLED_IMPRESSIONS = 405
        MEDIATION_CHAINS_FILLED = 584
        MUTED_IMPRESSIONS = 412
        MUTE_ELIGIBLE_IMPRESSIONS = 409
        OPPORTUNITIES = 463
        OVERDELIVERED_IMPRESSIONS = 432
        PARTNER_SALES_FILLED_POD_REQUESTS = 135
        PARTNER_SALES_FILL_RATE = 136
        PARTNER_SALES_PARTNER_MATCH_RATE = 137
        PARTNER_SALES_QUERIES = 132
        PARTNER_SALES_UNFILLED_IMPRESSIONS = 133
        PARTNER_SALES_UNMATCHED_QUERIES = 134
        PARTNER_SOLD_CODE_SERVED = 125
        PARTNER_SOLD_COVIEWED_IMPRESSIONS = 124
        PARTNER_SOLD_IMPRESSIONS = 123
        PROGRAMMATIC_ELIGIBLE_AD_REQUESTS = 177
        PROGRAMMATIC_MATCH_RATE = 178
        PROGRAMMATIC_RESPONSES_SERVED = 176
        REACH_IMPRESSIONS = 416
        RESPONSES_SERVED = 39
        RETENTION = 238
        REVENUE = 36
        REVENUE_PAID_THROUGH_MCM_AUTOPAYMENT = 214
        REVENUE_WITHOUT_CPD = 4
        REWARDS_GRANTED = 413
        RICH_MEDIA_AVERAGE_DISPLAY_TIME = 587
        RICH_MEDIA_AVERAGE_INTERACTION_TIME = 588
        RICH_MEDIA_BACKUP_IMAGES = 589
        RICH_MEDIA_CUSTOM_EVENT_COUNT = 599
        RICH_MEDIA_CUSTOM_EVENT_TIME = 600
        RICH_MEDIA_DISPLAY_TIME = 590
        RICH_MEDIA_EXPANDING_TIME = 591
        RICH_MEDIA_EXPANSIONS = 592
        RICH_MEDIA_FULL_SCREEN_IMPRESSIONS = 593
        RICH_MEDIA_INTERACTION_COUNT = 594
        RICH_MEDIA_INTERACTION_RATE = 595
        RICH_MEDIA_INTERACTION_TIME = 596
        RICH_MEDIA_INTERACTIVE_IMPRESSIONS = 597
        RICH_MEDIA_MANUAL_CLOSES = 598
        RICH_MEDIA_VIDEO_COMPLETES = 503
        RICH_MEDIA_VIDEO_INTERACTIONS = 505
        RICH_MEDIA_VIDEO_INTERACTION_RATE = 504
        RICH_MEDIA_VIDEO_MIDPOINTS = 506
        RICH_MEDIA_VIDEO_MUTES = 507
        RICH_MEDIA_VIDEO_PAUSES = 508
        RICH_MEDIA_VIDEO_PLAYS = 509
        RICH_MEDIA_VIDEO_REPLAYS = 510
        RICH_MEDIA_VIDEO_STOPS = 511
        RICH_MEDIA_VIDEO_UNMUTES = 512
        RICH_MEDIA_VIDEO_VIEW_RATE = 513
        RICH_MEDIA_VIDEO_VIEW_TIME = 514
        SELL_THROUGH_AVAILABLE_IMPRESSIONS = 477
        SELL_THROUGH_FORECASTED_IMPRESSIONS = 478
        SELL_THROUGH_RESERVED_IMPRESSIONS = 479
        SELL_THROUGH_SELL_THROUGH_RATE = 480
        SERVER_SIDE_UNWRAPPING_AVERAGE_LATENCY_MS = 434
        SERVER_SIDE_UNWRAPPING_CALLOUTS = 435
        SERVER_SIDE_UNWRAPPING_EMPTY_RESPONSES = 436
        SERVER_SIDE_UNWRAPPING_ERROR_RESPONSES = 437
        SERVER_SIDE_UNWRAPPING_SUCCESSFUL_RESPONSES = 438
        SERVER_SIDE_UNWRAPPING_TIMEOUTS = 439
        SESSIONS = 239
        TAG_LOAD_TO_FIRST_AD_REQUEST_0_500_PERCENT = 455
        TAG_LOAD_TO_FIRST_AD_REQUEST_1000_2000_PERCENT = 457
        TAG_LOAD_TO_FIRST_AD_REQUEST_2000_4000_PERCENT = 458
        TAG_LOAD_TO_FIRST_AD_REQUEST_4000_8000_PERCENT = 459
        TAG_LOAD_TO_FIRST_AD_REQUEST_500_1000_PERCENT = 456
        TAG_LOAD_TO_FIRST_AD_REQUEST_GT_8000_PERCENT = 460
        TARGETED_CLICKS = 276
        TARGETED_IMPRESSIONS = 277
        UNFILLED_IMPRESSIONS = 45
        UNIQUE_VISITORS = 417
        UNLOADED_IMPRESSIONS_DUE_TO_CPU = 408
        UNLOADED_IMPRESSIONS_DUE_TO_NETWORK = 406
        UNMATCHED_AD_REQUESTS = 43
        UNVIEWED_REASON_OTHER_PERCENT = 550
        UNVIEWED_REASON_SLOT_NEVER_ENTERED_VIEWPORT_PERCENT = 553
        UNVIEWED_REASON_USER_SCROLLED_BEFORE_AD_FILLED_PERCENT = 551
        UNVIEWED_REASON_USER_SCROLLED_BEFORE_AD_LOADED_PERCENT = 552
        UNVIEWED_REASON_USER_SCROLLED_BEFORE_ONE_SECOND_PERCENT = 549
        USER_ENGAGEMENT_DURATION_IN_SECONDS = 240
        USER_MESSAGES_AD_BLOCKING_EXTENSION_RATE = 486
        USER_MESSAGES_AD_BLOCKING_RECOVERY_ALLOWLISTED_COUNT = 487
        USER_MESSAGES_AD_BLOCKING_RECOVERY_MESSAGES_SHOWN = 488
        USER_MESSAGES_ALLOW_ADS_PAGEVIEWS = 489
        USER_MESSAGES_CCPA_MESSAGES_SHOWN = 490
        USER_MESSAGES_IDFA_ATT_ALERTS_SHOWN = 491
        USER_MESSAGES_IDFA_ATT_CONSENT = 492
        USER_MESSAGES_IDFA_ATT_CONSENT_RATE = 493
        USER_MESSAGES_IDFA_ATT_DECLINE_CONSENT = 494
        USER_MESSAGES_IDFA_ATT_DECLINE_RATE = 495
        USER_MESSAGES_IDFA_EXPLAINERS_SHOWN = 496
        USER_MESSAGES_IDFA_IAB_MESSAGES_SHOWN = 497
        USER_MESSAGES_IDFA_NO_DECISION = 498
        USER_MESSAGES_OFFERWALL_MESSAGES_SHOWN = 121
        USER_MESSAGES_OFFERWALL_SUCCESSFUL_ENGAGEMENTS = 122
        USER_MESSAGES_POST_OFFERWALL_PAGEVIEWS = 499
        USER_MESSAGES_TOTAL_ESTIMATED_REVENUE = 500
        USER_MESSAGES_UPTC_MESSAGES_SHOWN = 501
        USER_MESSAGES_UPTC_PERSONALIZATION_OPT_OUT_RATIO = 502
        VIDEO_ERROR_100_COUNT = 180
        VIDEO_ERROR_101_COUNT = 181
        VIDEO_ERROR_102_COUNT = 182
        VIDEO_ERROR_200_COUNT = 183
        VIDEO_ERROR_201_COUNT = 184
        VIDEO_ERROR_202_COUNT = 185
        VIDEO_ERROR_203_COUNT = 186
        VIDEO_ERROR_300_COUNT = 187
        VIDEO_ERROR_301_COUNT = 188
        VIDEO_ERROR_302_COUNT = 189
        VIDEO_ERROR_303_COUNT = 190
        VIDEO_ERROR_400_COUNT = 191
        VIDEO_ERROR_401_COUNT = 192
        VIDEO_ERROR_402_COUNT = 193
        VIDEO_ERROR_403_COUNT = 194
        VIDEO_ERROR_405_COUNT = 195
        VIDEO_ERROR_406_COUNT = 196
        VIDEO_ERROR_407_COUNT = 197
        VIDEO_ERROR_408_COUNT = 198
        VIDEO_ERROR_409_COUNT = 199
        VIDEO_ERROR_410_COUNT = 200
        VIDEO_ERROR_500_COUNT = 201
        VIDEO_ERROR_501_COUNT = 202
        VIDEO_ERROR_502_COUNT = 203
        VIDEO_ERROR_503_COUNT = 204
        VIDEO_ERROR_600_COUNT = 205
        VIDEO_ERROR_601_COUNT = 206
        VIDEO_ERROR_602_COUNT = 207
        VIDEO_ERROR_603_COUNT = 208
        VIDEO_ERROR_604_COUNT = 209
        VIDEO_ERROR_900_COUNT = 210
        VIDEO_ERROR_901_COUNT = 211
        VIDEO_INTERACTION_AVERAGE_INTERACTION_RATE = 92
        VIDEO_INTERACTION_COLLAPSES = 93
        VIDEO_INTERACTION_EXPANDS = 95
        VIDEO_INTERACTION_FULL_SCREENS = 96
        VIDEO_INTERACTION_MUTES = 97
        VIDEO_INTERACTION_PAUSES = 98
        VIDEO_INTERACTION_RESUMES = 99
        VIDEO_INTERACTION_REWINDS = 100
        VIDEO_INTERACTION_UNMUTES = 101
        VIDEO_INTERACTION_VIDEO_SKIPS = 102
        VIDEO_MONETIZABLE_CONTENT_VIEWS = 601
        VIDEO_REAL_TIME_CREATIVE_SERVES = 139
        VIDEO_REAL_TIME_ERROR_100_COUNT = 143
        VIDEO_REAL_TIME_ERROR_101_COUNT = 144
        VIDEO_REAL_TIME_ERROR_102_COUNT = 145
        VIDEO_REAL_TIME_ERROR_200_COUNT = 146
        VIDEO_REAL_TIME_ERROR_201_COUNT = 147
        VIDEO_REAL_TIME_ERROR_202_COUNT = 148
        VIDEO_REAL_TIME_ERROR_203_COUNT = 149
        VIDEO_REAL_TIME_ERROR_300_COUNT = 150
        VIDEO_REAL_TIME_ERROR_301_COUNT = 151
        VIDEO_REAL_TIME_ERROR_302_COUNT = 152
        VIDEO_REAL_TIME_ERROR_303_COUNT = 153
        VIDEO_REAL_TIME_ERROR_400_COUNT = 154
        VIDEO_REAL_TIME_ERROR_401_COUNT = 155
        VIDEO_REAL_TIME_ERROR_402_COUNT = 156
        VIDEO_REAL_TIME_ERROR_403_COUNT = 157
        VIDEO_REAL_TIME_ERROR_405_COUNT = 158
        VIDEO_REAL_TIME_ERROR_406_COUNT = 159
        VIDEO_REAL_TIME_ERROR_407_COUNT = 160
        VIDEO_REAL_TIME_ERROR_408_COUNT = 161
        VIDEO_REAL_TIME_ERROR_409_COUNT = 162
        VIDEO_REAL_TIME_ERROR_410_COUNT = 163
        VIDEO_REAL_TIME_ERROR_500_COUNT = 164
        VIDEO_REAL_TIME_ERROR_501_COUNT = 165
        VIDEO_REAL_TIME_ERROR_502_COUNT = 166
        VIDEO_REAL_TIME_ERROR_503_COUNT = 167
        VIDEO_REAL_TIME_ERROR_600_COUNT = 168
        VIDEO_REAL_TIME_ERROR_601_COUNT = 169
        VIDEO_REAL_TIME_ERROR_602_COUNT = 170
        VIDEO_REAL_TIME_ERROR_603_COUNT = 171
        VIDEO_REAL_TIME_ERROR_604_COUNT = 172
        VIDEO_REAL_TIME_ERROR_900_COUNT = 173
        VIDEO_REAL_TIME_ERROR_901_COUNT = 174
        VIDEO_REAL_TIME_IMPRESSIONS = 138
        VIDEO_REAL_TIME_MATCHED_QUERIES = 140
        VIDEO_REAL_TIME_TOTAL_ERROR_COUNT = 175
        VIDEO_REAL_TIME_TOTAL_QUERIES = 142
        VIDEO_REAL_TIME_UNMATCHED_QUERIES = 141
        VIDEO_VIEWERSHIP_AUTO_PLAYS = 103
        VIDEO_VIEWERSHIP_AVERAGE_VIEW_RATE = 104
        VIDEO_VIEWERSHIP_AVERAGE_VIEW_TIME = 105
        VIDEO_VIEWERSHIP_CLICK_TO_PLAYS = 106
        VIDEO_VIEWERSHIP_COMPLETES = 107
        VIDEO_VIEWERSHIP_COMPLETION_RATE = 108
        VIDEO_VIEWERSHIP_ENGAGED_VIEWS = 109
        VIDEO_VIEWERSHIP_FIRST_QUARTILES = 110
        VIDEO_VIEWERSHIP_MIDPOINTS = 111
        VIDEO_VIEWERSHIP_SKIP_BUTTONS_SHOWN = 112
        VIDEO_VIEWERSHIP_STARTS = 113
        VIDEO_VIEWERSHIP_THIRD_QUARTILES = 114
        VIDEO_VIEWERSHIP_TOTAL_ERROR_COUNT = 115
        VIDEO_VIEWERSHIP_TOTAL_ERROR_RATE = 94
        VIDEO_VIEWERSHIP_VIDEO_LENGTH = 116
        VIDEO_VIEWERSHIP_VIEW_THROUGH_RATE = 117
        YIELD_GROUP_AUCTIONS_WON = 80
        YIELD_GROUP_BIDS = 81
        YIELD_GROUP_BIDS_IN_AUCTION = 82
        YIELD_GROUP_CALLOUTS = 83
        YIELD_GROUP_ESTIMATED_CPM = 88
        YIELD_GROUP_ESTIMATED_REVENUE = 87
        YIELD_GROUP_IMPRESSIONS = 85
        YIELD_GROUP_MEDIATION_FILL_RATE = 89
        YIELD_GROUP_MEDIATION_MATCHED_QUERIES = 86
        YIELD_GROUP_MEDIATION_PASSBACKS = 118
        YIELD_GROUP_MEDIATION_THIRD_PARTY_ECPM = 90
        YIELD_GROUP_REVENUE_PAID_THROUGH_MCM_AUTOPAYMENT = 215
        YIELD_GROUP_SUCCESSFUL_RESPONSES = 84

    class TimePeriodColumn(proto.Enum):
        r"""Valid time period columns.

        Values:
            TIME_PERIOD_COLUMN_UNSPECIFIED (0):
                Default value. Report will have no time
                period column.
            TIME_PERIOD_COLUMN_DATE (1):
                A column for each date in the report.
            TIME_PERIOD_COLUMN_WEEK (2):
                A column for each week in the report.
            TIME_PERIOD_COLUMN_MONTH (3):
                A column for each month in the report.
            TIME_PERIOD_COLUMN_QUARTER (4):
                A column for each quarter in the report.
        """
        TIME_PERIOD_COLUMN_UNSPECIFIED = 0
        TIME_PERIOD_COLUMN_DATE = 1
        TIME_PERIOD_COLUMN_WEEK = 2
        TIME_PERIOD_COLUMN_MONTH = 3
        TIME_PERIOD_COLUMN_QUARTER = 4

    class MetricValueType(proto.Enum):
        r"""Possible metric value types to add.

        Values:
            PRIMARY (0):
                The values for the primary date_range.
            PRIMARY_PERCENT_OF_TOTAL (1):
                Each metrics' percent of the total for the primary
                date_range.
            COMPARISON (2):
                The values for the comparison_date_range.
            COMPARISON_PERCENT_OF_TOTAL (3):
                Each metrics' percent of the total for the
                comparison_date_range.
            ABSOLUTE_CHANGE (4):
                The absolute change between the primary and
                comparison date ranges.
            RELATIVE_CHANGE (5):
                The relative change between the primary and
                comparison date ranges.
        """
        PRIMARY = 0
        PRIMARY_PERCENT_OF_TOTAL = 1
        COMPARISON = 2
        COMPARISON_PERCENT_OF_TOTAL = 3
        ABSOLUTE_CHANGE = 4
        RELATIVE_CHANGE = 5

    class TimeZoneSource(proto.Enum):
        r"""The source to determine the time zone for the report.

        Values:
            TIME_ZONE_SOURCE_UNSPECIFIED (0):
                Unspecified default value.
            PUBLISHER (1):
                Use the publisher's time zone in network
                settings.
            AD_EXCHANGE (2):
                Use the time zone of the ad exchange.
                Only compatible with Ad Exchange dimensions and
                metrics.
            UTC (3):
                Use UTC time zone.
                Only compatible with Revenue Verification
                reports.
            PROVIDED (4):
                Use the time zone provided in the ReportDefinition.time_zone
                field. Has limited dimension and metric compatibility
                compared with PUBLISHER, and reports may take longer to run
                since the dates are dynamically calculated at request time.
        """
        TIME_ZONE_SOURCE_UNSPECIFIED = 0
        PUBLISHER = 1
        AD_EXCHANGE = 2
        UTC = 3
        PROVIDED = 4

    class Field(proto.Message):
        r"""A dimension or a metric in a report.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            dimension (google.ads.admanager_v1.types.ReportDefinition.Dimension):
                The dimension this field represents.

                This field is a member of `oneof`_ ``field``.
            metric (google.ads.admanager_v1.types.ReportDefinition.Metric):
                The metric this field represents.

                This field is a member of `oneof`_ ``field``.
        """

        dimension: "ReportDefinition.Dimension" = proto.Field(
            proto.ENUM,
            number=1,
            oneof="field",
            enum="ReportDefinition.Dimension",
        )
        metric: "ReportDefinition.Metric" = proto.Field(
            proto.ENUM,
            number=2,
            oneof="field",
            enum="ReportDefinition.Metric",
        )

    class DateRange(proto.Message):
        r"""A date range for a report.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            fixed (google.ads.admanager_v1.types.ReportDefinition.DateRange.FixedDateRange):
                A fixed date range.

                This field is a member of `oneof`_ ``date_range_type``.
            relative (google.ads.admanager_v1.types.ReportDefinition.DateRange.RelativeDateRange):
                A relative date range.

                This field is a member of `oneof`_ ``date_range_type``.
        """

        class RelativeDateRange(proto.Enum):
            r"""Options for relative date ranges.

            Values:
                RELATIVE_DATE_RANGE_UNSPECIFIED (0):
                    Default value. This value is unused.
                TODAY (1):
                    The date the report is run.
                YESTERDAY (2):
                    The date a day before the date that the
                    report is run.
                THIS_WEEK (3):
                    The full week in which this report is run.
                    Could include dates in the future.
                THIS_WEEK_TO_DATE (29):
                    From the beginning of the calendar week
                    (Monday to Sunday) in which the up to and
                    including the day the report is run.
                THIS_MONTH (4):
                    The full month in which this report is run.
                    Could include dates in the future.
                THIS_MONTH_TO_DATE (26):
                    From the beginning of the calendar month in
                    which the report is run, to up to and including
                    the day the report is run.
                THIS_QUARTER (5):
                    The full quarter in which this report is run.
                    Could include dates in the future.
                THIS_QUARTER_TO_DATE (27):
                    From the beginning of the calendar quarter in
                    which the report is run, up to and including the
                    day the report is run.
                THIS_YEAR (6):
                    The full year in which this report is run.
                    Could include dates in the future.
                THIS_YEAR_TO_DATE (28):
                    From the beginning of the calendar year in
                    which the report is run, to up to and including
                    the day the report is run.
                LAST_WEEK (7):
                    The entire previous calendar week, Monday to
                    Sunday (inclusive), preceding the calendar week
                    the report is run.
                LAST_MONTH (8):
                    The entire previous calendar month preceding
                    the calendar month the report is run.
                LAST_QUARTER (9):
                    The entire previous calendar quarter
                    preceding the calendar quarter the report is
                    run.
                LAST_YEAR (10):
                    The entire previous calendar year preceding
                    the calendar year the report is run.
                LAST_7_DAYS (11):
                    The 7 days preceding the day the report is
                    run.
                LAST_30_DAYS (12):
                    The 30 days preceding the day the report is
                    run.
                LAST_60_DAYS (13):
                    The 60 days preceding the day the report is
                    run.
                LAST_90_DAYS (14):
                    The 90 days preceding the day the report is
                    run.
                LAST_180_DAYS (15):
                    The 180 days preceding the day the report is
                    run.
                LAST_360_DAYS (16):
                    The 360 days preceding the day the report is
                    run.
                LAST_365_DAYS (17):
                    The 365 days preceding the day the report is
                    run.
                LAST_3_MONTHS (18):
                    The entire previous 3 calendar months
                    preceding the calendar month the report is run.
                LAST_6_MONTHS (19):
                    The entire previous 6 calendar months
                    preceding the calendar month the report is run.
                LAST_12_MONTHS (20):
                    The entire previous 6 calendar months
                    preceding the calendar month the report is run.
                ALL_AVAILABLE (21):
                    From 3 years before the report is run, to the
                    day before the report is run, inclusive.
                TOMORROW (30):
                    The date a day after the date that the report
                    is run.
                NEXT_90_DAYS (31):
                    The 90 days following the day the report is
                    run.
                NEXT_MONTH (32):
                    The entire calendar month following the
                    calendar month the report is run.
                NEXT_3_MONTHS (33):
                    The entire 3 calendar months following the
                    calendar month the report is run.
                NEXT_12_MONTHS (34):
                    The entire 12 calendar months following the
                    calendar month the report is run.
                NEXT_WEEK (35):
                    The entire calendar week, Monday to Sunday
                    (inclusive), following the calendar week the
                    report is run.
                NEXT_QUARTER (36):
                    The entire calendar quarter following the
                    calendar quarter the report is run.
                TO_END_OF_NEXT_MONTH (37):
                    From the date a day after the date that the
                    report is run, to the end of the calendar month
                    following the calendar month the report is run.
                PREVIOUS_PERIOD (22):
                    Only valid when used in the comparison_date_range field. The
                    complete period preceding the date period provided in
                    date_range.

                    In the case where date_range is a FixedDateRange of N days,
                    this will be a period of N days where the end date is the
                    date preceding the start date of the date_range.

                    In the case where date_range is a RelativeDateRange, this
                    will be a period of the same timeframe preceding the
                    date_range. In the case where the date_range does not
                    capture the full period because a report is run in the
                    middle of that period, this will still be the full preceding
                    period. For example, if date_range is THIS_WEEK, but the
                    report is run on a Wednesday, THIS_WEEK will be Monday -
                    Wednesday, but PREVIOUS_PERIOD will be Monday - Sunday.
                SAME_PERIOD_PREVIOUS_YEAR (24):
                    Only valid when used in the comparison_date_range field. The
                    period starting 1 year prior to the date period provided in
                    date_range.

                    In the case where date_range is a FixedDateRange, this will
                    be a date range starting 1 year prior to the date_range
                    start date and ending 1 year prior to the date_range end
                    date.

                    In the case where date_range is a RelativeDateRange, this
                    will be a period of the same timeframe exactly 1 year prior
                    to the date_range. In the case where the date_range does not
                    capture the full period because a report is run in the
                    middle of that period, this will still be the full period 1
                    year prior. For example, if date range is THIS_WEEK, but the
                    report is run on a Wednesday, THIS_WEEK will be Monday -
                    Wednesday, but SAME_PERIOD_PREVIOUS_YEAR will be Monday -
                    Sunday.
            """
            RELATIVE_DATE_RANGE_UNSPECIFIED = 0
            TODAY = 1
            YESTERDAY = 2
            THIS_WEEK = 3
            THIS_WEEK_TO_DATE = 29
            THIS_MONTH = 4
            THIS_MONTH_TO_DATE = 26
            THIS_QUARTER = 5
            THIS_QUARTER_TO_DATE = 27
            THIS_YEAR = 6
            THIS_YEAR_TO_DATE = 28
            LAST_WEEK = 7
            LAST_MONTH = 8
            LAST_QUARTER = 9
            LAST_YEAR = 10
            LAST_7_DAYS = 11
            LAST_30_DAYS = 12
            LAST_60_DAYS = 13
            LAST_90_DAYS = 14
            LAST_180_DAYS = 15
            LAST_360_DAYS = 16
            LAST_365_DAYS = 17
            LAST_3_MONTHS = 18
            LAST_6_MONTHS = 19
            LAST_12_MONTHS = 20
            ALL_AVAILABLE = 21
            TOMORROW = 30
            NEXT_90_DAYS = 31
            NEXT_MONTH = 32
            NEXT_3_MONTHS = 33
            NEXT_12_MONTHS = 34
            NEXT_WEEK = 35
            NEXT_QUARTER = 36
            TO_END_OF_NEXT_MONTH = 37
            PREVIOUS_PERIOD = 22
            SAME_PERIOD_PREVIOUS_YEAR = 24

        class FixedDateRange(proto.Message):
            r"""A date range between two fixed dates (inclusive of end date).

            Attributes:
                start_date (google.type.date_pb2.Date):
                    Required. The start date of this date range.
                end_date (google.type.date_pb2.Date):
                    Required. The end date (inclusive) of this
                    date range.
            """

            start_date: date_pb2.Date = proto.Field(
                proto.MESSAGE,
                number=1,
                message=date_pb2.Date,
            )
            end_date: date_pb2.Date = proto.Field(
                proto.MESSAGE,
                number=2,
                message=date_pb2.Date,
            )

        fixed: "ReportDefinition.DateRange.FixedDateRange" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="date_range_type",
            message="ReportDefinition.DateRange.FixedDateRange",
        )
        relative: "ReportDefinition.DateRange.RelativeDateRange" = proto.Field(
            proto.ENUM,
            number=2,
            oneof="date_range_type",
            enum="ReportDefinition.DateRange.RelativeDateRange",
        )

    class Filter(proto.Message):
        r"""A filter over one or more fields.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            field_filter (google.ads.admanager_v1.types.ReportDefinition.Filter.FieldFilter):
                A filter on a single field.

                This field is a member of `oneof`_ ``type``.
            not_filter (google.ads.admanager_v1.types.ReportDefinition.Filter):
                A filter whose result is negated.

                This field is a member of `oneof`_ ``type``.
            and_filter (google.ads.admanager_v1.types.ReportDefinition.Filter.FilterList):
                A list of filters whose results are AND-ed.

                This field is a member of `oneof`_ ``type``.
            or_filter (google.ads.admanager_v1.types.ReportDefinition.Filter.FilterList):
                A list of filters whose results are OR-ed.

                This field is a member of `oneof`_ ``type``.
        """

        class Operation(proto.Enum):
            r"""Supported filter operations.

            Values:
                IN (0):
                    For scalar operands, checks if the operand is
                    in the set of provided filter values.

                    For list operands, checks if any element in the
                    operand is in the set of provided filter values.

                    Default value.
                NOT_IN (1):
                    For scalar operands, checks that the operand
                    is not in the set of provided filter values.

                    For list operands, checks that none of the
                    elements in the operand is in the set of
                    provided filter values.
                CONTAINS (2):
                    For scalar string operands, checks if the
                    operand contains any of the provided filter
                    substrings.

                    For string list operands, checks if any string
                    in the operand contains any of the provided
                    filter substrings.
                NOT_CONTAINS (3):
                    For scalar string operands, checks that the
                    operand contains none of the provided filter
                    substrings.

                    For string list operands, checks that none of
                    the strings in the operand contain none of the
                    provided filter substrings.
                LESS_THAN (4):
                    Operand is less than the provided filter
                    value.
                LESS_THAN_EQUALS (5):
                    Operand is less than or equal to provided
                    filter value.
                GREATER_THAN (6):
                    Operand is greater than provided filter
                    value.
                GREATER_THAN_EQUALS (7):
                    Operand is greater than or equal to provided
                    filter value.
                BETWEEN (8):
                    Operand is between provided filter values.
                MATCHES (9):
                    Operand matches against a regular expression
                    or set of regular expressions (one must match).
                NOT_MATCHES (10):
                    Operand negative matches against a regular
                    expression or set of regular expressions (none
                    must match).
            """
            IN = 0
            NOT_IN = 1
            CONTAINS = 2
            NOT_CONTAINS = 3
            LESS_THAN = 4
            LESS_THAN_EQUALS = 5
            GREATER_THAN = 6
            GREATER_THAN_EQUALS = 7
            BETWEEN = 8
            MATCHES = 9
            NOT_MATCHES = 10

        class FieldFilter(proto.Message):
            r"""A filter on a specific field.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                field (google.ads.admanager_v1.types.ReportDefinition.Field):
                    Required. The field to filter on.
                operation (google.ads.admanager_v1.types.ReportDefinition.Filter.Operation):
                    Required. The operation of this filter.
                values (MutableSequence[google.ads.admanager_v1.types.ReportValue]):
                    Required. Values to filter to.
                slice_ (google.ads.admanager_v1.types.ReportDefinition.Slice):
                    Optional. Use to filter on a specific slice
                    of data.

                    This field is a member of `oneof`_ ``_slice``.
                time_period_index (int):
                    Optional. When using time period columns, use
                    this to filter on a specific column.

                    This field is a member of `oneof`_ ``_time_period_index``.
                metric_value_type (google.ads.admanager_v1.types.ReportDefinition.MetricValueType):
                    Optional. Use to specify which metric value
                    type to filter on. Defaults to PRIMARY.

                    This field is a member of `oneof`_ ``_metric_value_type``.
            """

            field: "ReportDefinition.Field" = proto.Field(
                proto.MESSAGE,
                number=1,
                message="ReportDefinition.Field",
            )
            operation: "ReportDefinition.Filter.Operation" = proto.Field(
                proto.ENUM,
                number=2,
                enum="ReportDefinition.Filter.Operation",
            )
            values: MutableSequence[report_value.ReportValue] = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message=report_value.ReportValue,
            )
            slice_: "ReportDefinition.Slice" = proto.Field(
                proto.MESSAGE,
                number=4,
                optional=True,
                message="ReportDefinition.Slice",
            )
            time_period_index: int = proto.Field(
                proto.INT32,
                number=5,
                optional=True,
            )
            metric_value_type: "ReportDefinition.MetricValueType" = proto.Field(
                proto.ENUM,
                number=6,
                optional=True,
                enum="ReportDefinition.MetricValueType",
            )

        class FilterList(proto.Message):
            r"""A list of filters.

            Attributes:
                filters (MutableSequence[google.ads.admanager_v1.types.ReportDefinition.Filter]):
                    Required. A list of filters.
            """

            filters: MutableSequence["ReportDefinition.Filter"] = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message="ReportDefinition.Filter",
            )

        field_filter: "ReportDefinition.Filter.FieldFilter" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="type",
            message="ReportDefinition.Filter.FieldFilter",
        )
        not_filter: "ReportDefinition.Filter" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="type",
            message="ReportDefinition.Filter",
        )
        and_filter: "ReportDefinition.Filter.FilterList" = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="type",
            message="ReportDefinition.Filter.FilterList",
        )
        or_filter: "ReportDefinition.Filter.FilterList" = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="type",
            message="ReportDefinition.Filter.FilterList",
        )

    class Sort(proto.Message):
        r"""Represents a sorting in a report.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            field (google.ads.admanager_v1.types.ReportDefinition.Field):
                Required. A field (dimension or metric) to
                sort by.
            descending (bool):
                Optional. The sort order. If true the sort
                will be descending.
            slice_ (google.ads.admanager_v1.types.ReportDefinition.Slice):
                Optional. Use to sort on a specific slice of
                data.

                This field is a member of `oneof`_ ``_slice``.
            time_period_index (int):
                Optional. When using time period columns, use
                this to sort on a specific column.

                This field is a member of `oneof`_ ``_time_period_index``.
            metric_value_type (google.ads.admanager_v1.types.ReportDefinition.MetricValueType):
                Optional. Use to specify which metric value
                type to sort on. Defaults to PRIMARY.

                This field is a member of `oneof`_ ``_metric_value_type``.
        """

        field: "ReportDefinition.Field" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="ReportDefinition.Field",
        )
        descending: bool = proto.Field(
            proto.BOOL,
            number=2,
        )
        slice_: "ReportDefinition.Slice" = proto.Field(
            proto.MESSAGE,
            number=3,
            optional=True,
            message="ReportDefinition.Slice",
        )
        time_period_index: int = proto.Field(
            proto.INT32,
            number=4,
            optional=True,
        )
        metric_value_type: "ReportDefinition.MetricValueType" = proto.Field(
            proto.ENUM,
            number=5,
            optional=True,
            enum="ReportDefinition.MetricValueType",
        )

    class Slice(proto.Message):
        r"""Use to specify a slice of data.

        For example, in a report, to focus on just data from the US, specify
        ``COUNTRY_NAME`` for dimension and value: ``"United States"``.

        Attributes:
            dimension (google.ads.admanager_v1.types.ReportDefinition.Dimension):
                Required. The dimension to slice on.
            value (google.ads.admanager_v1.types.ReportValue):
                Required. The value of the dimension.
        """

        dimension: "ReportDefinition.Dimension" = proto.Field(
            proto.ENUM,
            number=1,
            enum="ReportDefinition.Dimension",
        )
        value: report_value.ReportValue = proto.Field(
            proto.MESSAGE,
            number=2,
            message=report_value.ReportValue,
        )

    class Flag(proto.Message):
        r"""A flag for a report. Flags are used show if certain thresholds are
        met. Result rows that match the filter will have the corresponding
        [MetricValueGroup.flagValues][MetricValueGroup] index set to true.
        For more information about flags see:
        https://support.google.com/admanager/answer/15079975

        Attributes:
            filters (MutableSequence[google.ads.admanager_v1.types.ReportDefinition.Filter]):
                Required. Filters to apply for the flag.
            name (str):
                Optional. Name of the flag.
                The flag names RED, YELLOW, GREEN, BLUE, PURPLE,
                and GREY correspond to the colored flags that
                appear in the UI. The UI won't display flags
                with other names, but they are available for use
                by API clients.
        """

        filters: MutableSequence["ReportDefinition.Filter"] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="ReportDefinition.Filter",
        )
        name: str = proto.Field(
            proto.STRING,
            number=2,
        )

    dimensions: MutableSequence[Dimension] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=Dimension,
    )
    metrics: MutableSequence[Metric] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=Metric,
    )
    filters: MutableSequence[Filter] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=Filter,
    )
    time_zone_source: TimeZoneSource = proto.Field(
        proto.ENUM,
        number=20,
        enum=TimeZoneSource,
    )
    time_zone: str = proto.Field(
        proto.STRING,
        number=4,
    )
    currency_code: str = proto.Field(
        proto.STRING,
        number=5,
    )
    date_range: DateRange = proto.Field(
        proto.MESSAGE,
        number=6,
        message=DateRange,
    )
    comparison_date_range: DateRange = proto.Field(
        proto.MESSAGE,
        number=9,
        optional=True,
        message=DateRange,
    )
    custom_dimension_key_ids: MutableSequence[int] = proto.RepeatedField(
        proto.INT64,
        number=7,
    )
    line_item_custom_field_ids: MutableSequence[int] = proto.RepeatedField(
        proto.INT64,
        number=11,
    )
    order_custom_field_ids: MutableSequence[int] = proto.RepeatedField(
        proto.INT64,
        number=12,
    )
    creative_custom_field_ids: MutableSequence[int] = proto.RepeatedField(
        proto.INT64,
        number=13,
    )
    report_type: ReportType = proto.Field(
        proto.ENUM,
        number=8,
        enum=ReportType,
    )
    time_period_column: TimePeriodColumn = proto.Field(
        proto.ENUM,
        number=10,
        enum=TimePeriodColumn,
    )
    flags: MutableSequence[Flag] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message=Flag,
    )
    sorts: MutableSequence[Sort] = proto.RepeatedField(
        proto.MESSAGE,
        number=15,
        message=Sort,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
