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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.recaptchaenterprise.v1",
    manifest={
        "CreateAssessmentRequest",
        "TransactionEvent",
        "AnnotateAssessmentRequest",
        "AnnotateAssessmentResponse",
        "EndpointVerificationInfo",
        "AccountVerificationInfo",
        "PrivatePasswordLeakVerification",
        "Assessment",
        "Event",
        "TransactionData",
        "RiskAnalysis",
        "TokenProperties",
        "FraudPreventionAssessment",
        "AccountDefenderAssessment",
        "CreateKeyRequest",
        "ListKeysRequest",
        "ListKeysResponse",
        "RetrieveLegacySecretKeyRequest",
        "GetKeyRequest",
        "UpdateKeyRequest",
        "DeleteKeyRequest",
        "MigrateKeyRequest",
        "GetMetricsRequest",
        "Metrics",
        "RetrieveLegacySecretKeyResponse",
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
        "WafSettings",
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

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    assessment: "Assessment" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Assessment",
    )


class TransactionEvent(proto.Message):
    r"""Describes an event in the lifecycle of a payment transaction.

    Attributes:
        event_type (google.cloud.recaptchaenterprise_v1.types.TransactionEvent.TransactionEventType):
            Optional. The type of this transaction event.
        reason (str):
            Optional. The reason or standardized code
            that corresponds with this transaction event, if
            one exists. For example, a CHARGEBACK event with
            code 6005.
        value (float):
            Optional. The value that corresponds with
            this transaction event, if one exists. For
            example, a refund event where $5.00 was
            refunded. Currency is obtained from the original
            transaction data.
        event_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Timestamp when this transaction
            event occurred; otherwise assumed to be the time
            of the API call.
    """

    class TransactionEventType(proto.Enum):
        r"""Enum that represents an event in the payment transaction
        lifecycle.

        Values:
            TRANSACTION_EVENT_TYPE_UNSPECIFIED (0):
                Default, unspecified event type.
            MERCHANT_APPROVE (1):
                Indicates that the transaction is approved by the merchant.
                The accompanying reasons can include terms such as
                'INHOUSE', 'ACCERTIFY', 'CYBERSOURCE', or 'MANUAL_REVIEW'.
            MERCHANT_DENY (2):
                Indicates that the transaction is denied and concluded due
                to risks detected by the merchant. The accompanying reasons
                can include terms such as 'INHOUSE', 'ACCERTIFY',
                'CYBERSOURCE', or 'MANUAL_REVIEW'.
            MANUAL_REVIEW (3):
                Indicates that the transaction is being
                evaluated by a human, due to suspicion or risk.
            AUTHORIZATION (4):
                Indicates that the authorization attempt with
                the card issuer succeeded.
            AUTHORIZATION_DECLINE (5):
                Indicates that the authorization attempt with
                the card issuer failed. The accompanying reasons
                can include Visa's '54' indicating that the card
                is expired, or '82' indicating that the CVV is
                incorrect.
            PAYMENT_CAPTURE (6):
                Indicates that the transaction is completed
                because the funds were settled.
            PAYMENT_CAPTURE_DECLINE (7):
                Indicates that the transaction could not be
                completed because the funds were not settled.
            CANCEL (8):
                Indicates that the transaction has been canceled. Specify
                the reason for the cancellation. For example,
                'INSUFFICIENT_INVENTORY'.
            CHARGEBACK_INQUIRY (9):
                Indicates that the merchant has received a
                chargeback inquiry due to fraud for the
                transaction, requesting additional information
                before a fraud chargeback is officially issued
                and a formal chargeback notification is sent.
            CHARGEBACK_ALERT (10):
                Indicates that the merchant has received a
                chargeback alert due to fraud for the
                transaction. The process of resolving the
                dispute without involving the payment network is
                started.
            FRAUD_NOTIFICATION (11):
                Indicates that a fraud notification is issued for the
                transaction, sent by the payment instrument's issuing bank
                because the transaction appears to be fraudulent. We
                recommend including TC40 or SAFE data in the ``reason``
                field for this event type. For partial chargebacks, we
                recommend that you include an amount in the ``value`` field.
            CHARGEBACK (12):
                Indicates that the merchant is informed by the payment
                network that the transaction has entered the chargeback
                process due to fraud. Reason code examples include
                Discover's '6005' and '6041'. For partial chargebacks, we
                recommend that you include an amount in the ``value`` field.
            CHARGEBACK_REPRESENTMENT (13):
                Indicates that the transaction has entered the chargeback
                process due to fraud, and that the merchant has chosen to
                enter representment. Reason examples include Discover's
                '6005' and '6041'. For partial chargebacks, we recommend
                that you include an amount in the ``value`` field.
            CHARGEBACK_REVERSE (14):
                Indicates that the transaction has had a fraud chargeback
                which was illegitimate and was reversed as a result. For
                partial chargebacks, we recommend that you include an amount
                in the ``value`` field.
            REFUND_REQUEST (15):
                Indicates that the merchant has received a refund for a
                completed transaction. For partial refunds, we recommend
                that you include an amount in the ``value`` field. Reason
                example: 'TAX_EXEMPT' (partial refund of exempt tax)
            REFUND_DECLINE (16):
                Indicates that the merchant has received a refund request
                for this transaction, but that they have declined it. For
                partial refunds, we recommend that you include an amount in
                the ``value`` field. Reason example: 'TAX_EXEMPT' (partial
                refund of exempt tax)
            REFUND (17):
                Indicates that the completed transaction was refunded by the
                merchant. For partial refunds, we recommend that you include
                an amount in the ``value`` field. Reason example:
                'TAX_EXEMPT' (partial refund of exempt tax)
            REFUND_REVERSE (18):
                Indicates that the completed transaction was refunded by the
                merchant, and that this refund was reversed. For partial
                refunds, we recommend that you include an amount in the
                ``value`` field.
        """
        TRANSACTION_EVENT_TYPE_UNSPECIFIED = 0
        MERCHANT_APPROVE = 1
        MERCHANT_DENY = 2
        MANUAL_REVIEW = 3
        AUTHORIZATION = 4
        AUTHORIZATION_DECLINE = 5
        PAYMENT_CAPTURE = 6
        PAYMENT_CAPTURE_DECLINE = 7
        CANCEL = 8
        CHARGEBACK_INQUIRY = 9
        CHARGEBACK_ALERT = 10
        FRAUD_NOTIFICATION = 11
        CHARGEBACK = 12
        CHARGEBACK_REPRESENTMENT = 13
        CHARGEBACK_REVERSE = 14
        REFUND_REQUEST = 15
        REFUND_DECLINE = 16
        REFUND = 17
        REFUND_REVERSE = 18

    event_type: TransactionEventType = proto.Field(
        proto.ENUM,
        number=1,
        enum=TransactionEventType,
    )
    reason: str = proto.Field(
        proto.STRING,
        number=2,
    )
    value: float = proto.Field(
        proto.DOUBLE,
        number=3,
    )
    event_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


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
        reasons (MutableSequence[google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentRequest.Reason]):
            Optional. Optional reasons for the annotation
            that will be assigned to the Event.
        hashed_account_id (bytes):
            Optional. Unique stable hashed user identifier to apply to
            the assessment. This is an alternative to setting the
            hashed_account_id in CreateAssessment, for example when the
            account identifier is not yet known in the initial request.
            It is recommended that the identifier is hashed using
            hmac-sha256 with stable secret.
        transaction_event (google.cloud.recaptchaenterprise_v1.types.TransactionEvent):
            Optional. If the assessment is part of a
            payment transaction, provide details on payment
            lifecycle events that occur in the transaction.
    """

    class Annotation(proto.Enum):
        r"""Enum that represents the types of annotations.

        Values:
            ANNOTATION_UNSPECIFIED (0):
                Default unspecified type.
            LEGITIMATE (1):
                Provides information that the event turned
                out to be legitimate.
            FRAUDULENT (2):
                Provides information that the event turned
                out to be fraudulent.
            PASSWORD_CORRECT (3):
                Provides information that the event was related to a login
                event in which the user typed the correct password.
                Deprecated, prefer indicating CORRECT_PASSWORD through the
                reasons field instead.
            PASSWORD_INCORRECT (4):
                Provides information that the event was related to a login
                event in which the user typed the incorrect password.
                Deprecated, prefer indicating INCORRECT_PASSWORD through the
                reasons field instead.
        """
        ANNOTATION_UNSPECIFIED = 0
        LEGITIMATE = 1
        FRAUDULENT = 2
        PASSWORD_CORRECT = 3
        PASSWORD_INCORRECT = 4

    class Reason(proto.Enum):
        r"""Enum that represents potential reasons for annotating an
        assessment.

        Values:
            REASON_UNSPECIFIED (0):
                Default unspecified reason.
            CHARGEBACK (1):
                Indicates that the transaction had a chargeback issued with
                no other details. When possible, specify the type by using
                CHARGEBACK_FRAUD or CHARGEBACK_DISPUTE instead.
            CHARGEBACK_FRAUD (8):
                Indicates that the transaction had a
                chargeback issued related to an alleged
                unauthorized transaction from the cardholder's
                perspective (for example, the card number was
                stolen).
            CHARGEBACK_DISPUTE (9):
                Indicates that the transaction had a
                chargeback issued related to the cardholder
                having provided their card details but allegedly
                not being satisfied with the purchase (for
                example, misrepresentation, attempted
                cancellation).
            REFUND (10):
                Indicates that the completed payment
                transaction was refunded by the seller.
            REFUND_FRAUD (11):
                Indicates that the completed payment
                transaction was determined to be fraudulent by
                the seller, and was cancelled and refunded as a
                result.
            TRANSACTION_ACCEPTED (12):
                Indicates that the payment transaction was
                accepted, and the user was charged.
            TRANSACTION_DECLINED (13):
                Indicates that the payment transaction was
                declined, for example due to invalid card
                details.
            PAYMENT_HEURISTICS (2):
                Indicates the transaction associated with the
                assessment is suspected of being fraudulent
                based on the payment method, billing details,
                shipping address or other transaction
                information.
            INITIATED_TWO_FACTOR (7):
                Indicates that the user was served a 2FA challenge. An old
                assessment with ``ENUM_VALUES.INITIATED_TWO_FACTOR`` reason
                that has not been overwritten with ``PASSED_TWO_FACTOR`` is
                treated as an abandoned 2FA flow. This is equivalent to
                ``FAILED_TWO_FACTOR``.
            PASSED_TWO_FACTOR (3):
                Indicates that the user passed a 2FA
                challenge.
            FAILED_TWO_FACTOR (4):
                Indicates that the user failed a 2FA
                challenge.
            CORRECT_PASSWORD (5):
                Indicates the user provided the correct
                password.
            INCORRECT_PASSWORD (6):
                Indicates the user provided an incorrect
                password.
            SOCIAL_SPAM (14):
                Indicates that the user sent unwanted and
                abusive messages to other users of the platform,
                such as spam, scams, phishing, or social
                engineering.
        """
        REASON_UNSPECIFIED = 0
        CHARGEBACK = 1
        CHARGEBACK_FRAUD = 8
        CHARGEBACK_DISPUTE = 9
        REFUND = 10
        REFUND_FRAUD = 11
        TRANSACTION_ACCEPTED = 12
        TRANSACTION_DECLINED = 13
        PAYMENT_HEURISTICS = 2
        INITIATED_TWO_FACTOR = 7
        PASSED_TWO_FACTOR = 3
        FAILED_TWO_FACTOR = 4
        CORRECT_PASSWORD = 5
        INCORRECT_PASSWORD = 6
        SOCIAL_SPAM = 14

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    annotation: Annotation = proto.Field(
        proto.ENUM,
        number=2,
        enum=Annotation,
    )
    reasons: MutableSequence[Reason] = proto.RepeatedField(
        proto.ENUM,
        number=3,
        enum=Reason,
    )
    hashed_account_id: bytes = proto.Field(
        proto.BYTES,
        number=4,
    )
    transaction_event: "TransactionEvent" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="TransactionEvent",
    )


class AnnotateAssessmentResponse(proto.Message):
    r"""Empty response for AnnotateAssessment."""


class EndpointVerificationInfo(proto.Message):
    r"""Information about a verification endpoint that can be used
    for 2FA.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        email_address (str):
            Email address for which to trigger a
            verification request.

            This field is a member of `oneof`_ ``endpoint``.
        phone_number (str):
            Phone number for which to trigger a
            verification request. Should be given in E.164
            format.

            This field is a member of `oneof`_ ``endpoint``.
        request_token (str):
            Output only. Token to provide to the client
            to trigger endpoint verification. It must be
            used within 15 minutes.
        last_verification_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp of the last successful
            verification for the endpoint, if any.
    """

    email_address: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="endpoint",
    )
    phone_number: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="endpoint",
    )
    request_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    last_verification_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


class AccountVerificationInfo(proto.Message):
    r"""Information about account verification, used for identity
    verification.

    Attributes:
        endpoints (MutableSequence[google.cloud.recaptchaenterprise_v1.types.EndpointVerificationInfo]):
            Endpoints that can be used for identity
            verification.
        language_code (str):
            Language code preference for the verification
            message, set as a IETF BCP 47 language code.
        latest_verification_result (google.cloud.recaptchaenterprise_v1.types.AccountVerificationInfo.Result):
            Output only. Result of the latest account
            verification challenge.
        username (str):
            Username of the account that is being
            verified. Deprecated. Customers should now
            provide the hashed account ID field in Event.
    """

    class Result(proto.Enum):
        r"""Result of the account verification as contained in the
        verdict token issued at the end of the verification flow.

        Values:
            RESULT_UNSPECIFIED (0):
                No information about the latest account
                verification.
            SUCCESS_USER_VERIFIED (1):
                The user was successfully verified. This
                means the account verification challenge was
                successfully completed.
            ERROR_USER_NOT_VERIFIED (2):
                The user failed the verification challenge.
            ERROR_SITE_ONBOARDING_INCOMPLETE (3):
                The site is not properly onboarded to use the
                account verification feature.
            ERROR_RECIPIENT_NOT_ALLOWED (4):
                The recipient is not allowed for account
                verification. This can occur during integration
                but should not occur in production.
            ERROR_RECIPIENT_ABUSE_LIMIT_EXHAUSTED (5):
                The recipient has already been sent too many
                verification codes in a short amount of time.
            ERROR_CRITICAL_INTERNAL (6):
                The verification flow could not be completed
                due to a critical internal error.
            ERROR_CUSTOMER_QUOTA_EXHAUSTED (7):
                The client has exceeded their two factor
                request quota for this period of time.
            ERROR_VERIFICATION_BYPASSED (8):
                The request cannot be processed at the time
                because of an incident. This bypass can be
                restricted to a problematic destination email
                domain, a customer, or could affect the entire
                service.
            ERROR_VERDICT_MISMATCH (9):
                The request parameters do not match with the
                token provided and cannot be processed.
        """
        RESULT_UNSPECIFIED = 0
        SUCCESS_USER_VERIFIED = 1
        ERROR_USER_NOT_VERIFIED = 2
        ERROR_SITE_ONBOARDING_INCOMPLETE = 3
        ERROR_RECIPIENT_NOT_ALLOWED = 4
        ERROR_RECIPIENT_ABUSE_LIMIT_EXHAUSTED = 5
        ERROR_CRITICAL_INTERNAL = 6
        ERROR_CUSTOMER_QUOTA_EXHAUSTED = 7
        ERROR_VERIFICATION_BYPASSED = 8
        ERROR_VERDICT_MISMATCH = 9

    endpoints: MutableSequence["EndpointVerificationInfo"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="EndpointVerificationInfo",
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=3,
    )
    latest_verification_result: Result = proto.Field(
        proto.ENUM,
        number=7,
        enum=Result,
    )
    username: str = proto.Field(
        proto.STRING,
        number=2,
    )


class PrivatePasswordLeakVerification(proto.Message):
    r"""Private password leak verification info.

    Attributes:
        lookup_hash_prefix (bytes):
            Optional. Exactly 26-bit prefix of the
            SHA-256 hash of the canonicalized username. It
            is used to look up password leaks associated
            with that hash prefix.
        encrypted_user_credentials_hash (bytes):
            Optional. Encrypted Scrypt hash of the canonicalized
            username+password. It is re-encrypted by the server and
            returned through ``reencrypted_user_credentials_hash``.
        encrypted_leak_match_prefixes (MutableSequence[bytes]):
            Output only. List of prefixes of the encrypted potential
            password leaks that matched the given parameters. They must
            be compared with the client-side decryption prefix of
            ``reencrypted_user_credentials_hash``
        reencrypted_user_credentials_hash (bytes):
            Output only. Corresponds to the re-encryption of the
            ``encrypted_user_credentials_hash`` field. It is used to
            match potential password leaks within
            ``encrypted_leak_match_prefixes``.
    """

    lookup_hash_prefix: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )
    encrypted_user_credentials_hash: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )
    encrypted_leak_match_prefixes: MutableSequence[bytes] = proto.RepeatedField(
        proto.BYTES,
        number=3,
    )
    reencrypted_user_credentials_hash: bytes = proto.Field(
        proto.BYTES,
        number=4,
    )


class Assessment(proto.Message):
    r"""A reCAPTCHA Enterprise assessment resource.

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
        account_verification (google.cloud.recaptchaenterprise_v1.types.AccountVerificationInfo):
            Account verification information for identity
            verification. The assessment event must include
            a token and site key to use this feature.
        account_defender_assessment (google.cloud.recaptchaenterprise_v1.types.AccountDefenderAssessment):
            Assessment returned by account defender when a
            hashed_account_id is provided.
        private_password_leak_verification (google.cloud.recaptchaenterprise_v1.types.PrivatePasswordLeakVerification):
            The private password leak verification field
            contains the parameters that are used to to
            check for leaks privately without sharing user
            credentials.
        fraud_prevention_assessment (google.cloud.recaptchaenterprise_v1.types.FraudPreventionAssessment):
            Assessment returned by Fraud Prevention when
            TransactionData is provided.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    event: "Event" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Event",
    )
    risk_analysis: "RiskAnalysis" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="RiskAnalysis",
    )
    token_properties: "TokenProperties" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="TokenProperties",
    )
    account_verification: "AccountVerificationInfo" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="AccountVerificationInfo",
    )
    account_defender_assessment: "AccountDefenderAssessment" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="AccountDefenderAssessment",
    )
    private_password_leak_verification: "PrivatePasswordLeakVerification" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="PrivatePasswordLeakVerification",
    )
    fraud_prevention_assessment: "FraudPreventionAssessment" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="FraudPreventionAssessment",
    )


