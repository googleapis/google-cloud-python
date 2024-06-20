# Copyright 2016 Google LLC All rights reserved.
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


import unittest
from tests._helpers import OpenTelemetryBase, StatusCode
from google.cloud.spanner_v1 import RequestOptions

TABLE_NAME = "citizens"
COLUMNS = ["email", "first_name", "last_name", "age"]
VALUES = [
    ["phred@exammple.com", "Phred", "Phlyntstone", 32],
    ["bharney@example.com", "Bharney", "Rhubble", 31],
]
BASE_ATTRIBUTES = {
    "db.type": "spanner",
    "db.url": "spanner.googleapis.com",
    "db.instance": "testing",
    "net.host.name": "spanner.googleapis.com",
}


class _BaseTest(unittest.TestCase):
    PROJECT_ID = "project-id"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID
    DATABASE_ID = "database-id"
    DATABASE_NAME = INSTANCE_NAME + "/databases/" + DATABASE_ID
    SESSION_ID = "session-id"
    SESSION_NAME = DATABASE_NAME + "/sessions/" + SESSION_ID
    TRANSACTION_TAG = "transaction-tag"

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)


class Test_BatchBase(_BaseTest):
    def _getTargetClass(self):
        from google.cloud.spanner_v1.batch import _BatchBase

        return _BatchBase

    def _compare_values(self, result, source):
        for found, expected in zip(result, source):
            self.assertEqual(len(found), len(expected))
            for found_cell, expected_cell in zip(found, expected):
                if isinstance(expected_cell, int):
                    self.assertEqual(int(found_cell), expected_cell)
                else:
                    self.assertEqual(found_cell, expected_cell)

    def test_ctor(self):
        session = _Session()
        base = self._make_one(session)
        self.assertIs(base._session, session)
        self.assertEqual(len(base._mutations), 0)

    def test__check_state_virtual(self):
        session = _Session()
        base = self._make_one(session)
        with self.assertRaises(NotImplementedError):
            base._check_state()

    def test_insert(self):
        from google.cloud.spanner_v1 import Mutation

        session = _Session()
        base = self._make_one(session)

        base.insert(TABLE_NAME, columns=COLUMNS, values=VALUES)

        self.assertEqual(len(base._mutations), 1)
        mutation = base._mutations[0]
        self.assertIsInstance(mutation, Mutation)
        write = mutation.insert
        self.assertIsInstance(write, Mutation.Write)
        self.assertEqual(write.table, TABLE_NAME)
        self.assertEqual(write.columns, COLUMNS)
        self._compare_values(write.values, VALUES)

    def test_update(self):
        from google.cloud.spanner_v1 import Mutation

        session = _Session()
        base = self._make_one(session)

        base.update(TABLE_NAME, columns=COLUMNS, values=VALUES)

        self.assertEqual(len(base._mutations), 1)
        mutation = base._mutations[0]
        self.assertIsInstance(mutation, Mutation)
        write = mutation.update
        self.assertIsInstance(write, Mutation.Write)
        self.assertEqual(write.table, TABLE_NAME)
        self.assertEqual(write.columns, COLUMNS)
        self._compare_values(write.values, VALUES)

    def test_insert_or_update(self):
        from google.cloud.spanner_v1 import Mutation

        session = _Session()
        base = self._make_one(session)

        base.insert_or_update(TABLE_NAME, columns=COLUMNS, values=VALUES)

        self.assertEqual(len(base._mutations), 1)
        mutation = base._mutations[0]
        self.assertIsInstance(mutation, Mutation)
        write = mutation.insert_or_update
        self.assertIsInstance(write, Mutation.Write)
        self.assertEqual(write.table, TABLE_NAME)
        self.assertEqual(write.columns, COLUMNS)
        self._compare_values(write.values, VALUES)

    def test_replace(self):
        from google.cloud.spanner_v1 import Mutation

        session = _Session()
        base = self._make_one(session)

        base.replace(TABLE_NAME, columns=COLUMNS, values=VALUES)

        self.assertEqual(len(base._mutations), 1)
        mutation = base._mutations[0]
        self.assertIsInstance(mutation, Mutation)
        write = mutation.replace
        self.assertIsInstance(write, Mutation.Write)
        self.assertEqual(write.table, TABLE_NAME)
        self.assertEqual(write.columns, COLUMNS)
        self._compare_values(write.values, VALUES)

    def test_delete(self):
        from google.cloud.spanner_v1 import Mutation
        from google.cloud.spanner_v1.keyset import KeySet

        keys = [[0], [1], [2]]
        keyset = KeySet(keys=keys)
        session = _Session()
        base = self._make_one(session)

        base.delete(TABLE_NAME, keyset=keyset)

        self.assertEqual(len(base._mutations), 1)
        mutation = base._mutations[0]
        self.assertIsInstance(mutation, Mutation)
        delete = mutation.delete
        self.assertIsInstance(delete, Mutation.Delete)
        self.assertEqual(delete.table, TABLE_NAME)
        key_set_pb = delete.key_set
        self.assertEqual(len(key_set_pb.ranges), 0)
        self.assertEqual(len(key_set_pb.keys), len(keys))
        for found, expected in zip(key_set_pb.keys, keys):
            self.assertEqual([int(value) for value in found], expected)


