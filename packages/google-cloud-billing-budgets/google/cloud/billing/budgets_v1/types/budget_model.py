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


from google.protobuf import struct_pb2 as struct  # type: ignore
from google.type import money_pb2 as money  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.billing.budgets.v1",
    manifest={
        "Budget",
        "BudgetAmount",
        "LastPeriodAmount",
        "ThresholdRule",
        "NotificationsRule",
        "Filter",
    },
)


class Budget(proto.Message):
    r"""A budget is a plan that describes what you expect to spend on
    Cloud projects, plus the rules to execute as spend is tracked
    against that plan, (for example, send an alert when 90% of the
    target spend is met). Currently all plans are monthly budgets so
    the usage period(s) tracked are implied (calendar months of
    usage back-to-back).

    Attributes:
        name (str):
            Output only. Resource name of the budget. The resource name
            implies the scope of a budget. Values are of the form
            ``billingAccounts/{billingAccountId}/budgets/{budgetId}``.
        display_name (str):
            User data for display name in UI. The name
            must be less than or equal to 60 characters.
        budget_filter (~.budget_model.Filter):
            Optional. Filters that define which resources
            are used to compute the actual spend against the
            budget.
        amount (~.budget_model.BudgetAmount):
            Required. Budgeted amount.
        threshold_rules (Sequence[~.budget_model.ThresholdRule]):
            Optional. Rules that trigger alerts
            (notifications of thresholds being crossed) when
            spend exceeds the specified percentages of the
            budget.
        notifications_rule (~.budget_model.NotificationsRule):
            Optional. Rules to apply to notifications
            sent based on budget spend and thresholds.
        etag (str):
            Optional. Etag to validate that the object is
            unchanged for a read-modify-write operation.
            An empty etag will cause an update to overwrite
            other changes.
    """

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    budget_filter = proto.Field(proto.MESSAGE, number=3, message="Filter",)

    amount = proto.Field(proto.MESSAGE, number=4, message="BudgetAmount",)

    threshold_rules = proto.RepeatedField(
        proto.MESSAGE, number=5, message="ThresholdRule",
    )

    notifications_rule = proto.Field(
        proto.MESSAGE, number=6, message="NotificationsRule",
    )

    etag = proto.Field(proto.STRING, number=7)


class BudgetAmount(proto.Message):
    r"""The budgeted amount for each usage period.

    Attributes:
        specified_amount (~.money.Money):
            A specified amount to use as the budget. ``currency_code``
            is optional. If specified, it must match the currency of the
            billing account. The ``currency_code`` is provided on
            output.
        last_period_amount (~.budget_model.LastPeriodAmount):
            Use the last period's actual spend as the
            budget for the present period.
    """

    specified_amount = proto.Field(
        proto.MESSAGE, number=1, oneof="budget_amount", message=money.Money,
    )

    last_period_amount = proto.Field(
        proto.MESSAGE, number=2, oneof="budget_amount", message="LastPeriodAmount",
    )


class LastPeriodAmount(proto.Message):
    r"""Describes a budget amount targeted to last period's spend.
    At this time, the amount is automatically 100% of last period's
    spend; that is, there are no other options yet.
    Future configuration will be described here (for example,
    configuring a percentage of last period's spend).
    """


class ThresholdRule(proto.Message):
    r"""ThresholdRule contains a definition of a threshold which triggers an
    alert (a notification of a threshold being crossed) to be sent when
    spend goes above the specified amount. Alerts are automatically
    e-mailed to users with the Billing Account Administrator role or the
    Billing Account User role. The thresholds here have no effect on
    notifications sent to anything configured under
    ``Budget.all_updates_rule``.

    Attributes:
        threshold_percent (float):
            Required. Send an alert when this threshold
            is exceeded. This is a 1.0-based percentage, so
            0.5 = 50%. Validation: non-negative number.
        spend_basis (~.budget_model.ThresholdRule.Basis):
            Optional. The type of basis used to determine if spend has
            passed the threshold. Behavior defaults to CURRENT_SPEND if
            not set.
    """

    class Basis(proto.Enum):
        r"""The type of basis used to determine if spend has passed the
        threshold.
        """
        BASIS_UNSPECIFIED = 0
        CURRENT_SPEND = 1
        FORECASTED_SPEND = 2

    threshold_percent = proto.Field(proto.DOUBLE, number=1)

    spend_basis = proto.Field(proto.ENUM, number=2, enum=Basis,)


