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

"""Client for interacting with the Google Monitoring API."""

from gcloud.client import JSONClient
from gcloud.monitoring.connection import Connection
from gcloud.monitoring.metric import MetricDescriptor
from gcloud.monitoring.resource import ResourceDescriptor


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: string
    :param project: The target project. If not passed, falls back to the
                    default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def fetch_metric_descriptor(self, metric_type):
        """Look up a metric descriptor by type.

        :type metric_type: string
        :param metric_type: The metric type name.

        :rtype: :class:`~gcloud.monitoring.metric.MetricDescriptor`
        :returns: The metric descriptor instance.

        :raises: :class:`gcloud.exceptions.NotFound`
        """
        return MetricDescriptor._fetch(self, metric_type)

    def list_metric_descriptors(self, filter=None):
        """List all metric descriptors for the project.

        :type filter: string or None
        :param filter: An optional filter string describing the metric
                       descriptors to be returned.

        :rtype: list of :class:`~gcloud.monitoring.metric.MetricDescriptor`
        :returns: A list of metric descriptor instances.
        """
        # Allow "filter" as a parameter name: pylint: disable=redefined-builtin
        return MetricDescriptor._list(self, filter)

    def fetch_resource_descriptor(self, resource_type):
        """Look up a resource descriptor by type.

        :type resource_type: string
        :param resource_type: The resource type name.

        :rtype: :class:`~gcloud.monitoring.resource.ResourceDescriptor`
        :returns: The resource descriptor instance.

        :raises: :class:`gcloud.exceptions.NotFound`
        """
        return ResourceDescriptor._fetch(self, resource_type)

    def list_resource_descriptors(self, filter=None):
        """List all resource descriptors for the project.

        :type filter: string or None
        :param filter: An optional filter string describing the resource
                       descriptors to be returned.

        :rtype: list of :class:`~gcloud.monitoring.resource.ResourceDescriptor`
        :returns: A list of resource descriptor instances.
        """
        # Allow "filter" as a parameter name: pylint: disable=redefined-builtin
        return ResourceDescriptor._list(self, filter)
