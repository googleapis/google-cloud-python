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

from google.cloud.logging_v2._helpers import _add_defaults_to_filter
from google.cloud.logging_v2.entries import LogEntry
from google.cloud.logging_v2.entries import ProtobufEntry
from google.cloud.logging_v2.entries import StructEntry
from google.cloud.logging_v2.entries import TextEntry
from google.cloud.logging_v2.resource import Resource


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

    See https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.logs
    """

    def __init__(self, name, client, *, labels=None, resource=_GLOBAL_RESOURCE):
        """
        Args:
            name (str): The name of the logger.
            client (~logging_v2.client.Client):
                A client which holds credentials and project configuration
                for the logger (which requires a project).
            resource (~logging_v2.Resource): a monitored resource object
                representing the resource the code was run on.
            labels (Optional[dict]): Mapping of default labels for entries written
                via this logger.

        """
        self.name = name
        self._client = client
        self.labels = labels
        self.default_resource = resource

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
        return f"projects/{self.project}/logs/{self.name}"

    @property
    def path(self):
        """URI path for use in logging APIs"""
        return f"/{self.full_name}"

    def _require_client(self, client):
        """Check client or verify over-ride. Also sets ``parent``.

        Args:
            client (Union[None, ~logging_v2.client.Client]):
                The client to use.  If not passed, falls back to the
                ``client`` stored on the current sink.

        Returns:
            ~logging_v2.client.Client: The client passed in
                or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def batch(self, *, client=None):
        """Return a batch to use as a context manager.

        Args:
            client (Union[None, ~logging_v2.client.Client]):
                The client to use.  If not passed, falls back to the
                ``client`` stored on the current sink.

        Returns:
            Batch: A batch to use as a context manager.
        """
        client = self._require_client(client)
        return Batch(self, client)

    def _do_log(self, client, _entry_class, payload=None, **kw):
        """Helper for :meth:`log_empty`, :meth:`log_text`, etc."""
        client = self._require_client(client)

        # Apply defaults
        kw["log_name"] = kw.pop("log_name", self.full_name)
        kw["labels"] = kw.pop("labels", self.labels)
        kw["resource"] = kw.pop("resource", self.default_resource)

        if payload is not None:
            entry = _entry_class(payload=payload, **kw)
        else:
            entry = _entry_class(**kw)

        api_repr = entry.to_api_repr()
        client.logging_api.write_entries([api_repr])

    def log_empty(self, *, client=None, **kw):
        """Log an empty message via a POST request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/write

        Args:
            client (Optional[~logging_v2.client.Client]):
                The client to use.  If not passed, falls back to the
                ``client`` stored on the current sink.
            kw (Optional[dict]): additional keyword arguments for the entry.
                See :class:`~logging_v2.entries.LogEntry`.
        """
        self._do_log(client, LogEntry, **kw)

    def log_text(self, text, *, client=None, **kw):
        """Log a text message via a POST request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/write

        Args:
            text (str): the log message
            client (Optional[~logging_v2.client.Client]):
                The client to use.  If not passed, falls back to the
                ``client`` stored on the current sink.
            kw (Optional[dict]): additional keyword arguments for the entry.
                See :class:`~logging_v2.entries.LogEntry`.
        """
        self._do_log(client, TextEntry, text, **kw)

    def log_struct(self, info, *, client=None, **kw):
        """Log a structured message via a POST request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/write

        Args:
            info (dict): the log entry information
            client (Optional[~logging_v2.client.Client]):
                The client to use.  If not passed, falls back to the
                ``client`` stored on the current sink.
            kw (Optional[dict]): additional keyword arguments for the entry.
                See :class:`~logging_v2.entries.LogEntry`.
        """
        self._do_log(client, StructEntry, info, **kw)

    def log_proto(self, message, *, client=None, **kw):
        """Log a protobuf message via a POST request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list

        Args:
            message (google.protobuf.message.Message):
                The protobuf message to be logged.
            client (Optional[~logging_v2.client.Client]):
                The client to use.  If not passed, falls back to the
                ``client`` stored on the current sink.
            kw (Optional[dict]): additional keyword arguments for the entry.
                See :class:`~logging_v2.entries.LogEntry`.
        """
        self._do_log(client, ProtobufEntry, message, **kw)

    def delete(self, logger_name=None, *, client=None):
        """Delete all entries in a logger via a DELETE request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.logs/delete

        Args:
            logger_name (Optional[str]):  The resource name of the log to delete:

                ::

                    "projects/[PROJECT_ID]/logs/[LOG_ID]"
                    "organizations/[ORGANIZATION_ID]/logs/[LOG_ID]"
                    "billingAccounts/[BILLING_ACCOUNT_ID]/logs/[LOG_ID]"
                    "folders/[FOLDER_ID]/logs/[LOG_ID]"

                ``[LOG_ID]`` must be URL-encoded. For example,
                ``"projects/my-project-id/logs/syslog"``,
                ``"organizations/1234567890/logs/cloudresourcemanager.googleapis.com%2Factivity"``.
                If not passed, defaults to the project bound to the client.
            client (Optional[~logging_v2.client.Client]):
                The client to use.  If not passed, falls back to the
                ``client`` stored on the current logger.
        """
        client = self._require_client(client)
        if logger_name is None:
            logger_name = self.full_name
        client.logging_api.logger_delete(logger_name)

    def list_entries(
        self,
        *,
        resource_names=None,
        filter_=None,
        order_by=None,
        page_size=None,
        page_token=None,
    ):
        """Return a page of log entries.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list

        Args:
            resource_names (Optional[Sequence[str]]): Names of one or more parent resources
                from which to retrieve log entries:

                ::

                    "projects/[PROJECT_ID]"
                    "organizations/[ORGANIZATION_ID]"
                    "billingAccounts/[BILLING_ACCOUNT_ID]"
                    "folders/[FOLDER_ID]"

                If not passed, defaults to the project bound to the client.
            filter_ (Optional[str]): a filter expression. See
                https://cloud.google.com/logging/docs/view/advanced_filters
                By default, a 24 hour filter is applied.
            order_by (Optional[str]): One of :data:`~logging_v2.ASCENDING`
                or :data:`~logging_v2.DESCENDING`.
            page_size (Optional[int]):
                Optional. The maximum number of entries in each page of results
                from this request. Non-positive values are ignored. Defaults
                to a sensible value set by the API.
            page_token (Optional[str]):
                Optional. If present, return the next batch of entries, using
                the value, which must correspond to the ``nextPageToken`` value
                returned in the previous response.  Deprecated: use the ``pages``
                property of the returned iterator instead of manually passing
                the token.

        Returns:
            Iterator[~logging_v2.entries.LogEntry]
        """

        if resource_names is None:
            resource_names = [f"projects/{self.project}"]

        log_filter = f"logName={self.full_name}"
        if filter_ is not None:
            filter_ = f"{filter_} AND {log_filter}"
        else:
            filter_ = log_filter
        filter_ = _add_defaults_to_filter(filter_)
        return self.client.list_entries(
            resource_names=resource_names,
            filter_=filter_,
            order_by=order_by,
            page_size=page_size,
            page_token=page_token,
        )


