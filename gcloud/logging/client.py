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

"""Client for interacting with the Google Cloud Logging API."""

import os

try:
    from google.logging.v2.config_service_v2_api import (
        ConfigServiceV2Api as GeneratedSinksAPI)
    from google.logging.v2.logging_service_v2_api import (
        LoggingServiceV2Api as GeneratedLoggingAPI)
    from google.logging.v2.metrics_service_v2_api import (
        MetricsServiceV2Api as GeneratedMetricsAPI)
    from gcloud.logging._gax import _LoggingAPI as GAXLoggingAPI
    from gcloud.logging._gax import _MetricsAPI as GAXMetricsAPI
    from gcloud.logging._gax import _SinksAPI as GAXSinksAPI
except ImportError:  # pragma: NO COVER
    _HAVE_GAX = False
    GeneratedLoggingAPI = GAXLoggingAPI = None
    GeneratedMetricsAPI = GAXMetricsAPI = None
    GeneratedSinksAPI = GAXSinksAPI = None
else:
    _HAVE_GAX = True

from gcloud.client import JSONClient
from gcloud.logging.connection import Connection
from gcloud.logging.connection import _LoggingAPI as JSONLoggingAPI
from gcloud.logging.connection import _MetricsAPI as JSONMetricsAPI
from gcloud.logging.connection import _SinksAPI as JSONSinksAPI
from gcloud.logging.entries import ProtobufEntry
from gcloud.logging.entries import StructEntry
from gcloud.logging.entries import TextEntry
from gcloud.logging.logger import Logger
from gcloud.logging.metric import Metric
from gcloud.logging.sink import Sink