class Event(proto.Message):
    r"""The event being assessed.

    Attributes:
        token (str):
            Optional. The user response token provided by
            the reCAPTCHA Enterprise client-side integration
            on your site.
        site_key (str):
            Optional. The site key that was used to
            invoke reCAPTCHA Enterprise on your site and
            generate the token.
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
            Optional. Unique stable hashed user
            identifier for the request. The identifier must
            be hashed using hmac-sha256 with stable secret.
        transaction_data (google.cloud.recaptchaenterprise_v1.types.TransactionData):
            Optional. Data describing a payment
            transaction to be assessed. Sending this data
            enables reCAPTCHA Enterprise Fraud Prevention
            and the FraudPreventionAssessment component in
            the response.
    """

    token: str = proto.Field(
        proto.STRING,
        number=1,
    )
    site_key: str = proto.Field(
        proto.STRING,
        number=2,
    )
    user_agent: str = proto.Field(
        proto.STRING,
        number=3,
    )
    user_ip_address: str = proto.Field(
        proto.STRING,
        number=4,
    )
    expected_action: str = proto.Field(
        proto.STRING,
        number=5,
    )
    hashed_account_id: bytes = proto.Field(
        proto.BYTES,
        number=6,
    )
    transaction_data: "TransactionData" = proto.Field(
        proto.MESSAGE,
        number=13,
        message="TransactionData",
    )


