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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.recaptchaenterprise.v1",
    manifest={
        "CreateAssessmentRequest",
        "AnnotateAssessmentRequest",
        "AnnotateAssessmentResponse",
        "Assessment",
        "Event",
        "RiskAnalysis",
        "TokenProperties",
        "AccountDefenderAssessment",
        "CreateKeyRequest",
        "ListKeysRequest",
        "ListKeysResponse",
        "GetKeyRequest",
        "UpdateKeyRequest",
        "DeleteKeyRequest",
        "MigrateKeyRequest",
        "GetMetricsRequest",
        "Metrics",
        "Key",
        "TestingOptions",
        "WebKeySettings",
        "AndroidKeySettings",
        "IOSKeySettings",
        "ScoreDistribution",
        "ScoreMetrics",
        "ChallengeMetrics",
        "ListRelatedAccountGroupMembershipsRequest",
        "ListRelatedAccountGroupMembershipsResponse",
        "ListRelatedAccountGroupsRequest",
        "ListRelatedAccountGroupsResponse",
        "SearchRelatedAccountGroupMembershipsRequest",
        "SearchRelatedAccountGroupMembershipsResponse",
        "RelatedAccountGroupMembership",
        "RelatedAccountGroup",
    },
)


class CreateAssessmentRequest(proto.Message):
    r"""The create assessment request message.

    Attributes:
        parent (str):
            Required. The name of the project in which
            the assessment will be created, in the format
            "projects/{project}".
        assessment (google.cloud.recaptchaenterprise_v1.types.Assessment):
            Required. The assessment details.
    """

    parent = proto.Field(proto.STRING, number=1,)
    assessment = proto.Field(proto.MESSAGE, number=2, message="Assessment",)


class AnnotateAssessmentRequest(proto.Message):
    r"""The request message to annotate an Assessment.

    Attributes:
        name (str):
            Required. The resource name of the
            Assessment, in the format
            "projects/{project}/assessments/{assessment}".
        annotation (google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentRequest.Annotation):
            Optional. The annotation that will be
            assigned to the Event. This field can be left
            empty to provide reasons that apply to an event
            without concluding whether the event is
            legitimate or fraudulent.
        reasons (Sequence[google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentRequest.Reason]):
            Optional. Optional reasons for the annotation
            that will be assigned to the Event.
        hashed_account_id (bytes):
            Optional. Optional unique stable hashed user identifier to
            apply to the assessment. This is an alternative to setting
            the hashed_account_id in CreateAssessment, for example when
            the account identifier is not yet known in the initial
            request. It is recommended that the identifier is hashed
            using hmac-sha256 with stable secret.
    """

    class Annotation(proto.Enum):
        r"""Enum that represents the types of annotations."""
        ANNOTATION_UNSPECIFIED = 0
        LEGITIMATE = 1
        FRAUDULENT = 2
        PASSWORD_CORRECT = 3
        PASSWORD_INCORRECT = 4

    class Reason(proto.Enum):
        r"""Enum that represents potential reasons for annotating an
        assessment.
        """
        REASON_UNSPECIFIED = 0
        CHARGEBACK = 1
        CHARGEBACK_FRAUD = 8
        CHARGEBACK_DISPUTE = 9
        PAYMENT_HEURISTICS = 2
        INITIATED_TWO_FACTOR = 7
        PASSED_TWO_FACTOR = 3
        FAILED_TWO_FACTOR = 4
        CORRECT_PASSWORD = 5
        INCORRECT_PASSWORD = 6

    name = proto.Field(proto.STRING, number=1,)
    annotation = proto.Field(proto.ENUM, number=2, enum=Annotation,)
    reasons = proto.RepeatedField(proto.ENUM, number=3, enum=Reason,)
    hashed_account_id = proto.Field(proto.BYTES, number=4,)


class AnnotateAssessmentResponse(proto.Message):
    r"""Empty response for AnnotateAssessment.
    """


