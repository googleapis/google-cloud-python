# Copyright 2016 Google Inc. All rights reserved.
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

"""Google Monitoring API wrapper."""

from gcloud.monitoring.client import Client
from gcloud.monitoring.connection import Connection
from gcloud.monitoring.label import LabelDescriptor
from gcloud.monitoring.label import LabelValueType
from gcloud.monitoring.metric import Metric
from gcloud.monitoring.metric import MetricDescriptor
from gcloud.monitoring.metric import MetricKind
from gcloud.monitoring.metric import ValueType
from gcloud.monitoring.query import Aligner
from gcloud.monitoring.query import Query
from gcloud.monitoring.query import Reducer
from gcloud.monitoring.resource import Resource
from gcloud.monitoring.resource import ResourceDescriptor
from gcloud.monitoring.timeseries import Point
from gcloud.monitoring.timeseries import TimeSeries

__all__ = (
    'Client',
    'Connection',
    'LabelDescriptor', 'LabelValueType',
    'Metric', 'MetricDescriptor', 'MetricKind', 'ValueType',
    'Aligner', 'Query', 'Reducer',
    'Resource', 'ResourceDescriptor',
    'Point', 'TimeSeries',
    'SCOPE',
)


SCOPE = Connection.SCOPE
