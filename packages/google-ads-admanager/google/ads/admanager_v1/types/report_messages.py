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

from google.protobuf import timestamp_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import dayofweek_pb2  # type: ignore
from google.type import timeofday_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Report",
        "ReportDefinition",
        "ScheduleOptions",
        "Schedule",
    },
)


class Report(proto.Message):
    r"""The ``Report`` resource.

    Attributes:
        name (str):
            Identifier. The resource name of the report. Report resource
            name have the form:
            ``networks/{network_code}/reports/{report_id}``
        report_id (int):
            Output only. Report ID.
        visibility (google.ads.admanager_v1.types.Report.Visibility):
            Optional. The visibility of a report.
        report_definition (google.ads.admanager_v1.types.ReportDefinition):
            Required. The report definition of the
            report.
        display_name (str):
            Optional. Display name for the report.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant this report was last
            modified.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant this report was
            created.
        locale (str):
            Output only. The locale of this report.
            Locale is set from the user's locale at the time
            of the request. Locale can not be modified.
        schedule_options (google.ads.admanager_v1.types.ScheduleOptions):
            Optional. The schedule options of this
            report.
    """

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

    class Dimension(proto.Enum):
        r"""Reporting dimensions.

        Values:
            DIMENSION_UNSPECIFIED (0):
                Default value. This value is unused.
            ADVERTISER_DOMAIN_NAME (242):
                The domain name of the advertiser.
            ADVERTISER_EXTERNAL_ID (228):
                The ID used in an external system for
                advertiser identification
            ADVERTISER_ID (131):
                The ID of an advertiser company assigned to
                an order
            ADVERTISER_LABELS (230):
                Labels applied to the advertiser
                can be used for either competitive exclusion or
                ad exclusion
            ADVERTISER_LABEL_IDS (229):
                Label ids applied to the advertiser
                can be used for either competitive exclusion or
                ad exclusion
            ADVERTISER_NAME (132):
                The name of an advertiser company assigned to
                an order
            ADVERTISER_PRIMARY_CONTACT (227):
                The name of the contact associated with an
                advertiser company
            AD_LOCATION (390):
                Shows an ENUM value describing whether a
                given piece of publisher inventory was above
                (ATF) or below the fold (BTF) of a page.
            AD_LOCATION_NAME (391):
                Shows a localized string describing whether a
                given piece of publisher inventory was above
                (ATF) or below the fold (BTF) of a page.
            AD_UNIT_CODE (64):
                The code of the ad unit where the ad was
                requested.
            AD_UNIT_CODE_LEVEL_1 (65):
                The code of the first level ad unit of the ad
                unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_10 (74):
                The code of the tenth level ad unit of the ad
                unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_11 (75):
                The code of the eleventh level ad unit of the
                ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_12 (76):
                The code of the twelfth level ad unit of the
                ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_13 (77):
                The code of the thirteenth level ad unit of
                the ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_14 (78):
                The code of the fourteenth level ad unit of
                the ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_15 (79):
                The code of the fifteenth level ad unit of
                the ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_16 (80):
                The code of the sixteenth level ad unit of
                the ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_2 (66):
                The code of the second level ad unit of the
                ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_3 (67):
                The code of the third level ad unit of the ad
                unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_4 (68):
                The code of the fourth level ad unit of the
                ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_5 (69):
                The code of the fifth level ad unit of the ad
                unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_6 (70):
                The code of the sixth level ad unit of the ad
                unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_7 (71):
                The code of the seventh level ad unit of the
                ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_8 (72):
                The code of the eighth level ad unit of the
                ad unit where the ad was requested.
            AD_UNIT_CODE_LEVEL_9 (73):
                The code of the ninth level ad unit of the ad
                unit where the ad was requested.
            AD_UNIT_DEPTH (101):
                The depth of the ad unit's hierarchy
            AD_UNIT_ID (25):
                The ID of the ad unit where the ad was
                requested.
            AD_UNIT_ID_ALL_LEVEL (27):
                The full hierarchy of ad unit IDs where the
                ad was requested, from root to leaf, excluding
                the root ad unit ID.
            AD_UNIT_ID_LEVEL_1 (30):
                The first level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_10 (48):
                The tenth level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_11 (50):
                The eleventh level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_12 (52):
                The twelfth level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_13 (54):
                The thirteenth level ad unit ID of the ad
                unit where the ad was requested.
            AD_UNIT_ID_LEVEL_14 (56):
                The fourteenth level ad unit ID of the ad
                unit where the ad was requested.
            AD_UNIT_ID_LEVEL_15 (58):
                The fifteenth level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_16 (60):
                The sixteenth level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_2 (32):
                The second level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_3 (34):
                The third level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_4 (36):
                The fourth level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_5 (38):
                The fifth level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_6 (40):
                The sixth level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_7 (42):
                The seventh level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_8 (44):
                The eighth level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_LEVEL_9 (46):
                The ninth level ad unit ID of the ad unit
                where the ad was requested.
            AD_UNIT_ID_TOP_LEVEL (142):
                The top-level ad unit ID of the ad unit where
                the ad was requested.
            AD_UNIT_NAME (26):
                The name of the ad unit where the ad was
                requested.
            AD_UNIT_NAME_ALL_LEVEL (29):
                The full hierarchy of ad unit names where the
                ad was requested, from root to leaf, excluding
                the root ad unit name.
            AD_UNIT_NAME_LEVEL_1 (31):
                The first level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_10 (49):
                The tenth level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_11 (51):
                The eleventh level ad unit name of the ad
                unit where the ad was requested.
            AD_UNIT_NAME_LEVEL_12 (53):
                The twelfth level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_13 (55):
                The thirteenth level ad unit name of the ad
                unit where the ad was requested.
            AD_UNIT_NAME_LEVEL_14 (57):
                The fourteenth level ad unit name of the ad
                unit where the ad was requested.
            AD_UNIT_NAME_LEVEL_15 (59):
                The fifteenth level ad unit name of the ad
                unit where the ad was requested.
            AD_UNIT_NAME_LEVEL_16 (61):
                The sixteenth level ad unit name of the ad
                unit where the ad was requested.
            AD_UNIT_NAME_LEVEL_2 (33):
                The second level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_3 (35):
                The third level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_4 (37):
                The fourth level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_5 (39):
                The fifth level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_6 (41):
                The sixth level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_7 (43):
                The seventh level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_8 (45):
                The eighth level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_LEVEL_9 (47):
                The ninth level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_NAME_TOP_LEVEL (143):
                The top-level ad unit name of the ad unit
                where the ad was requested.
            AD_UNIT_REWARD_AMOUNT (63):
                The reward amount of the ad unit where the ad
                was requested.
            AD_UNIT_REWARD_TYPE (62):
                The reward type of the ad unit where the ad
                was requested.
            AD_UNIT_STATUS (206):
                The status of the ad unit
            AD_UNIT_STATUS_NAME (207):
                The name of the status of the ad unit
            APP_VERSION (392):
                The app version.
            BACKFILL_ADVERTISER_EXTERNAL_ID (349):
                The ID used in an external system for
                advertiser identification
            BACKFILL_ADVERTISER_ID (346):
                The ID of an advertiser company assigned to a
                backfill order
            BACKFILL_ADVERTISER_LABELS (351):
                Labels applied to the advertiser
                can be used for either competitive exclusion or
                ad exclusion
            BACKFILL_ADVERTISER_LABEL_IDS (350):
                Label ids applied to the advertiser
                can be used for either competitive exclusion or
                ad exclusion
            BACKFILL_ADVERTISER_NAME (347):
                The name of an advertiser company assigned to
                a backfill order
            BACKFILL_ADVERTISER_PRIMARY_CONTACT (348):
                The name of the contact associated with an
                advertiser company
            BACKFILL_CREATIVE_BILLING_TYPE (378):
                Enum value of Backfill creative billing type
            BACKFILL_CREATIVE_BILLING_TYPE_NAME (379):
                Localized string value of Backfill creative
                billing type
            BACKFILL_CREATIVE_CLICK_THROUGH_URL (376):
                Represents the click-through URL of a
                Backfill creative
            BACKFILL_CREATIVE_ID (370):
                The ID of a Backfill creative
            BACKFILL_CREATIVE_NAME (371):
                Backfill creative name
            BACKFILL_CREATIVE_THIRD_PARTY_VENDOR (377):
                Third party vendor name of a Backfill
                creative
            BACKFILL_CREATIVE_TYPE (374):
                Enum value of Backfill creative type
            BACKFILL_CREATIVE_TYPE_NAME (375):
                Localized string name of Backfill creative
                type
            BACKFILL_LINE_ITEM_ARCHIVED (278):
                Whether a Backfill line item is archived.
            BACKFILL_LINE_ITEM_COMPANION_DELIVERY_OPTION (258):
                Backfill line item comanion delivery option
                ENUM value.
            BACKFILL_LINE_ITEM_COMPANION_DELIVERY_OPTION_NAME (259):
                Localized Backfill line item comanion
                delivery option name.
            BACKFILL_LINE_ITEM_COMPUTED_STATUS (296):
                The computed status of the BackfillLineItem.
            BACKFILL_LINE_ITEM_COMPUTED_STATUS_NAME (297):
                The localized name of the computed status of
                the BackfillLineItem.
            BACKFILL_LINE_ITEM_CONTRACTED_QUANTITY (280):
                The contracted units bought for the Backfill
                line item.
            BACKFILL_LINE_ITEM_COST_PER_UNIT (272):
                The cost per unit of the Backfill line item.
            BACKFILL_LINE_ITEM_COST_TYPE (264):
                Backfill line item cost type ENUM value.
            BACKFILL_LINE_ITEM_COST_TYPE_NAME (265):
                Localized Backfill line item cost type name.
            BACKFILL_LINE_ITEM_CREATIVE_END_DATE (381):
                Represent the end date of a Backfill creative
                associated with a Backfill line item
            BACKFILL_LINE_ITEM_CREATIVE_ROTATION_TYPE (290):
                The creative rotation type of the
                BackfillLineItem.
            BACKFILL_LINE_ITEM_CREATIVE_ROTATION_TYPE_NAME (291):
                The localized name of the creative rotation
                type of the BackfillLineItem.
            BACKFILL_LINE_ITEM_CREATIVE_START_DATE (380):
                Represent the start date of a Backfill
                creative associated with a Backfill line item
            BACKFILL_LINE_ITEM_CURRENCY_CODE (288):
                The 3 letter currency code of the Backfill
                line item
            BACKFILL_LINE_ITEM_DELIVERY_INDICATOR (274):
                The progress made for the delivery of the
                Backfill line item.
            BACKFILL_LINE_ITEM_DELIVERY_RATE_TYPE (292):
                The delivery rate type of the
                BackfillLineItem.
            BACKFILL_LINE_ITEM_DELIVERY_RATE_TYPE_NAME (293):
                The localized name of the delivery rate type
                of the BackfillLineItem.
            BACKFILL_LINE_ITEM_DISCOUNT_ABSOLUTE (294):
                The discount of the BackfillLineItem in whole
                units in the BackfillLineItem's currency code,
                or if unspecified the Network's currency code.
            BACKFILL_LINE_ITEM_DISCOUNT_PERCENTAGE (295):
                The discount of the BackfillLineItem in
                percentage.
            BACKFILL_LINE_ITEM_END_DATE (267):
                The end date of the Backfill line item.
            BACKFILL_LINE_ITEM_END_DATE_TIME (269):
                The end date and time of the Backfill line
                item.
            BACKFILL_LINE_ITEM_ENVIRONMENT_TYPE (302):
                The ENUM value of the environment a Backfill
                line item is targeting.
            BACKFILL_LINE_ITEM_ENVIRONMENT_TYPE_NAME (257):
                The localized name of the environment a
                Backfill line item is targeting.
            BACKFILL_LINE_ITEM_EXTERNAL_DEAL_ID (285):
                The deal ID of the Backfill line item. Set
                for Programmatic Direct campaigns.
            BACKFILL_LINE_ITEM_EXTERNAL_ID (273):
                The external ID of the Backfill line item.
            BACKFILL_LINE_ITEM_FREQUENCY_CAP (303):
                The frequency cap of the Backfill line item
                (descriptive string).
            BACKFILL_LINE_ITEM_ID (298):
                Backfill line item ID.
            BACKFILL_LINE_ITEM_LAST_MODIFIED_BY_APP (289):
                The application that last modified the
                Backfill line item.
            BACKFILL_LINE_ITEM_LIFETIME_CLICKS (283):
                The total number of clicks delivered of the
                lifetime of the Backfill line item.
            BACKFILL_LINE_ITEM_LIFETIME_IMPRESSIONS (282):
                The total number of impressions delivered
                over the lifetime of the Backfill line item.
            BACKFILL_LINE_ITEM_LIFETIME_VIEWABLE_IMPRESSIONS (284):
                The total number of viewable impressions
                delivered over the lifetime of the Backfill line
                item.
            BACKFILL_LINE_ITEM_MAKEGOOD (276):
                Whether or not the Backfill line item is
                Makegood. Makegood refers to free inventory
                offered to buyers to compensate for mistakes or
                under-delivery in the original campaigns.
            BACKFILL_LINE_ITEM_NAME (299):
                Backfill line item name.
            BACKFILL_LINE_ITEM_NON_CPD_BOOKED_REVENUE (286):
                The cost of booking for the Backfill line
                item (non-CPD).
            BACKFILL_LINE_ITEM_OPTIMIZABLE (277):
                Whether a Backfill line item is eligible for
                opitimization.
            BACKFILL_LINE_ITEM_PRIMARY_GOAL_TYPE (262):
                Goal type ENUM value of the primary goal of
                the Backfill line item.
            BACKFILL_LINE_ITEM_PRIMARY_GOAL_TYPE_NAME (263):
                Localized goal type name of the primary goal
                of the Backfill line item.
            BACKFILL_LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE (260):
                Unit type ENUM value of the primary goal of
                the Backfill line item.
            BACKFILL_LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE_NAME (261):
                Localized unit type name of the primary goal
                of the Backfill line item.
            BACKFILL_LINE_ITEM_PRIORITY (266):
                The priority of this Backfill line item as a
                value between 1 and 16. In general, a lower
                priority means more serving priority for the
                Backfill line item.
            BACKFILL_LINE_ITEM_RESERVATION_STATUS (306):
                ENUM value describing the state of inventory
                reservation for the BackfillLineItem.
            BACKFILL_LINE_ITEM_RESERVATION_STATUS_NAME (307):
                Localized string describing the state of
                inventory reservation for the BackfillLineItem.
            BACKFILL_LINE_ITEM_START_DATE (268):
                The start date of the Backfill line item.
            BACKFILL_LINE_ITEM_START_DATE_TIME (270):
                The start date and time of the Backfill line
                item.
            BACKFILL_LINE_ITEM_TYPE (300):
                Backfill line item type ENUM value.
            BACKFILL_LINE_ITEM_TYPE_NAME (301):
                Localized Backfill line item type name.
            BACKFILL_LINE_ITEM_UNLIMITED_END (271):
                Whether the Backfill line item end time and
                end date is set to effectively never end.
            BACKFILL_LINE_ITEM_VALUE_COST_PER_UNIT (275):
                The artificial cost per unit used by the Ad
                server to help rank inventory.
            BACKFILL_LINE_ITEM_WEB_PROPERTY_CODE (287):
                The web property code used for dynamic
                allocation Backfill line items.
            BACKFILL_MASTER_COMPANION_CREATIVE_ID (372):
                The ID of Backfill creative, includes regular
                creatives, and master and companions in case of
                creative sets
            BACKFILL_MASTER_COMPANION_CREATIVE_NAME (373):
                Name of Backfill creative, includes regular
                creatives, and master and companions in case of
                creative sets
            BACKFILL_ORDER_AGENCY (313):
                Backfill order agency.
            BACKFILL_ORDER_AGENCY_ID (314):
                Backfill order agency ID.
            BACKFILL_ORDER_BOOKED_CPC (315):
                Backfill order booked CPC.
            BACKFILL_ORDER_BOOKED_CPM (316):
                Backfill order booked CPM.
            BACKFILL_ORDER_DELIVERY_STATUS (340):
                Backfill order delivery status ENUM value.
            BACKFILL_ORDER_DELIVERY_STATUS_NAME (341):
                Backfill order delivery status localized
                name.
            BACKFILL_ORDER_END_DATE (317):
                Backfill order end date.
            BACKFILL_ORDER_END_DATE_TIME (319):
                Backfill order end date and time.
            BACKFILL_ORDER_EXTERNAL_ID (320):
                Backfill order external ID.
            BACKFILL_ORDER_ID (338):
                Backfill order id.
            BACKFILL_ORDER_LABELS (334):
                Backfill order labels.
            BACKFILL_ORDER_LABEL_IDS (335):
                Backfill order labels IDs.
            BACKFILL_ORDER_LIFETIME_CLICKS (322):
                Backfill order lifetime clicks.
            BACKFILL_ORDER_LIFETIME_IMPRESSIONS (323):
                Backfill order lifetime impressions.
            BACKFILL_ORDER_NAME (339):
                Backfill order name.
            BACKFILL_ORDER_PO_NUMBER (324):
                Backfill order PO number.
            BACKFILL_ORDER_PROGRAMMATIC (321):
                Whether the Backfill order is programmatic.
            BACKFILL_ORDER_SALESPERSON (325):
                Backfill order sales person.
            BACKFILL_ORDER_SECONDARY_SALESPEOPLE (329):
                Backfill order secondary sales people.
            BACKFILL_ORDER_SECONDARY_SALESPEOPLE_ID (328):
                Backfill order secondary sales people ID.
            BACKFILL_ORDER_SECONDARY_TRAFFICKERS (331):
                Backfill order secondary traffickers.
            BACKFILL_ORDER_SECONDARY_TRAFFICKERS_ID (330):
                Backfill order secondary traffickers ID.
            BACKFILL_ORDER_START_DATE (332):
                Backfill order start date.
            BACKFILL_ORDER_START_DATE_TIME (333):
                Backfill order start date and time.
            BACKFILL_ORDER_TRAFFICKER (326):
                Backfill order trafficker.
            BACKFILL_ORDER_TRAFFICKER_ID (327):
                Backfill order trafficker ID.
            BACKFILL_ORDER_UNLIMITED_END (318):
                Whether the Backfill order end time and end
                date is set to effectively never end.
            BACKFILL_PROGRAMMATIC_BUYER_ID (336):
                The ID of the buyer on a backfill
                programmatic proposal.
            BACKFILL_PROGRAMMATIC_BUYER_NAME (337):
                The name of the buyer on a backfill
                programmatic proposal.
            BRANDING_TYPE (383):
                The amount of information about the
                Publisher's page sent to the buyer who purchased
                the impressions.
            BRANDING_TYPE_NAME (384):
                The localized version of branding type, the
                amount of information about the Publisher's page
                sent to the buyer who purchased the impressions.
            BROWSER_CATEGORY (119):
                Browser category.
            BROWSER_CATEGORY_NAME (120):
                Browser category name.
            BROWSER_ID (235):
                The ID of the browser.
            BROWSER_NAME (236):
                The name of the browser.
            CARRIER_ID (369):
                Mobile carrier ID.
            CARRIER_NAME (368):
                Name of the mobile carrier.
            CLASSIFIED_ADVERTISER_ID (133):
                The ID of an advertiser, classified by
                Google, associated with a creative transacted
            CLASSIFIED_ADVERTISER_NAME (134):
                The name of an advertiser, classified by
                Google, associated with a creative transacted
            CLASSIFIED_BRAND_ID (243):
                ID of the brand, as classified by Google,
            CLASSIFIED_BRAND_NAME (244):
                Name of the brand, as classified by Google,
            CONTENT_ID (246):
                ID of the video content served.
            CONTENT_NAME (247):
                Name of the video content served.
            COUNTRY_ID (11):
                The criteria ID of the country in which the
                ad served.
            COUNTRY_NAME (12):
                The name of the country in which the ad
                served.
            CREATIVE_BILLING_TYPE (366):
                Enum value of creative billing type
            CREATIVE_BILLING_TYPE_NAME (367):
                Localized string value of creative billing
                type
            CREATIVE_CLICK_THROUGH_URL (174):
                Represents the click-through URL of a
                creative
            CREATIVE_ID (138):
                The ID of a creative
            CREATIVE_NAME (139):
                Creative name
            CREATIVE_TECHNOLOGY (148):
                Creative technology ENUM
            CREATIVE_TECHNOLOGY_NAME (149):
                Creative technology locallized name
            CREATIVE_THIRD_PARTY_VENDOR (361):
                Third party vendor name of a creative
            CREATIVE_TYPE (344):
                Enum value of creative type
            CREATIVE_TYPE_NAME (345):
                Localized string name of creative type
            DATE (3):
                Breaks down reporting data by date.
            DAY_OF_WEEK (4):
                Breaks down reporting data by day of the
                week. Monday is 1 and 7 is Sunday.
            DEMAND_CHANNEL (9):
                Demand channel.
            DEMAND_CHANNEL_NAME (10):
                Demand channel name.
            DEMAND_SUBCHANNEL (22):
                Demand subchannel.
            DEMAND_SUBCHANNEL_NAME (23):
                Demand subchannel name.
            DEVICE (226):
                The device on which an ad was served.
            DEVICE_CATEGORY (15):
                The device category to which an ad is being
                targeted.
            DEVICE_CATEGORY_NAME (16):
                The name of the category of device
                (smartphone, feature phone, tablet, or desktop)
                to which an ad is being targeted.
            DEVICE_NAME (225):
                The localized name of the device on which an
                ad was served.
            EXCHANGE_THIRD_PARTY_COMPANY_ID (185):
                ID of the yield partner as classified by
                Google
            EXCHANGE_THIRD_PARTY_COMPANY_NAME (186):
                Name of the yield partner as classified by
                Google
            FIRST_LOOK_PRICING_RULE_ID (248):
                The ID of the first look pricing rule.
            FIRST_LOOK_PRICING_RULE_NAME (249):
                The name of the first look pricing rule.
            HOUR (100):
                Breaks down reporting data by hour in one
                day.
            INTERACTION_TYPE (223):
                The interaction type of an ad.
            INTERACTION_TYPE_NAME (224):
                The localized name of the interaction type of
                an ad.
            INVENTORY_FORMAT (17):
                Inventory format.
                The format of the ad unit (e.g, banner) where
                the ad was requested.
            INVENTORY_FORMAT_NAME (18):
                Inventory format name.
                The format of the ad unit (e.g, banner) where
                the ad was requested.
            INVENTORY_TYPE (19):
                Inventory type.
                The kind of web page or device where the ad was
                requested.
            INVENTORY_TYPE_NAME (20):
                Inventory type name.
                The kind of web page or device where the ad was
                requested.
            IS_ADX_DIRECT (382):
                Whether traffic is Adx Direct.
            IS_FIRST_LOOK_DEAL (401):
                Whether traffic is First Look.
            KEY_VALUES_ID (214):
                The Custom Targeting Value ID
            KEY_VALUES_NAME (215):
                The Custom Targeting Value formatted like
                <key_name>=<value_name>
            LINE_ITEM_ARCHIVED (188):
                Whether a Line item is archived.
            LINE_ITEM_COMPANION_DELIVERY_OPTION (204):
                Line item comanion delivery option ENUM
                value.
            LINE_ITEM_COMPANION_DELIVERY_OPTION_NAME (205):
                Localized line item comanion delivery option
                name.
            LINE_ITEM_COMPUTED_STATUS (250):
                The computed status of the LineItem.
            LINE_ITEM_COMPUTED_STATUS_NAME (251):
                The localized name of the computed status of
                the LineItem.
            LINE_ITEM_CONTRACTED_QUANTITY (92):
                The contracted units bought for the Line
                item.
            LINE_ITEM_COST_PER_UNIT (85):
                The cost per unit of the Line item.
            LINE_ITEM_COST_TYPE (212):
                Line item cost type ENUM value.
            LINE_ITEM_COST_TYPE_NAME (213):
                Localized line item cost type name.
            LINE_ITEM_CREATIVE_END_DATE (176):
                Represent the end date of a creative
                associated with line item
            LINE_ITEM_CREATIVE_ROTATION_TYPE (189):
                The creative rotation type of the LineItem.
            LINE_ITEM_CREATIVE_ROTATION_TYPE_NAME (190):
                The localized name of the creative rotation
                type of the LineItem.
            LINE_ITEM_CREATIVE_START_DATE (175):
                Represent the start date of a creative
                associated with line item
            LINE_ITEM_CURRENCY_CODE (180):
                The 3 letter currency code of the Line Item
            LINE_ITEM_DELIVERY_INDICATOR (87):
                The progress made for the delivery of the
                Line item.
            LINE_ITEM_DELIVERY_RATE_TYPE (191):
                The delivery rate type of the LineItem.
            LINE_ITEM_DELIVERY_RATE_TYPE_NAME (192):
                The localized name of the delivery rate type
                of the LineItem.
            LINE_ITEM_DISCOUNT_ABSOLUTE (195):
                The discount of the LineItem in whole units
                in the LineItem's currency code, or if
                unspecified the Network's currency code.
            LINE_ITEM_DISCOUNT_PERCENTAGE (196):
                The discount of the LineItem in percentage.
            LINE_ITEM_END_DATE (81):
                The end date of the Line item.
            LINE_ITEM_END_DATE_TIME (83):
                The end date and time of the Line item.
            LINE_ITEM_ENVIRONMENT_TYPE (201):
                The ENUM value of the environment a LineItem
                is targeting.
            LINE_ITEM_ENVIRONMENT_TYPE_NAME (202):
                The localized name of the environment a
                LineItem is targeting.
            LINE_ITEM_EXTERNAL_DEAL_ID (97):
                The deal ID of the Line item. Set for
                Programmatic Direct campaigns.
            LINE_ITEM_EXTERNAL_ID (86):
                The external ID of the Line item.
            LINE_ITEM_FREQUENCY_CAP (256):
                The frequency cap of the Line item
                (descriptive string).
            LINE_ITEM_ID (1):
                Line item ID.
            LINE_ITEM_LAST_MODIFIED_BY_APP (181):
                The application that last modified the Line
                Item.
            LINE_ITEM_LIFETIME_CLICKS (95):
                The total number of clicks delivered of the
                lifetime of the Line item.
            LINE_ITEM_LIFETIME_IMPRESSIONS (94):
                The total number of impressions delivered
                over the lifetime of the Line item.
            LINE_ITEM_LIFETIME_VIEWABLE_IMPRESSIONS (96):
                The total number of viewable impressions
                delivered over the lifetime of the Line item.
            LINE_ITEM_MAKEGOOD (89):
                Whether or not the Line item is Makegood.
                Makegood refers to free inventory offered to
                buyers to compensate for mistakes or
                under-delivery in the original campaigns.
            LINE_ITEM_NAME (2):
                Line item Name.
            LINE_ITEM_NON_CPD_BOOKED_REVENUE (98):
                The cost of booking for the Line item
                (non-CPD).
            LINE_ITEM_OPTIMIZABLE (90):
                Whether a Line item is eligible for
                opitimization.
            LINE_ITEM_PRIMARY_GOAL_TYPE (210):
                Goal type ENUM value of the primary goal of
                the line item.
            LINE_ITEM_PRIMARY_GOAL_TYPE_NAME (211):
                Localized goal type name of the primary goal
                of the line item.
            LINE_ITEM_PRIMARY_GOAL_UNITS_ABSOLUTE (93):
                The total number of impressions or clicks that are reserved
                for a line item. For line items of type BULK or
                PRICE_PRIORITY, this represents the number of remaining
                impressions reserved. If the line item has an impression cap
                goal, this represents the number of impressions or
                conversions that the line item will stop serving at if
                reached.
            LINE_ITEM_PRIMARY_GOAL_UNITS_PERCENTAGE (396):
                The percentage of impressions or clicks that
                are reserved for a line item. For line items of
                type SPONSORSHIP, this represents the percentage
                of available impressions reserved. For line
                items of type NETWORK or HOUSE, this represents
                the percentage of remaining impressions
                reserved.
            LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE (208):
                Unit type ENUM value of the primary goal of
                the line item.
            LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE_NAME (209):
                Localized unit type name of the primary goal
                of the line item.
            LINE_ITEM_PRIORITY (24):
                The priority of this Line item as a value
                between 1 and 16. In general, a lower priority
                means more serving priority for the Line item.
            LINE_ITEM_RESERVATION_STATUS (304):
                ENUM value describing the state of inventory
                reservation for the LineItem.
            LINE_ITEM_RESERVATION_STATUS_NAME (305):
                Localized string describing the state of
                inventory reservation for the LineItem.
            LINE_ITEM_START_DATE (82):
                The start date of the Line item.
            LINE_ITEM_START_DATE_TIME (84):
                The start date and time of the Line item.
            LINE_ITEM_TYPE (193):
                Line item type ENUM value.
            LINE_ITEM_TYPE_NAME (194):
                Localized line item type name.
            LINE_ITEM_UNLIMITED_END (187):
                Whether the Line item end time and end date
                is set to effectively never end.
            LINE_ITEM_VALUE_COST_PER_UNIT (88):
                The artificial cost per unit used by the Ad
                server to help rank inventory.
            LINE_ITEM_WEB_PROPERTY_CODE (179):
                The web property code used for dynamic
                allocation Line Items.
            MASTER_COMPANION_CREATIVE_ID (140):
                The ID of creative, includes regular
                creatives, and master and companions in case of
                creative sets
            MASTER_COMPANION_CREATIVE_NAME (141):
                Name of creative, includes regular creatives,
                and master and companions in case of creative
                sets
            MOBILE_APP_FREE (128):
                Whether the mobile app is free.
            MOBILE_APP_ICON_URL (129):
                URL of app icon for the mobile app.
            MOBILE_APP_ID (123):
                The ID of the Mobile App.
            MOBILE_APP_NAME (127):
                The name of the mobile app.
            MOBILE_APP_OWNERSHIP_STATUS (311):
                Ownership status of the mobile app.
            MOBILE_APP_OWNERSHIP_STATUS_NAME (312):
                Ownership status of the mobile app.
            MOBILE_APP_STORE (125):
                The App Store of the mobile app.
            MOBILE_APP_STORE_NAME (245):
                The localized name of the mobile app store.
            MOBILE_INVENTORY_TYPE (99):
                Mobile inventory type.
                Identifies whether a mobile ad came from a
                regular web page, an AMP web page, or a mobile
                app.
                Values match the Inventory type dimension
                available in the Overview Home dashboard. Note:
                Video takes precedence over any other value, for
                example, if there is an in-stream video
                impression on a desktop device, it will be
                attributed to in-stream video and not desktop
                web.
            MOBILE_INVENTORY_TYPE_NAME (21):
                Mobile inventory type name.
                Identifies whether a mobile ad came from a
                regular web page, an AMP web page, or a mobile
                app.
            MOBILE_SDK_VERSION_NAME (130):
                SDK version of the mobile device.
            MONTH_YEAR (6):
                Breaks down reporting data by month and year.
            NATIVE_AD_FORMAT_ID (255):
                Native ad format ID.
            NATIVE_AD_FORMAT_NAME (254):
                Native ad format name.
            NATIVE_STYLE_ID (253):
                Native style ID.
            NATIVE_STYLE_NAME (252):
                Native style name.
            OPERATING_SYSTEM_CATEGORY (117):
                Operating system category.
            OPERATING_SYSTEM_CATEGORY_NAME (118):
                Operating system category name.
            OPERATING_SYSTEM_VERSION_ID (238):
                ID of the operating system version.
            OPERATING_SYSTEM_VERSION_NAME (237):
                Details of the operating system, including
                version.
            ORDER_AGENCY (150):
                Order agency.
            ORDER_AGENCY_ID (151):
                Order agency ID.
            ORDER_BOOKED_CPC (152):
                Order booked CPC.
            ORDER_BOOKED_CPM (153):
                Order booked CPM.
            ORDER_DELIVERY_STATUS (231):
                Order delivery status ENUM value.
            ORDER_DELIVERY_STATUS_NAME (239):
                Order delivery status localized name.
            ORDER_END_DATE (154):
                Order end date.
            ORDER_END_DATE_TIME (155):
                Order end date and time.
            ORDER_EXTERNAL_ID (156):
                Order external ID.
            ORDER_ID (7):
                Order id.
            ORDER_LABELS (170):
                Order labels.
            ORDER_LABEL_IDS (171):
                Order labels IDs.
            ORDER_LIFETIME_CLICKS (158):
                Order lifetime clicks.
            ORDER_LIFETIME_IMPRESSIONS (159):
                Order lifetime impressions.
            ORDER_NAME (8):
                Order name.
            ORDER_PO_NUMBER (160):
                Order PO number.
            ORDER_PROGRAMMATIC (157):
                Whether the Order is programmatic.
            ORDER_SALESPERSON (161):
                Order sales person.
            ORDER_SECONDARY_SALESPEOPLE (164):
                Order secondary sales people.
            ORDER_SECONDARY_SALESPEOPLE_ID (165):
                Order secondary sales people ID.
            ORDER_SECONDARY_TRAFFICKERS (166):
                Order secondary traffickers.
            ORDER_SECONDARY_TRAFFICKERS_ID (167):
                Order secondary traffickers ID.
            ORDER_START_DATE (168):
                Order start date.
            ORDER_START_DATE_TIME (169):
                Order start date and time.
            ORDER_TRAFFICKER (162):
                Order trafficker.
            ORDER_TRAFFICKER_ID (163):
                Order trafficker ID.
            ORDER_UNLIMITED_END (203):
                Whether the Order end time and end date is
                set to effectively never end.
            PLACEMENT_ID (113):
                Placement ID
            PLACEMENT_ID_ALL (144):
                The full list of placement IDs associated
                with the ad unit.
            PLACEMENT_NAME (114):
                Placement name
            PLACEMENT_NAME_ALL (145):
                The full list of placement names associated
                with the ad unit.
            PLACEMENT_STATUS (362):
                Placement status ENUM value
            PLACEMENT_STATUS_ALL (363):
                The full list of placement status ENUM values
                associated with the ad unit.
            PLACEMENT_STATUS_NAME (364):
                Localized placement status name.
            PLACEMENT_STATUS_NAME_ALL (365):
                The full list of localized placement status
                names associated with the ad unit.
            PROGRAMMATIC_BUYER_ID (240):
                The ID of the buyer on a programmatic
                proposal.
            PROGRAMMATIC_BUYER_NAME (241):
                The name of the buyer on a programmatic
                proposal.
            PROGRAMMATIC_CHANNEL (13):
                Programmatic channel.
                The type of transaction that occurred in Ad
                Exchange.
            PROGRAMMATIC_CHANNEL_NAME (14):
                Programmatic channel name.
                The type of transaction that occurred in Ad
                Exchange.
            RENDERED_CREATIVE_SIZE (343):
                The size of a rendered creative, It can
                differ with the creative's size if a creative is
                shown in an ad slot of a different size.
            REQUESTED_AD_SIZES (352):
                Inventory Requested Ad Sizes dimension
            REQUEST_TYPE (146):
                Request type ENUM
            REQUEST_TYPE_NAME (147):
                Request type locallized name
            SERVER_SIDE_UNWRAPPING_ELIGIBLE (597):
                Indicates if a request was eligible for
                server-side unwrapping.
            SITE (387):
                Information about domain or subdomains.
            TARGETING_ID (232):
                The ID of the browser, device or other
                environment into which a line item or creative
                was served.
            TARGETING_NAME (233):
                Information about the browser, device and
                other environments into which a line item or
                creative was served.
            TARGETING_TYPE (385):
                The way in which advertisers targeted their
                ads.
            TARGETING_TYPE_NAME (386):
                The localized name of the way in which
                advertisers targeted their ads.
            TRAFFIC_SOURCE (388):
                Inventory Traffic source dimension
            TRAFFIC_SOURCE_NAME (389):
                Inventory Traffic source dimension name
            UNIFIED_PRICING_RULE_ID (393):
                Unified pricing rule ID dimension
            UNIFIED_PRICING_RULE_NAME (394):
                Unified pricing rule name dimension
            VIDEO_PLCMT (172):
                The video placement enum as defined by ADCOM
                1.0-202303.
            VIDEO_PLCMT_NAME (173):
                The localized name of the video placement as
                defined by ADCOM 1.0-202303.
            WEEK (5):
                Breaks down reporting data by week of the
                year.
            YIELD_GROUP_BUYER_NAME (184):
                Name of the company within a yield group
            YIELD_GROUP_ID (182):
                ID of the group of ad networks or exchanges
                used for Mediation and Open Bidding
            YIELD_GROUP_NAME (183):
                Name of the group of ad networks or exchanges
                used for Mediation and Open Bidding
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
                index 0 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_1_VALUE (11001):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 1 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_2_VALUE (11002):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 2 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_3_VALUE (11003):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 3 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_4_VALUE (11004):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 4 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_5_VALUE (11005):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 5 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_6_VALUE (11006):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 6 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_7_VALUE (11007):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 7 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_8_VALUE (11008):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 8 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_9_VALUE (11009):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 9 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_10_VALUE (11010):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 10 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_11_VALUE (11011):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 11 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_12_VALUE (11012):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 12 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_13_VALUE (11013):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 13 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type STRING or DROPDOWN.
            LINE_ITEM_CUSTOM_FIELD_14_VALUE (11014):
                Custom field value for Line Item with custom field ID equal
                to the ID in index 14 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type STRING or DROPDOWN.
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
                index 0 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_1_VALUE (17001):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 1 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_2_VALUE (17002):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 2 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_3_VALUE (17003):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 3 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_4_VALUE (17004):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 4 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_5_VALUE (17005):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 5 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_6_VALUE (17006):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 6 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_7_VALUE (17007):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 7 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_8_VALUE (17008):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 8 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_9_VALUE (17009):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 9 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_10_VALUE (17010):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 10 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_11_VALUE (17011):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 11 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_12_VALUE (17012):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 12 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_13_VALUE (17013):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 13 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type STRING or DROPDOWN.
            BACKFILL_LINE_ITEM_CUSTOM_FIELD_14_VALUE (17014):
                Custom field value for Backfill line item with custom field
                ID equal to the ID in index 14 of
                ``ReportDefinition.line_item_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type STRING or DROPDOWN.
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
                index 0 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_1_VALUE (19001):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 1 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_2_VALUE (19002):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 2 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_3_VALUE (19003):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 3 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_4_VALUE (19004):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 4 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_5_VALUE (19005):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 5 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_6_VALUE (19006):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 6 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_7_VALUE (19007):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 7 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_8_VALUE (19008):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 8 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_9_VALUE (19009):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 9 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_10_VALUE (19010):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 10 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_11_VALUE (19011):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 11 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_12_VALUE (19012):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 12 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_13_VALUE (19013):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 13 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type STRING or DROPDOWN.
            BACKFILL_ORDER_CUSTOM_FIELD_14_VALUE (19014):
                Custom field value for Backfill order with custom field ID
                equal to the ID in index 14 of
                ``ReportDefinition.order_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type STRING or DROPDOWN.
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
                index 0 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_1_VALUE (21001):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 1 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 1 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_2_VALUE (21002):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 2 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 2 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_3_VALUE (21003):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 3 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 3 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_4_VALUE (21004):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 4 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 4 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_5_VALUE (21005):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 5 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 5 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_6_VALUE (21006):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 6 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 6 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_7_VALUE (21007):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 7 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 7 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_8_VALUE (21008):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 8 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 8 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_9_VALUE (21009):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 9 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 9 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_10_VALUE (21010):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 10 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 10 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_11_VALUE (21011):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 11 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 11 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_12_VALUE (21012):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 12 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 12 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_13_VALUE (21013):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 13 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 13 is of type STRING or DROPDOWN.
            BACKFILL_CREATIVE_CUSTOM_FIELD_14_VALUE (21014):
                Custom field value for Backfill creative with custom field
                ID equal to the ID in index 14 of
                ``ReportDefinition.creative_custom_field_ids``. Treats the
                value as a string. Can only be used if the custom field at
                index 14 is of type STRING or DROPDOWN.
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
                equal to the id in index 0 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_1_VALUE (101001):
                Custom Dimension Value name for Custom Dimension with key
                equal to the id in index 1 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_2_VALUE (101002):
                Custom Dimension Value name for Custom Dimension with key
                equal to the id in index 2 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_3_VALUE (101003):
                Custom Dimension Value name for Custom Dimension with key
                equal to the id in index 3 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_4_VALUE (101004):
                Custom Dimension Value name for Custom Dimension with key
                equal to the id in index 4 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_5_VALUE (101005):
                Custom Dimension Value name for Custom Dimension with key
                equal to the id in index 5 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_6_VALUE (101006):
                Custom Dimension Value name for Custom Dimension with key
                equal to the id in index 6 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_7_VALUE (101007):
                Custom Dimension Value name for Custom Dimension with key
                equal to the id in index 7 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_8_VALUE (101008):
                Custom Dimension Value name for Custom Dimension with key
                equal to the id in index 8 of
                ``ReportDefinition.custom_dimension_key_ids``.
            CUSTOM_DIMENSION_9_VALUE (101009):
                Custom Dimension Value name for Custom Dimension with key
                equal to the id in index 9 of
                ``ReportDefinition.custom_dimension_key_ids``.
        """
        DIMENSION_UNSPECIFIED = 0
        ADVERTISER_DOMAIN_NAME = 242
        ADVERTISER_EXTERNAL_ID = 228
        ADVERTISER_ID = 131
        ADVERTISER_LABELS = 230
        ADVERTISER_LABEL_IDS = 229
        ADVERTISER_NAME = 132
        ADVERTISER_PRIMARY_CONTACT = 227
        AD_LOCATION = 390
        AD_LOCATION_NAME = 391
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
        AD_UNIT_DEPTH = 101
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
        APP_VERSION = 392
        BACKFILL_ADVERTISER_EXTERNAL_ID = 349
        BACKFILL_ADVERTISER_ID = 346
        BACKFILL_ADVERTISER_LABELS = 351
        BACKFILL_ADVERTISER_LABEL_IDS = 350
        BACKFILL_ADVERTISER_NAME = 347
        BACKFILL_ADVERTISER_PRIMARY_CONTACT = 348
        BACKFILL_CREATIVE_BILLING_TYPE = 378
        BACKFILL_CREATIVE_BILLING_TYPE_NAME = 379
        BACKFILL_CREATIVE_CLICK_THROUGH_URL = 376
        BACKFILL_CREATIVE_ID = 370
        BACKFILL_CREATIVE_NAME = 371
        BACKFILL_CREATIVE_THIRD_PARTY_VENDOR = 377
        BACKFILL_CREATIVE_TYPE = 374
        BACKFILL_CREATIVE_TYPE_NAME = 375
        BACKFILL_LINE_ITEM_ARCHIVED = 278
        BACKFILL_LINE_ITEM_COMPANION_DELIVERY_OPTION = 258
        BACKFILL_LINE_ITEM_COMPANION_DELIVERY_OPTION_NAME = 259
        BACKFILL_LINE_ITEM_COMPUTED_STATUS = 296
        BACKFILL_LINE_ITEM_COMPUTED_STATUS_NAME = 297
        BACKFILL_LINE_ITEM_CONTRACTED_QUANTITY = 280
        BACKFILL_LINE_ITEM_COST_PER_UNIT = 272
        BACKFILL_LINE_ITEM_COST_TYPE = 264
        BACKFILL_LINE_ITEM_COST_TYPE_NAME = 265
        BACKFILL_LINE_ITEM_CREATIVE_END_DATE = 381
        BACKFILL_LINE_ITEM_CREATIVE_ROTATION_TYPE = 290
        BACKFILL_LINE_ITEM_CREATIVE_ROTATION_TYPE_NAME = 291
        BACKFILL_LINE_ITEM_CREATIVE_START_DATE = 380
        BACKFILL_LINE_ITEM_CURRENCY_CODE = 288
        BACKFILL_LINE_ITEM_DELIVERY_INDICATOR = 274
        BACKFILL_LINE_ITEM_DELIVERY_RATE_TYPE = 292
        BACKFILL_LINE_ITEM_DELIVERY_RATE_TYPE_NAME = 293
        BACKFILL_LINE_ITEM_DISCOUNT_ABSOLUTE = 294
        BACKFILL_LINE_ITEM_DISCOUNT_PERCENTAGE = 295
        BACKFILL_LINE_ITEM_END_DATE = 267
        BACKFILL_LINE_ITEM_END_DATE_TIME = 269
        BACKFILL_LINE_ITEM_ENVIRONMENT_TYPE = 302
        BACKFILL_LINE_ITEM_ENVIRONMENT_TYPE_NAME = 257
        BACKFILL_LINE_ITEM_EXTERNAL_DEAL_ID = 285
        BACKFILL_LINE_ITEM_EXTERNAL_ID = 273
        BACKFILL_LINE_ITEM_FREQUENCY_CAP = 303
        BACKFILL_LINE_ITEM_ID = 298
        BACKFILL_LINE_ITEM_LAST_MODIFIED_BY_APP = 289
        BACKFILL_LINE_ITEM_LIFETIME_CLICKS = 283
        BACKFILL_LINE_ITEM_LIFETIME_IMPRESSIONS = 282
        BACKFILL_LINE_ITEM_LIFETIME_VIEWABLE_IMPRESSIONS = 284
        BACKFILL_LINE_ITEM_MAKEGOOD = 276
        BACKFILL_LINE_ITEM_NAME = 299
        BACKFILL_LINE_ITEM_NON_CPD_BOOKED_REVENUE = 286
        BACKFILL_LINE_ITEM_OPTIMIZABLE = 277
        BACKFILL_LINE_ITEM_PRIMARY_GOAL_TYPE = 262
        BACKFILL_LINE_ITEM_PRIMARY_GOAL_TYPE_NAME = 263
        BACKFILL_LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE = 260
        BACKFILL_LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE_NAME = 261
        BACKFILL_LINE_ITEM_PRIORITY = 266
        BACKFILL_LINE_ITEM_RESERVATION_STATUS = 306
        BACKFILL_LINE_ITEM_RESERVATION_STATUS_NAME = 307
        BACKFILL_LINE_ITEM_START_DATE = 268
        BACKFILL_LINE_ITEM_START_DATE_TIME = 270
        BACKFILL_LINE_ITEM_TYPE = 300
        BACKFILL_LINE_ITEM_TYPE_NAME = 301
        BACKFILL_LINE_ITEM_UNLIMITED_END = 271
        BACKFILL_LINE_ITEM_VALUE_COST_PER_UNIT = 275
        BACKFILL_LINE_ITEM_WEB_PROPERTY_CODE = 287
        BACKFILL_MASTER_COMPANION_CREATIVE_ID = 372
        BACKFILL_MASTER_COMPANION_CREATIVE_NAME = 373
        BACKFILL_ORDER_AGENCY = 313
        BACKFILL_ORDER_AGENCY_ID = 314
        BACKFILL_ORDER_BOOKED_CPC = 315
        BACKFILL_ORDER_BOOKED_CPM = 316
        BACKFILL_ORDER_DELIVERY_STATUS = 340
        BACKFILL_ORDER_DELIVERY_STATUS_NAME = 341
        BACKFILL_ORDER_END_DATE = 317
        BACKFILL_ORDER_END_DATE_TIME = 319
        BACKFILL_ORDER_EXTERNAL_ID = 320
        BACKFILL_ORDER_ID = 338
        BACKFILL_ORDER_LABELS = 334
        BACKFILL_ORDER_LABEL_IDS = 335
        BACKFILL_ORDER_LIFETIME_CLICKS = 322
        BACKFILL_ORDER_LIFETIME_IMPRESSIONS = 323
        BACKFILL_ORDER_NAME = 339
        BACKFILL_ORDER_PO_NUMBER = 324
        BACKFILL_ORDER_PROGRAMMATIC = 321
        BACKFILL_ORDER_SALESPERSON = 325
        BACKFILL_ORDER_SECONDARY_SALESPEOPLE = 329
        BACKFILL_ORDER_SECONDARY_SALESPEOPLE_ID = 328
        BACKFILL_ORDER_SECONDARY_TRAFFICKERS = 331
        BACKFILL_ORDER_SECONDARY_TRAFFICKERS_ID = 330
        BACKFILL_ORDER_START_DATE = 332
        BACKFILL_ORDER_START_DATE_TIME = 333
        BACKFILL_ORDER_TRAFFICKER = 326
        BACKFILL_ORDER_TRAFFICKER_ID = 327
        BACKFILL_ORDER_UNLIMITED_END = 318
        BACKFILL_PROGRAMMATIC_BUYER_ID = 336
        BACKFILL_PROGRAMMATIC_BUYER_NAME = 337
        BRANDING_TYPE = 383
        BRANDING_TYPE_NAME = 384
        BROWSER_CATEGORY = 119
        BROWSER_CATEGORY_NAME = 120
        BROWSER_ID = 235
        BROWSER_NAME = 236
        CARRIER_ID = 369
        CARRIER_NAME = 368
        CLASSIFIED_ADVERTISER_ID = 133
        CLASSIFIED_ADVERTISER_NAME = 134
        CLASSIFIED_BRAND_ID = 243
        CLASSIFIED_BRAND_NAME = 244
        CONTENT_ID = 246
        CONTENT_NAME = 247
        COUNTRY_ID = 11
        COUNTRY_NAME = 12
        CREATIVE_BILLING_TYPE = 366
        CREATIVE_BILLING_TYPE_NAME = 367
        CREATIVE_CLICK_THROUGH_URL = 174
        CREATIVE_ID = 138
        CREATIVE_NAME = 139
        CREATIVE_TECHNOLOGY = 148
        CREATIVE_TECHNOLOGY_NAME = 149
        CREATIVE_THIRD_PARTY_VENDOR = 361
        CREATIVE_TYPE = 344
        CREATIVE_TYPE_NAME = 345
        DATE = 3
        DAY_OF_WEEK = 4
        DEMAND_CHANNEL = 9
        DEMAND_CHANNEL_NAME = 10
        DEMAND_SUBCHANNEL = 22
        DEMAND_SUBCHANNEL_NAME = 23
        DEVICE = 226
        DEVICE_CATEGORY = 15
        DEVICE_CATEGORY_NAME = 16
        DEVICE_NAME = 225
        EXCHANGE_THIRD_PARTY_COMPANY_ID = 185
        EXCHANGE_THIRD_PARTY_COMPANY_NAME = 186
        FIRST_LOOK_PRICING_RULE_ID = 248
        FIRST_LOOK_PRICING_RULE_NAME = 249
        HOUR = 100
        INTERACTION_TYPE = 223
        INTERACTION_TYPE_NAME = 224
        INVENTORY_FORMAT = 17
        INVENTORY_FORMAT_NAME = 18
        INVENTORY_TYPE = 19
        INVENTORY_TYPE_NAME = 20
        IS_ADX_DIRECT = 382
        IS_FIRST_LOOK_DEAL = 401
        KEY_VALUES_ID = 214
        KEY_VALUES_NAME = 215
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
        LINE_ITEM_LAST_MODIFIED_BY_APP = 181
        LINE_ITEM_LIFETIME_CLICKS = 95
        LINE_ITEM_LIFETIME_IMPRESSIONS = 94
        LINE_ITEM_LIFETIME_VIEWABLE_IMPRESSIONS = 96
        LINE_ITEM_MAKEGOOD = 89
        LINE_ITEM_NAME = 2
        LINE_ITEM_NON_CPD_BOOKED_REVENUE = 98
        LINE_ITEM_OPTIMIZABLE = 90
        LINE_ITEM_PRIMARY_GOAL_TYPE = 210
        LINE_ITEM_PRIMARY_GOAL_TYPE_NAME = 211
        LINE_ITEM_PRIMARY_GOAL_UNITS_ABSOLUTE = 93
        LINE_ITEM_PRIMARY_GOAL_UNITS_PERCENTAGE = 396
        LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE = 208
        LINE_ITEM_PRIMARY_GOAL_UNIT_TYPE_NAME = 209
        LINE_ITEM_PRIORITY = 24
        LINE_ITEM_RESERVATION_STATUS = 304
        LINE_ITEM_RESERVATION_STATUS_NAME = 305
        LINE_ITEM_START_DATE = 82
        LINE_ITEM_START_DATE_TIME = 84
        LINE_ITEM_TYPE = 193
        LINE_ITEM_TYPE_NAME = 194
        LINE_ITEM_UNLIMITED_END = 187
        LINE_ITEM_VALUE_COST_PER_UNIT = 88
        LINE_ITEM_WEB_PROPERTY_CODE = 179
        MASTER_COMPANION_CREATIVE_ID = 140
        MASTER_COMPANION_CREATIVE_NAME = 141
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
        MOBILE_SDK_VERSION_NAME = 130
        MONTH_YEAR = 6
        NATIVE_AD_FORMAT_ID = 255
        NATIVE_AD_FORMAT_NAME = 254
        NATIVE_STYLE_ID = 253
        NATIVE_STYLE_NAME = 252
        OPERATING_SYSTEM_CATEGORY = 117
        OPERATING_SYSTEM_CATEGORY_NAME = 118
        OPERATING_SYSTEM_VERSION_ID = 238
        OPERATING_SYSTEM_VERSION_NAME = 237
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
        ORDER_SECONDARY_SALESPEOPLE = 164
        ORDER_SECONDARY_SALESPEOPLE_ID = 165
        ORDER_SECONDARY_TRAFFICKERS = 166
        ORDER_SECONDARY_TRAFFICKERS_ID = 167
        ORDER_START_DATE = 168
        ORDER_START_DATE_TIME = 169
        ORDER_TRAFFICKER = 162
        ORDER_TRAFFICKER_ID = 163
        ORDER_UNLIMITED_END = 203
        PLACEMENT_ID = 113
        PLACEMENT_ID_ALL = 144
        PLACEMENT_NAME = 114
        PLACEMENT_NAME_ALL = 145
        PLACEMENT_STATUS = 362
        PLACEMENT_STATUS_ALL = 363
        PLACEMENT_STATUS_NAME = 364
        PLACEMENT_STATUS_NAME_ALL = 365
        PROGRAMMATIC_BUYER_ID = 240
        PROGRAMMATIC_BUYER_NAME = 241
        PROGRAMMATIC_CHANNEL = 13
        PROGRAMMATIC_CHANNEL_NAME = 14
        RENDERED_CREATIVE_SIZE = 343
        REQUESTED_AD_SIZES = 352
        REQUEST_TYPE = 146
        REQUEST_TYPE_NAME = 147
        SERVER_SIDE_UNWRAPPING_ELIGIBLE = 597
        SITE = 387
        TARGETING_ID = 232
        TARGETING_NAME = 233
        TARGETING_TYPE = 385
        TARGETING_TYPE_NAME = 386
        TRAFFIC_SOURCE = 388
        TRAFFIC_SOURCE_NAME = 389
        UNIFIED_PRICING_RULE_ID = 393
        UNIFIED_PRICING_RULE_NAME = 394
        VIDEO_PLCMT = 172
        VIDEO_PLCMT_NAME = 173
        WEEK = 5
        YIELD_GROUP_BUYER_NAME = 184
        YIELD_GROUP_ID = 182
        YIELD_GROUP_NAME = 183
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
            ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME (61):
                Active View total average time in seconds
                that specific impressions are reported as being
                viewable.
            ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS (58):
                Total number of impressions that were
                eligible to measure viewability.
            ACTIVE_VIEW_MEASURABLE_IMPRESSIONS (57):
                The total number of impressions that were
                sampled and measured by active view.
            ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE (60):
                The percentage of total impressions that were
                measurable by active view (out of all the total
                impressions sampled for active view).
            ACTIVE_VIEW_VIEWABLE_IMPRESSIONS (56):
                The total number of impressions viewed on the
                user's screen.
            ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE (59):
                The percentage of total impressions viewed on
                the user's screen (out of the total impressions
                measurable by active view).
            ADSENSE_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME (73):
                Active View AdSense average time in seconds
                that specific impressions are reported as being
                viewable.
            ADSENSE_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS (70):
                Total number of impressions delivered by
                AdSense that were eligible to measure
                viewability.
            ADSENSE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS (69):
                The number of impressions delivered by
                AdSense that were sampled, and measurable by
                active view.
            ADSENSE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE (72):
                The percentage of impressions delivered by
                AdSense that were measurable by active view (out
                of all AdSense impressions sampled for active
                view).
            ADSENSE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS (68):
                The number of impressions delivered by
                AdSense viewed on the user's screen.
            ADSENSE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE (71):
                The percentage of impressions delivered by
                AdSense viewed on the user's screen (out of
                AdSense impressions measurable by active view).
            ADSENSE_AVERAGE_ECPM (26):
                The average effective
                cost-per-thousand-impressions earned from the
                ads delivered by AdSense through line item
                dynamic allocation.
            ADSENSE_CLICKS (23):
                Number of clicks delivered by AdSense demand
                channel.
            ADSENSE_CTR (24):
                The ratio of impressions served by AdSense
                that resulted in users clicking on an ad. The
                clickthrough rate (CTR) is updated nightly. The
                AdSense CTR is calculated as: (AdSense clicks /
                AdSense impressions).
            ADSENSE_IMPRESSIONS (22):
                Total impressions delivered by AdSense.
            ADSENSE_PERCENT_CLICKS (28):
                Ratio of clicks delivered by AdSense through
                line item dynamic allocation in relation to the
                total clicks delivered.
            ADSENSE_PERCENT_IMPRESSIONS (27):
                Ratio of impressions delivered by AdSense
                through line item dynamic allocation in relation
                to the total impressions delivered.
            ADSENSE_PERCENT_REVENUE (29):
                Ratio of revenue generated by AdSense through
                line item dynamic allocation in relation to the
                total revenue.
            ADSENSE_PERCENT_REVENUE_WITHOUT_CPD (30):
                Ratio of revenue generated by AdSense through
                line item dynamic allocation in relation to the
                total revenue (excluding CPD).
            ADSENSE_RESPONSES_SERVED (41):
                The total number of times that an AdSense ad
                is delivered.
            ADSENSE_REVENUE (25):
                Revenue generated from AdSense through line
                item dynamic allocation, calculated in the
                network's currency and time zone.
            AD_EXCHANGE_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME (79):
                Active View AdExchange average time in
                seconds that specific impressions are reported
                as being viewable.
            AD_EXCHANGE_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS (76):
                Total number of impressions delivered by Ad
                Exchange that were eligible to measure
                viewability.
            AD_EXCHANGE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS (75):
                The number of impressions delivered by Ad
                Exchange that were sampled, and measurable by
                active view.
            AD_EXCHANGE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE (78):
                The percentage of impressions delivered by Ad
                Exchange that were measurable by active view
                (out of all Ad Exchange impressions sampled for
                active view).
            AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS (74):
                The number of impressions delivered by Ad
                Exchange viewed on the user's screen.
            AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE (77):
                The percentage of impressions delivered by Ad
                Exchange viewed on the user's screen (out of Ad
                Exchange impressions measurable by active view).
            AD_EXCHANGE_AVERAGE_ECPM (18):
                The average effective
                cost-per-thousand-impressions earned from the
                ads delivered by Ad Exchange through line item
                dynamic allocation.
            AD_EXCHANGE_CLICKS (15):
                Number of clicks delivered by the Ad
                Exchange.
            AD_EXCHANGE_CTR (16):
                The ratio of impressions served by the Ad
                Exchange that resulted in users clicking on an
                ad. The clickthrough rate (CTR) is updated
                nightly. Ad Exchange CTR is calculated as: (Ad
                Exchange clicks / Ad Exchange impressions).
            AD_EXCHANGE_IMPRESSIONS (14):
                Total impressions delivered by the Ad
                Exchange.
            AD_EXCHANGE_PERCENT_CLICKS (20):
                Ratio of clicks delivered by Ad Exchange
                through line item dynamic allocation in relation
                to the total clicks delivered.
            AD_EXCHANGE_PERCENT_IMPRESSIONS (19):
                Ratio of impressions delivered by Ad Exchange
                through line item dynamic allocation in relation
                to the total impressions delivered.
            AD_EXCHANGE_PERCENT_REVENUE (21):
                Ratio of revenue generated by Ad Exchange
                through line item dynamic allocation in relation
                to the total revenue.
            AD_EXCHANGE_PERCENT_REVENUE_WITHOUT_CPD (31):
                Ratio of revenue generated by Ad Exchange
                through line item dynamic allocation in relation
                to the total revenue (excluding CPD).
            AD_EXCHANGE_RESPONSES_SERVED (42):
                The total number of times that an Ad Exchange
                ad is delivered.
            AD_EXCHANGE_REVENUE (17):
                Revenue generated from the Ad Exchange
                through line item dynamic allocation, calculated
                in your network's currency and time zone.
            AD_REQUESTS (38):
                The total number of times that an ad request
                is sent to the ad server including dynamic
                allocation.
            AD_SERVER_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME (67):
                Active View ad server average time in seconds
                that specific impressions are reported as being
                viewable.
            AD_SERVER_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS (64):
                Total number of impressions delivered by the
                ad server that were eligible to measure
                viewability.
            AD_SERVER_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS (63):
                The number of impressions delivered by the ad
                server that were sampled, and measurable by
                active view.
            AD_SERVER_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE (66):
                The percentage of impressions delivered by
                the ad server that were measurable by active
                view (out of all the ad server impressions
                sampled for active view).
            AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS (62):
                The number of impressions delivered by the ad
                server viewed on the user's screen.
            AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE (65):
                The percentage of impressions delivered by
                the ad server viewed on the user's screen (out
                of the ad server impressions measurable by
                active view).
            AD_SERVER_AVERAGE_ECPM (34):
                Average effective
                cost-per-thousand-impressions earned from the
                ads delivered by the Google Ad Manager server.
            AD_SERVER_AVERAGE_ECPM_WITHOUT_CPD (10):
                Average effective
                cost-per-thousand-impressions earned from the
                ads delivered by the Google Ad Manager server,
                excluding CPD value.
            AD_SERVER_BEGIN_TO_RENDER_IMPRESSIONS (262):
                Total raw impressions counted when creative
                begins to render or the first frame of a video
                is shown.
            AD_SERVER_CLICKS (7):
                Total clicks served by the Google Ad Manager
                server. It usually takes about 30 minutes for
                new clicks to be recorded and added to the total
                displayed in reporting.
            AD_SERVER_CPD_REVENUE (32):
                CPD revenue earned, calculated in your
                network's currency, for the ads delivered by the
                Google Ad Manager server. Sum of all booked
                revenue.
            AD_SERVER_CTR (8):
                Ratio of impressions served by the Google Ad
                Manager server that resulted in users clicking
                on an ad. The clickthrough rate (CTR) is updated
                nightly. The ad server CTR is calculated as: (Ad
                server clicks / Ad server impressions).
            AD_SERVER_IMPRESSIONS (6):
                Total impressions delivered by the Ad Server.
            AD_SERVER_PERCENT_CLICKS (12):
                Ratio of clicks delivered by the Google Ad
                Manager server in relation to the total clicks
                delivered.
            AD_SERVER_PERCENT_IMPRESSIONS (11):
                Ratio of impressions delivered by the Google
                Ad Manager server in relation to the total
                impressions delivered.
            AD_SERVER_PERCENT_REVENUE (35):
                Ratio of revenue generated by the Google Ad
                Manager server in relation to the total revenue.
            AD_SERVER_PERCENT_REVENUE_WITHOUT_CPD (13):
                Ratio of revenue generated by the Google Ad
                Manager server (excluding CPD) in relation to
                the total revenue.
            AD_SERVER_RESPONSES_SERVED (40):
                The total number of times that an ad is
                served by the ad server.
            AD_SERVER_REVENUE (33):
                All CPM, CPC, and CPD revenue earned,
                calculated in your network's currency, for the
                ads delivered by the Google Ad Manager server.
                Sum of all booked revenue.
            AD_SERVER_REVENUE_WITHOUT_CPD (9):
                Revenue (excluding CPD) earned, calculated in
                your network's currency, for the ads delivered
                by the Google Ad Manager server. Sum of all
                booked revenue.
            AD_SERVER_TRACKED_ADS (264):
                The number of tracked ads delivered by the ad
                server.
            AD_SERVER_UNFILTERED_BEGIN_TO_RENDER_IMPRESSIONS (261):
                Total raw impressions counted when creative
                begins to render or the first frame of a video
                is shown, before invalid traffic filtrations by
                Ad Server.
            AD_SERVER_UNFILTERED_CLICKS (259):
                Total clicks delivered by the Ad Server
                before spam filtering.
            AD_SERVER_UNFILTERED_IMPRESSIONS (260):
                Total impressions delivered by the Ad Server
                before spam filtering.
            AD_SERVER_UNFILTERED_TRACKED_ADS (263):
                The number of tracked ads delivered by the ad
                server before invalid traffic filtrations.
            AVERAGE_ECPM (37):
                eCPM averaged across the Google Ad Manager
                server, AdSense, and Ad Exchange.
            AVERAGE_ECPM_WITHOUT_CPD (5):
                eCPM averaged across the Google Ad Manager
                server (excluding CPD), AdSense, and Ad
                Exchange.
            CLICKS (2):
                The number of times a user clicked on an ad.
            CODE_SERVED_COUNT (44):
                The total number of times that the code for
                an ad is served by the ad server including
                dynamic allocation.
            CTR (3):
                For standard ads, your ad clickthrough rate
                (CTR) is the number of ad clicks divided by the
                number of individual ad impressions expressed as
                a fraction. Ad CTR = Clicks / Ad impressions.
            GOOGLE_SOLD_AUCTION_COVIEWED_IMPRESSIONS (129):
                The number of coviewed impressions sold by
                Google in partner sales.
            GOOGLE_SOLD_AUCTION_IMPRESSIONS (128):
                The number of auction impressions sold by
                Google in partner sales.
            GOOGLE_SOLD_COVIEWED_IMPRESSIONS (131):
                The number of coviewed impressions sold by
                Google in partner sales.
            GOOGLE_SOLD_IMPRESSIONS (130):
                The number of impressions sold by Google in
                partner sales.
            GOOGLE_SOLD_RESERVATION_COVIEWED_IMPRESSIONS (127):
                The number of coviewed impressions sold by
                Google in partner sales.
            GOOGLE_SOLD_RESERVATION_IMPRESSIONS (126):
                The number of reservation impressions sold by
                Google in partner sales.
            IMPRESSIONS (1):
                Total impressions from the Google Ad Manager
                server, AdSense, Ad Exchange, and yield group
                partners.
            PARTNER_SALES_FILLED_POD_REQUESTS (135):
                The number of filled pod requests (filled by
                partner or Google) in partner sales.
            PARTNER_SALES_FILL_RATE (136):
                The percent of filled requests to total ad
                requests in partner sales.
            PARTNER_SALES_PARTNER_MATCH_RATE (137):
                The percent of partner filled requests to
                total ad requests in partner sales.
            PARTNER_SALES_QUERIES (132):
                The number of queries eligible for partner
                sales.
            PARTNER_SALES_UNFILLED_IMPRESSIONS (133):
                The number of partner unfilled impressions in
                partner sales. If a pod request is not filled by
                partner but filled by Google, this metric will
                still count 1.
            PARTNER_SALES_UNMATCHED_QUERIES (134):
                The number of partner unmatched queries in
                partner sales. If an ad request is not filled by
                partner but filled by Google, this metric will
                still count 1.
            PARTNER_SOLD_CODE_SERVED (125):
                The number of code served sold by partner in
                partner sales.
            PARTNER_SOLD_COVIEWED_IMPRESSIONS (124):
                The number of coviewed impressions sold by
                partner in partner sales.
            PARTNER_SOLD_IMPRESSIONS (123):
                The number of impressions sold by partner in
                partner sales.
            PROGRAMMATIC_ELIGIBLE_AD_REQUESTS (177):
                The total number of ad requests eligible for
                programmatic inventory, including Programmatic
                Guaranteed, Preferred Deals, backfill, and open
                auction.
            PROGRAMMATIC_MATCH_RATE (178):
                The number of programmatic responses served
                divided by the number of programmatic eligible
                ad requests. Includes Ad Exchange, Open Bidding,
                and Preferred Deals.
            PROGRAMMATIC_RESPONSES_SERVED (176):
                Total number of ad responses served from programmatic demand
                sources. Includes Ad Exchange, Open Bidding, and Preferred
                Deals.

                Differs from AD_EXCHANGE_RESPONSES_SERVED, which doesn't
                include Open Bidding ad requests.
            RESPONSES_SERVED (39):
                The total number of times that an ad is
                served by the ad server including dynamic
                allocation.
            REVENUE (36):
                Total amount of CPM, CPC, and CPD revenue
                based on the number of units served by the
                Google Ad Manager server, AdSense, Ad Exchange,
                and third-party Mediation networks.
            REVENUE_WITHOUT_CPD (4):
                Total amount of revenue (excluding CPD) based
                on the number of units served by the Google Ad
                Manager server, AdSense, Ad Exchange, and
                third-party Mediation networks.
            SERVER_SIDE_UNWRAPPING_AVERAGE_LATENCY_MS (434):
                The average latency in milliseconds across
                all server-side unwrapping callout requests.
                There is no special handling for error or
                timeout responses. This reflects the entire
                chain of a parent callout request, which may
                result in multiple child callouts. This metric
                is not sliced by child callout dimensions.
            SERVER_SIDE_UNWRAPPING_CALLOUTS (435):
                The total number of server-side unwrapping
                callout requests.
            SERVER_SIDE_UNWRAPPING_EMPTY_RESPONSES (436):
                The total number of server-side unwrapping
                callouts that returned an empty response.
                Timeouts are not considered empty responses.
            SERVER_SIDE_UNWRAPPING_ERROR_RESPONSES (437):
                The total number of server-side unwrapping
                callouts that returned an error response.
                Timeouts and empty responses are not considered
                errors.
            SERVER_SIDE_UNWRAPPING_SUCCESSFUL_RESPONSES (438):
                The total number of successfully unwrapped,
                non-empty server-side wrapping callouts.
                Successful unwrapping does not indicate that the
                resulting creative was served.
            SERVER_SIDE_UNWRAPPING_TIMEOUTS (439):
                The total number of server-side unwrapping
                callouts that timed out before returning a
                response.
            UNFILLED_IMPRESSIONS (45):
                The total number of missed impressions due to
                the ad servers' inability to find ads to serve
                including dynamic allocation.
            UNMATCHED_AD_REQUESTS (43):
                The total number of times that an ad is not
                returned by the ad server.
            USER_MESSAGES_OFFERWALL_MESSAGES_SHOWN (121):
                Number of times an Offerwall message was
                shown to users.
            USER_MESSAGES_OFFERWALL_SUCCESSFUL_ENGAGEMENTS (122):
                The number of messages where the user gained
                an entitlement.
            VIDEO_INTERACTION_AVERAGE_INTERACTION_RATE (92):
                The number of user interactions with a video,
                on average, such as pause, full screen, mute,
                etc.
            VIDEO_INTERACTION_COLLAPSES (93):
                The number of times a user collapses a video,
                either to its original size or to a different
                size.
            VIDEO_INTERACTION_EXPANDS (95):
                The number of times a user expands a video.
            VIDEO_INTERACTION_FULL_SCREENS (96):
                The number of times ad clip played in full
                screen mode.
            VIDEO_INTERACTION_MUTES (97):
                The number of times video player was in mute
                state during play of ad clip.
            VIDEO_INTERACTION_PAUSES (98):
                The number of times user paused ad clip.
            VIDEO_INTERACTION_RESUMES (99):
                The number of times the user unpaused the
                video.
            VIDEO_INTERACTION_REWINDS (100):
                The number of times a user rewinds the video.
            VIDEO_INTERACTION_UNMUTES (101):
                The number of times a user unmutes the video.
            VIDEO_INTERACTION_VIDEO_SKIPS (102):
                The number of times a skippable video is
                skipped.
            VIDEO_REAL_TIME_CREATIVE_SERVES (139):
                The number of total creative serves in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_100_COUNT (143):
                The number of errors of type 100 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_101_COUNT (144):
                The number of errors of type 101 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_102_COUNT (145):
                The number of errors of type 102 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_200_COUNT (146):
                The number of errors of type 200 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_201_COUNT (147):
                The number of errors of type 201 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_202_COUNT (148):
                The number of errors of type 202 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_203_COUNT (149):
                The number of errors of type 203 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_300_COUNT (150):
                The number of errors of type 300 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_301_COUNT (151):
                The number of errors of type 301 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_302_COUNT (152):
                The number of errors of type 302 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_303_COUNT (153):
                The number of errors of type 303 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_400_COUNT (154):
                The number of errors of type 400 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_401_COUNT (155):
                The number of errors of type 401 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_402_COUNT (156):
                The number of errors of type 402 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_403_COUNT (157):
                The number of errors of type 403 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_405_COUNT (158):
                The number of errors of type 405 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_406_COUNT (159):
                The number of errors of type 406 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_407_COUNT (160):
                The number of errors of type 407 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_408_COUNT (161):
                The number of errors of type 408 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_409_COUNT (162):
                The number of errors of type 409 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_410_COUNT (163):
                The number of errors of type 410 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_500_COUNT (164):
                The number of errors of type 500 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_501_COUNT (165):
                The number of errors of type 501 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_502_COUNT (166):
                The number of errors of type 502 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_503_COUNT (167):
                The number of errors of type 503 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_600_COUNT (168):
                The number of errors of type 600 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_601_COUNT (169):
                The number of errors of type 601 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_602_COUNT (170):
                The number of errors of type 602 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_603_COUNT (171):
                The number of errors of type 603 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_604_COUNT (172):
                The number of errors of type 604 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_900_COUNT (173):
                The number of errors of type 900 in video
                realtime reporting.
            VIDEO_REAL_TIME_ERROR_901_COUNT (174):
                The number of errors of type 901 in video
                realtime reporting.
            VIDEO_REAL_TIME_IMPRESSIONS (138):
                The number of total impressions in video
                realtime reporting.
            VIDEO_REAL_TIME_MATCHED_QUERIES (140):
                The number of matched queries in video
                realtime reporting.
            VIDEO_REAL_TIME_TOTAL_ERROR_COUNT (175):
                The number of all errors in video realtime
                reporting.
            VIDEO_REAL_TIME_TOTAL_QUERIES (142):
                The number of total queries in video realtime
                reporting.
            VIDEO_REAL_TIME_UNMATCHED_QUERIES (141):
                The number of unmatched queries in video
                realtime reporting.
            VIDEO_VIEWERSHIP_AUTO_PLAYS (103):
                Number of times that the publisher specified
                a video ad played automatically.
            VIDEO_VIEWERSHIP_AVERAGE_VIEW_RATE (104):
                Average percentage of the video watched by
                users.
            VIDEO_VIEWERSHIP_AVERAGE_VIEW_TIME (105):
                Average time(seconds) users watched the
                video.
            VIDEO_VIEWERSHIP_CLICK_TO_PLAYS (106):
                Number of times that the publisher specified
                a video ad was clicked to play.
            VIDEO_VIEWERSHIP_COMPLETES (107):
                The number of times the video played to
                completion.
            VIDEO_VIEWERSHIP_COMPLETION_RATE (108):
                Percentage of times the video played to the
                end.
            VIDEO_VIEWERSHIP_ENGAGED_VIEWS (109):
                The number of engaged views: ad is viewed to
                completion or for 30s, whichever comes first.
            VIDEO_VIEWERSHIP_FIRST_QUARTILES (110):
                The number of times the video played to 25%
                of its length.
            VIDEO_VIEWERSHIP_MIDPOINTS (111):
                The number of times the video reached its
                midpoint during play.
            VIDEO_VIEWERSHIP_SKIP_BUTTONS_SHOWN (112):
                The number of times a skip button is shown in
                video.
            VIDEO_VIEWERSHIP_STARTS (113):
                The number of impressions where the video was
                played.
            VIDEO_VIEWERSHIP_THIRD_QUARTILES (114):
                The number of times the video played to 75%
                of its length.
            VIDEO_VIEWERSHIP_TOTAL_ERROR_COUNT (115):
                The number of times an error occurred, such
                as a VAST redirect error, a video playback
                error, or an invalid response error.
            VIDEO_VIEWERSHIP_TOTAL_ERROR_RATE (94):
                The percentage of video error count.
            VIDEO_VIEWERSHIP_VIDEO_LENGTH (116):
                Duration of the video creative.
            VIDEO_VIEWERSHIP_VIEW_THROUGH_RATE (117):
                View-through rate represented as a
                percentage.
            YIELD_GROUP_AUCTIONS_WON (80):
                Number of winning bids received from Open
                Bidding buyers, even when the winning bid is
                placed at the end of a mediation for mobile apps
                chain.
            YIELD_GROUP_BIDS (81):
                Number of bids received from Open Bidding
                buyers, regardless of whether the returned bid
                competes in an auction.
            YIELD_GROUP_BIDS_IN_AUCTION (82):
                Number of bids received from Open Bidding
                buyers that competed in the auction.
            YIELD_GROUP_CALLOUTS (83):
                Number of times a yield partner is asked to
                return bid to fill a yield group request.
            YIELD_GROUP_ESTIMATED_CPM (88):
                The estimated net rate for yield groups or
                individual yield group partners.
            YIELD_GROUP_ESTIMATED_REVENUE (87):
                Total net revenue earned by a yield group,
                based upon the yield group estimated CPM and
                yield group impressions recorded.
            YIELD_GROUP_IMPRESSIONS (85):
                Number of matched yield group requests where
                a yield partner delivered their ad to publisher
                inventory.
            YIELD_GROUP_MEDIATION_FILL_RATE (89):
                Yield group Mediation fill rate indicating
                how often a network fills an ad request.
            YIELD_GROUP_MEDIATION_MATCHED_QUERIES (86):
                Total requests where a Mediation chain was
                served.
            YIELD_GROUP_MEDIATION_PASSBACKS (118):
                The number of mediation chain passback across
                all channels.
            YIELD_GROUP_MEDIATION_THIRD_PARTY_ECPM (90):
                Revenue per thousand impressions based on
                data collected by Ad Manager from third-party ad
                network reports.
            YIELD_GROUP_SUCCESSFUL_RESPONSES (84):
                Number of times a yield group buyer
                successfully returned a bid in response to a
                yield group callout.
        """
        METRIC_UNSPECIFIED = 0
        ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME = 61
        ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS = 58
        ACTIVE_VIEW_MEASURABLE_IMPRESSIONS = 57
        ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE = 60
        ACTIVE_VIEW_VIEWABLE_IMPRESSIONS = 56
        ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE = 59
        ADSENSE_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME = 73
        ADSENSE_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS = 70
        ADSENSE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS = 69
        ADSENSE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE = 72
        ADSENSE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS = 68
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
        AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS = 74
        AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE = 77
        AD_EXCHANGE_AVERAGE_ECPM = 18
        AD_EXCHANGE_CLICKS = 15
        AD_EXCHANGE_CTR = 16
        AD_EXCHANGE_IMPRESSIONS = 14
        AD_EXCHANGE_PERCENT_CLICKS = 20
        AD_EXCHANGE_PERCENT_IMPRESSIONS = 19
        AD_EXCHANGE_PERCENT_REVENUE = 21
        AD_EXCHANGE_PERCENT_REVENUE_WITHOUT_CPD = 31
        AD_EXCHANGE_RESPONSES_SERVED = 42
        AD_EXCHANGE_REVENUE = 17
        AD_REQUESTS = 38
        AD_SERVER_ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME = 67
        AD_SERVER_ACTIVE_VIEW_ELIGIBLE_IMPRESSIONS = 64
        AD_SERVER_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS = 63
        AD_SERVER_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS_RATE = 66
        AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS = 62
        AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE = 65
        AD_SERVER_AVERAGE_ECPM = 34
        AD_SERVER_AVERAGE_ECPM_WITHOUT_CPD = 10
        AD_SERVER_BEGIN_TO_RENDER_IMPRESSIONS = 262
        AD_SERVER_CLICKS = 7
        AD_SERVER_CPD_REVENUE = 32
        AD_SERVER_CTR = 8
        AD_SERVER_IMPRESSIONS = 6
        AD_SERVER_PERCENT_CLICKS = 12
        AD_SERVER_PERCENT_IMPRESSIONS = 11
        AD_SERVER_PERCENT_REVENUE = 35
        AD_SERVER_PERCENT_REVENUE_WITHOUT_CPD = 13
        AD_SERVER_RESPONSES_SERVED = 40
        AD_SERVER_REVENUE = 33
        AD_SERVER_REVENUE_WITHOUT_CPD = 9
        AD_SERVER_TRACKED_ADS = 264
        AD_SERVER_UNFILTERED_BEGIN_TO_RENDER_IMPRESSIONS = 261
        AD_SERVER_UNFILTERED_CLICKS = 259
        AD_SERVER_UNFILTERED_IMPRESSIONS = 260
        AD_SERVER_UNFILTERED_TRACKED_ADS = 263
        AVERAGE_ECPM = 37
        AVERAGE_ECPM_WITHOUT_CPD = 5
        CLICKS = 2
        CODE_SERVED_COUNT = 44
        CTR = 3
        GOOGLE_SOLD_AUCTION_COVIEWED_IMPRESSIONS = 129
        GOOGLE_SOLD_AUCTION_IMPRESSIONS = 128
        GOOGLE_SOLD_COVIEWED_IMPRESSIONS = 131
        GOOGLE_SOLD_IMPRESSIONS = 130
        GOOGLE_SOLD_RESERVATION_COVIEWED_IMPRESSIONS = 127
        GOOGLE_SOLD_RESERVATION_IMPRESSIONS = 126
        IMPRESSIONS = 1
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
        RESPONSES_SERVED = 39
        REVENUE = 36
        REVENUE_WITHOUT_CPD = 4
        SERVER_SIDE_UNWRAPPING_AVERAGE_LATENCY_MS = 434
        SERVER_SIDE_UNWRAPPING_CALLOUTS = 435
        SERVER_SIDE_UNWRAPPING_EMPTY_RESPONSES = 436
        SERVER_SIDE_UNWRAPPING_ERROR_RESPONSES = 437
        SERVER_SIDE_UNWRAPPING_SUCCESSFUL_RESPONSES = 438
        SERVER_SIDE_UNWRAPPING_TIMEOUTS = 439
        UNFILLED_IMPRESSIONS = 45
        UNMATCHED_AD_REQUESTS = 43
        USER_MESSAGES_OFFERWALL_MESSAGES_SHOWN = 121
        USER_MESSAGES_OFFERWALL_SUCCESSFUL_ENGAGEMENTS = 122
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
        YIELD_GROUP_SUCCESSFUL_RESPONSES = 84

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

    class ReportType(proto.Enum):
        r"""Supported report types.

        Values:
            REPORT_TYPE_UNSPECIFIED (0):
                Default value. This value is unused.
            HISTORICAL (1):
                Historical.
        """
        REPORT_TYPE_UNSPECIFIED = 0
        HISTORICAL = 1

    class Visibility(proto.Enum):
        r"""The visibility of a report.

        Values:
            HIDDEN (0):
                Default value. Reports with hidden visibility
                will not appear in the Ad Manager UI.
            DRAFT (1):
                Reports with draft visibility will appear in
                the Ad Manager UI only if the user has
                configured the UI to show them.
            SAVED (2):
                Reports with saved visibility will appear in
                the Ad Manager UI by default.
        """
        HIDDEN = 0
        DRAFT = 1
        SAVED = 2

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

    class Value(proto.Message):
        r"""Represents a single value in a report.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            int_value (int):
                For integer values.

                This field is a member of `oneof`_ ``value``.
            double_value (float):
                For double values.

                This field is a member of `oneof`_ ``value``.
            string_value (str):
                For string values.

                This field is a member of `oneof`_ ``value``.
            bool_value (bool):
                For boolean values.

                This field is a member of `oneof`_ ``value``.
            int_list_value (google.ads.admanager_v1.types.Report.Value.IntList):
                For lists of integer values.

                This field is a member of `oneof`_ ``value``.
            string_list_value (google.ads.admanager_v1.types.Report.Value.StringList):
                For lists of string values.

                This field is a member of `oneof`_ ``value``.
            bytes_value (bytes):
                For bytes values.

                This field is a member of `oneof`_ ``value``.
        """

        class IntList(proto.Message):
            r"""A list of integer values.

            Attributes:
                values (MutableSequence[int]):
                    The values
            """

            values: MutableSequence[int] = proto.RepeatedField(
                proto.INT64,
                number=1,
            )

        class StringList(proto.Message):
            r"""A list of string values.

            Attributes:
                values (MutableSequence[str]):
                    The values
            """

            values: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=1,
            )

        int_value: int = proto.Field(
            proto.INT64,
            number=1,
            oneof="value",
        )
        double_value: float = proto.Field(
            proto.DOUBLE,
            number=2,
            oneof="value",
        )
        string_value: str = proto.Field(
            proto.STRING,
            number=3,
            oneof="value",
        )
        bool_value: bool = proto.Field(
            proto.BOOL,
            number=4,
            oneof="value",
        )
        int_list_value: "Report.Value.IntList" = proto.Field(
            proto.MESSAGE,
            number=6,
            oneof="value",
            message="Report.Value.IntList",
        )
        string_list_value: "Report.Value.StringList" = proto.Field(
            proto.MESSAGE,
            number=7,
            oneof="value",
            message="Report.Value.StringList",
        )
        bytes_value: bytes = proto.Field(
            proto.BYTES,
            number=8,
            oneof="value",
        )

    class Sort(proto.Message):
        r"""Represents a sorting in a report.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            field (google.ads.admanager_v1.types.Report.Field):
                Required. A field (dimension or metric) to
                sort by.
            descending (bool):
                Optional. The sort order. If true the sort
                will be descending.
            slice_ (google.ads.admanager_v1.types.Report.Slice):
                Optional. Use to sort on a specific slice of
                data.

                This field is a member of `oneof`_ ``_slice``.
            time_period_index (int):
                Optional. When using time period columns, use
                this to sort on a specific column.

                This field is a member of `oneof`_ ``_time_period_index``.
            metric_value_type (google.ads.admanager_v1.types.Report.MetricValueType):
                Optional. Use to specify which metric value
                type to sort on. Defaults to PRIMARY.

                This field is a member of `oneof`_ ``_metric_value_type``.
        """

        field: "Report.Field" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Report.Field",
        )
        descending: bool = proto.Field(
            proto.BOOL,
            number=2,
        )
        slice_: "Report.Slice" = proto.Field(
            proto.MESSAGE,
            number=3,
            optional=True,
            message="Report.Slice",
        )
        time_period_index: int = proto.Field(
            proto.INT32,
            number=4,
            optional=True,
        )
        metric_value_type: "Report.MetricValueType" = proto.Field(
            proto.ENUM,
            number=5,
            optional=True,
            enum="Report.MetricValueType",
        )

    class DataTable(proto.Message):
        r"""A table containing report data including dimension and metric
        values.

        """

        class Row(proto.Message):
            r"""A row of report data.

            Attributes:
                dimension_values (MutableSequence[google.ads.admanager_v1.types.Report.Value]):
                    The order of the dimension values is the same
                    as the order of the dimensions specified in the
                    request.
                metric_value_groups (MutableSequence[google.ads.admanager_v1.types.Report.DataTable.MetricValueGroup]):
                    The length of the metric_value_groups field will be equal to
                    the length of the date_ranges field in the fetch response.
                    The metric_value_groups field is ordered such that each
                    index corresponds to the date_range at the same index. For
                    example, given date_ranges [x, y], metric_value_groups will
                    have a length of two. The first entry in metric_value_groups
                    represents the metrics for date x and the second entry in
                    metric_value_groups represents the metrics for date y.
            """

            dimension_values: MutableSequence["Report.Value"] = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message="Report.Value",
            )
            metric_value_groups: MutableSequence[
                "Report.DataTable.MetricValueGroup"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="Report.DataTable.MetricValueGroup",
            )

        class MetricValueGroup(proto.Message):
            r"""Contains all metric values requested for a single date range
            and set of column dimension values (returned in the columns
            field of the response). The order of the metrics in each field
            corresponds to the order of the metrics specified in the
            request.

            Attributes:
                primary_values (MutableSequence[google.ads.admanager_v1.types.Report.Value]):
                    Data for the PRIMARY MetricValueType.
                primary_percent_of_total_values (MutableSequence[google.ads.admanager_v1.types.Report.Value]):
                    Data for the PRIMARY_PERCENT_OF_TOTAL MetricValueType.
                comparison_values (MutableSequence[google.ads.admanager_v1.types.Report.Value]):
                    Data for the COMPARISON MetricValueType.
                comparison_percent_of_total_values (MutableSequence[google.ads.admanager_v1.types.Report.Value]):
                    Data for the COMPARISON_PERCENT_OF_TOTAL MetricValueType.
                absolute_change_values (MutableSequence[google.ads.admanager_v1.types.Report.Value]):
                    Data for the ABSOLUTE_CHANGE MetricValueType.
                relative_change_values (MutableSequence[google.ads.admanager_v1.types.Report.Value]):
                    Data for the RELATIVE_CHANGE MetricValueType.
                flag_values (MutableSequence[bool]):
                    If true, the flag's conditions are met. If false, the flag's
                    conditions are not met. flag_values has the same length as
                    flags and index i of flag_values represents the flag at
                    index i of flags.
            """

            primary_values: MutableSequence["Report.Value"] = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message="Report.Value",
            )
            primary_percent_of_total_values: MutableSequence[
                "Report.Value"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="Report.Value",
            )
            comparison_values: MutableSequence["Report.Value"] = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message="Report.Value",
            )
            comparison_percent_of_total_values: MutableSequence[
                "Report.Value"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=4,
                message="Report.Value",
            )
            absolute_change_values: MutableSequence[
                "Report.Value"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=5,
                message="Report.Value",
            )
            relative_change_values: MutableSequence[
                "Report.Value"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=6,
                message="Report.Value",
            )
            flag_values: MutableSequence[bool] = proto.RepeatedField(
                proto.BOOL,
                number=7,
            )

    class Field(proto.Message):
        r"""A dimension or a metric in a report.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            dimension (google.ads.admanager_v1.types.Report.Dimension):
                The dimension this field represents.

                This field is a member of `oneof`_ ``field``.
            metric (google.ads.admanager_v1.types.Report.Metric):
                The metric this field represents.

                This field is a member of `oneof`_ ``field``.
        """

        dimension: "Report.Dimension" = proto.Field(
            proto.ENUM,
            number=1,
            oneof="field",
            enum="Report.Dimension",
        )
        metric: "Report.Metric" = proto.Field(
            proto.ENUM,
            number=2,
            oneof="field",
            enum="Report.Metric",
        )

    class Slice(proto.Message):
        r"""Use to specify a slice of data.

        For example, in a report, to focus on just data from the US, specify
        ``COUNTRY_NAME`` for dimension and value: ``"United States"``.

        Attributes:
            dimension (google.ads.admanager_v1.types.Report.Dimension):
                Required. The dimension to slice on.
            value (google.ads.admanager_v1.types.Report.Value):
                Required. The value of the dimension.
        """

        dimension: "Report.Dimension" = proto.Field(
            proto.ENUM,
            number=1,
            enum="Report.Dimension",
        )
        value: "Report.Value" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Report.Value",
        )

    class Filter(proto.Message):
        r"""A filter over one or more fields.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            field_filter (google.ads.admanager_v1.types.Report.Filter.FieldFilter):
                A filter on a single field.

                This field is a member of `oneof`_ ``type``.
            not_filter (google.ads.admanager_v1.types.Report.Filter):
                A filter whose result is negated.

                This field is a member of `oneof`_ ``type``.
            and_filter (google.ads.admanager_v1.types.Report.Filter.FilterList):
                A list of filters whose results are AND-ed.

                This field is a member of `oneof`_ ``type``.
            or_filter (google.ads.admanager_v1.types.Report.Filter.FilterList):
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
                    Operand matches against a regex or set of
                    regexes (one must match)
                NOT_MATCHES (10):
                    Operand negative matches against a regex or
                    set of regexes (none must match)
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
                field (google.ads.admanager_v1.types.Report.Field):
                    Required. The field to filter on.
                operation (google.ads.admanager_v1.types.Report.Filter.Operation):
                    Required. The operation of this filter.
                values (MutableSequence[google.ads.admanager_v1.types.Report.Value]):
                    Required. Values to filter to.
                slice_ (google.ads.admanager_v1.types.Report.Slice):
                    Optional. Use to filter on a specific slice
                    of data.

                    This field is a member of `oneof`_ ``_slice``.
                time_period_index (int):
                    Optional. When using time period columns, use
                    this to filter on a specific column.

                    This field is a member of `oneof`_ ``_time_period_index``.
                metric_value_type (google.ads.admanager_v1.types.Report.MetricValueType):
                    Optional. Use to specify which metric value
                    type to filter on. Defaults to PRIMARY.

                    This field is a member of `oneof`_ ``_metric_value_type``.
            """

            field: "Report.Field" = proto.Field(
                proto.MESSAGE,
                number=1,
                message="Report.Field",
            )
            operation: "Report.Filter.Operation" = proto.Field(
                proto.ENUM,
                number=2,
                enum="Report.Filter.Operation",
            )
            values: MutableSequence["Report.Value"] = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message="Report.Value",
            )
            slice_: "Report.Slice" = proto.Field(
                proto.MESSAGE,
                number=4,
                optional=True,
                message="Report.Slice",
            )
            time_period_index: int = proto.Field(
                proto.INT32,
                number=5,
                optional=True,
            )
            metric_value_type: "Report.MetricValueType" = proto.Field(
                proto.ENUM,
                number=6,
                optional=True,
                enum="Report.MetricValueType",
            )

        class FilterList(proto.Message):
            r"""A list of filters.

            Attributes:
                filters (MutableSequence[google.ads.admanager_v1.types.Report.Filter]):
                    Required. A list of filters.
            """

            filters: MutableSequence["Report.Filter"] = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message="Report.Filter",
            )

        field_filter: "Report.Filter.FieldFilter" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="type",
            message="Report.Filter.FieldFilter",
        )
        not_filter: "Report.Filter" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="type",
            message="Report.Filter",
        )
        and_filter: "Report.Filter.FilterList" = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="type",
            message="Report.Filter.FilterList",
        )
        or_filter: "Report.Filter.FilterList" = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="type",
            message="Report.Filter.FilterList",
        )

    class Flag(proto.Message):
        r"""A flag for a report. Flags are used show if certain thresholds are
        met. Result rows that match the filter will have the corresponding
        [MetricValueGroup.flagValues][MetricValueGroup] index set to true.
        For more information about flags see:
        https://support.google.com/admanager/answer/15079975

        Attributes:
            filters (MutableSequence[google.ads.admanager_v1.types.Report.Filter]):
                Required. Filters to apply for the flag.
            name (str):
                Optional. Name of the flag.
                The flag names RED, YELLOW, GREEN, BLUE, PURPLE,
                and GREY correspond to the colored flags that
                appear in the UI. The UI will not display flags
                with other names, but they are available for use
                by API clients.
        """

        filters: MutableSequence["Report.Filter"] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Report.Filter",
        )
        name: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class DateRange(proto.Message):
        r"""A date range for a report.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            fixed (google.ads.admanager_v1.types.Report.DateRange.FixedDateRange):
                A fixed date range.

                This field is a member of `oneof`_ ``date_range_type``.
            relative (google.ads.admanager_v1.types.Report.DateRange.RelativeDateRange):
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
                PREVIOUS_PERIOD (22):
                    Only valid when used in the comparison_date_range field. The
                    complete period preceding the date period provided in
                    date_range.

                    In the case where date_range is a FixedDateRange of N days,
                    this will be a period of N days where the end date is the
                    date preceding the start date of the date_range.

                    In the case where date_range is a RelativeDateRange, this
                    will be a period of the same time frame preceding the
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
                    will be a period of the same time frame exactly 1 year prior
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

        fixed: "Report.DateRange.FixedDateRange" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="date_range_type",
            message="Report.DateRange.FixedDateRange",
        )
        relative: "Report.DateRange.RelativeDateRange" = proto.Field(
            proto.ENUM,
            number=2,
            oneof="date_range_type",
            enum="Report.DateRange.RelativeDateRange",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    report_id: int = proto.Field(
        proto.INT64,
        number=3,
    )
    visibility: Visibility = proto.Field(
        proto.ENUM,
        number=2,
        enum=Visibility,
    )
    report_definition: "ReportDefinition" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="ReportDefinition",
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    locale: str = proto.Field(
        proto.STRING,
        number=8,
    )
    schedule_options: "ScheduleOptions" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="ScheduleOptions",
    )


