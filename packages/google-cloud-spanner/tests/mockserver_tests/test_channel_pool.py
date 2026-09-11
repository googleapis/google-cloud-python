# Copyright 2026 Google LLC All rights reserved.
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

from google.cloud.spanner_v1._async.channel_pool import (
    ChannelPoolOptions as AsyncChannelPoolOptions,
)
from google.cloud.spanner_v1.channel_pool import ChannelPoolOptions
from tests.mockserver_tests.mock_server_test_base import (
    AsyncMockServerTestBase,
    MockServerTestBase,
    add_select1_result,
)


class TestChannelPool(MockServerTestBase):
    def test_channel_pool_creates_distinct_tcp_connections(self):
        add_select1_result()
        channel_pool_options = ChannelPoolOptions(min_channels=4, max_channels=4)
        database = self.instance.database(
            "test-database-channel-pool",
            channel_pool_options=channel_pool_options,
        )
        _ = database.spanner_api
        self.addCleanup(database.close)

        self.assertEqual(len(database._channel_pool._active_entries), 4)

        # Pin each query to a specific channel entry to deterministically exercise
        # all channels in the pool without relying on randomized P2C selection.
        for entry in database._channel_pool._active_entries:
            with database.snapshot(multi_use=True) as snapshot:
                snapshot._affinity.pin_entry(entry)
                results = snapshot.execute_sql("select 1")
                first_row = next(iter(results))
                self.assertEqual(1, first_row[0])

        # Verify that all requests were recorded with their peer address.
        self.assertGreaterEqual(len(self.spanner_service.requests_peers), 4)
        self.assertNotIn(None, self.spanner_service.requests_peers)

        # Map channel slot (from x-goog-spanner-request-id) to peer connections.
        channel_slot_to_peers = {}
        for metadata, peer in zip(
            self.spanner_service.requests_metadata,
            self.spanner_service.requests_peers,
        ):
            request_id_header = metadata.get("x-goog-spanner-request-id", "")
            parts = request_id_header.split(".")
            if len(parts) >= 4:
                channel_slot = parts[3]
                channel_slot_to_peers.setdefault(channel_slot, set()).add(peer)

        # 1. Verify that all 4 channels in the pool were actively used.
        active_channel_ids = {
            str(entry.id) for entry in database._channel_pool._active_entries
        }
        self.assertEqual(
            set(channel_slot_to_peers.keys()),
            active_channel_ids,
            "Not all pooled channels were used to execute requests.",
        )

        # 2. Verify that each channel used exactly one TCP connection.
        for channel_slot, peers in channel_slot_to_peers.items():
            self.assertEqual(
                len(peers),
                1,
                f"Channel slot {channel_slot} used multiple TCP connections: {peers}",
            )

        # 3. Verify that all 4 channels used distinct TCP connections (no collapsing).
        all_peers = set(self.spanner_service.requests_peers)
        self.assertEqual(
            len(all_peers),
            4,
            f"Expected 4 distinct TCP connections, got {len(all_peers)}: {all_peers}",
        )


class TestAsyncChannelPool(AsyncMockServerTestBase):
    async def test_async_channel_pool_creates_distinct_tcp_connections(self):
        add_select1_result()
        channel_pool_options = AsyncChannelPoolOptions(min_channels=4, max_channels=4)
        database = await self.instance.database(
            "test-database-channel-pool-async",
            channel_pool_options=channel_pool_options,
        )
        _ = database.spanner_api
        self.addAsyncCleanup(database.close)

        self.assertEqual(len(database._channel_pool._active_entries), 4)

        # Pin each query to a specific channel entry to deterministically exercise
        # all channels in the pool without relying on randomized P2C selection.
        for entry in database._channel_pool._active_entries:
            async with database.snapshot(multi_use=True) as snapshot:
                snapshot._affinity.pin_entry(entry)
                results = await snapshot.execute_sql("select 1")
                first_row = None
                async for row in results:
                    first_row = row
                    break
                self.assertEqual(1, first_row[0])

        # Verify that all requests were recorded with their peer address.
        self.assertGreaterEqual(len(self.spanner_service.requests_peers), 4)
        self.assertNotIn(None, self.spanner_service.requests_peers)

        # Map channel slot (from x-goog-spanner-request-id) to peer connections.
        channel_slot_to_peers = {}
        for metadata, peer in zip(
            self.spanner_service.requests_metadata,
            self.spanner_service.requests_peers,
        ):
            request_id_header = metadata.get("x-goog-spanner-request-id", "")
            parts = request_id_header.split(".")
            if len(parts) >= 4:
                channel_slot = parts[3]
                channel_slot_to_peers.setdefault(channel_slot, set()).add(peer)

        # 1. Verify that all 4 channels in the pool were actively used.
        active_channel_ids = {
            str(entry.id) for entry in database._channel_pool._active_entries
        }
        self.assertEqual(
            set(channel_slot_to_peers.keys()),
            active_channel_ids,
            "Not all pooled channels were used to execute requests.",
        )

        # 2. Verify that each channel used exactly one TCP connection.
        for channel_slot, peers in channel_slot_to_peers.items():
            self.assertEqual(
                len(peers),
                1,
                f"Channel slot {channel_slot} used multiple TCP connections: {peers}",
            )

        # 3. Verify that all 4 channels used distinct TCP connections (no collapsing).
        all_peers = set(self.spanner_service.requests_peers)
        self.assertEqual(
            len(all_peers),
            4,
            f"Expected 4 distinct TCP connections, got {len(all_peers)}: {all_peers}",
        )
