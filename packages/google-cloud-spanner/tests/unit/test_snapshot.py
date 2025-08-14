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
from datetime import timedelta, datetime
from threading import Lock
from typing import Mapping

from google.api_core import gapic_v1
import mock
from google.api_core.exceptions import InternalServerError, Aborted

from google.cloud.spanner_admin_database_v1 import Database
from google.cloud.spanner_v1 import (
    RequestOptions,
    DirectedReadOptions,
    BeginTransactionRequest,
    TransactionOptions,
    TransactionSelector,
)
from google.cloud.spanner_v1.snapshot import _SnapshotBase
from tests._builders import (
    build_precommit_token_pb,
    build_spanner_api,
    build_session,
    build_transaction_pb,
    build_snapshot,
)
from tests._helpers import (
    OpenTelemetryBase,
    LIB_VERSION,
    StatusCode,
    HAS_OPENTELEMETRY_INSTALLED,
    enrich_with_otel_scope,
)
from google.cloud.spanner_v1._helpers import (
    _metadata_with_request_id,
    AtomicCounter,
)
from google.cloud.spanner_v1.param_types import INT64
from google.cloud.spanner_v1.request_id_header import (
    REQ_RAND_PROCESS_ID,
    build_request_id,
)
from google.api_core.retry import Retry

TABLE_NAME = "citizens"
COLUMNS = ["email", "first_name", "last_name", "age"]
SQL_QUERY = """\
SELECT first_name, last_name, age FROM citizens ORDER BY age"""
SQL_QUERY_WITH_PARAM = """
SELECT first_name, last_name, email FROM citizens WHERE age <= @max_age"""
PARAMS = {"max_age": 30}
PARAM_TYPES = {"max_age": INT64}
SQL_QUERY_WITH_BYTES_PARAM = """\
SELECT image_name FROM images WHERE @bytes IN image_data"""
PARAMS_WITH_BYTES = {"bytes": b"FACEDACE"}
RESUME_TOKEN = b"DEADBEEF"
TXN_ID = b"DEAFBEAD"
SECONDS = 3
MICROS = 123456
DURATION = timedelta(seconds=SECONDS, microseconds=MICROS)
TIMESTAMP = datetime.now()

BASE_ATTRIBUTES = {
    "db.type": "spanner",
    "db.url": "spanner.googleapis.com",
    "db.instance": "testing",
    "net.host.name": "spanner.googleapis.com",
    "gcp.client.service": "spanner",
    "gcp.client.version": LIB_VERSION,
    "gcp.client.repo": "googleapis/python-spanner",
}
enrich_with_otel_scope(BASE_ATTRIBUTES)

DIRECTED_READ_OPTIONS = {
    "include_replicas": {
        "replica_selections": [
            {
                "location": "us-west1",
                "type_": DirectedReadOptions.ReplicaSelection.Type.READ_ONLY,
            },
        ],
        "auto_failover_disabled": True,
    },
}
DIRECTED_READ_OPTIONS_FOR_CLIENT = {
    "include_replicas": {
        "replica_selections": [
            {
                "location": "us-east1",
            },
        ],
    },
}

PRECOMMIT_TOKEN_1 = build_precommit_token_pb(precommit_token=b"1", seq_num=1)
PRECOMMIT_TOKEN_2 = build_precommit_token_pb(precommit_token=b"2", seq_num=2)

# Common errors for testing.
INTERNAL_SERVER_ERROR_UNEXPECTED_EOS = InternalServerError(
    "Received unexpected EOS on DATA frame from server"
)


class _Derived(_SnapshotBase):
    """A minimally-implemented _SnapshotBase-derived class for testing"""

    # Use a simplified implementation of _build_transaction_options_pb
    # that always returns the same transaction options.
    TRANSACTION_OPTIONS = TransactionOptions()

    def _build_transaction_options_pb(self) -> TransactionOptions:
        return self.TRANSACTION_OPTIONS