class ReportDefinition(proto.Message):
    r"""The definition of how a report should be run.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        dimensions (MutableSequence[google.ads.admanager_v1.types.Report.Dimension]):
            Required. The list of dimensions to report
            on. If empty, the report will have no
            dimensions, and any metrics will be totals.
        metrics (MutableSequence[google.ads.admanager_v1.types.Report.Metric]):
            Required. The list of metrics to report on.
            If empty, the report will have no metrics.
        filters (MutableSequence[google.ads.admanager_v1.types.Report.Filter]):
            Optional. The filters for this report.
        time_zone_source (google.ads.admanager_v1.types.Report.TimeZoneSource):
            Optional. Where to get the time zone for this report.
            Defaults to using the network time zone setting (PUBLISHER).
            If source is PROVIDED, the time_zone field in the report
            definition must also be provided with the desired time zone.
        time_zone (str):
            Optional. If time_zone_source is PROVIDED, this is the time
            zone to use for this report. Leave empty for any other time
            zone source. Time zone in IANA format (e.g.
            "America/New_York").
        currency_code (str):
            Optional. The ISO 4217 currency code for this
            report. Defaults to publisher currency code if
            not specified.
        date_range (google.ads.admanager_v1.types.Report.DateRange):
            Required. The primary date range of this
            report.
        comparison_date_range (google.ads.admanager_v1.types.Report.DateRange):
            Optional. The comparison date range of this
            report. If unspecified, the report will not have
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
        report_type (google.ads.admanager_v1.types.Report.ReportType):
            Required. The type of this report.
        time_period_column (google.ads.admanager_v1.types.Report.TimePeriodColumn):
            Optional. Include a time period column to introduce
            comparison columns in the report for each generated period.
            For example, set to "QUARTERS" here to have a column for
            each quarter present in the primary date range. If "PREVIOUS
            PERIOD" is specified in comparison_date_range, then each
            quarter column will also include comparison values for its
            relative previous quarter.
        flags (MutableSequence[google.ads.admanager_v1.types.Report.Flag]):
            Optional. List of flags for this report. Used
            to flag rows in a result set based on a set of
            defined filters.
        sorts (MutableSequence[google.ads.admanager_v1.types.Report.Sort]):
            Optional. Default sorts to apply to this
            report.
    """

    dimensions: MutableSequence["Report.Dimension"] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum="Report.Dimension",
    )
    metrics: MutableSequence["Report.Metric"] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum="Report.Metric",
    )
    filters: MutableSequence["Report.Filter"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="Report.Filter",
    )
    time_zone_source: "Report.TimeZoneSource" = proto.Field(
        proto.ENUM,
        number=20,
        enum="Report.TimeZoneSource",
    )
    time_zone: str = proto.Field(
        proto.STRING,
        number=4,
    )
    currency_code: str = proto.Field(
        proto.STRING,
        number=5,
    )
    date_range: "Report.DateRange" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="Report.DateRange",
    )
    comparison_date_range: "Report.DateRange" = proto.Field(
        proto.MESSAGE,
        number=9,
        optional=True,
        message="Report.DateRange",
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
    report_type: "Report.ReportType" = proto.Field(
        proto.ENUM,
        number=8,
        enum="Report.ReportType",
    )
    time_period_column: "Report.TimePeriodColumn" = proto.Field(
        proto.ENUM,
        number=10,
        enum="Report.TimePeriodColumn",
    )
    flags: MutableSequence["Report.Flag"] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message="Report.Flag",
    )
    sorts: MutableSequence["Report.Sort"] = proto.RepeatedField(
        proto.MESSAGE,
        number=15,
        message="Report.Sort",
    )


