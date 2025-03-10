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
from google.shopping.merchant_notifications_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.notifications_api_service import NotificationsApiServiceClient
from .services.notifications_api_service import NotificationsApiServiceAsyncClient

from .types.notificationsapi import CreateNotificationSubscriptionRequest
from .types.notificationsapi import DeleteNotificationSubscriptionRequest
from .types.notificationsapi import GetNotificationSubscriptionRequest
from .types.notificationsapi import ListNotificationSubscriptionsRequest
from .types.notificationsapi import ListNotificationSubscriptionsResponse
from .types.notificationsapi import NotificationSubscription
from .types.notificationsapi import ProductChange
from .types.notificationsapi import ProductStatusChangeMessage
from .types.notificationsapi import UpdateNotificationSubscriptionRequest
from .types.notificationsapi import Attribute
from .types.notificationsapi import Resource

__all__ = (
    'NotificationsApiServiceAsyncClient',
'Attribute',
'CreateNotificationSubscriptionRequest',
'DeleteNotificationSubscriptionRequest',
'GetNotificationSubscriptionRequest',
'ListNotificationSubscriptionsRequest',
'ListNotificationSubscriptionsResponse',
'NotificationSubscription',
'NotificationsApiServiceClient',
'ProductChange',
'ProductStatusChangeMessage',
'Resource',
'UpdateNotificationSubscriptionRequest',
)