class Test_restart_on_unavailable(OpenTelemetryBase):
    def build_spanner_api(self):
        from google.cloud.spanner_v1 import SpannerClient

        return mock.create_autospec(SpannerClient, instance=True)

    def _call_fut(
        self,
        derived,
        restart,
        request,
        span_name=None,
        session=None,
        attributes=None,
        metadata=None,
    ):
        from google.cloud.spanner_v1.snapshot import _restart_on_unavailable

        return _restart_on_unavailable(
            restart,
            request,
            metadata,
            span_name,
            session,
            attributes,
            transaction=derived,
            request_id_manager=None if not session else session._database,
        )

    def _make_item(self, value, resume_token=b"", metadata=None):
        return mock.Mock(
            value=value,
            resume_token=resume_token,
            metadata=metadata,
            precommit_token=None,
            _pb=None,
            spec=["value", "resume_token", "metadata", "precommit_token"],
        )

    def test_iteration_w_empty_raw(self):
        raw = _MockIterator()
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], return_value=raw)
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), [])
        restart.assert_called_once_with(
            request=request,
            metadata=[
                (
                    "x-goog-spanner-request-id",
                    f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1",
                )
            ],
        )
        self.assertNoSpans()

    def test_iteration_w_non_empty_raw(self):
        ITEMS = (self._make_item(0), self._make_item(1))
        raw = _MockIterator(*ITEMS)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], return_value=raw)
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(ITEMS))
        restart.assert_called_once_with(
            request=request,
            metadata=[
                (
                    "x-goog-spanner-request-id",
                    f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1",
                )
            ],
        )
        self.assertNoSpans()

    def test_iteration_w_raw_w_resume_token(self):
        ITEMS = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
            self._make_item(2),
            self._make_item(3),
        )
        raw = _MockIterator(*ITEMS)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], return_value=raw)
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(ITEMS))
        restart.assert_called_once_with(
            request=request,
            metadata=[
                (
                    "x-goog-spanner-request-id",
                    f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1",
                )
            ],
        )
        self.assertNoSpans()

    def test_iteration_w_raw_raising_unavailable_no_token(self):
        from google.api_core.exceptions import ServiceUnavailable

        ITEMS = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
            self._make_item(2),
        )
        before = _MockIterator(fail_after=True, error=ServiceUnavailable("testing"))
        after = _MockIterator(*ITEMS)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(ITEMS))
        self.assertEqual(len(restart.mock_calls), 2)
        self.assertEqual(request.resume_token, b"")
        self.assertNoSpans()

    def test_iteration_w_raw_raising_retryable_internal_error_no_token(self):
        ITEMS = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
            self._make_item(2),
        )
        before = _MockIterator(
            fail_after=True,
            error=INTERNAL_SERVER_ERROR_UNEXPECTED_EOS,
        )
        after = _MockIterator(*ITEMS)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(ITEMS))
        self.assertEqual(len(restart.mock_calls), 2)
        self.assertEqual(request.resume_token, b"")
        self.assertNoSpans()

    def test_iteration_w_raw_raising_non_retryable_internal_error_no_token(self):
        from google.api_core.exceptions import InternalServerError

        ITEMS = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
            self._make_item(2),
        )
        before = _MockIterator(fail_after=True, error=InternalServerError("testing"))
        after = _MockIterator(*ITEMS)
        request = mock.Mock(spec=["resume_token"])
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        with self.assertRaises(InternalServerError):
            list(resumable)
        restart.assert_called_once_with(
            request=request,
            metadata=[
                (
                    "x-goog-spanner-request-id",
                    f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1",
                )
            ],
        )
        self.assertNoSpans()

    def test_iteration_w_raw_raising_unavailable(self):
        from google.api_core.exceptions import ServiceUnavailable

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2),)  # discarded after 503
        LAST = (self._make_item(3),)
        before = _MockIterator(
            *(FIRST + SECOND), fail_after=True, error=ServiceUnavailable("testing")
        )
        after = _MockIterator(*LAST)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(FIRST + LAST))
        self.assertEqual(len(restart.mock_calls), 2)
        self.assertEqual(request.resume_token, RESUME_TOKEN)
        self.assertNoSpans()

    def test_iteration_w_raw_raising_retryable_internal_error(self):
        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2),)  # discarded after 503
        LAST = (self._make_item(3),)
        before = _MockIterator(
            *(FIRST + SECOND),
            fail_after=True,
            error=INTERNAL_SERVER_ERROR_UNEXPECTED_EOS,
        )
        after = _MockIterator(*LAST)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(FIRST + LAST))
        self.assertEqual(len(restart.mock_calls), 2)
        self.assertEqual(request.resume_token, RESUME_TOKEN)
        self.assertNoSpans()

    def test_iteration_w_raw_raising_non_retryable_internal_error(self):
        from google.api_core.exceptions import InternalServerError

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2),)  # discarded after 503
        LAST = (self._make_item(3),)
        before = _MockIterator(
            *(FIRST + SECOND), fail_after=True, error=InternalServerError("testing")
        )
        after = _MockIterator(*LAST)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        with self.assertRaises(InternalServerError):
            list(resumable)
        restart.assert_called_once_with(
            request=request,
            metadata=[
                (
                    "x-goog-spanner-request-id",
                    f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1",
                )
            ],
        )
        self.assertNoSpans()

    def test_iteration_w_raw_raising_unavailable_after_token(self):
        from google.api_core.exceptions import ServiceUnavailable

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2), self._make_item(3))
        before = _MockIterator(
            *FIRST, fail_after=True, error=ServiceUnavailable("testing")
        )
        after = _MockIterator(*SECOND)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(FIRST + SECOND))
        self.assertEqual(len(restart.mock_calls), 2)
        self.assertEqual(request.resume_token, RESUME_TOKEN)
        self.assertNoSpans()

    def test_iteration_w_raw_w_multiuse(self):
        from google.cloud.spanner_v1 import (
            ReadRequest,
        )

        FIRST = (
            self._make_item(0),
            self._make_item(1),
        )
        before = _MockIterator(*FIRST)
        request = ReadRequest(transaction=None)
        restart = mock.Mock(spec=[], return_value=before)
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        derived._multi_use = True
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(FIRST))
        self.assertEqual(len(restart.mock_calls), 1)
        begin_count = sum(
            [1 for args in restart.call_args_list if "begin" in args.kwargs.__str__()]
        )
        self.assertEqual(begin_count, 1)
        self.assertNoSpans()

    def test_iteration_w_raw_raising_unavailable_w_multiuse(self):
        from google.api_core.exceptions import ServiceUnavailable
        from google.cloud.spanner_v1 import (
            ReadRequest,
        )

        FIRST = (
            self._make_item(0),
            self._make_item(1),
        )
        SECOND = (self._make_item(2), self._make_item(3))
        before = _MockIterator(
            *FIRST, fail_after=True, error=ServiceUnavailable("testing")
        )
        after = _MockIterator(*SECOND)
        request = ReadRequest(transaction=None)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        derived._multi_use = True
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(SECOND))
        self.assertEqual(len(restart.mock_calls), 2)
        begin_count = sum(
            [1 for args in restart.call_args_list if "begin" in args.kwargs.__str__()]
        )

        # Since the transaction id was not set before the Unavailable error, the statement will be retried with inline begin.
        self.assertEqual(begin_count, 2)
        self.assertNoSpans()

    def test_iteration_w_raw_raising_unavailable_after_token_w_multiuse(self):
        from google.api_core.exceptions import ServiceUnavailable

        from google.cloud.spanner_v1 import ResultSetMetadata
        from google.cloud.spanner_v1 import (
            Transaction as TransactionPB,
            ReadRequest,
        )

        transaction_pb = TransactionPB(id=TXN_ID)
        metadata_pb = ResultSetMetadata(transaction=transaction_pb)
        FIRST = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN, metadata=metadata_pb),
        )
        SECOND = (self._make_item(2), self._make_item(3))
        before = _MockIterator(
            *FIRST, fail_after=True, error=ServiceUnavailable("testing")
        )
        after = _MockIterator(*SECOND)
        request = ReadRequest(transaction=None)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        derived._multi_use = True

        resumable = self._call_fut(derived, restart, request, session=session)

        self.assertEqual(list(resumable), list(FIRST + SECOND))
        self.assertEqual(len(restart.mock_calls), 2)
        self.assertEqual(request.resume_token, RESUME_TOKEN)
        transaction_id_selector_count = sum(
            [
                1
                for args in restart.call_args_list
                if 'id: "DEAFBEAD"' in args.kwargs.__str__()
            ]
        )

        # Statement will be retried with Transaction id.
        self.assertEqual(transaction_id_selector_count, 2)
        self.assertNoSpans()

    def test_iteration_w_raw_raising_retryable_internal_error_after_token(self):
        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2), self._make_item(3))
        before = _MockIterator(
            *FIRST,
            fail_after=True,
            error=INTERNAL_SERVER_ERROR_UNEXPECTED_EOS,
        )
        after = _MockIterator(*SECOND)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        self.assertEqual(list(resumable), list(FIRST + SECOND))
        self.assertEqual(len(restart.mock_calls), 2)
        self.assertEqual(request.resume_token, RESUME_TOKEN)
        self.assertNoSpans()

    def test_iteration_w_raw_raising_non_retryable_internal_error_after_token(self):
        from google.api_core.exceptions import InternalServerError

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2), self._make_item(3))
        before = _MockIterator(
            *FIRST, fail_after=True, error=InternalServerError("testing")
        )
        after = _MockIterator(*SECOND)
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], side_effect=[before, after])
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(derived, restart, request, session=session)
        with self.assertRaises(InternalServerError):
            list(resumable)
        restart.assert_called_once_with(
            request=request,
            metadata=[
                (
                    "x-goog-spanner-request-id",
                    f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1",
                )
            ],
        )
        self.assertNoSpans()

    def test_iteration_w_span_creation(self):
        name = "TestSpan"
        extra_atts = {"test_att": 1}
        raw = _MockIterator()
        request = mock.Mock(test="test", spec=["test", "resume_token"])
        restart = mock.Mock(spec=[], return_value=raw)
        database = _Database()
        database.spanner_api = build_spanner_api()
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        resumable = self._call_fut(
            derived, restart, request, name, _Session(_Database()), extra_atts
        )
        self.assertEqual(list(resumable), [])
        req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1"
        self.assertSpanAttributes(
            name,
            attributes=dict(
                BASE_ATTRIBUTES, test_att=1, x_goog_spanner_request_id=req_id
            ),
        )

    def test_iteration_w_multiple_span_creation(self):
        from google.api_core.exceptions import ServiceUnavailable

        if HAS_OPENTELEMETRY_INSTALLED:
            FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
            SECOND = (self._make_item(2),)  # discarded after 503
            LAST = (self._make_item(3),)
            before = _MockIterator(
                *(FIRST + SECOND), fail_after=True, error=ServiceUnavailable("testing")
            )
            after = _MockIterator(*LAST)
            request = mock.Mock(test="test", spec=["test", "resume_token"])
            restart = mock.Mock(spec=[], side_effect=[before, after])
            name = "TestSpan"
            database = _Database()
            database.spanner_api = build_spanner_api()
            session = _Session(database)
            derived = _build_snapshot_derived(session)
            resumable = self._call_fut(
                derived, restart, request, name, _Session(_Database())
            )
            self.assertEqual(list(resumable), list(FIRST + LAST))
            self.assertEqual(len(restart.mock_calls), 2)
            self.assertEqual(request.resume_token, RESUME_TOKEN)

            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 2)
            for i, span in enumerate(span_list):
                self.assertEqual(span.name, name)
                req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.{i + 1}"
                self.assertEqual(
                    dict(span.attributes),
                    dict(
                        enrich_with_otel_scope(BASE_ATTRIBUTES),
                        x_goog_spanner_request_id=req_id,
                    ),
                )