class TestBatch(_BaseTest, OpenTelemetryBase):
    def _getTargetClass(self):
        from google.cloud.spanner_v1.batch import Batch

        return Batch

    def test_ctor(self):
        session = _Session()
        batch = self._make_one(session)
        self.assertIs(batch._session, session)

    def test_commit_already_committed(self):
        from google.cloud.spanner_v1.keyset import KeySet

        keys = [[0], [1], [2]]
        keyset = KeySet(keys=keys)
        database = _Database()
        session = _Session(database)
        batch = self._make_one(session)
        batch.committed = object()
        batch.delete(TABLE_NAME, keyset=keyset)

        with self.assertRaises(ValueError):
            batch.commit()

        self.assertNoSpans()

    def test_commit_grpc_error(self):
        from google.api_core.exceptions import Unknown
        from google.cloud.spanner_v1.keyset import KeySet

        keys = [[0], [1], [2]]
        keyset = KeySet(keys=keys)
        database = _Database()
        database.spanner_api = _FauxSpannerAPI(_rpc_error=True)
        session = _Session(database)
        batch = self._make_one(session)
        batch.delete(TABLE_NAME, keyset=keyset)

        with self.assertRaises(Unknown):
            batch.commit()

        self.assertSpanAttributes(
            "CloudSpanner.Commit",
            status=StatusCode.ERROR,
            attributes=dict(BASE_ATTRIBUTES, num_mutations=1),
        )

    def test_commit_ok(self):
        import datetime
        from google.cloud.spanner_v1 import CommitResponse
        from google.cloud.spanner_v1 import TransactionOptions
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(_commit_response=response)
        session = _Session(database)
        batch = self._make_one(session)
        batch.insert(TABLE_NAME, COLUMNS, VALUES)

        committed = batch.commit()

        self.assertEqual(committed, now)
        self.assertEqual(batch.committed, committed)

        (
            session,
            mutations,
            single_use_txn,
            request_options,
            max_commit_delay,
            metadata,
        ) = api._committed
        self.assertEqual(session, self.SESSION_NAME)
        self.assertEqual(mutations, batch._mutations)
        self.assertIsInstance(single_use_txn, TransactionOptions)
        self.assertTrue(type(single_use_txn).pb(single_use_txn).HasField("read_write"))
        self.assertEqual(
            metadata,
            [
                ("google-cloud-resource-prefix", database.name),
                ("x-goog-spanner-route-to-leader", "true"),
            ],
        )
        self.assertEqual(request_options, RequestOptions())
        self.assertEqual(max_commit_delay, None)

        self.assertSpanAttributes(
            "CloudSpanner.Commit", attributes=dict(BASE_ATTRIBUTES, num_mutations=1)
        )

    def _test_commit_with_options(
        self,
        request_options=None,
        max_commit_delay_in=None,
        exclude_txn_from_change_streams=False,
    ):
        import datetime
        from google.cloud.spanner_v1 import CommitResponse
        from google.cloud.spanner_v1 import TransactionOptions
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(_commit_response=response)
        session = _Session(database)
        batch = self._make_one(session)
        batch.transaction_tag = self.TRANSACTION_TAG
        batch.insert(TABLE_NAME, COLUMNS, VALUES)
        committed = batch.commit(
            request_options=request_options,
            max_commit_delay=max_commit_delay_in,
            exclude_txn_from_change_streams=exclude_txn_from_change_streams,
        )

        self.assertEqual(committed, now)
        self.assertEqual(batch.committed, committed)

        if type(request_options) is dict:
            expected_request_options = RequestOptions(request_options)
        else:
            expected_request_options = request_options
        expected_request_options.transaction_tag = self.TRANSACTION_TAG
        expected_request_options.request_tag = None

        (
            session,
            mutations,
            single_use_txn,
            actual_request_options,
            max_commit_delay,
            metadata,
        ) = api._committed
        self.assertEqual(session, self.SESSION_NAME)
        self.assertEqual(mutations, batch._mutations)
        self.assertIsInstance(single_use_txn, TransactionOptions)
        self.assertTrue(type(single_use_txn).pb(single_use_txn).HasField("read_write"))
        self.assertEqual(
            single_use_txn.exclude_txn_from_change_streams,
            exclude_txn_from_change_streams,
        )
        self.assertEqual(
            metadata,
            [
                ("google-cloud-resource-prefix", database.name),
                ("x-goog-spanner-route-to-leader", "true"),
            ],
        )
        self.assertEqual(actual_request_options, expected_request_options)

        self.assertSpanAttributes(
            "CloudSpanner.Commit", attributes=dict(BASE_ATTRIBUTES, num_mutations=1)
        )

        self.assertEqual(max_commit_delay_in, max_commit_delay)

    def test_commit_w_request_tag_success(self):
        request_options = RequestOptions(
            request_tag="tag-1",
        )
        self._test_commit_with_options(request_options=request_options)

    def test_commit_w_transaction_tag_success(self):
        request_options = RequestOptions(
            transaction_tag="tag-1-1",
        )
        self._test_commit_with_options(request_options=request_options)

    def test_commit_w_request_and_transaction_tag_success(self):
        request_options = RequestOptions(
            request_tag="tag-1",
            transaction_tag="tag-1-1",
        )
        self._test_commit_with_options(request_options=request_options)

    def test_commit_w_request_and_transaction_tag_dictionary_success(self):
        request_options = {"request_tag": "tag-1", "transaction_tag": "tag-1-1"}
        self._test_commit_with_options(request_options=request_options)

    def test_commit_w_incorrect_tag_dictionary_error(self):
        request_options = {"incorrect_tag": "tag-1-1"}
        with self.assertRaises(ValueError):
            self._test_commit_with_options(request_options=request_options)

    def test_commit_w_max_commit_delay(self):
        import datetime

        request_options = RequestOptions(
            request_tag="tag-1",
        )
        self._test_commit_with_options(
            request_options=request_options,
            max_commit_delay_in=datetime.timedelta(milliseconds=100),
        )

    def test_commit_w_exclude_txn_from_change_streams(self):
        request_options = RequestOptions(
            request_tag="tag-1",
        )
        self._test_commit_with_options(
            request_options=request_options, exclude_txn_from_change_streams=True
        )

    def test_context_mgr_already_committed(self):
        import datetime
        from google.cloud._helpers import UTC

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI()
        session = _Session(database)
        batch = self._make_one(session)
        batch.committed = now

        with self.assertRaises(ValueError):
            with batch:
                pass  # pragma: NO COVER

        self.assertEqual(api._committed, None)

    def test_context_mgr_success(self):
        import datetime
        from google.cloud.spanner_v1 import CommitResponse
        from google.cloud.spanner_v1 import TransactionOptions
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(_commit_response=response)
        session = _Session(database)
        batch = self._make_one(session)

        with batch:
            batch.insert(TABLE_NAME, COLUMNS, VALUES)

        self.assertEqual(batch.committed, now)

        (
            session,
            mutations,
            single_use_txn,
            request_options,
            _,
            metadata,
        ) = api._committed
        self.assertEqual(session, self.SESSION_NAME)
        self.assertEqual(mutations, batch._mutations)
        self.assertIsInstance(single_use_txn, TransactionOptions)
        self.assertTrue(type(single_use_txn).pb(single_use_txn).HasField("read_write"))
        self.assertEqual(
            metadata,
            [
                ("google-cloud-resource-prefix", database.name),
                ("x-goog-spanner-route-to-leader", "true"),
            ],
        )
        self.assertEqual(request_options, RequestOptions())

        self.assertSpanAttributes(
            "CloudSpanner.Commit", attributes=dict(BASE_ATTRIBUTES, num_mutations=1)
        )

    def test_context_mgr_failure(self):
        import datetime
        from google.cloud.spanner_v1 import CommitResponse
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(_commit_response=response)
        session = _Session(database)
        batch = self._make_one(session)

        class _BailOut(Exception):
            pass

        with self.assertRaises(_BailOut):
            with batch:
                batch.insert(TABLE_NAME, COLUMNS, VALUES)
                raise _BailOut()

        self.assertEqual(batch.committed, None)
        self.assertEqual(api._committed, None)
        self.assertEqual(len(batch._mutations), 1)


