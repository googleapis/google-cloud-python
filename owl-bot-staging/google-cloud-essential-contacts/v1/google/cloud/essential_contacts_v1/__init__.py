# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from google.cloud.essential_contacts_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.essential_contacts_service import EssentialContactsServiceClient
from .services.essential_contacts_service import EssentialContactsServiceAsyncClient

from .types.enums import NotificationCategory
from .types.enums import ValidationState
from .types.service import ComputeContactsRequest
from .types.service import ComputeContactsResponse
from .types.service import Contact
from .types.service import CreateContactRequest
from .types.service import DeleteContactRequest
from .types.service import GetContactRequest
from .types.service import ListContactsRequest
from .types.service import ListContactsResponse
from .types.service import SendTestMessageRequest
from .types.service import UpdateContactRequest

__all__ = (
    'EssentialContactsServiceAsyncClient',
'ComputeContactsRequest',
'ComputeContactsResponse',
'Contact',
'CreateContactRequest',
'DeleteContactRequest',
'EssentialContactsServiceClient',
'GetContactRequest',
'ListContactsRequest',
'ListContactsResponse',
'NotificationCategory',
'SendTestMessageRequest',
'UpdateContactRequest',
'ValidationState',
)