class NotificationsRule(proto.Message):
    r"""NotificationsRule defines notifications that are sent based
    on budget spend and thresholds.

    Attributes:
        pubsub_topic (str):
            Optional. The name of the Pub/Sub topic where budget related
            messages will be published, in the form
            ``projects/{project_id}/topics/{topic_id}``. Updates are
            sent at regular intervals to the topic. The topic needs to
            be created before the budget is created; see
            https://cloud.google.com/billing/docs/how-to/budgets#manage-notifications
            for more details. Caller is expected to have
            ``pubsub.topics.setIamPolicy`` permission on the topic when
            it's set for a budget, otherwise, the API call will fail
            with PERMISSION_DENIED. See
            https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications
            for more details on Pub/Sub roles and permissions.
        schema_version (str):
            Optional. The schema version of the notification sent to
            ``pubsub_topic``. Only "1.0" is accepted. It represents the
            JSON schema as defined in
            https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format
        monitoring_notification_channels (Sequence[str]):
            Optional. Targets to send notifications to when a threshold
            is exceeded. This is in addition to default recipients who
            have billing account IAM roles. The value is the full REST
            resource name of a monitoring notification channel with the
            form
            ``projects/{project_id}/notificationChannels/{channel_id}``.
            A maximum of 5 channels are allowed. See
            https://cloud.google.com/billing/docs/how-to/budgets-notification-recipients
            for more details.
        disable_default_iam_recipients (bool):
            Optional. When set to true, disables default
            notifications sent when a threshold is exceeded.
            Default notifications are sent to those with
            Billing Account Administrator and Billing
            Account User IAM roles for the target account.
    """

    pubsub_topic = proto.Field(proto.STRING, number=1)

    schema_version = proto.Field(proto.STRING, number=2)

    monitoring_notification_channels = proto.RepeatedField(proto.STRING, number=3)

    disable_default_iam_recipients = proto.Field(proto.BOOL, number=4)


class Filter(proto.Message):
    r"""A filter for a budget, limiting the scope of the cost to
    calculate.

    Attributes:
        projects (Sequence[str]):
            Optional. A set of projects of the form
            ``projects/{project}``, specifying that usage from only this
            set of projects should be included in the budget. If
            omitted, the report will include all usage for the billing
            account, regardless of which project the usage occurred on.
            Only zero or one project can be specified currently.
        credit_types (Sequence[str]):
            Optional. If
            [Filter.credit_types_treatment][google.cloud.billing.budgets.v1.Filter.credit_types_treatment]
            is INCLUDE_SPECIFIED_CREDITS, this is a list of credit types
            to be subtracted from gross cost to determine the spend for
            threshold calculations.

            If
            [Filter.credit_types_treatment][google.cloud.billing.budgets.v1.Filter.credit_types_treatment]
            is **not** INCLUDE_SPECIFIED_CREDITS, this field must be
            empty. See `a list of acceptable credit type
            values <https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables#credits-type>`__.
        credit_types_treatment (~.budget_model.Filter.CreditTypesTreatment):
            Optional. If not set, default behavior is
            ``INCLUDE_ALL_CREDITS``.
        services (Sequence[str]):
            Optional. A set of services of the form
            ``services/{service_id}``, specifying that usage from only
            this set of services should be included in the budget. If
            omitted, the report will include usage for all the services.
            The service names are available through the Catalog API:
            https://cloud.google.com/billing/v1/how-tos/catalog-api.
        subaccounts (Sequence[str]):
            Optional. A set of subaccounts of the form
            ``billingAccounts/{account_id}``, specifying that usage from
            only this set of subaccounts should be included in the
            budget. If a subaccount is set to the name of the parent
            account, usage from the parent account will be included. If
            the field is omitted, the report will include usage from the
            parent account and all subaccounts, if they exist.
        labels (Sequence[~.budget_model.Filter.LabelsEntry]):
            Optional. A single label and value pair
            specifying that usage from only this set of
            labeled resources should be included in the
            budget. Currently, multiple entries or multiple
            values per entry are not allowed. If omitted,
            the report will include all labeled and
            unlabeled usage.
    """

    class CreditTypesTreatment(proto.Enum):
        r"""Specifies how credits should be treated when determining
        spend for threshold calculations.
        """
        CREDIT_TYPES_TREATMENT_UNSPECIFIED = 0
        INCLUDE_ALL_CREDITS = 1
        EXCLUDE_ALL_CREDITS = 2
        INCLUDE_SPECIFIED_CREDITS = 3

    projects = proto.RepeatedField(proto.STRING, number=1)

    credit_types = proto.RepeatedField(proto.STRING, number=7)

    credit_types_treatment = proto.Field(
        proto.ENUM, number=4, enum=CreditTypesTreatment,
    )

    services = proto.RepeatedField(proto.STRING, number=3)

    subaccounts = proto.RepeatedField(proto.STRING, number=5)

    labels = proto.MapField(
        proto.STRING, proto.MESSAGE, number=6, message=struct.ListValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
