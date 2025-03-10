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
from google.apps.events_subscriptions_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.subscriptions_service import SubscriptionsServiceClient
from .services.subscriptions_service import SubscriptionsServiceAsyncClient

from .types.subscription_resource import NotificationEndpoint
from .types.subscription_resource import PayloadOptions
from .types.subscription_resource import Subscription
from .types.subscriptions_service import CreateSubscriptionMetadata
from .types.subscriptions_service import CreateSubscriptionRequest
from .types.subscriptions_service import DeleteSubscriptionMetadata
from .types.subscriptions_service import DeleteSubscriptionRequest
from .types.subscriptions_service import GetSubscriptionRequest
from .types.subscriptions_service import ListSubscriptionsRequest
from .types.subscriptions_service import ListSubscriptionsResponse
from .types.subscriptions_service import ReactivateSubscriptionMetadata
from .types.subscriptions_service import ReactivateSubscriptionRequest
from .types.subscriptions_service import UpdateSubscriptionMetadata
from .types.subscriptions_service import UpdateSubscriptionRequest

__all__ = (
    'SubscriptionsServiceAsyncClient',
'CreateSubscriptionMetadata',
'CreateSubscriptionRequest',
'DeleteSubscriptionMetadata',
'DeleteSubscriptionRequest',
'GetSubscriptionRequest',
'ListSubscriptionsRequest',
'ListSubscriptionsResponse',
'NotificationEndpoint',
'PayloadOptions',
'ReactivateSubscriptionMetadata',
'ReactivateSubscriptionRequest',
'Subscription',
'SubscriptionsServiceClient',
'UpdateSubscriptionMetadata',
'UpdateSubscriptionRequest',
)
