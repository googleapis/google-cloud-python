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

"""Define API Loggers."""

from google.cloud.logging.entries import LogEntry
from google.cloud.logging.entries import ProtobufEntry
from google.cloud.logging.entries import StructEntry
from google.cloud.logging.entries import TextEntry
from google.cloud.logging.resource import Resource


_GLOBAL_RESOURCE = Resource(type="global", labels={})


_OUTBOUND_ENTRY_FIELDS = (  # (name, default)
    ("type_", None),
    ("log_name", None),
    ("payload", None),
    ("labels", None),
    ("insert_id", None),
    ("severity", None),
    ("http_request", None),
    ("timestamp", None),
    ("resource", _GLOBAL_RESOURCE),
    ("trace", None),
    ("span_id", None),
    ("trace_sampled", None),
    ("source_location", None),
)


class Logger(object):
    """Loggers represent named targets for log entries.

    See
    https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.logs

    :type name: str
    :param name: the name of the logger

    :type client: :class:`google.cloud.logging.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the logger (which requires a project).

    :type labels: dict
    :param labels: (optional) mapping of default labels for entries written
                   via this logger.
    """

    def __init__(self, name, client, labels=None):
        self.name = name
        self._client = client
        self.labels = labels

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
        """Fully-qualified name used in logging APIs"""
        return "projects/%s/logs/%s" % (self.project, self.name)

    @property
    def path(self):
        """URI path for use in logging APIs"""
        return "/%s" % (self.full_name,)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`~google.cloud.logging.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current logger.

        :rtype: :class:`google.cloud.logging.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def batch(self, client=None):
        """Return a batch to use as a context manager.

        :type client: :class:`~google.cloud.logging.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :rtype: :class:`Batch`
        :returns: A batch to use as a context manager.
        """
        client = self._require_client(client)
        return Batch(self, client)

    def _do_log(self, client, _entry_class, payload=None, **kw):
        """Helper for :meth:`log_empty`, :meth:`log_text`, etc.
        """
        client = self._require_client(client)

        # Apply defaults
        kw["log_name"] = kw.pop("log_name", self.full_name)
        kw["labels"] = kw.pop("labels", self.labels)
        kw["resource"] = kw.pop("resource", _GLOBAL_RESOURCE)

        if payload is not None:
            entry = _entry_class(payload=payload, **kw)
        else:
            entry = _entry_class(**kw)

        api_repr = entry.to_api_repr()
        client.logging_api.write_entries([api_repr])

    def log_empty(self, client=None, **kw):
        """API call:  log an empty message via a POST request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/write

        :type client: :class:`~google.cloud.logging.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current logger.

        :type kw: dict
        :param kw: (optional) additional keyword arguments for the entry.
                   See :class:`~google.cloud.logging.entries.LogEntry`.
        """
        self._do_log(client, LogEntry, **kw)

    def log_text(self, text, client=None, **kw):
        """API call:  log a text message via a POST request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/write

        :type text: str
        :param text: the log message.

        :type client: :class:`~google.cloud.logging.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current logger.

        :type kw: dict
        :param kw: (optional) additional keyword arguments for the entry.
                   See :class:`~google.cloud.logging.entries.LogEntry`.
        """
        self._do_log(client, TextEntry, text, **kw)

    def log_struct(self, info, client=None, **kw):
        """API call:  log a structured message via a POST request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/write

        :type info: dict
        :param info: the log entry information

        :type client: :class:`~google.cloud.logging.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current logger.

        :type kw: dict
        :param kw: (optional) additional keyword arguments for the entry.
                   See :class:`~google.cloud.logging.entries.LogEntry`.
        """
        self._do_log(client, StructEntry, info, **kw)

    def log_proto(self, message, client=None, **kw):
        """API call:  log a protobuf message via a POST request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list

        :type message: :class:`~google.protobuf.message.Message`
        :param message: The protobuf message to be logged.

        :type client: :class:`~google.cloud.logging.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current logger.

        :type kw: dict
        :param kw: (optional) additional keyword arguments for the entry.
                   See :class:`~google.cloud.logging.entries.LogEntry`.
        """
        self._do_log(client, ProtobufEntry, message, **kw)

    def delete(self, client=None):
        """API call:  delete all entries in a logger via a DELETE request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.logs/delete

        :type client: :class:`~google.cloud.logging.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current logger.
        """
        client = self._require_client(client)
        client.logging_api.logger_delete(self.project, self.name)

    def list_entries(
        self,
        projects=None,
        filter_=None,
        order_by=None,
        page_size=None,
        page_token=None,
    ):
        """Return a page of log entries.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list

        :type projects: list of strings
        :param projects: project IDs to include. If not passed,
                            defaults to the project bound to the client.

        :type filter_: str
        :param filter_:
            a filter expression. See
            https://cloud.google.com/logging/docs/view/advanced_filters

        :type order_by: str
        :param order_by: One of :data:`~google.cloud.logging.ASCENDING`
                         or :data:`~google.cloud.logging.DESCENDING`.

        :type page_size: int
        :param page_size:
            Optional. The maximum number of entries in each page of results
            from this request. Non-positive values are ignored. Defaults
            to a sensible value set by the API.

        :type page_token: str
        :param page_token:
            Optional. If present, return the next batch of entries, using
            the value, which must correspond to the ``nextPageToken`` value
            returned in the previous response.  Deprecated: use the ``pages``
            property of the returned iterator instead of manually passing
            the token.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of log entries accessible to the current logger.
                  See :class:`~google.cloud.logging.entries.LogEntry`.
        """
        log_filter = "logName=%s" % (self.full_name,)
        if filter_ is not None:
            filter_ = "%s AND %s" % (filter_, log_filter)
        else:
            filter_ = log_filter
        return self.client.list_entries(
            projects=projects,
            filter_=filter_,
            order_by=order_by,
            page_size=page_size,
            page_token=page_token,
        )


