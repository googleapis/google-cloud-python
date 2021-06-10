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
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore


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
            Required. The organization address for the
            customer. To enforce US laws and embargoes, we
            require a region and zip code. You must provide
            valid addresses for every customer. To set the
            customer's language, use the Customer-level
            language code.
        primary_contact_info (google.cloud.channel_v1.types.ContactInfo):
            Primary contact info.
        alternate_email (str):
            Secondary contact email. You need to provide
            an alternate email to create different domains
            if a primary contact email already exists. Users
            will receive a notification with credentials
            when you create an admin.google.com account.
            Secondary emails are also recovery email
            addresses.
        domain (str):
            Required. The customer's primary domain. Must
            match the primary contact email's domain.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the customer was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the customer was
            updated.
        cloud_identity_id (str):
            Output only. The customer's Cloud Identity ID
            if the customer has a Cloud Identity resource.
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

    name = proto.Field(proto.STRING, number=1,)
    org_display_name = proto.Field(proto.STRING, number=2,)
    org_postal_address = proto.Field(
        proto.MESSAGE, number=3, message=postal_address_pb2.PostalAddress,
    )
    primary_contact_info = proto.Field(proto.MESSAGE, number=4, message="ContactInfo",)
    alternate_email = proto.Field(proto.STRING, number=5,)
    domain = proto.Field(proto.STRING, number=6,)
    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,)
    cloud_identity_id = proto.Field(proto.STRING, number=9,)
    language_code = proto.Field(proto.STRING, number=10,)
    cloud_identity_info = proto.Field(
        proto.MESSAGE, number=12, message=common.CloudIdentityInfo,
    )
    channel_partner_id = proto.Field(proto.STRING, number=13,)


class ContactInfo(proto.Message):
    r"""Contact information for a customer account.
    Attributes:
        first_name (str):
            The customer account contact's first name.
        last_name (str):
            The customer account contact's last name.
        display_name (str):
            Output only. The customer account contact's
            display name, formatted as a combination of the
            customer's first and last name.
        email (str):
            The customer account's contact email.
            Required for entitlements that create
            admin.google.com accounts, and serves as the
            customer's username for those accounts.
        title (str):
            Optional. The customer account contact's job
            title.
        phone (str):
            The customer account's contact phone number.
    """

    first_name = proto.Field(proto.STRING, number=1,)
    last_name = proto.Field(proto.STRING, number=2,)
    display_name = proto.Field(proto.STRING, number=4,)
    email = proto.Field(proto.STRING, number=5,)
    title = proto.Field(proto.STRING, number=6,)
    phone = proto.Field(proto.STRING, number=7,)


__all__ = tuple(sorted(__protobuf__.manifest))
