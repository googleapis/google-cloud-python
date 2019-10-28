# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import
import sys

from google.api_core.protobuf_helpers import get_messages

from google.cloud.talent_v4beta1.proto import application_pb2
from google.cloud.talent_v4beta1.proto import application_service_pb2
from google.cloud.talent_v4beta1.proto import common_pb2
from google.cloud.talent_v4beta1.proto import company_pb2
from google.cloud.talent_v4beta1.proto import company_service_pb2
from google.cloud.talent_v4beta1.proto import completion_service_pb2
from google.cloud.talent_v4beta1.proto import event_pb2
from google.cloud.talent_v4beta1.proto import event_service_pb2
from google.cloud.talent_v4beta1.proto import filters_pb2
from google.cloud.talent_v4beta1.proto import histogram_pb2
from google.cloud.talent_v4beta1.proto import job_pb2
from google.cloud.talent_v4beta1.proto import job_service_pb2
from google.cloud.talent_v4beta1.proto import profile_pb2
from google.cloud.talent_v4beta1.proto import profile_service_pb2
from google.cloud.talent_v4beta1.proto import tenant_pb2
from google.cloud.talent_v4beta1.proto import tenant_service_pb2
from google.longrunning import operations_pb2
from google.protobuf import any_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2
from google.protobuf import wrappers_pb2
from google.rpc import status_pb2
from google.type import date_pb2
from google.type import latlng_pb2
from google.type import money_pb2
from google.type import postal_address_pb2
from google.type import timeofday_pb2


_shared_modules = [
    operations_pb2,
    any_pb2,
    duration_pb2,
    empty_pb2,
    field_mask_pb2,
    timestamp_pb2,
    wrappers_pb2,
    status_pb2,
    date_pb2,
    latlng_pb2,
    money_pb2,
    postal_address_pb2,
    timeofday_pb2,
]

_local_modules = [
    application_pb2,
    application_service_pb2,
    common_pb2,
    company_pb2,
    company_service_pb2,
    completion_service_pb2,
    event_pb2,
    event_service_pb2,
    filters_pb2,
    histogram_pb2,
    job_pb2,
    job_service_pb2,
    profile_pb2,
    profile_service_pb2,
    tenant_pb2,
    tenant_service_pb2,
]

names = []

for module in _shared_modules:  # pragma: NO COVER
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)
for module in _local_modules:
    for name, message in get_messages(module).items():
        message.__module__ = "google.cloud.talent_v4beta1.types"
        setattr(sys.modules[__name__], name, message)
        names.append(name)


__all__ = tuple(sorted(names))