class TransactionData(proto.Message):
    r"""Transaction data associated with a payment protected by
    reCAPTCHA Enterprise. All fields are optional.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        transaction_id (str):
            Unique identifier for the transaction. This
            custom identifier can be used to reference this
            transaction in the future, for example, labeling
            a refund or chargeback event. Two attempts at
            the same transaction should use the same
            transaction id.

            This field is a member of `oneof`_ ``_transaction_id``.
        payment_method (str):
            The payment method for the transaction. The allowed values
            are:

            -  credit-card
            -  debit-card
            -  gift-card
            -  processor-{name} (If a third-party is used, for example,
               processor-paypal)
            -  custom-{name} (If an alternative method is used, for
               example, custom-crypto)
        card_bin (str):
            The Bank Identification Number - generally
            the first 6 or 8 digits of the card.
        card_last_four (str):
            The last four digits of the card.
        currency_code (str):
            The currency code in ISO-4217 format.
        value (float):
            The decimal value of the transaction in the
            specified currency.
        shipping_value (float):
            The value of shipping in the specified
            currency. 0 for free or no shipping.
        shipping_address (google.cloud.recaptchaenterprise_v1.types.TransactionData.Address):
            Destination address if this transaction
            involves shipping a physical item.
        billing_address (google.cloud.recaptchaenterprise_v1.types.TransactionData.Address):
            Address associated with the payment method
            when applicable.
        user (google.cloud.recaptchaenterprise_v1.types.TransactionData.User):
            Information about the user paying/initiating
            the transaction.
        merchants (MutableSequence[google.cloud.recaptchaenterprise_v1.types.TransactionData.User]):
            Information about the user or users
            fulfilling the transaction.
        items (MutableSequence[google.cloud.recaptchaenterprise_v1.types.TransactionData.Item]):
            Items purchased in this transaction.
        gateway_info (google.cloud.recaptchaenterprise_v1.types.TransactionData.GatewayInfo):
            Information about the payment gateway's
            response to the transaction.
    """

    class Address(proto.Message):
        r"""Structured address format for billing and shipping addresses.

        Attributes:
            recipient (str):
                The recipient name, potentially including
                information such as "care of".
            address (MutableSequence[str]):
                The first lines of the address. The first
                line generally contains the street name and
                number, and further lines may include
                information such as an apartment number.
            locality (str):
                The town/city of the address.
            administrative_area (str):
                The state, province, or otherwise
                administrative area of the address.
            region_code (str):
                The CLDR country/region of the address.
            postal_code (str):
                The postal or ZIP code of the address.
        """

        recipient: str = proto.Field(
            proto.STRING,
            number=1,
        )
        address: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        locality: str = proto.Field(
            proto.STRING,
            number=3,
        )
        administrative_area: str = proto.Field(
            proto.STRING,
            number=4,
        )
        region_code: str = proto.Field(
            proto.STRING,
            number=5,
        )
        postal_code: str = proto.Field(
            proto.STRING,
            number=6,
        )

    class User(proto.Message):
        r"""Details about a user's account involved in the transaction.

        Attributes:
            account_id (str):
                Unique account identifier for this user. If using account
                defender, this should match the hashed_account_id field.
                Otherwise, a unique and persistent identifier for this
                account.
            creation_ms (int):
                The epoch milliseconds of the user's account
                creation.
            email (str):
                The email address of the user.
            email_verified (bool):
                Whether the email has been verified to be
                accessible by the user (OTP or similar).
            phone_number (str):
                The phone number of the user, with country
                code.
            phone_verified (bool):
                Whether the phone number has been verified to
                be accessible by the user (OTP or similar).
        """

        account_id: str = proto.Field(
            proto.STRING,
            number=6,
        )
        creation_ms: int = proto.Field(
            proto.INT64,
            number=1,
        )
        email: str = proto.Field(
            proto.STRING,
            number=2,
        )
        email_verified: bool = proto.Field(
            proto.BOOL,
            number=3,
        )
        phone_number: str = proto.Field(
            proto.STRING,
            number=4,
        )
        phone_verified: bool = proto.Field(
            proto.BOOL,
            number=5,
        )

    class Item(proto.Message):
        r"""Line items being purchased in this transaction.

        Attributes:
            name (str):
                The full name of the item.
            value (float):
                The value per item that the user is paying,
                in the transaction currency, after discounts.
            quantity (int):
                The quantity of this item that is being
                purchased.
            merchant_account_id (str):
                When a merchant is specified, its corresponding account_id.
                Necessary to populate marketplace-style transactions.
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        value: float = proto.Field(
            proto.DOUBLE,
            number=2,
        )
        quantity: int = proto.Field(
            proto.INT64,
            number=3,
        )
        merchant_account_id: str = proto.Field(
            proto.STRING,
            number=4,
        )

    class GatewayInfo(proto.Message):
        r"""Details about the transaction from the gateway.

        Attributes:
            name (str):
                Name of the gateway service (for example,
                stripe, square, paypal).
            gateway_response_code (str):
                Gateway response code describing the state of
                the transaction.
            avs_response_code (str):
                AVS response code from the gateway
                (available only when reCAPTCHA Enterprise is
                called after authorization).
            cvv_response_code (str):
                CVV response code from the gateway
                (available only when reCAPTCHA Enterprise is
                called after authorization).
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        gateway_response_code: str = proto.Field(
            proto.STRING,
            number=2,
        )
        avs_response_code: str = proto.Field(
            proto.STRING,
            number=3,
        )
        cvv_response_code: str = proto.Field(
            proto.STRING,
            number=4,
        )

    transaction_id: str = proto.Field(
        proto.STRING,
        number=11,
        optional=True,
    )
    payment_method: str = proto.Field(
        proto.STRING,
        number=1,
    )
    card_bin: str = proto.Field(
        proto.STRING,
        number=2,
    )
    card_last_four: str = proto.Field(
        proto.STRING,
        number=3,
    )
    currency_code: str = proto.Field(
        proto.STRING,
        number=4,
    )
    value: float = proto.Field(
        proto.DOUBLE,
        number=5,
    )
    shipping_value: float = proto.Field(
        proto.DOUBLE,
        number=12,
    )
    shipping_address: Address = proto.Field(
        proto.MESSAGE,
        number=6,
        message=Address,
    )
    billing_address: Address = proto.Field(
        proto.MESSAGE,
        number=7,
        message=Address,
    )
    user: User = proto.Field(
        proto.MESSAGE,
        number=8,
        message=User,
    )
    merchants: MutableSequence[User] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message=User,
    )
    items: MutableSequence[Item] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message=Item,
    )
    gateway_info: GatewayInfo = proto.Field(
        proto.MESSAGE,
        number=10,
        message=GatewayInfo,
    )


