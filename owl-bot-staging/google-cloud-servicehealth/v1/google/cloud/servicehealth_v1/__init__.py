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
from google.cloud.servicehealth_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.service_health import ServiceHealthClient
from .services.service_health import ServiceHealthAsyncClient

from .types.event_resources import Asset
from .types.event_resources import Event
from .types.event_resources import EventImpact
from .types.event_resources import EventUpdate
from .types.event_resources import GetEventRequest
from .types.event_resources import GetOrganizationEventRequest
from .types.event_resources import GetOrganizationImpactRequest
from .types.event_resources import ListEventsRequest
from .types.event_resources import ListEventsResponse
from .types.event_resources import ListOrganizationEventsRequest
from .types.event_resources import ListOrganizationEventsResponse
from .types.event_resources import ListOrganizationImpactsRequest
from .types.event_resources import ListOrganizationImpactsResponse
from .types.event_resources import Location
from .types.event_resources import OrganizationEvent
from .types.event_resources import OrganizationImpact
from .types.event_resources import Product
from .types.event_resources import EventView
from .types.event_resources import OrganizationEventView

__all__ = (
    'ServiceHealthAsyncClient',
'Asset',
'Event',
'EventImpact',
'EventUpdate',
'EventView',
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
'OrganizationEventView',
'OrganizationImpact',
'Product',
'ServiceHealthClient',
)
