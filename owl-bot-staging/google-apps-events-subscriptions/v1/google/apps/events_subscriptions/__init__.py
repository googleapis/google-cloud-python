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
from google.apps.events_subscriptions import gapic_version as package_version

__version__ = package_version.__version__


from google.apps.events_subscriptions_v1.services.subscriptions_service.client import SubscriptionsServiceClient
from google.apps.events_subscriptions_v1.services.subscriptions_service.async_client import SubscriptionsServiceAsyncClient

from google.apps.events_subscriptions_v1.types.subscription_resource import NotificationEndpoint
from google.apps.events_subscriptions_v1.types.subscription_resource import PayloadOptions
from google.apps.events_subscriptions_v1.types.subscription_resource import Subscription
from google.apps.events_subscriptions_v1.types.subscriptions_service import CreateSubscriptionMetadata
from google.apps.events_subscriptions_v1.types.subscriptions_service import CreateSubscriptionRequest
from google.apps.events_subscriptions_v1.types.subscriptions_service import DeleteSubscriptionMetadata
from google.apps.events_subscriptions_v1.types.subscriptions_service import DeleteSubscriptionRequest
from google.apps.events_subscriptions_v1.types.subscriptions_service import GetSubscriptionRequest
from google.apps.events_subscriptions_v1.types.subscriptions_service import ListSubscriptionsRequest
from google.apps.events_subscriptions_v1.types.subscriptions_service import ListSubscriptionsResponse
from google.apps.events_subscriptions_v1.types.subscriptions_service import ReactivateSubscriptionMetadata
from google.apps.events_subscriptions_v1.types.subscriptions_service import ReactivateSubscriptionRequest
from google.apps.events_subscriptions_v1.types.subscriptions_service import UpdateSubscriptionMetadata
from google.apps.events_subscriptions_v1.types.subscriptions_service import UpdateSubscriptionRequest

__all__ = ('SubscriptionsServiceClient',
    'SubscriptionsServiceAsyncClient',
    'NotificationEndpoint',
    'PayloadOptions',
    'Subscription',
    'CreateSubscriptionMetadata',
    'CreateSubscriptionRequest',
    'DeleteSubscriptionMetadata',
    'DeleteSubscriptionRequest',
    'GetSubscriptionRequest',
    'ListSubscriptionsRequest',
    'ListSubscriptionsResponse',
    'ReactivateSubscriptionMetadata',
    'ReactivateSubscriptionRequest',
    'UpdateSubscriptionMetadata',
    'UpdateSubscriptionRequest',
)