class RiskAnalysis(proto.Message):
    r"""Risk analysis result for an event.

    Attributes:
        score (float):
            Legitimate event score from 0.0 to 1.0.
            (1.0 means very likely legitimate traffic while
            0.0 means very likely non-legitimate traffic).
        reasons (MutableSequence[google.cloud.recaptchaenterprise_v1.types.RiskAnalysis.ClassificationReason]):
            Reasons contributing to the risk analysis
            verdict.
    """

    class ClassificationReason(proto.Enum):
        r"""Reasons contributing to the risk analysis verdict.

        Values:
            CLASSIFICATION_REASON_UNSPECIFIED (0):
                Default unspecified type.
            AUTOMATION (1):
                Interactions matched the behavior of an
                automated agent.
            UNEXPECTED_ENVIRONMENT (2):
                The event originated from an illegitimate
                environment.
            TOO_MUCH_TRAFFIC (3):
                Traffic volume from the event source is
                higher than normal.
            UNEXPECTED_USAGE_PATTERNS (4):
                Interactions with the site were significantly
                different than expected patterns.
            LOW_CONFIDENCE_SCORE (5):
                Too little traffic has been received from
                this site thus far to generate quality risk
                analysis.
            SUSPECTED_CARDING (6):
                The request matches behavioral
                characteristics of a carding attack.
            SUSPECTED_CHARGEBACK (7):
                The request matches behavioral
                characteristics of chargebacks for fraud.
        """
        CLASSIFICATION_REASON_UNSPECIFIED = 0
        AUTOMATION = 1
        UNEXPECTED_ENVIRONMENT = 2
        TOO_MUCH_TRAFFIC = 3
        UNEXPECTED_USAGE_PATTERNS = 4
        LOW_CONFIDENCE_SCORE = 5
        SUSPECTED_CARDING = 6
        SUSPECTED_CHARGEBACK = 7

    score: float = proto.Field(
        proto.FLOAT,
        number=1,
    )
    reasons: MutableSequence[ClassificationReason] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=ClassificationReason,
    )