_USE_GAX = _HAVE_GAX and (os.environ.get('GCLOUD_ENABLE_GAX') is not None)


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of.
                    If not passed, falls back to the default inferred
                    from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection
    _logging_api = _sinks_api = _metrics_api = None

    @property
    def logging_api(self):
        """Helper for logging-related API calls.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/entries
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.logs
        """
        if self._logging_api is None:
            if _USE_GAX:
                generated = GeneratedLoggingAPI()
                self._logging_api = GAXLoggingAPI(generated)
            else:
                self._logging_api = JSONLoggingAPI(self.connection)
        return self._logging_api

    @property
    def sinks_api(self):
        """Helper for log sink-related API calls.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.sinks
        """
        if self._sinks_api is None:
            if _USE_GAX:
                generated = GeneratedSinksAPI()
                self._sinks_api = GAXSinksAPI(generated)
            else:
                self._sinks_api = JSONSinksAPI(self.connection)
        return self._sinks_api

    @property
    def metrics_api(self):
        """Helper for log metric-related API calls.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics
        """
        if self._metrics_api is None:
            if _USE_GAX:
                generated = GeneratedMetricsAPI()
                self._metrics_api = GAXMetricsAPI(generated)
            else:
                self._metrics_api = JSONMetricsAPI(self.connection)
        return self._metrics_api

    def logger(self, name):
        """Creates a logger bound to the current client.

        :type name: str
        :param name: the name of the logger to be constructed.

        :rtype: :class:`gcloud.logging.logger.Logger`
        :returns: Logger created with the current client.
        """
        return Logger(name, client=self)

    def _entry_from_resource(self, resource, loggers):
        """Detect correct entry type from resource and instantiate.

        :type resource: dict
        :param resource: one entry resource from API response

        :type loggers: dict or None
        :param loggers: A mapping of logger fullnames -> loggers.  If not
                        passed, the entry will have a newly-created logger.

        :rtype: One of:
                :class:`gcloud.logging.entries.TextEntry`,
                :class:`gcloud.logging.entries.StructEntry`,
                :class:`gcloud.logging.entries.ProtobufEntry`
        :returns: the entry instance, constructed via the resource
        """
        if 'textPayload' in resource:
            return TextEntry.from_api_repr(resource, self, loggers)
        elif 'jsonPayload' in resource:
            return StructEntry.from_api_repr(resource, self, loggers)
        elif 'protoPayload' in resource:
            return ProtobufEntry.from_api_repr(resource, self, loggers)
        raise ValueError('Cannot parse log entry resource')

    def list_entries(self, projects=None, filter_=None, order_by=None,
                     page_size=None, page_token=None):
        """Return a page of log entries.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/entries/list

        :type projects: list of strings
        :param projects: project IDs to include. If not passed,
                            defaults to the project bound to the client.

        :type filter_: str
        :param filter_: a filter expression. See:
                        https://cloud.google.com/logging/docs/view/advanced_filters

        :type order_by: str
        :param order_by: One of :data:`gcloud.logging.ASCENDING` or
                         :data:`gcloud.logging.DESCENDING`.

        :type page_size: int
        :param page_size: maximum number of entries to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of entries. If not
                           passed, the API will return the first page of
                           entries.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.logging.entry.TextEntry`, plus a
                  "next page token" string:  if not None, indicates that
                  more entries can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        if projects is None:
            projects = [self.project]

        resources, token = self.logging_api.list_entries(
            projects=projects, filter_=filter_, order_by=order_by,
            page_size=page_size, page_token=page_token)
        loggers = {}
        entries = [self._entry_from_resource(resource, loggers)
                   for resource in resources]
        return entries, token

    def sink(self, name, filter_=None, destination=None):
        """Creates a sink bound to the current client.

        :type name: str
        :param name: the name of the sink to be constructed.

        :type filter_: str
        :param filter_: (optional) the advanced logs filter expression
                        defining the entries exported by the sink.  If not
                        passed, the instance should already exist, to be
                        refreshed via :meth:`Sink.reload`.

        :type destination: str
        :param destination: destination URI for the entries exported by
                            the sink.  If not passed, the instance should
                            already exist, to be refreshed via
                            :meth:`Sink.reload`.

        :rtype: :class:`gcloud.logging.sink.Sink`
        :returns: Sink created with the current client.
        """
        return Sink(name, filter_, destination, client=self)

    def list_sinks(self, page_size=None, page_token=None):
        """List sinks for the project associated with this client.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.sinks/list

        :type page_size: int
        :param page_size: maximum number of sinks to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of sinks. If not
                           passed, the API will return the first page of
                           sinks.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.logging.sink.Sink`, plus a
                  "next page token" string:  if not None, indicates that
                  more sinks can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        resources, token = self.sinks_api.list_sinks(
            self.project, page_size, page_token)
        sinks = [Sink.from_api_repr(resource, self)
                 for resource in resources]
        return sinks, token

    def metric(self, name, filter_=None, description=''):
        """Creates a metric bound to the current client.

        :type name: str
        :param name: the name of the metric to be constructed.

        :type filter_: str
        :param filter_: the advanced logs filter expression defining the
                        entries tracked by the metric.  If not
                        passed, the instance should already exist, to be
                        refreshed via :meth:`Metric.reload`.

        :type description: str
        :param description: the description of the metric to be constructed.
                            If not passed, the instance should already exist,
                            to be refreshed via :meth:`Metric.reload`.

        :rtype: :class:`gcloud.logging.metric.Metric`
        :returns: Metric created with the current client.
        """
        return Metric(name, filter_, client=self, description=description)

    def list_metrics(self, page_size=None, page_token=None):
        """List metrics for the project associated with this client.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/list

        :type page_size: int
        :param page_size: maximum number of metrics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of metrics. If not
                           passed, the API will return the first page of
                           metrics.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.logging.metric.Metric`, plus a
                  "next page token" string:  if not None, indicates that
                  more metrics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        resources, token = self.metrics_api.list_metrics(
            self.project, page_size, page_token)
        metrics = [Metric.from_api_repr(resource, self)
                   for resource in resources]
        return metrics, token
