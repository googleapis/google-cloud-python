# Copyright 2015 Google Inc. All rights reserved.
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

"""Google Cloud DNS API wrapper.

The main concepts with this API are:

- :class:`gcloud.DNS.zone.ManagedZone` represents an collection of tables.
- :class:`gcloud.DNS.resource_record_set.ResourceRecordSet` represents a
  single resource definition within a zone.
- :class:`gcloud.DNS.changes.Changes` represents a set of changes (adding/
  deleting resource record sets) to a zone.
"""

from gcloud.dns.zone import Changes
from gcloud.dns.client import Client
from gcloud.dns.connection import Connection
from gcloud.dns.zone import ManagedZone
from gcloud.dns.resource_record_set import ResourceRecordSet


SCOPE = Connection.SCOPE