class Assessment(proto.Message):
    r"""A recaptcha assessment resource.

    Attributes:
        name (str):
            Output only. The resource name for the
            Assessment in the format
            "projects/{project}/assessments/{assessment}".
        event (google.cloud.recaptchaenterprise_v1.types.Event):
            The event being assessed.
        risk_analysis (google.cloud.recaptchaenterprise_v1.types.RiskAnalysis):
            Output only. The risk analysis result for the
            event being assessed.
        token_properties (google.cloud.recaptchaenterprise_v1.types.TokenProperties):
            Output only. Properties of the provided event
            token.
        account_defender_assessment (google.cloud.recaptchaenterprise_v1.types.AccountDefenderAssessment):
            Assessment returned by Account Defender when a
            hashed_account_id is provided.
    """

    name = proto.Field(proto.STRING, number=1,)
    event = proto.Field(proto.MESSAGE, number=2, message="Event",)
    risk_analysis = proto.Field(proto.MESSAGE, number=3, message="RiskAnalysis",)
    token_properties = proto.Field(proto.MESSAGE, number=4, message="TokenProperties",)
    account_defender_assessment = proto.Field(
        proto.MESSAGE, number=6, message="AccountDefenderAssessment",
    )


class Event(proto.Message):
    r"""

    Attributes:
        token (str):
            Optional. The user response token provided by
            the reCAPTCHA client-side integration on your
            site.
        site_key (str):
            Optional. The site key that was used to
            invoke reCAPTCHA on your site and generate the
            token.
        user_agent (str):
            Optional. The user agent present in the
            request from the user's device related to this
            event.
        user_ip_address (str):
            Optional. The IP address in the request from
            the user's device related to this event.
        expected_action (str):
            Optional. The expected action for this type
            of event. This should be the same action
            provided at token generation time on client-side
            platforms already integrated with recaptcha
            enterprise.
        hashed_account_id (bytes):
            Optional. Optional unique stable hashed user
            identifier for the request. The identifier
            should ideally be hashed using sha256 with
            stable secret.
    """

    token = proto.Field(proto.STRING, number=1,)
    site_key = proto.Field(proto.STRING, number=2,)
    user_agent = proto.Field(proto.STRING, number=3,)
    user_ip_address = proto.Field(proto.STRING, number=4,)
    expected_action = proto.Field(proto.STRING, number=5,)
    hashed_account_id = proto.Field(proto.BYTES, number=6,)


class RiskAnalysis(proto.Message):
    r"""Risk analysis result for an event.

    Attributes:
        score (float):
            Legitimate event score from 0.0 to 1.0.
            (1.0 means very likely legitimate traffic while
            0.0 means very likely non-legitimate traffic).
        reasons (Sequence[google.cloud.recaptchaenterprise_v1.types.RiskAnalysis.ClassificationReason]):
            Reasons contributing to the risk analysis
            verdict.
    """

    class ClassificationReason(proto.Enum):
        r"""Reasons contributing to the risk analysis verdict."""
        CLASSIFICATION_REASON_UNSPECIFIED = 0
        AUTOMATION = 1
        UNEXPECTED_ENVIRONMENT = 2
        TOO_MUCH_TRAFFIC = 3
        UNEXPECTED_USAGE_PATTERNS = 4
        LOW_CONFIDENCE_SCORE = 5

    score = proto.Field(proto.FLOAT, number=1,)
    reasons = proto.RepeatedField(proto.ENUM, number=2, enum=ClassificationReason,)


