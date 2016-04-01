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

"""Define Logging API Metrics."""

import re

from gcloud._helpers import _name_from_project_path
from gcloud.exceptions import NotFound


_METRIC_TEMPLATE = re.compile(r"""
    projects/            # static prefix
    (?P<project>[^/]+)   # initial letter, wordchars + hyphen
    /metrics/            # static midfix
    (?P<name>[^/]+)      # initial letter, wordchars + allowed punc
""", re.VERBOSE)


def _metric_name_from_path(path, project):
    """Validate a metric URI path and get the metric name.

    :type path: string
    :param path: URI path for a metric API request.

    :type project: string
    :param project: The project associated with the request. It is
                    included for validation purposes.

    :rtype: string
    :returns: Metric name parsed from ``path``.
    :raises: :class:`ValueError` if the ``path`` is ill-formed or if
             the project from the ``path`` does not agree with the
             ``project`` passed in.
    """
    return _name_from_project_path(path, project, _METRIC_TEMPLATE)


class Metric(object):
    """Metrics represent named filters for log entries.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics

    :type name: string
    :param name: the name of the metric

    :type filter_: string
    :param filter_: the advanced logs filter expression defining the entries
                   tracked by the metric.

    :type client: :class:`gcloud.logging.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the metric (which requires a project).

    :type description: string
    :param description: an optional description of the metric
    """
    def __init__(self, name, filter_, client, description=''):
        self.name = name
        self._client = client
        self.filter_ = filter_
        self.description = description

    @property
    def client(self):
        """Clent bound to the logger."""
        return self._client

    @property
    def project(self):
        """Project bound to the logger."""
        return self._client.project

    @property
    def full_name(self):
        """Fully-qualified name used in metric APIs"""
        return 'projects/%s/metrics/%s' % (self.project, self.name)

    @property
    def path(self):
        """URL path for the metric's APIs"""
        return '/%s' % (self.full_name,)

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a metric given its API representation

        :type resource: dict
        :param resource: metric resource representation returned from the API

        :type client: :class:`gcloud.logging.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the metric.

        :rtype: :class:`gcloud.logging.metric.Metric`
        :returns: Metric parsed from ``resource``.
        """
        metric_name = resource['name']
        filter_ = resource['filter']
        description = resource.get('description', '')
        return cls(metric_name, filter_, client=client,
                   description=description)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current metric.

        :rtype: :class:`gcloud.logging.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def create(self, client=None):
        """API call:  create the metric via a PUT request

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/create

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current metric.
        """
        client = self._require_client(client)
        target = '/projects/%s/metrics' % (self.project,)
        data = {
            'name': self.name,
            'filter': self.filter_,
        }
        if self.description:
            data['description'] = self.description
        client.connection.api_request(method='POST', path=target, data=data)

    def exists(self, client=None):
        """API call:  test for the existence of the metric via a GET request

        See
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/get

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current metric.
        """
        client = self._require_client(client)

        try:
            client.connection.api_request(method='GET', path=self.path)
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  sync local metric configuration via a GET request

        See
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/get

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current metric.
        """
        client = self._require_client(client)
        data = client.connection.api_request(method='GET', path=self.path)
        self.description = data.get('description', '')
        self.filter_ = data['filter']

    def update(self, client=None):
        """API call:  update metric configuration via a PUT request

        See
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/update

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current metric.
        """
        client = self._require_client(client)
        data = {'name': self.name, 'filter': self.filter_}
        if self.description:
            data['description'] = self.description
        client.connection.api_request(method='PUT', path=self.path, data=data)

    def delete(self, client=None):
        """API call:  delete a metric via a DELETE request

        See
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/delete

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current metric.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)
