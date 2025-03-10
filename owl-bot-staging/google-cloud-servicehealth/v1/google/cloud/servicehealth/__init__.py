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
from google.cloud.servicehealth import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.servicehealth_v1.services.service_health.client import ServiceHealthClient
from google.cloud.servicehealth_v1.services.service_health.async_client import ServiceHealthAsyncClient

from google.cloud.servicehealth_v1.types.event_resources import Asset
from google.cloud.servicehealth_v1.types.event_resources import Event
from google.cloud.servicehealth_v1.types.event_resources import EventImpact
from google.cloud.servicehealth_v1.types.event_resources import EventUpdate
from google.cloud.servicehealth_v1.types.event_resources import GetEventRequest
from google.cloud.servicehealth_v1.types.event_resources import GetOrganizationEventRequest
from google.cloud.servicehealth_v1.types.event_resources import GetOrganizationImpactRequest
from google.cloud.servicehealth_v1.types.event_resources import ListEventsRequest
from google.cloud.servicehealth_v1.types.event_resources import ListEventsResponse
from google.cloud.servicehealth_v1.types.event_resources import ListOrganizationEventsRequest
from google.cloud.servicehealth_v1.types.event_resources import ListOrganizationEventsResponse
from google.cloud.servicehealth_v1.types.event_resources import ListOrganizationImpactsRequest
from google.cloud.servicehealth_v1.types.event_resources import ListOrganizationImpactsResponse
from google.cloud.servicehealth_v1.types.event_resources import Location
from google.cloud.servicehealth_v1.types.event_resources import OrganizationEvent
from google.cloud.servicehealth_v1.types.event_resources import OrganizationImpact
from google.cloud.servicehealth_v1.types.event_resources import Product
from google.cloud.servicehealth_v1.types.event_resources import EventView
from google.cloud.servicehealth_v1.types.event_resources import OrganizationEventView

__all__ = ('ServiceHealthClient',
    'ServiceHealthAsyncClient',
    'Asset',
    'Event',
    'EventImpact',
    'EventUpdate',
    'GetEventRequest',
    'GetOrganizationEventRequest',
    'GetOrganizationImpactRequest',
    'ListEventsRequest',
    'ListEventsResponse',
    'ListOrganizationEventsRequest',
    'ListOrganizationEventsResponse',
    'ListOrganizationImpactsRequest',
    'ListOrganizationImpactsResponse',
    'Location',
    'OrganizationEvent',
    'OrganizationImpact',
    'Product',
    'EventView',
    'OrganizationEventView',
)
