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


from google.cloud.channel_v1.types import common
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.type import postal_address_pb2 as postal_address  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.channel.v1", manifest={"Customer", "ContactInfo",},
)


class Customer(proto.Message):
    r"""Entity representing a customer of a reseller or distributor.

    Attributes:
        name (str):
            Output only. Resource name of the customer. Format:
            accounts/{account_id}/customers/{customer_id}
        org_display_name (str):
            Required. Name of the organization that the
            customer entity represents.
        org_postal_address (google.type.postal_address_pb2.PostalAddress):
            Required. Address of the organization of the
            customer entity. Region and zip codes are
            required to enforce US laws and embargoes.
            Language code is discarded. Use the Customer-
            level language code to set the customer's
            language.
        primary_contact_info (google.cloud.channel_v1.types.ContactInfo):
            Primary contact info.
        alternate_email (str):
            Secondary contact email.
            Alternate email and primary contact email are
            required to have different domains if primary
            contact email is present.
            When creating admin.google.com accounts, users
            get notified credentials at this email. This
            email address is also used as a recovery email.
        domain (str):
            Required. Primary domain used by the
            customer. Domain of primary contact email is
            required to be same as the provided domain.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the customer
            is created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the customer
            is updated.
        cloud_identity_id (str):
            Output only. Customer's cloud_identity_id. Populated only if
            a Cloud Identity resource exists for this customer.
        language_code (str):
            Optional. The BCP-47 language code, such as "en-US" or
            "sr-Latn". For more information, see
            https://www.unicode.org/reports/tr35/#Unicode_locale_identifier.
        cloud_identity_info (google.cloud.channel_v1.types.CloudIdentityInfo):
            Output only. Cloud Identity information for
            the customer. Populated only if a Cloud Identity
            account exists for this customer.
        channel_partner_id (str):
            Cloud Identity ID of the customer's channel
            partner. Populated only if a channel partner
            exists for this customer.
    """

    name = proto.Field(proto.STRING, number=1)

    org_display_name = proto.Field(proto.STRING, number=2)

    org_postal_address = proto.Field(
        proto.MESSAGE, number=3, message=postal_address.PostalAddress,
    )

    primary_contact_info = proto.Field(proto.MESSAGE, number=4, message="ContactInfo",)

    alternate_email = proto.Field(proto.STRING, number=5)

    domain = proto.Field(proto.STRING, number=6)

    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=8, message=timestamp.Timestamp,)

    cloud_identity_id = proto.Field(proto.STRING, number=9)

    language_code = proto.Field(proto.STRING, number=10)

    cloud_identity_info = proto.Field(
        proto.MESSAGE, number=12, message=common.CloudIdentityInfo,
    )

    channel_partner_id = proto.Field(proto.STRING, number=13)


class ContactInfo(proto.Message):
    r"""Contact information for a customer account.

    Attributes:
        first_name (str):
            First name of the contact in the customer
            account.
        last_name (str):
            Last name of the contact in the customer
            account.
        display_name (str):
            Output only. Display name of the contact in
            the customer account. Populated by combining
            customer first name and last name.
        email (str):
            Email of the contact in the customer account.
            Email is required for entitlements that need
            creation of admin.google.com accounts. The email
            will be the username used in credentials to
            access the admin.google.com account.
        title (str):
            Optional. Job title of the contact in the
            customer account.
        phone (str):
            Phone number of the contact in the customer
            account.
    """

    first_name = proto.Field(proto.STRING, number=1)

    last_name = proto.Field(proto.STRING, number=2)

    display_name = proto.Field(proto.STRING, number=4)

    email = proto.Field(proto.STRING, number=5)

    title = proto.Field(proto.STRING, number=6)

    phone = proto.Field(proto.STRING, number=7)


__all__ = tuple(sorted(__protobuf__.manifest))