class Batch(object):
    """Context manager:  collect entries to log via a single API call.

    Helper returned by :meth:`Logger.batch`

    :type logger: :class:`google.cloud.logging.logger.Logger`
    :param logger: the logger to which entries will be logged.

    :type client: :class:`google.cloud.logging.client.Client`
    :param client: The client to use.

    :type resource: :class:`~google.cloud.logging.resource.Resource`
    :param resource: (Optional) Monitored resource of the batch, defaults
                     to None, which requires that every entry should have a
                     resource specified. Since the methods used to write
                     entries default the entry's resource to the global
                     resource type, this parameter is only required
                     if explicitly set to None. If no entries' resource are
                     set to None, this parameter will be ignored on the server.
    """

    def __init__(self, logger, client, resource=None):
        self.logger = logger
        self.entries = []
        self.client = client
        self.resource = resource

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()

    def log_empty(self, **kw):
        """Add a entry without payload to be logged during :meth:`commit`.

        :type kw: dict
        :param kw: (optional) additional keyword arguments for the entry.
                   See :class:`~google.cloud.logging.entries.LogEntry`.
        """
        self.entries.append(LogEntry(**kw))

    def log_text(self, text, **kw):
        """Add a text entry to be logged during :meth:`commit`.

        :type text: str
        :param text: the text entry

        :type kw: dict
        :param kw: (optional) additional keyword arguments for the entry.
                   See :class:`~google.cloud.logging.entries.LogEntry`.
        """
        self.entries.append(TextEntry(payload=text, **kw))

    def log_struct(self, info, **kw):
        """Add a struct entry to be logged during :meth:`commit`.

        :type info: dict
        :param info: the struct entry

        :type kw: dict
        :param kw: (optional) additional keyword arguments for the entry.
                   See :class:`~google.cloud.logging.entries.LogEntry`.
        """
        self.entries.append(StructEntry(payload=info, **kw))

    def log_proto(self, message, **kw):
        """Add a protobuf entry to be logged during :meth:`commit`.

        :type message: protobuf message
        :param message: the protobuf entry

        :type kw: dict
        :param kw: (optional) additional keyword arguments for the entry.
                   See :class:`~google.cloud.logging.entries.LogEntry`.
        """
        self.entries.append(ProtobufEntry(payload=message, **kw))

    def commit(self, client=None):
        """Send saved log entries as a single API call.

        :type client: :class:`~google.cloud.logging.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current batch.
        """
        if client is None:
            client = self.client

        kwargs = {"logger_name": self.logger.full_name}

        if self.resource is not None:
            kwargs["resource"] = self.resource._to_dict()

        if self.logger.labels is not None:
            kwargs["labels"] = self.logger.labels

        entries = [entry.to_api_repr() for entry in self.entries]

        client.logging_api.write_entries(entries, **kwargs)
        del self.entries[:]