class ScheduleOptions(proto.Message):
    r"""The options for a scheduled report.

    Attributes:
        schedule (google.ads.admanager_v1.types.Schedule):
            Information pertaining to schedule itself.
        delivery_condition (google.ads.admanager_v1.types.ScheduleOptions.DeliveryCondition):
            Option for when to deliver the scheduled
            report.
        flags (MutableSequence[google.ads.admanager_v1.types.Report.Flag]):
            Optional. The flags evaluated when
            ReportDeliveryOption.WHEN_FLAG_PRESENT is specified.
    """

    class DeliveryCondition(proto.Enum):
        r"""Condition for when to email the scheduled report.

        Values:
            NEVER (0):
                Never deliver report.
            ALWAYS (1):
                Always deliver report.
            WHEN_FLAG_CONDITIONS_MET (2):
                Deliver report when flag's conditions are
                met.
        """
        NEVER = 0
        ALWAYS = 1
        WHEN_FLAG_CONDITIONS_MET = 2

    schedule: "Schedule" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Schedule",
    )
    delivery_condition: DeliveryCondition = proto.Field(
        proto.ENUM,
        number=2,
        enum=DeliveryCondition,
    )
    flags: MutableSequence["Report.Flag"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="Report.Flag",
    )


class Schedule(proto.Message):
    r"""The schedule for the report

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        weekly_schedule (google.ads.admanager_v1.types.Schedule.WeeklySchedule):
            Days of week to schedule report run.

            This field is a member of `oneof`_ ``frequency_schedule``.
        monthly_schedule (google.ads.admanager_v1.types.Schedule.MonthlySchedule):
            Days of month to schedule report run.

            This field is a member of `oneof`_ ``frequency_schedule``.
        start_date (google.type.date_pb2.Date):
            Date for the first run of the report.
        end_date (google.type.date_pb2.Date):
            Date for the final run of the report.
        frequency (google.ads.admanager_v1.types.Schedule.Frequency):
            Frequency to run report.
        start_time (google.type.timeofday_pb2.TimeOfDay):
            Indicates start time for schedule to run Will use the
            time_zone from ``ReportDefinition``. Defaults to the
            publisher's time zone if not specified.

            For HOURLY, TWO_TIMES_DAILY, THREE_TIMES_DAILY, or
            FOUR_TIMES_DAILY, this will be the time of day that the
            first report will run on the first day. For example, if the
            start time is 2:00 PM, and the frequency is
            THREE_TIMES_DAILY, the first day will have reports scheduled
            at 2:00 PM, 10:00 PM. Each subsequent day will have reports
            scheduled at 6:00 AM, 2:00 PM, 10:00 PM.
    """

    class Frequency(proto.Enum):
        r"""Frequency to run report.

        Values:
            FREQUENCY_UNSPECIFIED (0):
                No Frequency specified.
            HOURLY (1):
                Schedule report to run every hour.
            TWO_TIMES_DAILY (2):
                Schedule report to run twice a day (every 12
                hours).
            THREE_TIMES_DAILY (3):
                Schedule report to run three times a day
                (every 8 hours).
            FOUR_TIMES_DAILY (4):
                Schedule report to run four times a day
                (every 6 hours).
            DAILY (5):
                Schedule report to run on a daily basis.
            WEEKLY (6):
                Schedule report to run on a weekly basis.
            MONTHLY (7):
                Schedule report to run on a monthly basis.
        """
        FREQUENCY_UNSPECIFIED = 0
        HOURLY = 1
        TWO_TIMES_DAILY = 2
        THREE_TIMES_DAILY = 3
        FOUR_TIMES_DAILY = 4
        DAILY = 5
        WEEKLY = 6
        MONTHLY = 7

    class WeeklySchedule(proto.Message):
        r"""Days of week to schedule report run.

        Attributes:
            weekly_scheduled_days (MutableSequence[google.type.dayofweek_pb2.DayOfWeek]):
                Specifies days of the week on which to run
                report.
        """

        weekly_scheduled_days: MutableSequence[
            dayofweek_pb2.DayOfWeek
        ] = proto.RepeatedField(
            proto.ENUM,
            number=1,
            enum=dayofweek_pb2.DayOfWeek,
        )

    class MonthlySchedule(proto.Message):
        r"""Days of Month to schedule report run.

        Attributes:
            monthly_scheduled_days (MutableSequence[int]):
                Specifies days of the month to run report.
                Range is from 1-31. Will ignore days that are
                not valid for the given month.
        """

        monthly_scheduled_days: MutableSequence[int] = proto.RepeatedField(
            proto.INT32,
            number=1,
        )

    weekly_schedule: WeeklySchedule = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="frequency_schedule",
        message=WeeklySchedule,
    )
    monthly_schedule: MonthlySchedule = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="frequency_schedule",
        message=MonthlySchedule,
    )
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
    frequency: Frequency = proto.Field(
        proto.ENUM,
        number=3,
        enum=Frequency,
    )
    start_time: timeofday_pb2.TimeOfDay = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timeofday_pb2.TimeOfDay,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
