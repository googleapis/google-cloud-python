# Copyright 2021 Google LLC All rights reserved.
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

import concurrent.futures
import datetime
import mock
import typing

import google
from google.cloud.firestore_v1.base_client import BaseClient
from google.cloud.firestore_v1.document import DocumentReference, DocumentSnapshot
from google.cloud._helpers import _datetime_to_pb_timestamp, UTC  # type: ignore
from google.cloud.firestore_v1._helpers import build_timestamp
from google.cloud.firestore_v1.async_client import AsyncClient
from google.cloud.firestore_v1.client import Client
from google.protobuf.timestamp_pb2 import Timestamp  # type: ignore


def make_test_credentials() -> google.auth.credentials.Credentials:  # type: ignore
    import google.auth.credentials  # type: ignore

    return mock.Mock(spec=google.auth.credentials.Credentials)


def make_client(project_name: typing.Optional[str] = None) -> Client:
    return Client(
        project=project_name or "project-project", credentials=make_test_credentials(),
    )


def make_async_client() -> AsyncClient:
    return AsyncClient(project="project-project", credentials=make_test_credentials())


def build_test_timestamp(
    year: int = 2021,
    month: int = 1,
    day: int = 1,
    hour: int = 12,
    minute: int = 0,
    second: int = 0,
) -> Timestamp:
    return _datetime_to_pb_timestamp(
        datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            tzinfo=UTC,
        ),
    )


def build_document_snapshot(
    *,
    collection_name: str = "col",
    document_id: str = "doc",
    client: typing.Optional[BaseClient] = None,
    data: typing.Optional[typing.Dict] = None,
    exists: bool = True,
    create_time: typing.Optional[Timestamp] = None,
    read_time: typing.Optional[Timestamp] = None,
    update_time: typing.Optional[Timestamp] = None,
) -> DocumentSnapshot:
    return DocumentSnapshot(
        DocumentReference(collection_name, document_id, client=client),
        data or {"hello", "world"},
        exists=exists,
        read_time=read_time or build_timestamp(),
        create_time=create_time or build_timestamp(),
        update_time=update_time or build_timestamp(),
    )


class FakeThreadPoolExecutor:
    def __init__(self, *args, **kwargs):
        self._shutdown = False

    def submit(self, callable) -> typing.NoReturn:
        if self._shutdown:
            raise RuntimeError(
                "cannot schedule new futures after shutdown"
            )  # pragma: NO COVER
        future = concurrent.futures.Future()
        future.set_result(callable())
        return future

    def shutdown(self):
        self._shutdown = True

    def __repr__(self):
        return f"FakeThreadPoolExecutor(shutdown={self._shutdown})"
