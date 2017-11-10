# Copyright 2016 Google LLC
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

"""Google Stackdriver Monitoring API wrapper."""


from pkg_resources import get_distribution
__version__ = get_distribution('google-cloud-monitoring').version

from google.cloud.monitoring.client import Client
from google.cloud.monitoring.group import Group
from google.cloud.monitoring.label import LabelDescriptor
from google.cloud.monitoring.label import LabelValueType
from google.cloud.monitoring.metric import Metric
from google.cloud.monitoring.metric import MetricDescriptor
from google.cloud.monitoring.metric import MetricKind
from google.cloud.monitoring.metric import ValueType
from google.cloud.monitoring.query import Aligner
from google.cloud.monitoring.query import Query
from google.cloud.monitoring.query import Reducer
from google.cloud.monitoring.resource import Resource
from google.cloud.monitoring.resource import ResourceDescriptor
from google.cloud.monitoring.timeseries import Point
from google.cloud.monitoring.timeseries import TimeSeries

__all__ = (
    'Client',
    'Group',
    'LabelDescriptor', 'LabelValueType',
    'Metric', 'MetricDescriptor', 'MetricKind', 'ValueType',
    'Aligner', 'Query', 'Reducer',
    'Resource', 'ResourceDescriptor',
    'Point', 'TimeSeries',
    'SCOPE',
)


SCOPE = Client.SCOPE