class Batch(object):
    def __init__(self, logger, client, *, resource=None):
        """Context manager:  collect entries to log via a single API call.

        Helper returned by :meth:`Logger.batch`

        Args:
            logger (logging_v2.logger.Logger):
                the logger to which entries will be logged.
            client (~logging_V2.client.Cilent):
                The client to use.
            resource (Optional[~logging_v2.resource.Resource]):
                Monitored resource of the batch, defaults
                to None, which requires that every entry should have a
                resource specified. Since the methods used to write
                entries default the entry's resource to the global
                resource type, this parameter is only required
                if explicitly set to None. If no entries' resource are
                set to None, this parameter will be ignored on the server.
        """
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

        Args:
            kw (Optional[dict]): Additional keyword arguments for the entry.
                See :class:`~logging_v2.entries.LogEntry`.
        """
        self.entries.append(LogEntry(**kw))

    def log_text(self, text, **kw):
        """Add a text entry to be logged during :meth:`commit`.

        Args:
            text (str): the text entry
            kw (Optional[dict]): Additional keyword arguments for the entry.
                See :class:`~logging_v2.entries.LogEntry`.
        """
        self.entries.append(TextEntry(payload=text, **kw))

    def log_struct(self, info, **kw):
        """Add a struct entry to be logged during :meth:`commit`.

        Args:
            info (dict): The struct entry,
            kw (Optional[dict]): Additional keyword arguments for the entry.
                See :class:`~logging_v2.entries.LogEntry`.
        """
        self.entries.append(StructEntry(payload=info, **kw))

    def log_proto(self, message, **kw):
        """Add a protobuf entry to be logged during :meth:`commit`.

        Args:
            message (google.protobuf.Message): The protobuf entry.
            kw (Optional[dict]): Additional keyword arguments for the entry.
                See :class:`~logging_v2.entries.LogEntry`.
        """
        self.entries.append(ProtobufEntry(payload=message, **kw))

    def commit(self, *, client=None):
        """Send saved log entries as a single API call.

        Args:
            client (Optional[~logging_v2.client.Client]):
                The client to use.  If not passed, falls back to the
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
