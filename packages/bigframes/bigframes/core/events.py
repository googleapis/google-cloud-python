# Copyright 2025 Google LLC
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

from __future__ import annotations

import dataclasses
import datetime
import threading
from typing import Any, Callable, Optional, Set
import uuid

import google.cloud.bigquery._job_helpers
import google.cloud.bigquery.job.query
import google.cloud.bigquery.table

import bigframes.session.executor


class Subscriber:
    def __init__(self, callback: Callable[[Event], None], *, publisher: Publisher):
        self._publisher = publisher
        self._callback = callback
        self._subscriber_id = uuid.uuid4()

    def __call__(self, *args, **kwargs):
        return self._callback(*args, **kwargs)

    def __hash__(self) -> int:
        return hash(self._subscriber_id)

    def __eq__(self, value: object):
        if not isinstance(value, Subscriber):
            return NotImplemented
        return value._subscriber_id == self._subscriber_id

    def close(self):
        self._publisher.unsubscribe(self)
        del self._publisher
        del self._callback

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None:
            self(
                UnknownErrorEvent(
                    exc_type=exc_type,
                    exc_value=exc_value,
                    traceback=traceback,
                )
            )
        self.close()


class Publisher:
    def __init__(self):
        self._subscribers_lock = threading.Lock()
        self._subscribers: Set[Subscriber] = set()

    def subscribe(self, callback: Callable[[Event], None]) -> Subscriber:
        # TODO(b/448176657): figure out how to handle subscribers/publishers in
        # a background thread. Maybe subscribers should be thread-local?
        subscriber = Subscriber(callback, publisher=self)
        with self._subscribers_lock:
            self._subscribers.add(subscriber)
        return subscriber

    def unsubscribe(self, subscriber: Subscriber):
        with self._subscribers_lock:
            self._subscribers.remove(subscriber)

    def publish(self, event: Event):
        with self._subscribers_lock:
            for subscriber in self._subscribers:
                subscriber(event)


class Event:
    pass


@dataclasses.dataclass(frozen=True)
class SessionClosed(Event):
    session_id: str


class ExecutionStarted(Event):
    pass


class ExecutionRunning(Event):
    pass


@dataclasses.dataclass(frozen=True)
class ExecutionFinished(Event):
    result: Optional[bigframes.session.executor.ExecuteResult] = None


@dataclasses.dataclass(frozen=True)
class UnknownErrorEvent(Event):
    exc_type: Any
    exc_value: Any
    traceback: Any


@dataclasses.dataclass(frozen=True)
class BigQuerySentEvent(ExecutionRunning):
    """Query sent to BigQuery."""

    query: str
    billing_project: Optional[str] = None
    location: Optional[str] = None
    job_id: Optional[str] = None
    request_id: Optional[str] = None

    @classmethod
    def from_bqclient(cls, event: google.cloud.bigquery._job_helpers.QuerySentEvent):
        return cls(
            query=event.query,
            billing_project=event.billing_project,
            location=event.location,
            job_id=event.job_id,
            request_id=event.request_id,
        )


@dataclasses.dataclass(frozen=True)
class BigQueryRetryEvent(ExecutionRunning):
    """Query sent another time because the previous attempt failed."""

    query: str
    billing_project: Optional[str] = None
    location: Optional[str] = None
    job_id: Optional[str] = None
    request_id: Optional[str] = None

    @classmethod
    def from_bqclient(cls, event: google.cloud.bigquery._job_helpers.QueryRetryEvent):
        return cls(
            query=event.query,
            billing_project=event.billing_project,
            location=event.location,
            job_id=event.job_id,
            request_id=event.request_id,
        )


@dataclasses.dataclass(frozen=True)
class BigQueryReceivedEvent(ExecutionRunning):
    """Query received and acknowledged by the BigQuery API."""

    billing_project: Optional[str] = None
    location: Optional[str] = None
    job_id: Optional[str] = None
    statement_type: Optional[str] = None
    state: Optional[str] = None
    query_plan: Optional[list[google.cloud.bigquery.job.query.QueryPlanEntry]] = None
    created: Optional[datetime.datetime] = None
    started: Optional[datetime.datetime] = None
    ended: Optional[datetime.datetime] = None

    @classmethod
    def from_bqclient(
        cls, event: google.cloud.bigquery._job_helpers.QueryReceivedEvent
    ):
        return cls(
            billing_project=event.billing_project,
            location=event.location,
            job_id=event.job_id,
            statement_type=event.statement_type,
            state=event.state,
            query_plan=event.query_plan,
            created=event.created,
            started=event.started,
            ended=event.ended,
        )


@dataclasses.dataclass(frozen=True)
class BigQueryFinishedEvent(ExecutionRunning):
    """Query finished successfully."""

    billing_project: Optional[str] = None
    location: Optional[str] = None
    query_id: Optional[str] = None
    job_id: Optional[str] = None
    destination: Optional[google.cloud.bigquery.table.TableReference] = None
    total_rows: Optional[int] = None
    total_bytes_processed: Optional[int] = None
    slot_millis: Optional[int] = None
    created: Optional[datetime.datetime] = None
    started: Optional[datetime.datetime] = None
    ended: Optional[datetime.datetime] = None

    @classmethod
    def from_bqclient(
        cls, event: google.cloud.bigquery._job_helpers.QueryFinishedEvent
    ):
        return cls(
            billing_project=event.billing_project,
            location=event.location,
            query_id=event.query_id,
            job_id=event.job_id,
            destination=event.destination,
            total_rows=event.total_rows,
            total_bytes_processed=event.total_bytes_processed,
            slot_millis=event.slot_millis,
            created=event.created,
            started=event.started,
            ended=event.ended,
        )


@dataclasses.dataclass(frozen=True)
class BigQueryUnknownEvent(ExecutionRunning):
    """Got unknown event from the BigQuery client library."""

    # TODO: should we just skip sending unknown events?

    event: object

    @classmethod
    def from_bqclient(cls, event):
        return cls(event)
