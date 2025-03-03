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
from google.cloud.advisorynotifications import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.advisorynotifications_v1.services.advisory_notifications_service.client import AdvisoryNotificationsServiceClient
from google.cloud.advisorynotifications_v1.services.advisory_notifications_service.async_client import AdvisoryNotificationsServiceAsyncClient

from google.cloud.advisorynotifications_v1.types.service import Attachment
from google.cloud.advisorynotifications_v1.types.service import Csv
from google.cloud.advisorynotifications_v1.types.service import GetNotificationRequest
from google.cloud.advisorynotifications_v1.types.service import GetSettingsRequest
from google.cloud.advisorynotifications_v1.types.service import ListNotificationsRequest
from google.cloud.advisorynotifications_v1.types.service import ListNotificationsResponse
from google.cloud.advisorynotifications_v1.types.service import Message
from google.cloud.advisorynotifications_v1.types.service import Notification
from google.cloud.advisorynotifications_v1.types.service import NotificationSettings
from google.cloud.advisorynotifications_v1.types.service import Settings
from google.cloud.advisorynotifications_v1.types.service import Subject
from google.cloud.advisorynotifications_v1.types.service import Text
from google.cloud.advisorynotifications_v1.types.service import UpdateSettingsRequest
from google.cloud.advisorynotifications_v1.types.service import LocalizationState
from google.cloud.advisorynotifications_v1.types.service import NotificationType
from google.cloud.advisorynotifications_v1.types.service import NotificationView

__all__ = ('AdvisoryNotificationsServiceClient',
    'AdvisoryNotificationsServiceAsyncClient',
    'Attachment',
    'Csv',
    'GetNotificationRequest',
    'GetSettingsRequest',
    'ListNotificationsRequest',
    'ListNotificationsResponse',
    'Message',
    'Notification',
    'NotificationSettings',
    'Settings',
    'Subject',
    'Text',
    'UpdateSettingsRequest',
    'LocalizationState',
    'NotificationType',
    'NotificationView',
)