class TokenProperties(proto.Message):
    r"""

    Attributes:
        valid (bool):
            Whether the provided user response token is valid. When
            valid = false, the reason could be specified in
            invalid_reason or it could also be due to a user failing to
            solve a challenge or a sitekey mismatch (i.e the sitekey
            used to generate the token was different than the one
            specified in the assessment).
        invalid_reason (google.cloud.recaptchaenterprise_v1.types.TokenProperties.InvalidReason):
            Reason associated with the response when
            valid = false.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp corresponding to the generation
            of the token.
        hostname (str):
            The hostname of the page on which the token
            was generated.
        action (str):
            Action name provided at token generation.
    """

    class InvalidReason(proto.Enum):
        r"""Enum that represents the types of invalid token reasons."""
        INVALID_REASON_UNSPECIFIED = 0
        UNKNOWN_INVALID_REASON = 1
        MALFORMED = 2
        EXPIRED = 3
        DUPE = 4
        MISSING = 5
        BROWSER_ERROR = 6

    valid = proto.Field(proto.BOOL, number=1,)
    invalid_reason = proto.Field(proto.ENUM, number=2, enum=InvalidReason,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    hostname = proto.Field(proto.STRING, number=4,)
    action = proto.Field(proto.STRING, number=5,)


class AccountDefenderAssessment(proto.Message):
    r"""Account Defender risk assessment.

    Attributes:
        labels (Sequence[google.cloud.recaptchaenterprise_v1.types.AccountDefenderAssessment.AccountDefenderLabel]):
            Labels for this request.
    """

    class AccountDefenderLabel(proto.Enum):
        r"""Labels returned by Account Defender for this request."""
        ACCOUNT_DEFENDER_LABEL_UNSPECIFIED = 0
        PROFILE_MATCH = 1
        SUSPICIOUS_LOGIN_ACTIVITY = 2
        SUSPICIOUS_ACCOUNT_CREATION = 3
        RELATED_ACCOUNTS_NUMBER_HIGH = 4

    labels = proto.RepeatedField(proto.ENUM, number=1, enum=AccountDefenderLabel,)


class CreateKeyRequest(proto.Message):
    r"""The create key request message.

    Attributes:
        parent (str):
            Required. The name of the project in which
            the key will be created, in the format
            "projects/{project}".
        key (google.cloud.recaptchaenterprise_v1.types.Key):
            Required. Information to create a reCAPTCHA
            Enterprise key.
    """

    parent = proto.Field(proto.STRING, number=1,)
    key = proto.Field(proto.MESSAGE, number=2, message="Key",)


class ListKeysRequest(proto.Message):
    r"""The list keys request message.

    Attributes:
        parent (str):
            Required. The name of the project that
            contains the keys that will be listed, in the
            format "projects/{project}".
        page_size (int):
            Optional. The maximum number of keys to
            return. Default is 10. Max limit is 1000.
        page_token (str):
            Optional. The next_page_token value returned from a
            previous. ListKeysRequest, if any.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListKeysResponse(proto.Message):
    r"""Response to request to list keys in a project.

    Attributes:
        keys (Sequence[google.cloud.recaptchaenterprise_v1.types.Key]):
            Key details.
        next_page_token (str):
            Token to retrieve the next page of results.
            It is set to empty if no keys remain in results.
    """

    @property
    def raw_page(self):
        return self

    keys = proto.RepeatedField(proto.MESSAGE, number=1, message="Key",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetKeyRequest(proto.Message):
    r"""The get key request message.

    Attributes:
        name (str):
            Required. The name of the requested key, in
            the format "projects/{project}/keys/{key}".
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateKeyRequest(proto.Message):
    r"""The update key request message.

    Attributes:
        key (google.cloud.recaptchaenterprise_v1.types.Key):
            Required. The key to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The mask to control which fields of
            the key get updated. If the mask is not present,
            all fields will be updated.
    """

    key = proto.Field(proto.MESSAGE, number=1, message="Key",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteKeyRequest(proto.Message):
    r"""The delete key request message.

    Attributes:
        name (str):
            Required. The name of the key to be deleted,
            in the format "projects/{project}/keys/{key}".
    """

    name = proto.Field(proto.STRING, number=1,)


class MigrateKeyRequest(proto.Message):
    r"""The migrate key request message.

    Attributes:
        name (str):
            Required. The name of the key to be migrated,
            in the format "projects/{project}/keys/{key}".
    """

    name = proto.Field(proto.STRING, number=1,)


class GetMetricsRequest(proto.Message):
    r"""The get metrics request message.

    Attributes:
        name (str):
            Required. The name of the requested metrics,
            in the format
            "projects/{project}/keys/{key}/metrics".
    """

    name = proto.Field(proto.STRING, number=1,)


class Metrics(proto.Message):
    r"""Metrics for a single Key.

    Attributes:
        name (str):
            Output only. The name of the metrics, in the
            format "projects/{project}/keys/{key}/metrics".
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Inclusive start time aligned to a day (UTC).
        score_metrics (Sequence[google.cloud.recaptchaenterprise_v1.types.ScoreMetrics]):
            Metrics will be continuous and in order by
            dates, and in the granularity of day. All Key
            types should have score-based data.
        challenge_metrics (Sequence[google.cloud.recaptchaenterprise_v1.types.ChallengeMetrics]):
            Metrics will be continuous and in order by
            dates, and in the granularity of day. Only
            challenge-based keys (CHECKBOX, INVISIBLE), will
            have challenge-based data.
    """

    name = proto.Field(proto.STRING, number=4,)
    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    score_metrics = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ScoreMetrics",
    )
    challenge_metrics = proto.RepeatedField(
        proto.MESSAGE, number=3, message="ChallengeMetrics",
    )


class Key(proto.Message):
    r"""A key used to identify and configure applications (web and/or
    mobile) that use reCAPTCHA Enterprise.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            The resource name for the Key in the format
            "projects/{project}/keys/{key}".
        display_name (str):
            Human-readable display name of this key.
            Modifiable by user.
        web_settings (google.cloud.recaptchaenterprise_v1.types.WebKeySettings):
            Settings for keys that can be used by
            websites.

            This field is a member of `oneof`_ ``platform_settings``.
        android_settings (google.cloud.recaptchaenterprise_v1.types.AndroidKeySettings):
            Settings for keys that can be used by Android
            apps.

            This field is a member of `oneof`_ ``platform_settings``.
        ios_settings (google.cloud.recaptchaenterprise_v1.types.IOSKeySettings):
            Settings for keys that can be used by iOS
            apps.

            This field is a member of `oneof`_ ``platform_settings``.
        labels (Sequence[google.cloud.recaptchaenterprise_v1.types.Key.LabelsEntry]):
            See <a
            href="https://cloud.google.com/recaptcha-
            enterprise/docs/labels"> Creating and managing
            labels</a>.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp corresponding to the creation
            of this Key.
        testing_options (google.cloud.recaptchaenterprise_v1.types.TestingOptions):
            Options for user acceptance testing.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    web_settings = proto.Field(
        proto.MESSAGE, number=3, oneof="platform_settings", message="WebKeySettings",
    )
    android_settings = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="platform_settings",
        message="AndroidKeySettings",
    )
    ios_settings = proto.Field(
        proto.MESSAGE, number=5, oneof="platform_settings", message="IOSKeySettings",
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=6,)
    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    testing_options = proto.Field(proto.MESSAGE, number=9, message="TestingOptions",)


class TestingOptions(proto.Message):
    r"""Options for user acceptance testing.

    Attributes:
        testing_score (float):
            All assessments for this Key will return this
            score. Must be between 0 (likely not legitimate)
            and 1 (likely legitimate) inclusive.
        testing_challenge (google.cloud.recaptchaenterprise_v1.types.TestingOptions.TestingChallenge):
            For challenge-based keys only (CHECKBOX,
            INVISIBLE), all challenge requests for this site
            will return nocaptcha if NOCAPTCHA, or an
            unsolvable challenge if CHALLENGE.
    """

    class TestingChallenge(proto.Enum):
        r"""Enum that represents the challenge option for challenge-based
        (CHECKBOX, INVISIBLE) testing keys.
        """
        TESTING_CHALLENGE_UNSPECIFIED = 0
        NOCAPTCHA = 1
        UNSOLVABLE_CHALLENGE = 2

    testing_score = proto.Field(proto.FLOAT, number=1,)
    testing_challenge = proto.Field(proto.ENUM, number=2, enum=TestingChallenge,)


class WebKeySettings(proto.Message):
    r"""Settings specific to keys that can be used by websites.

    Attributes:
        allow_all_domains (bool):
            If set to true, it means allowed_domains will not be
            enforced.
        allowed_domains (Sequence[str]):
            Domains or subdomains of websites allowed to
            use the key. All subdomains of an allowed domain
            are automatically allowed. A valid domain
            requires a host and must not include any path,
            port, query or fragment. Examples: 'example.com'
            or 'subdomain.example.com'
        allow_amp_traffic (bool):
            If set to true, the key can be used on AMP
            (Accelerated Mobile Pages) websites. This is
            supported only for the SCORE integration type.
        integration_type (google.cloud.recaptchaenterprise_v1.types.WebKeySettings.IntegrationType):
            Required. Describes how this key is
            integrated with the website.
        challenge_security_preference (google.cloud.recaptchaenterprise_v1.types.WebKeySettings.ChallengeSecurityPreference):
            Settings for the frequency and difficulty at
            which this key triggers captcha challenges. This
            should only be specified for IntegrationTypes
            CHECKBOX and INVISIBLE.
    """

    class IntegrationType(proto.Enum):
        r"""Enum that represents the integration types for web keys."""
        INTEGRATION_TYPE_UNSPECIFIED = 0
        SCORE = 1
        CHECKBOX = 2
        INVISIBLE = 3

    class ChallengeSecurityPreference(proto.Enum):
        r"""Enum that represents the possible challenge frequency and
        difficulty configurations for a web key.
        """
        CHALLENGE_SECURITY_PREFERENCE_UNSPECIFIED = 0
        USABILITY = 1
        BALANCE = 2
        SECURITY = 3

    allow_all_domains = proto.Field(proto.BOOL, number=3,)
    allowed_domains = proto.RepeatedField(proto.STRING, number=1,)
    allow_amp_traffic = proto.Field(proto.BOOL, number=2,)
    integration_type = proto.Field(proto.ENUM, number=4, enum=IntegrationType,)
    challenge_security_preference = proto.Field(
        proto.ENUM, number=5, enum=ChallengeSecurityPreference,
    )


class AndroidKeySettings(proto.Message):
    r"""Settings specific to keys that can be used by Android apps.

    Attributes:
        allow_all_package_names (bool):
            If set to true, allowed_package_names are not enforced.
        allowed_package_names (Sequence[str]):
            Android package names of apps allowed to use
            the key. Example: 'com.companyname.appname'
    """

    allow_all_package_names = proto.Field(proto.BOOL, number=2,)
    allowed_package_names = proto.RepeatedField(proto.STRING, number=1,)


class IOSKeySettings(proto.Message):
    r"""Settings specific to keys that can be used by iOS apps.

    Attributes:
        allow_all_bundle_ids (bool):
            If set to true, allowed_bundle_ids are not enforced.
        allowed_bundle_ids (Sequence[str]):
            iOS bundle ids of apps allowed to use the
            key. Example:
            'com.companyname.productname.appname'
    """

    allow_all_bundle_ids = proto.Field(proto.BOOL, number=2,)
    allowed_bundle_ids = proto.RepeatedField(proto.STRING, number=1,)


class ScoreDistribution(proto.Message):
    r"""Score distribution.

    Attributes:
        score_buckets (Sequence[google.cloud.recaptchaenterprise_v1.types.ScoreDistribution.ScoreBucketsEntry]):
            Map key is score value multiplied by 100. The scores are
            discrete values between [0, 1]. The maximum number of
            buckets is on order of a few dozen, but typically much lower
            (ie. 10).
    """

    score_buckets = proto.MapField(proto.INT32, proto.INT64, number=1,)


class ScoreMetrics(proto.Message):
    r"""Metrics related to scoring.

    Attributes:
        overall_metrics (google.cloud.recaptchaenterprise_v1.types.ScoreDistribution):
            Aggregated score metrics for all traffic.
        action_metrics (Sequence[google.cloud.recaptchaenterprise_v1.types.ScoreMetrics.ActionMetricsEntry]):
            Action-based metrics. The map key is the
            action name which specified by the site owners
            at time of the "execute" client-side call.
            Populated only for SCORE keys.
    """

    overall_metrics = proto.Field(proto.MESSAGE, number=1, message="ScoreDistribution",)
    action_metrics = proto.MapField(
        proto.STRING, proto.MESSAGE, number=2, message="ScoreDistribution",
    )


class ChallengeMetrics(proto.Message):
    r"""Metrics related to challenges.

    Attributes:
        pageload_count (int):
            Count of reCAPTCHA checkboxes or badges
            rendered. This is mostly equivalent to a count
            of pageloads for pages that include reCAPTCHA.
        nocaptcha_count (int):
            Count of nocaptchas (successful verification
            without a challenge) issued.
        failed_count (int):
            Count of submitted challenge solutions that
            were incorrect or otherwise deemed suspicious
            such that a subsequent challenge was triggered.
        passed_count (int):
            Count of nocaptchas (successful verification
            without a challenge) plus submitted challenge
            solutions that were correct and resulted in
            verification.
    """

    pageload_count = proto.Field(proto.INT64, number=1,)
    nocaptcha_count = proto.Field(proto.INT64, number=2,)
    failed_count = proto.Field(proto.INT64, number=3,)
    passed_count = proto.Field(proto.INT64, number=4,)


class ListRelatedAccountGroupMembershipsRequest(proto.Message):
    r"""The request message to list memberships in a related account
    group.

    Attributes:
        parent (str):
            Required. The resource name for the related account group in
            the format
            ``projects/{project}/relatedaccountgroups/{relatedaccountgroup}``.
        page_size (int):
            Optional. The maximum number of accounts to
            return. The service may return fewer than this
            value. If unspecified, at most 50 accounts will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListRelatedAccountGroupMemberships`` call.

            When paginating, all other parameters provided to
            ``ListRelatedAccountGroupMemberships`` must match the call
            that provided the page token.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListRelatedAccountGroupMembershipsResponse(proto.Message):
    r"""The response to a ``ListRelatedAccountGroupMemberships`` call.

    Attributes:
        related_account_group_memberships (Sequence[google.cloud.recaptchaenterprise_v1.types.RelatedAccountGroupMembership]):
            The memberships listed by the query.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    related_account_group_memberships = proto.RepeatedField(
        proto.MESSAGE, number=1, message="RelatedAccountGroupMembership",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class ListRelatedAccountGroupsRequest(proto.Message):
    r"""The request message to list related account groups.

    Attributes:
        parent (str):
            Required. The name of the project to list
            related account groups from, in the format
            "projects/{project}".
        page_size (int):
            Optional. The maximum number of groups to
            return. The service may return fewer than this
            value. If unspecified, at most 50 groups will be
            returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListRelatedAccountGroups`` call. Provide this to retrieve
            the subsequent page.

            When paginating, all other parameters provided to
            ``ListRelatedAccountGroups`` must match the call that
            provided the page token.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListRelatedAccountGroupsResponse(proto.Message):
    r"""The response to a ``ListRelatedAccountGroups`` call.

    Attributes:
        related_account_groups (Sequence[google.cloud.recaptchaenterprise_v1.types.RelatedAccountGroup]):
            The groups of related accounts listed by the
            query.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    related_account_groups = proto.RepeatedField(
        proto.MESSAGE, number=1, message="RelatedAccountGroup",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class SearchRelatedAccountGroupMembershipsRequest(proto.Message):
    r"""The request message to search related account group
    memberships.

    Attributes:
        parent (str):
            Required. The name of the project to search
            related account group memberships from, in the
            format "projects/{project}".
        hashed_account_id (bytes):
            Optional. The unique stable hashed user identifier we should
            search connections to. The identifier should correspond to a
            ``hashed_account_id`` provided in a previous
            CreateAssessment or AnnotateAssessment call.
        page_size (int):
            Optional. The maximum number of groups to
            return. The service may return fewer than this
            value. If unspecified, at most 50 groups will be
            returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``SearchRelatedAccountGroupMemberships`` call. Provide this
            to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``SearchRelatedAccountGroupMemberships`` must match the call
            that provided the page token.
    """

    parent = proto.Field(proto.STRING, number=1,)
    hashed_account_id = proto.Field(proto.BYTES, number=2,)
    page_size = proto.Field(proto.INT32, number=3,)
    page_token = proto.Field(proto.STRING, number=4,)


class SearchRelatedAccountGroupMembershipsResponse(proto.Message):
    r"""The response to a ``SearchRelatedAccountGroupMemberships`` call.

    Attributes:
        related_account_group_memberships (Sequence[google.cloud.recaptchaenterprise_v1.types.RelatedAccountGroupMembership]):
            The queried memberships.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    related_account_group_memberships = proto.RepeatedField(
        proto.MESSAGE, number=1, message="RelatedAccountGroupMembership",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class RelatedAccountGroupMembership(proto.Message):
    r"""A membership in a group of related accounts.

    Attributes:
        name (str):
            Required. The resource name for this membership in the
            format
            ``projects/{project}/relatedaccountgroups/{relatedaccountgroup}/memberships/{membership}``.
        hashed_account_id (bytes):
            The unique stable hashed user identifier of the member. The
            identifier corresponds to a ``hashed_account_id`` provided
            in a previous CreateAssessment or AnnotateAssessment call.
    """

    name = proto.Field(proto.STRING, number=1,)
    hashed_account_id = proto.Field(proto.BYTES, number=2,)


class RelatedAccountGroup(proto.Message):
    r"""A group of related accounts.

    Attributes:
        name (str):
            Required. The resource name for the related account group in
            the format
            ``projects/{project}/relatedaccountgroups/{related_account_group}``.
    """

    name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
