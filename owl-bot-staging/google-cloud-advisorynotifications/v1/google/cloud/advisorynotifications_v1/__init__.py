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
from google.cloud.advisorynotifications_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.advisory_notifications_service import AdvisoryNotificationsServiceClient
from .services.advisory_notifications_service import AdvisoryNotificationsServiceAsyncClient

from .types.service import Attachment
from .types.service import Csv
from .types.service import GetNotificationRequest
from .types.service import GetSettingsRequest
from .types.service import ListNotificationsRequest
from .types.service import ListNotificationsResponse
from .types.service import Message
from .types.service import Notification
from .types.service import NotificationSettings
from .types.service import Settings
from .types.service import Subject
from .types.service import Text
from .types.service import UpdateSettingsRequest
from .types.service import LocalizationState
from .types.service import NotificationType
from .types.service import NotificationView

__all__ = (
    'AdvisoryNotificationsServiceAsyncClient',
'AdvisoryNotificationsServiceClient',
'Attachment',
'Csv',
'GetNotificationRequest',
'GetSettingsRequest',
'ListNotificationsRequest',
'ListNotificationsResponse',
'LocalizationState',
'Message',
'Notification',
'NotificationSettings',
'NotificationType',
'NotificationView',
'Settings',
'Subject',
'Text',
'UpdateSettingsRequest',
)