class TokenProperties(proto.Message):
    r"""Properties of the provided event token.

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
            was generated (Web keys only).
        android_package_name (str):
            The name of the Android package with which
            the token was generated (Android keys only).
        ios_bundle_id (str):
            The ID of the iOS bundle with which the token
            was generated (iOS keys only).
        action (str):
            Action name provided at token generation.
    """

    class InvalidReason(proto.Enum):
        r"""Enum that represents the types of invalid token reasons.

        Values:
            INVALID_REASON_UNSPECIFIED (0):
                Default unspecified type.
            UNKNOWN_INVALID_REASON (1):
                If the failure reason was not accounted for.
            MALFORMED (2):
                The provided user verification token was
                malformed.
            EXPIRED (3):
                The user verification token had expired.
            DUPE (4):
                The user verification had already been seen.
            MISSING (5):
                The user verification token was not present.
            BROWSER_ERROR (6):
                A retriable error (such as network failure)
                occurred on the browser. Could easily be
                simulated by an attacker.
        """
        INVALID_REASON_UNSPECIFIED = 0
        UNKNOWN_INVALID_REASON = 1
        MALFORMED = 2
        EXPIRED = 3
        DUPE = 4
        MISSING = 5
        BROWSER_ERROR = 6

    valid: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    invalid_reason: InvalidReason = proto.Field(
        proto.ENUM,
        number=2,
        enum=InvalidReason,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    hostname: str = proto.Field(
        proto.STRING,
        number=4,
    )
    android_package_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    ios_bundle_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    action: str = proto.Field(
        proto.STRING,
        number=5,
    )


class FraudPreventionAssessment(proto.Message):
    r"""Assessment for Fraud Prevention.

    Attributes:
        transaction_risk (float):
            Probability (0-1) of this transaction being
            fraudulent. Summarizes the combined risk of
            attack vectors below.
        stolen_instrument_verdict (google.cloud.recaptchaenterprise_v1.types.FraudPreventionAssessment.StolenInstrumentVerdict):
            Assessment of this transaction for risk of a
            stolen instrument.
        card_testing_verdict (google.cloud.recaptchaenterprise_v1.types.FraudPreventionAssessment.CardTestingVerdict):
            Assessment of this transaction for risk of
            being part of a card testing attack.
    """

    class StolenInstrumentVerdict(proto.Message):
        r"""Information about stolen instrument fraud, where the user is
        not the legitimate owner of the instrument being used for the
        purchase.

        Attributes:
            risk (float):
                Probability (0-1) of this transaction being
                executed with a stolen instrument.
        """

        risk: float = proto.Field(
            proto.FLOAT,
            number=1,
        )

    class CardTestingVerdict(proto.Message):
        r"""Information about card testing fraud, where an adversary is
        testing fraudulently obtained cards or brute forcing their
        details.

        Attributes:
            risk (float):
                Probability (0-1) of this transaction attempt
                being part of a card testing attack.
        """

        risk: float = proto.Field(
            proto.FLOAT,
            number=1,
        )

    transaction_risk: float = proto.Field(
        proto.FLOAT,
        number=1,
    )
    stolen_instrument_verdict: StolenInstrumentVerdict = proto.Field(
        proto.MESSAGE,
        number=2,
        message=StolenInstrumentVerdict,
    )
    card_testing_verdict: CardTestingVerdict = proto.Field(
        proto.MESSAGE,
        number=3,
        message=CardTestingVerdict,
    )


class AccountDefenderAssessment(proto.Message):
    r"""Account defender risk assessment.

    Attributes:
        labels (MutableSequence[google.cloud.recaptchaenterprise_v1.types.AccountDefenderAssessment.AccountDefenderLabel]):
            Labels for this request.
    """

    class AccountDefenderLabel(proto.Enum):
        r"""Labels returned by account defender for this request.

        Values:
            ACCOUNT_DEFENDER_LABEL_UNSPECIFIED (0):
                Default unspecified type.
            PROFILE_MATCH (1):
                The request matches a known good profile for
                the user.
            SUSPICIOUS_LOGIN_ACTIVITY (2):
                The request is potentially a suspicious login
                event and must be further verified either
                through multi-factor authentication or another
                system.
            SUSPICIOUS_ACCOUNT_CREATION (3):
                The request matched a profile that previously
                had suspicious account creation behavior. This
                can mean that this is a fake account.
            RELATED_ACCOUNTS_NUMBER_HIGH (4):
                The account in the request has a high number
                of related accounts. It does not necessarily
                imply that the account is bad but can require
                further investigation.
        """
        ACCOUNT_DEFENDER_LABEL_UNSPECIFIED = 0
        PROFILE_MATCH = 1
        SUSPICIOUS_LOGIN_ACTIVITY = 2
        SUSPICIOUS_ACCOUNT_CREATION = 3
        RELATED_ACCOUNTS_NUMBER_HIGH = 4

    labels: MutableSequence[AccountDefenderLabel] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=AccountDefenderLabel,
    )


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

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    key: "Key" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Key",
    )


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

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListKeysResponse(proto.Message):
    r"""Response to request to list keys in a project.

    Attributes:
        keys (MutableSequence[google.cloud.recaptchaenterprise_v1.types.Key]):
            Key details.
        next_page_token (str):
            Token to retrieve the next page of results.
            It is set to empty if no keys remain in results.
    """

    @property
    def raw_page(self):
        return self

    keys: MutableSequence["Key"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Key",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class RetrieveLegacySecretKeyRequest(proto.Message):
    r"""The retrieve legacy secret key request message.

    Attributes:
        key (str):
            Required. The public key name linked to the
            requested secret key in the format
            "projects/{project}/keys/{key}".
    """

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetKeyRequest(proto.Message):
    r"""The get key request message.

    Attributes:
        name (str):
            Required. The name of the requested key, in
            the format "projects/{project}/keys/{key}".
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


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

    key: "Key" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Key",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteKeyRequest(proto.Message):
    r"""The delete key request message.

    Attributes:
        name (str):
            Required. The name of the key to be deleted,
            in the format "projects/{project}/keys/{key}".
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class MigrateKeyRequest(proto.Message):
    r"""The migrate key request message.

    Attributes:
        name (str):
            Required. The name of the key to be migrated,
            in the format "projects/{project}/keys/{key}".
        skip_billing_check (bool):
            Optional. If true, skips the billing check. A reCAPTCHA
            Enterprise key or migrated key behaves differently than a
            reCAPTCHA (non-Enterprise version) key when you reach a
            quota limit (see
            https://cloud.google.com/recaptcha-enterprise/quotas#quota_limit).
            To avoid any disruption of your usage, we check that a
            billing account is present. If your usage of reCAPTCHA is
            under the free quota, you can safely skip the billing check
            and proceed with the migration. See
            https://cloud.google.com/recaptcha-enterprise/docs/billing-information.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    skip_billing_check: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class GetMetricsRequest(proto.Message):
    r"""The get metrics request message.

    Attributes:
        name (str):
            Required. The name of the requested metrics,
            in the format
            "projects/{project}/keys/{key}/metrics".
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Metrics(proto.Message):
    r"""Metrics for a single Key.

    Attributes:
        name (str):
            Output only. The name of the metrics, in the
            format "projects/{project}/keys/{key}/metrics".
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Inclusive start time aligned to a day (UTC).
        score_metrics (MutableSequence[google.cloud.recaptchaenterprise_v1.types.ScoreMetrics]):
            Metrics will be continuous and in order by
            dates, and in the granularity of day. All Key
            types should have score-based data.
        challenge_metrics (MutableSequence[google.cloud.recaptchaenterprise_v1.types.ChallengeMetrics]):
            Metrics will be continuous and in order by
            dates, and in the granularity of day. Only
            challenge-based keys (CHECKBOX, INVISIBLE), will
            have challenge-based data.
    """

    name: str = proto.Field(
        proto.STRING,
        number=4,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    score_metrics: MutableSequence["ScoreMetrics"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="ScoreMetrics",
    )
    challenge_metrics: MutableSequence["ChallengeMetrics"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="ChallengeMetrics",
    )


class RetrieveLegacySecretKeyResponse(proto.Message):
    r"""Secret key is used only in legacy reCAPTCHA. It must be used
    in a 3rd party integration with legacy reCAPTCHA.

    Attributes:
        legacy_secret_key (str):
            The secret key (also known as shared secret)
            authorizes communication between your
            application backend and the reCAPTCHA Enterprise
            server to create an assessment.
            The secret key needs to be kept safe for
            security purposes.
    """

    legacy_secret_key: str = proto.Field(
        proto.STRING,
        number=1,
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
        labels (MutableMapping[str, str]):
            See <a
            href="https://cloud.google.com/recaptcha-enterprise/docs/labels">
            Creating and managing labels</a>.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp corresponding to
            the creation of this Key.
        testing_options (google.cloud.recaptchaenterprise_v1.types.TestingOptions):
            Options for user acceptance testing.
        waf_settings (google.cloud.recaptchaenterprise_v1.types.WafSettings):
            Settings for WAF
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    web_settings: "WebKeySettings" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="platform_settings",
        message="WebKeySettings",
    )
    android_settings: "AndroidKeySettings" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="platform_settings",
        message="AndroidKeySettings",
    )
    ios_settings: "IOSKeySettings" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="platform_settings",
        message="IOSKeySettings",
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    testing_options: "TestingOptions" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="TestingOptions",
    )
    waf_settings: "WafSettings" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="WafSettings",
    )


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

        Values:
            TESTING_CHALLENGE_UNSPECIFIED (0):
                Perform the normal risk analysis and return
                either nocaptcha or a challenge depending on
                risk and trust factors.
            NOCAPTCHA (1):
                Challenge requests for this key always return
                a nocaptcha, which does not require a solution.
            UNSOLVABLE_CHALLENGE (2):
                Challenge requests for this key always return
                an unsolvable challenge.
        """
        TESTING_CHALLENGE_UNSPECIFIED = 0
        NOCAPTCHA = 1
        UNSOLVABLE_CHALLENGE = 2

    testing_score: float = proto.Field(
        proto.FLOAT,
        number=1,
    )
    testing_challenge: TestingChallenge = proto.Field(
        proto.ENUM,
        number=2,
        enum=TestingChallenge,
    )


class WebKeySettings(proto.Message):
    r"""Settings specific to keys that can be used by websites.

    Attributes:
        allow_all_domains (bool):
            If set to true, it means allowed_domains will not be
            enforced.
        allowed_domains (MutableSequence[str]):
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
        r"""Enum that represents the integration types for web keys.

        Values:
            INTEGRATION_TYPE_UNSPECIFIED (0):
                Default type that indicates this enum hasn't
                been specified. This is not a valid
                IntegrationType, one of the other types must be
                specified instead.
            SCORE (1):
                Only used to produce scores. It doesn't
                display the "I'm not a robot" checkbox and never
                shows captcha challenges.
            CHECKBOX (2):
                Displays the "I'm not a robot" checkbox and
                may show captcha challenges after it is checked.
            INVISIBLE (3):
                Doesn't display the "I'm not a robot"
                checkbox, but may show captcha challenges after
                risk analysis.
        """
        INTEGRATION_TYPE_UNSPECIFIED = 0
        SCORE = 1
        CHECKBOX = 2
        INVISIBLE = 3

    class ChallengeSecurityPreference(proto.Enum):
        r"""Enum that represents the possible challenge frequency and
        difficulty configurations for a web key.

        Values:
            CHALLENGE_SECURITY_PREFERENCE_UNSPECIFIED (0):
                Default type that indicates this enum hasn't
                been specified.
            USABILITY (1):
                Key tends to show fewer and easier
                challenges.
            BALANCE (2):
                Key tends to show balanced (in amount and
                difficulty) challenges.
            SECURITY (3):
                Key tends to show more and harder challenges.
        """
        CHALLENGE_SECURITY_PREFERENCE_UNSPECIFIED = 0
        USABILITY = 1
        BALANCE = 2
        SECURITY = 3

    allow_all_domains: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    allowed_domains: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    allow_amp_traffic: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    integration_type: IntegrationType = proto.Field(
        proto.ENUM,
        number=4,
        enum=IntegrationType,
    )
    challenge_security_preference: ChallengeSecurityPreference = proto.Field(
        proto.ENUM,
        number=5,
        enum=ChallengeSecurityPreference,
    )


