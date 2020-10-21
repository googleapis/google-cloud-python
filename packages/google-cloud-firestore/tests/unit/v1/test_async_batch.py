# Copyright 2020 Google LLC All rights reserved.
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

import pytest
import aiounittest

import mock
from tests.unit.v1.test__helpers import AsyncMock


class TestAsyncWriteBatch(aiounittest.AsyncTestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.async_batch import AsyncWriteBatch

        return AsyncWriteBatch

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        batch = self._make_one(mock.sentinel.client)
        self.assertIs(batch._client, mock.sentinel.client)
        self.assertEqual(batch._write_pbs, [])
        self.assertIsNone(batch.write_results)
        self.assertIsNone(batch.commit_time)

    async def _commit_helper(self, retry=None, timeout=None):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1 import _helpers
        from google.cloud.firestore_v1.types import firestore
        from google.cloud.firestore_v1.types import write

        # Create a minimal fake GAPIC with a dummy result.
        firestore_api = AsyncMock(spec=["commit"])
        timestamp = timestamp_pb2.Timestamp(seconds=1234567, nanos=123456798)
        commit_response = firestore.CommitResponse(
            write_results=[write.WriteResult(), write.WriteResult()],
            commit_time=timestamp,
        )
        firestore_api.commit.return_value = commit_response
        kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

        # Attach the fake GAPIC to a real client.
        client = _make_client("grand")
        client._firestore_api_internal = firestore_api

        # Actually make a batch with some mutations and call commit().
        batch = self._make_one(client)
        document1 = client.document("a", "b")
        batch.create(document1, {"ten": 10, "buck": "ets"})
        document2 = client.document("c", "d", "e", "f")
        batch.delete(document2)
        write_pbs = batch._write_pbs[::]

        write_results = await batch.commit(**kwargs)

        self.assertEqual(write_results, list(commit_response.write_results))
        self.assertEqual(batch.write_results, write_results)
        self.assertEqual(batch.commit_time.timestamp_pb(), timestamp)
        # Make sure batch has no more "changes".
        self.assertEqual(batch._write_pbs, [])

        # Verify the mocks.
        firestore_api.commit.assert_called_once_with(
            request={
                "database": client._database_string,
                "writes": write_pbs,
                "transaction": None,
            },
            metadata=client._rpc_metadata,
            **kwargs,
        )

    @pytest.mark.asyncio
    async def test_commit(self):
        await self._commit_helper()

    @pytest.mark.asyncio
    async def test_commit_w_retry_timeout(self):
        from google.api_core.retry import Retry

        retry = Retry(predicate=object())
        timeout = 123.0

        await self._commit_helper(retry=retry, timeout=timeout)

    @pytest.mark.asyncio
    async def test_as_context_mgr_wo_error(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1.types import firestore
        from google.cloud.firestore_v1.types import write

        firestore_api = AsyncMock(spec=["commit"])
        timestamp = timestamp_pb2.Timestamp(seconds=1234567, nanos=123456798)
        commit_response = firestore.CommitResponse(
            write_results=[write.WriteResult(), write.WriteResult()],
            commit_time=timestamp,
        )
        firestore_api.commit.return_value = commit_response
        client = _make_client()
        client._firestore_api_internal = firestore_api
        batch = self._make_one(client)
        document1 = client.document("a", "b")
        document2 = client.document("c", "d", "e", "f")

        async with batch as ctx_mgr:
            self.assertIs(ctx_mgr, batch)
            ctx_mgr.create(document1, {"ten": 10, "buck": "ets"})
            ctx_mgr.delete(document2)
            write_pbs = batch._write_pbs[::]

        self.assertEqual(batch.write_results, list(commit_response.write_results))
        self.assertEqual(batch.commit_time.timestamp_pb(), timestamp)
        # Make sure batch has no more "changes".
        self.assertEqual(batch._write_pbs, [])

        # Verify the mocks.
        firestore_api.commit.assert_called_once_with(
            request={
                "database": client._database_string,
                "writes": write_pbs,
                "transaction": None,
            },
            metadata=client._rpc_metadata,
        )

    @pytest.mark.asyncio
    async def test_as_context_mgr_w_error(self):
        firestore_api = AsyncMock(spec=["commit"])
        client = _make_client()
        client._firestore_api_internal = firestore_api
        batch = self._make_one(client)
        document1 = client.document("a", "b")
        document2 = client.document("c", "d", "e", "f")

        with self.assertRaises(RuntimeError):
            async with batch as ctx_mgr:
                ctx_mgr.create(document1, {"ten": 10, "buck": "ets"})
                ctx_mgr.delete(document2)
                raise RuntimeError("testing")

        # batch still has its changes, as _aexit_ (and commit) is not invoked
        # changes are preserved so commit can be retried
        self.assertIsNone(batch.write_results)
        self.assertIsNone(batch.commit_time)
        self.assertEqual(len(batch._write_pbs), 2)

        firestore_api.commit.assert_not_called()


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project="seventy-nine"):
    from google.cloud.firestore_v1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)