class Test_SnapshotBase(OpenTelemetryBase):
    def test_ctor(self):
        session = build_session()
        derived = _build_snapshot_derived(session=session)

        # Attributes from _SessionWrapper.
        self.assertIs(derived._session, session)

        # Attributes from _SnapshotBase.
        self.assertTrue(derived._read_only)
        self.assertFalse(derived._multi_use)
        self.assertEqual(derived._execute_sql_request_count, 0)
        self.assertEqual(derived._read_request_count, 0)
        self.assertIsNone(derived._transaction_id)
        self.assertIsNone(derived._precommit_token)
        self.assertIsInstance(derived._lock, type(Lock()))

        self.assertNoSpans()

    def test__build_transaction_selector_pb_single_use(self):
        derived = _build_snapshot_derived(multi_use=False)

        actual_selector = derived._build_transaction_selector_pb()

        expected_selector = TransactionSelector(single_use=_Derived.TRANSACTION_OPTIONS)
        self.assertEqual(actual_selector, expected_selector)

    def test__build_transaction_selector_pb_multi_use(self):
        derived = _build_snapshot_derived(multi_use=True)

        # Select new transaction.
        expected_options = _Derived.TRANSACTION_OPTIONS
        expected_selector = TransactionSelector(begin=expected_options)
        self.assertEqual(expected_selector, derived._build_transaction_selector_pb())

        # Select existing transaction.
        transaction_id = b"transaction-id"
        begin_transaction = derived._session._database.spanner_api.begin_transaction
        begin_transaction.return_value = build_transaction_pb(id=transaction_id)

        derived.begin()

        expected_selector = TransactionSelector(id=transaction_id)
        self.assertEqual(expected_selector, derived._build_transaction_selector_pb())

    def test_begin_error_not_multi_use(self):
        derived = _build_snapshot_derived(multi_use=False)

        with self.assertRaises(ValueError):
            derived.begin()

        self.assertNoSpans()

    def test_begin_error_already_begun(self):
        derived = _build_snapshot_derived(multi_use=True)
        derived.begin()

        self.reset()
        with self.assertRaises(ValueError):
            derived.begin()

        self.assertNoSpans()

    def test_begin_error_other(self):
        derived = _build_snapshot_derived(multi_use=True)

        database = derived._session._database
        begin_transaction = database.spanner_api.begin_transaction
        begin_transaction.side_effect = RuntimeError()

        with self.assertRaises(RuntimeError):
            derived.begin()

        if not HAS_OPENTELEMETRY_INSTALLED:
            return

        self.assertSpanAttributes(
            name="CloudSpanner._Derived.begin",
            status=StatusCode.ERROR,
            attributes=_build_span_attributes(database),
        )

    def test_begin_read_write(self):
        derived = _build_snapshot_derived(multi_use=True, read_only=False)

        begin_transaction = derived._session._database.spanner_api.begin_transaction
        begin_transaction.return_value = build_transaction_pb()

        self._execute_begin(derived)

    def test_begin_read_only(self):
        derived = _build_snapshot_derived(multi_use=True, read_only=True)

        begin_transaction = derived._session._database.spanner_api.begin_transaction
        begin_transaction.return_value = build_transaction_pb()

        self._execute_begin(derived)

    def test_begin_precommit_token(self):
        derived = _build_snapshot_derived(multi_use=True)

        begin_transaction = derived._session._database.spanner_api.begin_transaction
        begin_transaction.return_value = build_transaction_pb(
            precommit_token=PRECOMMIT_TOKEN_1
        )

        self._execute_begin(derived)

    def test_begin_retry_for_internal_server_error(self):
        derived = _build_snapshot_derived(multi_use=True)

        begin_transaction = derived._session._database.spanner_api.begin_transaction
        begin_transaction.side_effect = [
            INTERNAL_SERVER_ERROR_UNEXPECTED_EOS,
            build_transaction_pb(),
        ]

        self._execute_begin(derived, attempts=2)

        expected_statuses = [
            (
                "Transaction Begin Attempt Failed. Retrying",
                {"attempt": 1, "sleep_seconds": 4},
            )
        ]
        actual_statuses = self.finished_spans_events_statuses()
        self.assertEqual(expected_statuses, actual_statuses)

    def test_begin_retry_for_aborted(self):
        derived = _build_snapshot_derived(multi_use=True)

        begin_transaction = derived._session._database.spanner_api.begin_transaction
        begin_transaction.side_effect = [
            Aborted("test"),
            build_transaction_pb(),
        ]

        self._execute_begin(derived, attempts=2)

        expected_statuses = [
            (
                "Transaction Begin Attempt Failed. Retrying",
                {"attempt": 1, "sleep_seconds": 4},
            )
        ]
        actual_statuses = self.finished_spans_events_statuses()
        self.assertEqual(expected_statuses, actual_statuses)

    def _execute_begin(self, derived: _Derived, attempts: int = 1):
        """Helper for testing _SnapshotBase.begin(). Executes method and verifies
        transaction state, begin transaction API call, and span attributes and events.
        """

        session = derived._session
        database = session._database

        transaction_id = derived.begin()

        # Verify transaction state.
        begin_transaction = database.spanner_api.begin_transaction
        expected_transaction_id = begin_transaction.return_value.id or None
        expected_precommit_token = (
            begin_transaction.return_value.precommit_token or None
        )

        self.assertEqual(transaction_id, expected_transaction_id)
        self.assertEqual(derived._transaction_id, expected_transaction_id)
        self.assertEqual(derived._precommit_token, expected_precommit_token)

        # Verify begin transaction API call.
        self.assertEqual(begin_transaction.call_count, attempts)

        expected_metadata = [
            ("google-cloud-resource-prefix", database.name),
            ("x-goog-spanner-request-id", _build_request_id(database, attempts)),
        ]
        if not derived._read_only and database._route_to_leader_enabled:
            expected_metadata.insert(-1, ("x-goog-spanner-route-to-leader", "true"))

        database.spanner_api.begin_transaction.assert_called_with(
            request=BeginTransactionRequest(
                session=session.name, options=_Derived.TRANSACTION_OPTIONS
            ),
            metadata=expected_metadata,
        )

        if not HAS_OPENTELEMETRY_INSTALLED:
            return

        # Verify span attributes.
        expected_span_name = "CloudSpanner._Derived.begin"
        self.assertSpanAttributes(
            name=expected_span_name,
            attributes=_build_span_attributes(database, attempt=attempts),
        )

    def test_read_other_error(self):
        from google.cloud.spanner_v1.keyset import KeySet

        keyset = KeySet(all_=True)
        database = _Database()
        database.spanner_api = build_spanner_api()
        database.spanner_api.streaming_read.side_effect = RuntimeError()
        session = _Session(database)
        derived = _build_snapshot_derived(session)

        with self.assertRaises(RuntimeError):
            list(derived.read(TABLE_NAME, COLUMNS, keyset))

        req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1"
        self.assertSpanAttributes(
            "CloudSpanner._Derived.read",
            status=StatusCode.ERROR,
            attributes=dict(
                BASE_ATTRIBUTES,
                table_id=TABLE_NAME,
                columns=tuple(COLUMNS),
                x_goog_spanner_request_id=req_id,
            ),
        )

    def _execute_read(
        self,
        multi_use,
        first=True,
        count=0,
        partition=None,
        timeout=gapic_v1.method.DEFAULT,
        retry=gapic_v1.method.DEFAULT,
        request_options=None,
        directed_read_options=None,
        directed_read_options_at_client_level=None,
        use_multiplexed=False,
    ):
        """Helper for testing _SnapshotBase.read(). Executes method and verifies
        transaction state, begin transaction API call, and span attributes and events.
        """

        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1 import (
            PartialResultSet,
            ResultSetMetadata,
            ResultSetStats,
        )
        from google.cloud.spanner_v1 import ReadRequest
        from google.cloud.spanner_v1 import Type, StructType
        from google.cloud.spanner_v1 import TypeCode
        from google.cloud.spanner_v1.keyset import KeySet
        from google.cloud.spanner_v1._helpers import _make_value_pb

        VALUES = [["bharney", 31], ["phred", 32]]
        VALUE_PBS = [[_make_value_pb(item) for item in row] for row in VALUES]
        struct_type_pb = StructType(
            fields=[
                StructType.Field(name="name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="age", type_=Type(code=TypeCode.INT64)),
            ]
        )

        # If the transaction had not already begun, the first result
        # set will include metadata with information about the transaction.
        transaction_pb = build_transaction_pb(id=TXN_ID) if first else None
        metadata_pb = ResultSetMetadata(
            row_type=struct_type_pb,
            transaction=transaction_pb,
        )

        stats_pb = ResultSetStats(
            query_stats=Struct(fields={"rows_returned": _make_value_pb(2)})
        )

        # Precommit tokens will be included in the result sets if the transaction is on
        # a multiplexed session. Precommit tokens may be returned out of order.
        partial_result_set_1_args = {"metadata": metadata_pb}
        if use_multiplexed:
            partial_result_set_1_args["precommit_token"] = PRECOMMIT_TOKEN_2
        partial_result_set_1 = PartialResultSet(**partial_result_set_1_args)

        partial_result_set_2_args = {"stats": stats_pb}
        if use_multiplexed:
            partial_result_set_2_args["precommit_token"] = PRECOMMIT_TOKEN_1
        partial_result_set_2 = PartialResultSet(**partial_result_set_2_args)

        result_sets = [partial_result_set_1, partial_result_set_2]

        for i in range(len(result_sets)):
            result_sets[i].values.extend(VALUE_PBS[i])
        KEYS = [["bharney@example.com"], ["phred@example.com"]]
        keyset = KeySet(keys=KEYS)
        INDEX = "email-address-index"
        LIMIT = 20
        database = _Database(
            directed_read_options=directed_read_options_at_client_level
        )

        api = database.spanner_api = build_spanner_api()
        api.streaming_read.return_value = _MockIterator(*result_sets)
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        derived._multi_use = multi_use
        derived._read_request_count = count

        if not first:
            derived._transaction_id = TXN_ID

        if request_options is None:
            request_options = RequestOptions()
        elif type(request_options) is dict:
            request_options = RequestOptions(request_options)

        transaction_selector_pb = derived._build_transaction_selector_pb()

        if partition is not None:  # 'limit' and 'partition' incompatible
            result_set = derived.read(
                TABLE_NAME,
                COLUMNS,
                keyset,
                index=INDEX,
                partition=partition,
                retry=retry,
                timeout=timeout,
                request_options=request_options,
                directed_read_options=directed_read_options,
            )
        else:
            result_set = derived.read(
                TABLE_NAME,
                COLUMNS,
                keyset,
                index=INDEX,
                limit=LIMIT,
                retry=retry,
                timeout=timeout,
                request_options=request_options,
                directed_read_options=directed_read_options,
            )

        self.assertEqual(derived._read_request_count, count + 1)

        self.assertEqual(list(result_set), VALUES)
        self.assertEqual(result_set.metadata, metadata_pb)
        self.assertEqual(result_set.stats, stats_pb)

        if partition is not None:
            expected_limit = 0
        else:
            expected_limit = LIMIT

        # Transaction tag is ignored for read request.
        expected_request_options = request_options
        expected_request_options.transaction_tag = None

        expected_directed_read_options = (
            directed_read_options
            if directed_read_options is not None
            else directed_read_options_at_client_level
        )

        expected_request = ReadRequest(
            session=session.name,
            table=TABLE_NAME,
            columns=COLUMNS,
            key_set=keyset._to_pb(),
            transaction=transaction_selector_pb,
            index=INDEX,
            limit=expected_limit,
            partition_token=partition,
            request_options=expected_request_options,
            directed_read_options=expected_directed_read_options,
        )
        req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1"
        api.streaming_read.assert_called_once_with(
            request=expected_request,
            metadata=[
                ("google-cloud-resource-prefix", database.name),
                (
                    "x-goog-spanner-request-id",
                    req_id,
                ),
            ],
            retry=retry,
            timeout=timeout,
        )

        self.assertSpanAttributes(
            "CloudSpanner._Derived.read",
            attributes=dict(
                BASE_ATTRIBUTES,
                table_id=TABLE_NAME,
                columns=tuple(COLUMNS),
                x_goog_spanner_request_id=req_id,
            ),
        )

        if first:
            self.assertEqual(derived._transaction_id, TXN_ID)

        if use_multiplexed:
            self.assertEqual(derived._precommit_token, PRECOMMIT_TOKEN_2)

    def test_read_wo_multi_use(self):
        self._execute_read(multi_use=False)

    def test_read_w_request_tag_success(self):
        request_options = RequestOptions(
            request_tag="tag-1",
        )
        self._execute_read(multi_use=False, request_options=request_options)

    def test_read_w_transaction_tag_success(self):
        request_options = RequestOptions(
            transaction_tag="tag-1-1",
        )
        self._execute_read(multi_use=False, request_options=request_options)

    def test_read_w_request_and_transaction_tag_success(self):
        request_options = RequestOptions(
            request_tag="tag-1",
            transaction_tag="tag-1-1",
        )
        self._execute_read(multi_use=False, request_options=request_options)

    def test_read_w_request_and_transaction_tag_dictionary_success(self):
        request_options = {"request_tag": "tag-1", "transaction_tag": "tag-1-1"}
        self._execute_read(multi_use=False, request_options=request_options)

    def test_read_w_incorrect_tag_dictionary_error(self):
        request_options = {"incorrect_tag": "tag-1-1"}
        with self.assertRaises(ValueError):
            self._execute_read(multi_use=False, request_options=request_options)

    def test_read_wo_multi_use_w_read_request_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._execute_read(multi_use=False, count=1)

    def test_read_w_multi_use_w_first(self):
        self._execute_read(multi_use=True, first=True)

    def test_read_w_multi_use_wo_first(self):
        self._execute_read(multi_use=True, first=False)

    def test_read_w_multi_use_wo_first_w_count_gt_0(self):
        self._execute_read(multi_use=True, first=False, count=1)

    def test_read_w_multi_use_w_first_w_partition(self):
        PARTITION = b"FADEABED"
        self._execute_read(multi_use=True, first=True, partition=PARTITION)

    def test_read_w_multi_use_w_first_w_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._execute_read(multi_use=True, first=True, count=1)

    def test_read_w_timeout_param(self):
        self._execute_read(multi_use=True, first=False, timeout=2.0)

    def test_read_w_retry_param(self):
        self._execute_read(multi_use=True, first=False, retry=Retry(deadline=60))

    def test_read_w_timeout_and_retry_params(self):
        self._execute_read(
            multi_use=True, first=False, retry=Retry(deadline=60), timeout=2.0
        )

    def test_read_w_directed_read_options(self):
        self._execute_read(multi_use=False, directed_read_options=DIRECTED_READ_OPTIONS)

    def test_read_w_directed_read_options_at_client_level(self):
        self._execute_read(
            multi_use=False,
            directed_read_options_at_client_level=DIRECTED_READ_OPTIONS_FOR_CLIENT,
        )

    def test_read_w_directed_read_options_override(self):
        self._execute_read(
            multi_use=False,
            directed_read_options=DIRECTED_READ_OPTIONS,
            directed_read_options_at_client_level=DIRECTED_READ_OPTIONS_FOR_CLIENT,
        )

    def test_read_w_precommit_tokens(self):
        self._execute_read(multi_use=True, use_multiplexed=True)

    def test_execute_sql_other_error(self):
        database = _Database()
        database.spanner_api = build_spanner_api()
        database.spanner_api.execute_streaming_sql.side_effect = RuntimeError()
        session = _Session(database)
        derived = _build_snapshot_derived(session)

        with self.assertRaises(RuntimeError):
            list(derived.execute_sql(SQL_QUERY))

        self.assertEqual(derived._execute_sql_request_count, 1)

        req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1"
        self.assertSpanAttributes(
            "CloudSpanner._Derived.execute_sql",
            status=StatusCode.ERROR,
            attributes=dict(
                BASE_ATTRIBUTES,
                **{"db.statement": SQL_QUERY, "x_goog_spanner_request_id": req_id},
            ),
        )

    def _execute_sql_helper(
        self,
        multi_use,
        first=True,
        count=0,
        partition=None,
        sql_count=0,
        query_options=None,
        request_options=None,
        timeout=gapic_v1.method.DEFAULT,
        retry=gapic_v1.method.DEFAULT,
        directed_read_options=None,
        directed_read_options_at_client_level=None,
        use_multiplexed=False,
    ):
        """Helper for testing _SnapshotBase.execute_sql(). Executes method and verifies
        transaction state, begin transaction API call, and span attributes and events.
        """

        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1 import (
            PartialResultSet,
            ResultSetMetadata,
            ResultSetStats,
        )
        from google.cloud.spanner_v1 import ExecuteSqlRequest
        from google.cloud.spanner_v1 import Type, StructType
        from google.cloud.spanner_v1 import TypeCode
        from google.cloud.spanner_v1._helpers import (
            _make_value_pb,
            _merge_query_options,
        )

        VALUES = [["bharney", "rhubbyl", 31], ["phred", "phlyntstone", 32]]
        VALUE_PBS = [[_make_value_pb(item) for item in row] for row in VALUES]
        MODE = 2  # PROFILE
        struct_type_pb = StructType(
            fields=[
                StructType.Field(name="first_name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="last_name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="age", type_=Type(code=TypeCode.INT64)),
            ]
        )

        # If the transaction has not already begun, the first result set will
        # include metadata with information about the newly-begun transaction.
        transaction_pb = build_transaction_pb(id=TXN_ID) if first else None
        metadata_pb = ResultSetMetadata(
            row_type=struct_type_pb,
            transaction=transaction_pb,
        )

        stats_pb = ResultSetStats(
            query_stats=Struct(fields={"rows_returned": _make_value_pb(2)})
        )

        # Precommit tokens will be included in the result sets if the transaction is on
        # a multiplexed session. Return the precommit tokens out of order to verify that
        # the transaction tracks the one with the highest sequence number.
        partial_result_set_1_args = {"metadata": metadata_pb}
        if use_multiplexed:
            partial_result_set_1_args["precommit_token"] = PRECOMMIT_TOKEN_2
        partial_result_set_1 = PartialResultSet(**partial_result_set_1_args)

        partial_result_set_2_args = {"stats": stats_pb}
        if use_multiplexed:
            partial_result_set_2_args["precommit_token"] = PRECOMMIT_TOKEN_1
        partial_result_set_2 = PartialResultSet(**partial_result_set_2_args)

        result_sets = [partial_result_set_1, partial_result_set_2]

        for i in range(len(result_sets)):
            result_sets[i].values.extend(VALUE_PBS[i])
        iterator = _MockIterator(*result_sets)
        database = _Database(
            directed_read_options=directed_read_options_at_client_level
        )
        api = database.spanner_api = build_spanner_api()
        api.execute_streaming_sql.return_value = iterator
        session = _Session(database)
        derived = _build_snapshot_derived(session, multi_use=multi_use)
        derived._read_request_count = count
        derived._execute_sql_request_count = sql_count
        if not first:
            derived._transaction_id = TXN_ID

        if request_options is None:
            request_options = RequestOptions()
        elif type(request_options) is dict:
            request_options = RequestOptions(request_options)

        transaction_selector_pb = derived._build_transaction_selector_pb()

        result_set = derived.execute_sql(
            SQL_QUERY_WITH_PARAM,
            PARAMS,
            PARAM_TYPES,
            query_mode=MODE,
            query_options=query_options,
            request_options=request_options,
            partition=partition,
            retry=retry,
            timeout=timeout,
            directed_read_options=directed_read_options,
        )

        self.assertEqual(derived._read_request_count, count + 1)

        self.assertEqual(list(result_set), VALUES)
        self.assertEqual(result_set.metadata, metadata_pb)
        self.assertEqual(result_set.stats, stats_pb)

        expected_params = Struct(
            fields={key: _make_value_pb(value) for (key, value) in PARAMS.items()}
        )

        expected_query_options = database._instance._client._query_options
        if query_options:
            expected_query_options = _merge_query_options(
                expected_query_options, query_options
            )

        if derived._read_only:
            # Transaction tag is ignored for read only requests.
            expected_request_options = request_options
            expected_request_options.transaction_tag = None

        expected_directed_read_options = (
            directed_read_options
            if directed_read_options is not None
            else directed_read_options_at_client_level
        )

        expected_request = ExecuteSqlRequest(
            session=session.name,
            sql=SQL_QUERY_WITH_PARAM,
            transaction=transaction_selector_pb,
            params=expected_params,
            param_types=PARAM_TYPES,
            query_mode=MODE,
            query_options=expected_query_options,
            request_options=expected_request_options,
            partition_token=partition,
            seqno=sql_count,
            directed_read_options=expected_directed_read_options,
        )
        req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1"
        api.execute_streaming_sql.assert_called_once_with(
            request=expected_request,
            metadata=[
                ("google-cloud-resource-prefix", database.name),
                (
                    "x-goog-spanner-request-id",
                    req_id,
                ),
            ],
            timeout=timeout,
            retry=retry,
        )

        self.assertEqual(derived._execute_sql_request_count, sql_count + 1)

        self.assertSpanAttributes(
            "CloudSpanner._Derived.execute_sql",
            status=StatusCode.OK,
            attributes=dict(
                BASE_ATTRIBUTES,
                **{
                    "db.statement": SQL_QUERY_WITH_PARAM,
                    "x_goog_spanner_request_id": req_id,
                },
            ),
        )

        if first:
            self.assertEqual(derived._transaction_id, TXN_ID)

        if use_multiplexed:
            self.assertEqual(derived._precommit_token, PRECOMMIT_TOKEN_2)

    def test_execute_sql_wo_multi_use(self):
        self._execute_sql_helper(multi_use=False)

    def test_execute_sql_wo_multi_use_w_read_request_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._execute_sql_helper(multi_use=False, count=1)

    def test_execute_sql_w_multi_use_wo_first(self):
        self._execute_sql_helper(multi_use=True, first=False, sql_count=1)

    def test_execute_sql_w_multi_use_wo_first_w_count_gt_0(self):
        self._execute_sql_helper(multi_use=True, first=False, count=1)

    def test_execute_sql_w_multi_use_w_first(self):
        self._execute_sql_helper(multi_use=True, first=True)

    def test_execute_sql_w_multi_use_w_first_w_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._execute_sql_helper(multi_use=True, first=True, count=1)

    def test_execute_sql_w_retry(self):
        self._execute_sql_helper(multi_use=False, retry=None)

    def test_execute_sql_w_timeout(self):
        self._execute_sql_helper(multi_use=False, timeout=None)

    def test_execute_sql_w_query_options(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        self._execute_sql_helper(
            multi_use=False,
            query_options=ExecuteSqlRequest.QueryOptions(optimizer_version="3"),
        )

    def test_execute_sql_w_request_options(self):
        self._execute_sql_helper(
            multi_use=False,
            request_options=RequestOptions(
                priority=RequestOptions.Priority.PRIORITY_MEDIUM
            ),
        )

    def test_execute_sql_w_request_tag_success(self):
        request_options = RequestOptions(
            request_tag="tag-1",
        )
        self._execute_sql_helper(multi_use=False, request_options=request_options)

    def test_execute_sql_w_transaction_tag_success(self):
        request_options = RequestOptions(
            transaction_tag="tag-1-1",
        )
        self._execute_sql_helper(multi_use=False, request_options=request_options)

    def test_execute_sql_w_request_and_transaction_tag_success(self):
        request_options = RequestOptions(
            request_tag="tag-1",
            transaction_tag="tag-1-1",
        )
        self._execute_sql_helper(multi_use=False, request_options=request_options)

    def test_execute_sql_w_request_and_transaction_tag_dictionary_success(self):
        request_options = {"request_tag": "tag-1", "transaction_tag": "tag-1-1"}
        self._execute_sql_helper(multi_use=False, request_options=request_options)

    def test_execute_sql_w_incorrect_tag_dictionary_error(self):
        request_options = {"incorrect_tag": "tag-1-1"}
        with self.assertRaises(ValueError):
            self._execute_sql_helper(multi_use=False, request_options=request_options)

    def test_execute_sql_w_directed_read_options(self):
        self._execute_sql_helper(
            multi_use=False, directed_read_options=DIRECTED_READ_OPTIONS
        )

    def test_execute_sql_w_directed_read_options_at_client_level(self):
        self._execute_sql_helper(
            multi_use=False,
            directed_read_options_at_client_level=DIRECTED_READ_OPTIONS_FOR_CLIENT,
        )

    def test_execute_sql_w_directed_read_options_override(self):
        self._execute_sql_helper(
            multi_use=False,
            directed_read_options=DIRECTED_READ_OPTIONS,
            directed_read_options_at_client_level=DIRECTED_READ_OPTIONS_FOR_CLIENT,
        )

    def test_execute_sql_w_precommit_tokens(self):
        self._execute_sql_helper(multi_use=True, use_multiplexed=True)

    def _partition_read_helper(
        self,
        multi_use,
        w_txn,
        size=None,
        max_partitions=None,
        index=None,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
    ):
        from google.cloud.spanner_v1.keyset import KeySet
        from google.cloud.spanner_v1 import Partition
        from google.cloud.spanner_v1 import PartitionOptions
        from google.cloud.spanner_v1 import PartitionReadRequest
        from google.cloud.spanner_v1 import PartitionResponse
        from google.cloud.spanner_v1 import Transaction

        keyset = KeySet(all_=True)
        new_txn_id = b"ABECAB91"
        token_1 = b"FACE0FFF"
        token_2 = b"BADE8CAF"
        response = PartitionResponse(
            partitions=[
                Partition(partition_token=token_1),
                Partition(partition_token=token_2),
            ],
            transaction=Transaction(id=new_txn_id),
        )
        database = _Database()
        api = database.spanner_api = build_spanner_api()
        api.partition_read.return_value = response
        session = _Session(database)
        derived = _build_snapshot_derived(session)
        derived._multi_use = multi_use

        if w_txn:
            derived._transaction_id = TXN_ID

        transaction_selector_pb = derived._build_transaction_selector_pb()

        tokens = list(
            derived.partition_read(
                TABLE_NAME,
                COLUMNS,
                keyset,
                index=index,
                partition_size_bytes=size,
                max_partitions=max_partitions,
                retry=retry,
                timeout=timeout,
            )
        )

        self.assertEqual(tokens, [token_1, token_2])

        expected_partition_options = PartitionOptions(
            partition_size_bytes=size, max_partitions=max_partitions
        )

        expected_request = PartitionReadRequest(
            session=session.name,
            table=TABLE_NAME,
            columns=COLUMNS,
            key_set=keyset._to_pb(),
            transaction=transaction_selector_pb,
            index=index,
            partition_options=expected_partition_options,
        )
        req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1"
        api.partition_read.assert_called_once_with(
            request=expected_request,
            metadata=[
                ("google-cloud-resource-prefix", database.name),
                ("x-goog-spanner-route-to-leader", "true"),
                (
                    "x-goog-spanner-request-id",
                    req_id,
                ),
            ],
            retry=retry,
            timeout=timeout,
        )

        want_span_attributes = dict(
            BASE_ATTRIBUTES,
            table_id=TABLE_NAME,
            columns=tuple(COLUMNS),
            x_goog_spanner_request_id=req_id,
        )
        if index:
            want_span_attributes["index"] = index
        self.assertSpanAttributes(
            "CloudSpanner._Derived.partition_read",
            status=StatusCode.OK,
            attributes=want_span_attributes,
        )

    def test_partition_read_single_use_raises(self):
        with self.assertRaises(ValueError):
            self._partition_read_helper(multi_use=False, w_txn=True)

    def test_partition_read_wo_existing_transaction_raises(self):
        with self.assertRaises(ValueError):
            self._partition_read_helper(multi_use=True, w_txn=False)

    def test_partition_read_other_error(self):
        from google.cloud.spanner_v1.keyset import KeySet

        keyset = KeySet(all_=True)
        database = _Database()
        database.spanner_api = build_spanner_api()
        database.spanner_api.partition_read.side_effect = RuntimeError()
        session = _Session(database)
        derived = _build_snapshot_derived(session, multi_use=True)
        derived._transaction_id = TXN_ID

        with self.assertRaises(RuntimeError):
            list(derived.partition_read(TABLE_NAME, COLUMNS, keyset))

        req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1"
        self.assertSpanAttributes(
            "CloudSpanner._Derived.partition_read",
            status=StatusCode.ERROR,
            attributes=dict(
                BASE_ATTRIBUTES,
                table_id=TABLE_NAME,
                columns=tuple(COLUMNS),
                x_goog_spanner_request_id=req_id,
            ),
        )

    def test_partition_read_w_retry(self):
        from google.cloud.spanner_v1.keyset import KeySet
        from google.cloud.spanner_v1 import Partition
        from google.cloud.spanner_v1 import PartitionResponse
        from google.cloud.spanner_v1 import Transaction

        keyset = KeySet(all_=True)
        database = _Database()
        api = database.spanner_api = build_spanner_api()
        new_txn_id = b"ABECAB91"
        token_1 = b"FACE0FFF"
        token_2 = b"BADE8CAF"
        response = PartitionResponse(
            partitions=[
                Partition(partition_token=token_1),
                Partition(partition_token=token_2),
            ],
            transaction=Transaction(id=new_txn_id),
        )
        database.spanner_api.partition_read.side_effect = [
            INTERNAL_SERVER_ERROR_UNEXPECTED_EOS,
            response,
        ]

        session = _Session(database)
        derived = _build_snapshot_derived(session)
        derived._multi_use = True
        derived._transaction_id = TXN_ID

        list(derived.partition_read(TABLE_NAME, COLUMNS, keyset))

        self.assertEqual(api.partition_read.call_count, 2)

    def test_partition_read_ok_w_index_no_options(self):
        self._partition_read_helper(multi_use=True, w_txn=True, index="index")

    def test_partition_read_ok_w_size(self):
        self._partition_read_helper(multi_use=True, w_txn=True, size=2000)

    def test_partition_read_ok_w_max_partitions(self):
        self._partition_read_helper(multi_use=True, w_txn=True, max_partitions=4)

    def test_partition_read_ok_w_timeout_param(self):
        self._partition_read_helper(multi_use=True, w_txn=True, timeout=2.0)

    def test_partition_read_ok_w_retry_param(self):
        self._partition_read_helper(
            multi_use=True, w_txn=True, retry=Retry(deadline=60)
        )

    def test_partition_read_ok_w_timeout_and_retry_params(self):
        self._partition_read_helper(
            multi_use=True, w_txn=True, retry=Retry(deadline=60), timeout=2.0
        )

    def _partition_query_helper(
        self,
        multi_use,
        w_txn,
        size=None,
        max_partitions=None,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
    ):
        """Helper for testing _SnapshotBase.partition_query(). Executes method and verifies
        transaction state, begin transaction API call, and span attributes and events.
        """

        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1 import Partition
        from google.cloud.spanner_v1 import PartitionOptions
        from google.cloud.spanner_v1 import PartitionQueryRequest
        from google.cloud.spanner_v1 import PartitionResponse
        from google.cloud.spanner_v1 import Transaction
        from google.cloud.spanner_v1._helpers import _make_value_pb

        new_txn_id = b"ABECAB91"
        token_1 = b"FACE0FFF"
        token_2 = b"BADE8CAF"
        response = PartitionResponse(
            partitions=[
                Partition(partition_token=token_1),
                Partition(partition_token=token_2),
            ],
            transaction=Transaction(id=new_txn_id),
        )
        database = _Database()
        api = database.spanner_api = build_spanner_api()
        api.partition_query.return_value = response
        session = _Session(database)
        derived = _build_snapshot_derived(session, multi_use=multi_use)
        if w_txn:
            derived._transaction_id = TXN_ID

        transaction_selector_pb = derived._build_transaction_selector_pb()

        tokens = list(
            derived.partition_query(
                SQL_QUERY_WITH_PARAM,
                PARAMS,
                PARAM_TYPES,
                partition_size_bytes=size,
                max_partitions=max_partitions,
                retry=retry,
                timeout=timeout,
            )
        )

        self.assertEqual(tokens, [token_1, token_2])

        expected_params = Struct(
            fields={key: _make_value_pb(value) for (key, value) in PARAMS.items()}
        )

        expected_partition_options = PartitionOptions(
            partition_size_bytes=size, max_partitions=max_partitions
        )

        expected_request = PartitionQueryRequest(
            session=session.name,
            sql=SQL_QUERY_WITH_PARAM,
            transaction=transaction_selector_pb,
            params=expected_params,
            param_types=PARAM_TYPES,
            partition_options=expected_partition_options,
        )
        req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1"
        api.partition_query.assert_called_once_with(
            request=expected_request,
            metadata=[
                ("google-cloud-resource-prefix", database.name),
                ("x-goog-spanner-route-to-leader", "true"),
                (
                    "x-goog-spanner-request-id",
                    req_id,
                ),
            ],
            retry=retry,
            timeout=timeout,
        )

        self.assertSpanAttributes(
            "CloudSpanner._Derived.partition_query",
            status=StatusCode.OK,
            attributes=dict(
                BASE_ATTRIBUTES,
                **{
                    "db.statement": SQL_QUERY_WITH_PARAM,
                    "x_goog_spanner_request_id": req_id,
                },
            ),
        )

    def test_partition_query_other_error(self):
        database = _Database()
        database.spanner_api = build_spanner_api()
        database.spanner_api.partition_query.side_effect = RuntimeError()
        session = _Session(database)
        derived = _build_snapshot_derived(session, multi_use=True)
        derived._transaction_id = TXN_ID

        with self.assertRaises(RuntimeError):
            list(derived.partition_query(SQL_QUERY))

        req_id = f"1.{REQ_RAND_PROCESS_ID}.{database._nth_client_id}.{database._channel_id}.1.1"
        self.assertSpanAttributes(
            "CloudSpanner._Derived.partition_query",
            status=StatusCode.ERROR,
            attributes=dict(
                BASE_ATTRIBUTES,
                **{"db.statement": SQL_QUERY, "x_goog_spanner_request_id": req_id},
            ),
        )

    def test_partition_query_single_use_raises(self):
        with self.assertRaises(ValueError):
            self._partition_query_helper(multi_use=False, w_txn=True)

    def test_partition_query_wo_transaction_raises(self):
        with self.assertRaises(ValueError):
            self._partition_query_helper(multi_use=True, w_txn=False)

    def test_partition_query_ok_w_index_no_options(self):
        self._partition_query_helper(multi_use=True, w_txn=True)

    def test_partition_query_ok_w_size(self):
        self._partition_query_helper(multi_use=True, w_txn=True, size=2000)

    def test_partition_query_ok_w_max_partitions(self):
        self._partition_query_helper(multi_use=True, w_txn=True, max_partitions=4)

    def test_partition_query_ok_w_timeout_param(self):
        self._partition_query_helper(multi_use=True, w_txn=True, timeout=2.0)

    def test_partition_query_ok_w_retry_param(self):
        self._partition_query_helper(
            multi_use=True, w_txn=True, retry=Retry(deadline=30)
        )

    def test_partition_query_ok_w_timeout_and_retry_params(self):
        self._partition_query_helper(
            multi_use=True, w_txn=True, retry=Retry(deadline=60), timeout=2.0
        )


class TestSnapshot(OpenTelemetryBase):
    PROJECT_ID = "project-id"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID
    DATABASE_ID = "database-id"
    DATABASE_NAME = INSTANCE_NAME + "/databases/" + DATABASE_ID
    SESSION_ID = "session-id"
    SESSION_NAME = DATABASE_NAME + "/sessions/" + SESSION_ID

    def _getTargetClass(self):
        from google.cloud.spanner_v1.snapshot import Snapshot

        return Snapshot

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _makeDuration(self, seconds=1, microseconds=0):
        import datetime

        return datetime.timedelta(seconds=seconds, microseconds=microseconds)

    def test_ctor_defaults(self):
        session = build_session()
        snapshot = build_snapshot(session=session)

        # Attributes from _SessionWrapper.
        self.assertIs(snapshot._session, session)

        # Attributes from _SnapshotBase.
        self.assertTrue(snapshot._read_only)
        self.assertFalse(snapshot._multi_use)
        self.assertEqual(snapshot._execute_sql_request_count, 0)
        self.assertEqual(snapshot._read_request_count, 0)
        self.assertIsNone(snapshot._transaction_id)
        self.assertIsNone(snapshot._precommit_token)
        self.assertIsInstance(snapshot._lock, type(Lock()))

        # Attributes from Snapshot.
        self.assertTrue(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertIsNone(snapshot._exact_staleness)

    def test_ctor_w_multiple_options(self):
        with self.assertRaises(ValueError):
            build_snapshot(read_timestamp=datetime.min, max_staleness=timedelta())

    def test_ctor_w_read_timestamp(self):
        snapshot = build_snapshot(read_timestamp=TIMESTAMP)
        self.assertEqual(snapshot._read_timestamp, TIMESTAMP)

    def test_ctor_w_min_read_timestamp(self):
        snapshot = build_snapshot(min_read_timestamp=TIMESTAMP)
        self.assertEqual(snapshot._min_read_timestamp, TIMESTAMP)

    def test_ctor_w_max_staleness(self):
        snapshot = build_snapshot(max_staleness=DURATION)
        self.assertEqual(snapshot._max_staleness, DURATION)

    def test_ctor_w_exact_staleness(self):
        snapshot = build_snapshot(exact_staleness=DURATION)
        self.assertEqual(snapshot._exact_staleness, DURATION)

    def test_ctor_w_multi_use(self):
        snapshot = build_snapshot(multi_use=True)
        self.assertTrue(snapshot._multi_use)

    def test_ctor_w_multi_use_and_read_timestamp(self):
        snapshot = build_snapshot(multi_use=True, read_timestamp=TIMESTAMP)
        self.assertTrue(snapshot._multi_use)
        self.assertEqual(snapshot._read_timestamp, TIMESTAMP)

    def test_ctor_w_multi_use_and_min_read_timestamp(self):
        with self.assertRaises(ValueError):
            build_snapshot(multi_use=True, min_read_timestamp=TIMESTAMP)

    def test_ctor_w_multi_use_and_max_staleness(self):
        with self.assertRaises(ValueError):
            build_snapshot(multi_use=True, max_staleness=DURATION)

    def test_ctor_w_multi_use_and_exact_staleness(self):
        snapshot = build_snapshot(multi_use=True, exact_staleness=DURATION)
        self.assertTrue(snapshot._multi_use)
        self.assertEqual(snapshot._exact_staleness, DURATION)

    def test__build_transaction_options_strong(self):
        snapshot = build_snapshot()
        options = snapshot._build_transaction_options_pb()

        self.assertEqual(
            options,
            TransactionOptions(
                read_only=TransactionOptions.ReadOnly(
                    strong=True, return_read_timestamp=True
                )
            ),
        )

    def test__build_transaction_options_w_read_timestamp(self):
        snapshot = build_snapshot(read_timestamp=TIMESTAMP)
        options = snapshot._build_transaction_options_pb()

        self.assertEqual(
            options,
            TransactionOptions(
                read_only=TransactionOptions.ReadOnly(
                    read_timestamp=TIMESTAMP, return_read_timestamp=True
                )
            ),
        )

    def test__build_transaction_options_w_min_read_timestamp(self):
        snapshot = build_snapshot(min_read_timestamp=TIMESTAMP)
        options = snapshot._build_transaction_options_pb()

        self.assertEqual(
            options,
            TransactionOptions(
                read_only=TransactionOptions.ReadOnly(
                    min_read_timestamp=TIMESTAMP, return_read_timestamp=True
                )
            ),
        )

    def test__build_transaction_options_w_max_staleness(self):
        snapshot = build_snapshot(max_staleness=DURATION)
        options = snapshot._build_transaction_options_pb()

        self.assertEqual(
            options,
            TransactionOptions(
                read_only=TransactionOptions.ReadOnly(
                    max_staleness=DURATION, return_read_timestamp=True
                )
            ),
        )

    def test__build_transaction_options_w_exact_staleness(self):
        snapshot = build_snapshot(exact_staleness=DURATION)
        options = snapshot._build_transaction_options_pb()

        self.assertEqual(
            options,
            TransactionOptions(
                read_only=TransactionOptions.ReadOnly(
                    exact_staleness=DURATION, return_read_timestamp=True
                )
            ),
        )


class _Client(object):
    NTH_CLIENT = AtomicCounter()

    def __init__(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        self._query_options = ExecuteSqlRequest.QueryOptions(optimizer_version="1")
        self._nth_client_id = _Client.NTH_CLIENT.increment()
        self._nth_request = AtomicCounter()

    @property
    def _next_nth_request(self):
        return self._nth_request.increment()


class _Instance(object):
    def __init__(self):
        self._client = _Client()


class _Database(object):
    def __init__(self, directed_read_options=None):
        self.name = "testing"
        self._nth_request = 0
        self._instance = _Instance()
        self._route_to_leader_enabled = True
        self._directed_read_options = directed_read_options

    @property
    def observability_options(self):
        return dict(db_name=self.name)

    @property
    def _next_nth_request(self):
        self._nth_request += 1
        return self._nth_request

    @property
    def _nth_client_id(self):
        return 1

    def metadata_with_request_id(
        self, nth_request, nth_attempt, prior_metadata=[], span=None
    ):
        return _metadata_with_request_id(
            self._nth_client_id,
            self._channel_id,
            nth_request,
            nth_attempt,
            prior_metadata,
            span,
        )

    @property
    def _channel_id(self):
        return 1


class _Session(object):
    def __init__(self, database=None, name=TestSnapshot.SESSION_NAME):
        self._database = database
        self.name = name

    @property
    def session_id(self):
        return self.name


class _MockIterator(object):
    def __init__(self, *values, **kw):
        self._iter_values = iter(values)
        self._fail_after = kw.pop("fail_after", False)
        self._error = kw.pop("error", Exception)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._iter_values)
        except StopIteration:
            if self._fail_after:
                raise self._error
            raise

    next = __next__


def _build_snapshot_derived(session=None, multi_use=False, read_only=True) -> _Derived:
    """Builds and returns an instance of a minimally-
    implemented _Derived class for testing."""

    session = session or build_session()
    if session.session_id is None:
        session._session_id = "session-id"

    derived = _Derived(session=session)
    derived._multi_use = multi_use
    derived._read_only = read_only

    return derived


def _build_span_attributes(database: Database, attempt: int = 1) -> Mapping[str, str]:
    """Builds the attributes for spans using the given database and extra attributes."""

    return enrich_with_otel_scope(
        {
            "db.type": "spanner",
            "db.url": "spanner.googleapis.com",
            "db.instance": database.name,
            "net.host.name": "spanner.googleapis.com",
            "gcp.client.service": "spanner",
            "gcp.client.version": LIB_VERSION,
            "gcp.client.repo": "googleapis/python-spanner",
            "x_goog_spanner_request_id": _build_request_id(database, attempt),
        }
    )


def _build_request_id(database: Database, attempt: int) -> str:
    """Builds a request ID for an Spanner Client API request with the given database and attempt number."""

    client = database._instance._client
    return build_request_id(
        client_id=client._nth_client_id,
        channel_id=database._channel_id,
        nth_request=client._nth_request.value,
        attempt=attempt,
    )