class TestMutationGroups(_BaseTest, OpenTelemetryBase):
    def _getTargetClass(self):
        from google.cloud.spanner_v1.batch import MutationGroups

        return MutationGroups

    def test_ctor(self):
        session = _Session()
        groups = self._make_one(session)
        self.assertIs(groups._session, session)

    def test_batch_write_already_committed(self):
        from google.cloud.spanner_v1.keyset import KeySet

        keys = [[0], [1], [2]]
        keyset = KeySet(keys=keys)
        database = _Database()
        database.spanner_api = _FauxSpannerAPI(_batch_write_response=[])
        session = _Session(database)
        groups = self._make_one(session)
        group = groups.group()
        group.delete(TABLE_NAME, keyset=keyset)
        groups.batch_write()
        self.assertSpanAttributes(
            "CloudSpanner.BatchWrite",
            status=StatusCode.OK,
            attributes=dict(BASE_ATTRIBUTES, num_mutation_groups=1),
        )
        assert groups.committed
        # The second call to batch_write should raise an error.
        with self.assertRaises(ValueError):
            groups.batch_write()

    def test_batch_write_grpc_error(self):
        from google.api_core.exceptions import Unknown
        from google.cloud.spanner_v1.keyset import KeySet

        keys = [[0], [1], [2]]
        keyset = KeySet(keys=keys)
        database = _Database()
        database.spanner_api = _FauxSpannerAPI(_rpc_error=True)
        session = _Session(database)
        groups = self._make_one(session)
        group = groups.group()
        group.delete(TABLE_NAME, keyset=keyset)

        with self.assertRaises(Unknown):
            groups.batch_write()

        self.assertSpanAttributes(
            "CloudSpanner.BatchWrite",
            status=StatusCode.ERROR,
            attributes=dict(BASE_ATTRIBUTES, num_mutation_groups=1),
        )

    def _test_batch_write_with_request_options(
        self, request_options=None, exclude_txn_from_change_streams=False
    ):
        import datetime
        from google.cloud.spanner_v1 import BatchWriteResponse
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.rpc.status_pb2 import Status

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        status_pb = Status(code=200)
        response = BatchWriteResponse(
            commit_timestamp=now_pb, indexes=[0], status=status_pb
        )
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(_batch_write_response=[response])
        session = _Session(database)
        groups = self._make_one(session)
        group = groups.group()
        group.insert(TABLE_NAME, COLUMNS, VALUES)

        response_iter = groups.batch_write(
            request_options,
            exclude_txn_from_change_streams=exclude_txn_from_change_streams,
        )
        self.assertEqual(len(response_iter), 1)
        self.assertEqual(response_iter[0], response)

        (
            session,
            mutation_groups,
            actual_request_options,
            metadata,
            request_exclude_txn_from_change_streams,
        ) = api._batch_request
        self.assertEqual(session, self.SESSION_NAME)
        self.assertEqual(mutation_groups, groups._mutation_groups)
        self.assertEqual(
            metadata,
            [
                ("google-cloud-resource-prefix", database.name),
                ("x-goog-spanner-route-to-leader", "true"),
            ],
        )
        if request_options is None:
            expected_request_options = RequestOptions()
        elif type(request_options) is dict:
            expected_request_options = RequestOptions(request_options)
        else:
            expected_request_options = request_options
        self.assertEqual(actual_request_options, expected_request_options)
        self.assertEqual(
            request_exclude_txn_from_change_streams, exclude_txn_from_change_streams
        )

        self.assertSpanAttributes(
            "CloudSpanner.BatchWrite",
            status=StatusCode.OK,
            attributes=dict(BASE_ATTRIBUTES, num_mutation_groups=1),
        )

    def test_batch_write_no_request_options(self):
        self._test_batch_write_with_request_options()

    def test_batch_write_w_transaction_tag_success(self):
        self._test_batch_write_with_request_options(
            RequestOptions(transaction_tag="tag-1-1")
        )

    def test_batch_write_w_transaction_tag_dictionary_success(self):
        self._test_batch_write_with_request_options({"transaction_tag": "tag-1-1"})

    def test_batch_write_w_incorrect_tag_dictionary_error(self):
        with self.assertRaises(ValueError):
            self._test_batch_write_with_request_options({"incorrect_tag": "tag-1-1"})

    def test_batch_write_w_exclude_txn_from_change_streams(self):
        self._test_batch_write_with_request_options(
            exclude_txn_from_change_streams=True
        )


class _Session(object):
    def __init__(self, database=None, name=TestBatch.SESSION_NAME):
        self._database = database
        self.name = name


class _Database(object):
    name = "testing"
    _route_to_leader_enabled = True


class _FauxSpannerAPI:
    _create_instance_conflict = False
    _instance_not_found = False
    _committed = None
    _batch_request = None
    _rpc_error = False

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def commit(
        self,
        request=None,
        metadata=None,
    ):
        from google.api_core.exceptions import Unknown

        max_commit_delay = None
        if type(request).pb(request).HasField("max_commit_delay"):
            max_commit_delay = request.max_commit_delay

        assert request.transaction_id == b""
        self._committed = (
            request.session,
            request.mutations,
            request.single_use_transaction,
            request.request_options,
            max_commit_delay,
            metadata,
        )
        if self._rpc_error:
            raise Unknown("error")
        return self._commit_response

    def batch_write(
        self,
        request=None,
        metadata=None,
    ):
        from google.api_core.exceptions import Unknown

        self._batch_request = (
            request.session,
            request.mutation_groups,
            request.request_options,
            metadata,
            request.exclude_txn_from_change_streams,
        )
        if self._rpc_error:
            raise Unknown("error")
        return self._batch_write_response