class AndroidKeySettings(proto.Message):
    r"""Settings specific to keys that can be used by Android apps.

    Attributes:
        allow_all_package_names (bool):
            If set to true, allowed_package_names are not enforced.
        allowed_package_names (MutableSequence[str]):
            Android package names of apps allowed to use
            the key. Example: 'com.companyname.appname'
    """

    allow_all_package_names: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    allowed_package_names: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class IOSKeySettings(proto.Message):
    r"""Settings specific to keys that can be used by iOS apps.

    Attributes:
        allow_all_bundle_ids (bool):
            If set to true, allowed_bundle_ids are not enforced.
        allowed_bundle_ids (MutableSequence[str]):
            iOS bundle ids of apps allowed to use the
            key. Example:
            'com.companyname.productname.appname'
    """

    allow_all_bundle_ids: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    allowed_bundle_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class ScoreDistribution(proto.Message):
    r"""Score distribution.

    Attributes:
        score_buckets (MutableMapping[int, int]):
            Map key is score value multiplied by 100. The scores are
            discrete values between [0, 1]. The maximum number of
            buckets is on order of a few dozen, but typically much lower
            (ie. 10).
    """

    score_buckets: MutableMapping[int, int] = proto.MapField(
        proto.INT32,
        proto.INT64,
        number=1,
    )


