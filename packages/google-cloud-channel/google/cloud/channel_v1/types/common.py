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

from google.protobuf import any_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.channel.v1",
    manifest={"EduData", "CloudIdentityInfo", "Value", "AdminUser",},
)


class EduData(proto.Message):
    r"""Required Edu Attributes
    Attributes:
        institute_type (google.cloud.channel_v1.types.EduData.InstituteType):
            Designated institute type of customer.
        institute_size (google.cloud.channel_v1.types.EduData.InstituteSize):
            Size of the institute.
        website (str):
            Web address for the edu customer's
            institution.
    """

    class InstituteType(proto.Enum):
        r"""Enum to specify the institute type."""
        INSTITUTE_TYPE_UNSPECIFIED = 0
        K12 = 1
        UNIVERSITY = 2

    class InstituteSize(proto.Enum):
        r"""Number of students and staff the institute has."""
        INSTITUTE_SIZE_UNSPECIFIED = 0
        SIZE_1_100 = 1
        SIZE_101_500 = 2
        SIZE_501_1000 = 3
        SIZE_1001_2000 = 4
        SIZE_2001_5000 = 5
        SIZE_5001_10000 = 6
        SIZE_10001_OR_MORE = 7

    institute_type = proto.Field(proto.ENUM, number=1, enum=InstituteType,)
    institute_size = proto.Field(proto.ENUM, number=2, enum=InstituteSize,)
    website = proto.Field(proto.STRING, number=3,)


class CloudIdentityInfo(proto.Message):
    r"""Cloud Identity information for the Cloud Channel Customer.
    Attributes:
        customer_type (google.cloud.channel_v1.types.CloudIdentityInfo.CustomerType):
            CustomerType indicates verification type
            needed for using services.
        primary_domain (str):
            Output only. The primary domain name.
        is_domain_verified (bool):
            Output only. Whether the domain is verified. This field is
            not returned for a Customer's cloud_identity_info resource.
            Partners can use the domains.get() method of the Workspace
            SDK's Directory API, or listen to the
            PRIMARY_DOMAIN_VERIFIED Pub/Sub event in to track domain
            verification of their resolve Workspace customers.
        alternate_email (str):
            The alternate email.
        phone_number (str):
            Phone number associated with the Cloud
            Identity.
        language_code (str):
            Language code.
        admin_console_uri (str):
            Output only. URI of Customer's Admin console
            dashboard.
        edu_data (google.cloud.channel_v1.types.EduData):
            Edu information about the customer.
    """

    class CustomerType(proto.Enum):
        r"""CustomerType of the customer"""
        CUSTOMER_TYPE_UNSPECIFIED = 0
        DOMAIN = 1
        TEAM = 2

    customer_type = proto.Field(proto.ENUM, number=1, enum=CustomerType,)
    primary_domain = proto.Field(proto.STRING, number=9,)
    is_domain_verified = proto.Field(proto.BOOL, number=4,)
    alternate_email = proto.Field(proto.STRING, number=6,)
    phone_number = proto.Field(proto.STRING, number=7,)
    language_code = proto.Field(proto.STRING, number=8,)
    admin_console_uri = proto.Field(proto.STRING, number=10,)
    edu_data = proto.Field(proto.MESSAGE, number=22, message="EduData",)


class Value(proto.Message):
    r"""Data type and value of a parameter.
    Attributes:
        int64_value (int):
            Represents an int64 value.
        string_value (str):
            Represents a string value.
        double_value (float):
            Represents a double value.
        proto_value (google.protobuf.any_pb2.Any):
            Represents an 'Any' proto value.
        bool_value (bool):
            Represents a boolean value.
    """

    int64_value = proto.Field(proto.INT64, number=1, oneof="kind",)
    string_value = proto.Field(proto.STRING, number=2, oneof="kind",)
    double_value = proto.Field(proto.DOUBLE, number=3, oneof="kind",)
    proto_value = proto.Field(
        proto.MESSAGE, number=4, oneof="kind", message=any_pb2.Any,
    )
    bool_value = proto.Field(proto.BOOL, number=5, oneof="kind",)


class AdminUser(proto.Message):
    r"""Information needed to create an Admin User for Google
    Workspace.

    Attributes:
        email (str):
            Primary email of the admin user.
        given_name (str):
            Given name of the admin user.
        family_name (str):
            Family name of the admin user.
    """

    email = proto.Field(proto.STRING, number=1,)
    given_name = proto.Field(proto.STRING, number=2,)
    family_name = proto.Field(proto.STRING, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