class ScoreMetrics(proto.Message):
    r"""Metrics related to scoring.

    Attributes:
        overall_metrics (google.cloud.recaptchaenterprise_v1.types.ScoreDistribution):
            Aggregated score metrics for all traffic.
        action_metrics (MutableMapping[str, google.cloud.recaptchaenterprise_v1.types.ScoreDistribution]):
            Action-based metrics. The map key is the
            action name which specified by the site owners
            at time of the "execute" client-side call.
    """

    overall_metrics: "ScoreDistribution" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ScoreDistribution",
    )
    action_metrics: MutableMapping[str, "ScoreDistribution"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=2,
        message="ScoreDistribution",
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

    pageload_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    nocaptcha_count: int = proto.Field(
        proto.INT64,
        number=2,
    )
    failed_count: int = proto.Field(
        proto.INT64,
        number=3,
    )
    passed_count: int = proto.Field(
        proto.INT64,
        number=4,
    )


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
            return. The service might return fewer than this
            value. If unspecified, at most 50 accounts are
            returned. The maximum value is 1000; values
            above 1000 are coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListRelatedAccountGroupMemberships`` call.

            When paginating, all other parameters provided to
            ``ListRelatedAccountGroupMemberships`` must match the call
            that provided the page token.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListRelatedAccountGroupMembershipsResponse(proto.Message):
    r"""The response to a ``ListRelatedAccountGroupMemberships`` call.

    Attributes:
        related_account_group_memberships (MutableSequence[google.cloud.recaptchaenterprise_v1.types.RelatedAccountGroupMembership]):
            The memberships listed by the query.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    related_account_group_memberships: MutableSequence[
        "RelatedAccountGroupMembership"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RelatedAccountGroupMembership",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListRelatedAccountGroupsRequest(proto.Message):
    r"""The request message to list related account groups.

    Attributes:
        parent (str):
            Required. The name of the project to list
            related account groups from, in the format
            "projects/{project}".
        page_size (int):
            Optional. The maximum number of groups to
            return. The service might return fewer than this
            value. If unspecified, at most 50 groups are
            returned. The maximum value is 1000; values
            above 1000 are coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListRelatedAccountGroups`` call. Provide this to retrieve
            the subsequent page.

            When paginating, all other parameters provided to
            ``ListRelatedAccountGroups`` must match the call that
            provided the page token.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListRelatedAccountGroupsResponse(proto.Message):
    r"""The response to a ``ListRelatedAccountGroups`` call.

    Attributes:
        related_account_groups (MutableSequence[google.cloud.recaptchaenterprise_v1.types.RelatedAccountGroup]):
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

    related_account_groups: MutableSequence[
        "RelatedAccountGroup"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RelatedAccountGroup",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class SearchRelatedAccountGroupMembershipsRequest(proto.Message):
    r"""The request message to search related account group
    memberships.

    Attributes:
        project (str):
            Required. The name of the project to search
            related account group memberships from. Specify
            the project name in the following format:

            "projects/{project}".
        hashed_account_id (bytes):
            Optional. The unique stable hashed user identifier we should
            search connections to. The identifier should correspond to a
            ``hashed_account_id`` provided in a previous
            ``CreateAssessment`` or ``AnnotateAssessment`` call.
        page_size (int):
            Optional. The maximum number of groups to
            return. The service might return fewer than this
            value. If unspecified, at most 50 groups are
            returned. The maximum value is 1000; values
            above 1000 are coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``SearchRelatedAccountGroupMemberships`` call. Provide this
            to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``SearchRelatedAccountGroupMemberships`` must match the call
            that provided the page token.
    """

    project: str = proto.Field(
        proto.STRING,
        number=1,
    )
    hashed_account_id: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )


class SearchRelatedAccountGroupMembershipsResponse(proto.Message):
    r"""The response to a ``SearchRelatedAccountGroupMemberships`` call.

    Attributes:
        related_account_group_memberships (MutableSequence[google.cloud.recaptchaenterprise_v1.types.RelatedAccountGroupMembership]):
            The queried memberships.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    related_account_group_memberships: MutableSequence[
        "RelatedAccountGroupMembership"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RelatedAccountGroupMembership",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


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
            in a previous ``CreateAssessment`` or ``AnnotateAssessment``
            call.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    hashed_account_id: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )


class RelatedAccountGroup(proto.Message):
    r"""A group of related accounts.

    Attributes:
        name (str):
            Required. The resource name for the related account group in
            the format
            ``projects/{project}/relatedaccountgroups/{related_account_group}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class WafSettings(proto.Message):
    r"""Settings specific to keys that can be used for WAF (Web
    Application Firewall).

    Attributes:
        waf_service (google.cloud.recaptchaenterprise_v1.types.WafSettings.WafService):
            Required. The WAF service that uses this key.
        waf_feature (google.cloud.recaptchaenterprise_v1.types.WafSettings.WafFeature):
            Required. The WAF feature for which this key
            is enabled.
    """

    class WafFeature(proto.Enum):
        r"""Supported WAF features. For more information, see
        https://cloud.google.com/recaptcha-enterprise/docs/usecase#comparison_of_features.

        Values:
            WAF_FEATURE_UNSPECIFIED (0):
                Undefined feature.
            CHALLENGE_PAGE (1):
                Redirects suspicious traffic to reCAPTCHA.
            SESSION_TOKEN (2):
                Use reCAPTCHA session-tokens to protect the
                whole user session on the site's domain.
            ACTION_TOKEN (3):
                Use reCAPTCHA action-tokens to protect user
                actions.
        """
        WAF_FEATURE_UNSPECIFIED = 0
        CHALLENGE_PAGE = 1
        SESSION_TOKEN = 2
        ACTION_TOKEN = 3

    class WafService(proto.Enum):
        r"""Web Application Firewalls supported by reCAPTCHA Enterprise.

        Values:
            WAF_SERVICE_UNSPECIFIED (0):
                Undefined WAF
            CA (1):
                Cloud Armor
        """
        WAF_SERVICE_UNSPECIFIED = 0
        CA = 1

    waf_service: WafService = proto.Field(
        proto.ENUM,
        number=1,
        enum=WafService,
    )
    waf_feature: WafFeature = proto.Field(
        proto.ENUM,
        number=2,
        enum=WafFeature,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
