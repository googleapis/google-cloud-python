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

"""Model a set of read-only queries to a database as a snapshot."""
__CROSS_SYNC_OUTPUT__ = "google.cloud.spanner_v1.snapshot"
import functools
from typing import List, Optional, Union

from google.api_core import gapic_v1
from google.api_core.exceptions import (
    Aborted,
    InternalServerError,
    InvalidArgument,
    ServiceUnavailable,
)
from google.protobuf.struct_pb2 import Struct

from google.cloud.aio._cross_sync import CrossSync
from google.cloud.spanner_v1._async._helpers import _retry
from google.cloud.spanner_v1._async.streamed import StreamedResultSet
from google.cloud.spanner_v1._helpers import (
    AtomicCounter,
    _augment_error_with_request_id,
    _check_rst_stream_error,
    _make_value_pb,
    _merge_query_options,
    _metadata_with_leader_aware_routing,
    _metadata_with_prefix,
    _SessionWrapper,
    _validate_client_context,
    _merge_client_context,
    _merge_request_options,
)
from google.cloud.spanner_v1._opentelemetry_tracing import add_span_event, trace_call
from google.cloud.spanner_v1.metrics.metrics_capture import MetricsCapture
from google.cloud.spanner_v1.types import MultiplexedSessionPrecommitToken
from google.cloud.spanner_v1.types.mutation import Mutation
from google.cloud.spanner_v1.types.result_set import PartialResultSet, ResultSet
from google.cloud.spanner_v1.types.spanner import (
    BeginTransactionRequest,
    ExecuteSqlRequest,
    PartitionOptions,
    PartitionQueryRequest,
    PartitionReadRequest,
    ReadRequest,
    RequestOptions,
)
from google.cloud.spanner_v1.types.transaction import (
    Transaction,
    TransactionOptions,
    TransactionSelector,
)

_STREAM_RESUMPTION_INTERNAL_ERROR_MESSAGES = (
    "RST_STREAM",
    "Received unexpected EOS on DATA frame from server",
)


@CrossSync.convert
async def _restart_on_unavailable(
    method,
    request,
    metadata=None,
    trace_name=None,
    session=None,
    attributes=None,
    transaction=None,
    transaction_selector=None,
    observability_options=None,
    request_id_manager=None,
    resource_info=None,
):
    """Restart iteration after :exc:`.ServiceUnavailable`.

    :type method: callable
    :param method: function returning iterator

    :type request: proto
    :param request: request proto to call the method with

    :type transaction: :class:`google.cloud.spanner_v1.snapshot._SnapshotBase`
    :param transaction: Snapshot or Transaction class object based on the type of transaction

    :type transaction_selector: :class:`transaction_pb2.TransactionSelector`
    :param transaction_selector: Transaction selector object to be used in request if transaction is not passed,
    if both transaction_selector and transaction are passed, then transaction is given priority.
    """

    resume_token: bytes = b""
    item_buffer: List[PartialResultSet] = []

    if transaction is not None:
        transaction_selector = transaction._build_transaction_selector_pb()
    elif transaction_selector is None:
        raise InvalidArgument(
            "Either transaction or transaction_selector should be set"
        )

    request.transaction = transaction_selector
    iterator = None
    attempt = 1
    nth_request = getattr(request_id_manager, "_next_nth_request", 0)
    current_request_id = None

    while True:
        try:
            # Get results iterator.
            if iterator is None:
                with trace_call(
                    trace_name,
                    session,
                    attributes,
                    observability_options=observability_options,
                    metadata=metadata,
                ) as span, MetricsCapture(resource_info):
                    (
                        call_metadata,
                        current_request_id,
                    ) = request_id_manager.metadata_and_request_id(
                        nth_request,
                        attempt,
                        metadata,
                        span,
                    )
                    iterator = await CrossSync.run_if_async(
                        method,
                        request=request,
                        metadata=call_metadata,
                    )

            # Add items from iterator to buffer.
            item: PartialResultSet
            async for item in iterator:
                item_buffer.append(item)

                # Update the transaction from the response.
                if transaction is not None:
                    transaction._update_for_result_set_pb(item)
                if (
                    item._pb is not None
                    and item._pb.HasField("precommit_token")
                    and transaction is not None
                ):
                    await transaction._update_for_precommit_token_pb(
                        item.precommit_token
                    )

                if item.resume_token:
                    resume_token = item.resume_token
                    break

        except ServiceUnavailable:
            del item_buffer[:]
            request.resume_token = resume_token
            if transaction is not None:
                transaction_selector = transaction._build_transaction_selector_pb()
            request.transaction = transaction_selector
            attempt += 1
            iterator = None
            continue

        except InternalServerError as exc:
            resumable_error = any(
                resumable_message in exc.message
                for resumable_message in _STREAM_RESUMPTION_INTERNAL_ERROR_MESSAGES
            )
            if not resumable_error:
                raise _augment_error_with_request_id(exc, current_request_id)
            del item_buffer[:]
            request.resume_token = resume_token
            if transaction is not None:
                transaction_selector = transaction._build_transaction_selector_pb()
            attempt += 1
            request.transaction = transaction_selector
            iterator = None
            continue

        except Exception as exc:
            # Augment any other exception with the request ID
            raise _augment_error_with_request_id(exc, current_request_id)

        if len(item_buffer) == 0:
            break

        for item in item_buffer:
            yield item

        del item_buffer[:]


class _SnapshotBase(_SessionWrapper):
    """Base class for Snapshot.

    Allows reuse of API request methods with different transaction selector.

    :type session: :class:`~google.cloud.spanner_v1.session.Session`
    :param session: the session used to perform transaction operations.
    """

    _read_only: bool = True
    _multi_use: bool = False

    def __init__(self, session, client_context=None):
        super().__init__(session)
        self._client_context = _validate_client_context(client_context)
        self._execute_sql_request_count: int = 0
        self._read_request_count: int = 0
        self._transaction_id: Optional[bytes] = None
        self._precommit_token: Optional[MultiplexedSessionPrecommitToken] = None
        self._lock: CrossSync.Lock = CrossSync.Lock()

    @property
    def _resource_info(self):
        """Resource information for metrics labels."""
        database = self._session._database
        return {
            "project": database._instance._client.project,
            "instance": database._instance.instance_id,
            "database": database.database_id,
        }

    @CrossSync.convert
    async def begin(self) -> bytes:
        """Begins a transaction on the database.

        :rtype: bytes
        :returns: identifier for the transaction.

        :raises ValueError: if the transaction has already begun.
        """
        return await self._begin_transaction()

    @CrossSync.convert
    @CrossSync.convert
    async def read(
        self,
        table,
        columns,
        keyset,
        index="",
        limit=0,
        partition=None,
        request_options=None,
        data_boost_enabled=False,
        directed_read_options=None,
        *,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
        column_info=None,
        lazy_decode=False,
    ):
        """Perform a ``StreamingRead`` API request for rows in a table."""
        if self._read_request_count > 0:
            if not self._multi_use:
                raise ValueError("Cannot re-use single-use snapshot.")
            if self._transaction_id is None:
                raise ValueError("Transaction has not begun.")

        session = self._session
        database = session._database
        api = database.spanner_api

        metadata = _metadata_with_prefix(database.name)
        if not self._read_only and database._route_to_leader_enabled:
            metadata.append(
                _metadata_with_leader_aware_routing(database._route_to_leader_enabled)
            )

        client_context = _merge_client_context(
            database._instance._client._client_context, self._client_context
        )
        request_options = _merge_request_options(request_options, client_context)

        if request_options is None:
            request_options = RequestOptions()
        elif type(request_options) is dict:
            request_options = RequestOptions(request_options)

        if self._read_only:
            request_options.transaction_tag = None
            if (
                directed_read_options is None
                and database._directed_read_options is not None
            ):
                directed_read_options = database._directed_read_options
        elif self.transaction_tag is not None:
            request_options.transaction_tag = self.transaction_tag

        read_request = ReadRequest(
            session=session.name,
            table=table,
            columns=columns,
            key_set=keyset._to_pb(),
            index=index,
            limit=limit,
            partition_token=partition,
            request_options=request_options,
            data_boost_enabled=data_boost_enabled,
            directed_read_options=directed_read_options,
        )

        streaming_read_method = functools.partial(
            api.streaming_read,
            request=read_request,
            metadata=metadata,
            retry=retry,
            timeout=timeout,
        )

        return await self._get_streamed_result_set(
            method=streaming_read_method,
            request=read_request,
            metadata=metadata,
            trace_attributes={
                "table_id": table,
                "columns": columns,
                "request_options": request_options,
            },
            column_info=column_info,
            lazy_decode=lazy_decode,
        )

    @CrossSync.convert
    @CrossSync.convert
    async def execute_sql(
        self,
        sql,
        params=None,
        param_types=None,
        query_mode=None,
        query_options=None,
        request_options=None,
        last_statement=False,
        partition=None,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
        data_boost_enabled=False,
        directed_read_options=None,
        column_info=None,
        lazy_decode=False,
    ):
        """Perform an ``ExecuteStreamingSql`` API request."""
        if self._read_request_count > 0:
            if not self._multi_use:
                raise ValueError("Cannot re-use single-use snapshot.")
            if self._transaction_id is None:
                raise ValueError("Transaction has not begun.")

        if params is not None:
            params_pb = Struct(
                fields={key: _make_value_pb(value) for key, value in params.items()}
            )
        else:
            params_pb = {}

        session = self._session
        database = session._database
        api = database.spanner_api

        metadata = _metadata_with_prefix(database.name)
        if not self._read_only and database._route_to_leader_enabled:
            metadata.append(
                _metadata_with_leader_aware_routing(database._route_to_leader_enabled)
            )

        default_query_options = database._instance._client._query_options
        query_options = _merge_query_options(default_query_options, query_options)

        client_context = _merge_client_context(
            database._instance._client._client_context, self._client_context
        )
        request_options = _merge_request_options(request_options, client_context)

        if request_options is None:
            request_options = RequestOptions()
        elif type(request_options) is dict:
            request_options = RequestOptions(request_options)

        if self._read_only:
            request_options.transaction_tag = None
            if (
                directed_read_options is None
                and database._directed_read_options is not None
            ):
                directed_read_options = database._directed_read_options
        elif self.transaction_tag is not None:
            request_options.transaction_tag = self.transaction_tag

        execute_sql_request = ExecuteSqlRequest(
            session=session.name,
            sql=sql,
            params=params_pb,
            param_types=param_types,
            query_mode=query_mode,
            partition_token=partition,
            seqno=self._execute_sql_request_count,
            query_options=query_options,
            request_options=request_options,
            last_statement=last_statement,
            data_boost_enabled=data_boost_enabled,
            directed_read_options=directed_read_options,
        )

        execute_streaming_sql_method = functools.partial(
            api.execute_streaming_sql,
            request=execute_sql_request,
            metadata=metadata,
            retry=retry,
            timeout=timeout,
        )

        return await self._get_streamed_result_set(
            method=execute_streaming_sql_method,
            request=execute_sql_request,
            metadata=metadata,
            trace_attributes={"db.statement": sql, "request_options": request_options},
            column_info=column_info,
            lazy_decode=lazy_decode,
        )

    @CrossSync.convert
    async def _get_streamed_result_set(
        self, method, request, metadata, trace_attributes, column_info, lazy_decode
    ):
        """Returns the streamed result set for a read or execute SQL request."""
        session = self._session
        database = session._database

        is_execute_sql_request = isinstance(request, ExecuteSqlRequest)
        trace_method_name = "execute_sql" if is_execute_sql_request else "read"
        trace_name = f"CloudSpanner.{type(self).__name__}.{trace_method_name}"

        is_inline_begin = False
        if self._transaction_id is None:
            is_inline_begin = True
            await self._lock.acquire()

        try:
            iterator = _restart_on_unavailable(
                method=method,
                request=request,
                session=session,
                metadata=metadata,
                trace_name=trace_name,
                attributes=trace_attributes,
                transaction=self,
                observability_options=getattr(database, "observability_options", None),
                request_id_manager=database,
                resource_info=self._resource_info,
            )

            if is_execute_sql_request:
                self._execute_sql_request_count += 1

            self._read_request_count += 1

            streamed_result_set_args = {
                "response_iterator": iterator,
                "column_info": column_info,
                "lazy_decode": lazy_decode,
            }

            if self._multi_use:
                streamed_result_set_args["source"] = self

            return StreamedResultSet(**streamed_result_set_args)
        finally:
            if is_inline_begin:
                self._lock.release()

    @CrossSync.convert
    async def partition_read(
        self,
        table,
        columns,
        keyset,
        index="",
        partition_size_bytes=None,
        max_partitions=None,
        *,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
    ):
        """Perform a ``PartitionRead`` API request for rows in a table."""
        if self._transaction_id is None:
            raise ValueError("Transaction has not begun.")
        if not self._multi_use:
            raise ValueError("Cannot partition a single-use transaction.")

        session = self._session
        database = session._database
        api = database.spanner_api

        metadata = _metadata_with_prefix(database.name)
        if database._route_to_leader_enabled:
            metadata.append(
                _metadata_with_leader_aware_routing(database._route_to_leader_enabled)
            )

        transaction = self._build_transaction_selector_pb()
        partition_options = PartitionOptions(
            partition_size_bytes=partition_size_bytes, max_partitions=max_partitions
        )

        partition_read_request = PartitionReadRequest(
            session=session.name,
            table=table,
            columns=columns,
            key_set=keyset._to_pb(),
            transaction=transaction,
            index=index,
            partition_options=partition_options,
        )

        trace_attributes = {"table_id": table, "columns": columns}
        can_include_index = index != "" and index is not None
        if can_include_index:
            trace_attributes["index"] = index

        with trace_call(
            f"CloudSpanner.{type(self).__name__}.partition_read",
            session,
            extra_attributes=trace_attributes,
            observability_options=getattr(database, "observability_options", None),
            metadata=metadata,
        ) as span, MetricsCapture(self._resource_info):
            nth_request = getattr(database, "_next_nth_request", 0)
            attempt = AtomicCounter()

            async def attempt_tracking_method():
                all_metadata = database.metadata_with_request_id(
                    nth_request, attempt.increment(), metadata, span
                )
                partition_read_method = functools.partial(
                    api.partition_read,
                    request=partition_read_request,
                    metadata=all_metadata,
                    retry=retry,
                    timeout=timeout,
                )
                return await partition_read_method()

            response = await _retry(
                attempt_tracking_method,
                allowed_exceptions={InternalServerError: _check_rst_stream_error},
            )

        return [partition.partition_token for partition in response.partitions]

    @CrossSync.convert
    async def partition_query(
        self,
        sql,
        params=None,
        param_types=None,
        partition_size_bytes=None,
        max_partitions=None,
        *,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
    ):
        """Perform a ``PartitionQuery`` API request."""
        if self._transaction_id is None:
            raise ValueError("Transaction has not begun.")
        if not self._multi_use:
            raise ValueError("Cannot partition a single-use transaction.")

        if params is not None:
            params_pb = Struct(
                fields={key: _make_value_pb(value) for key, value in params.items()}
            )
        else:
            params_pb = Struct()

        session = self._session
        database = session._database
        api = database.spanner_api

        metadata = _metadata_with_prefix(database.name)
        if database._route_to_leader_enabled:
            metadata.append(
                _metadata_with_leader_aware_routing(database._route_to_leader_enabled)
            )

        transaction = self._build_transaction_selector_pb()
        partition_options = PartitionOptions(
            partition_size_bytes=partition_size_bytes, max_partitions=max_partitions
        )

        partition_query_request = PartitionQueryRequest(
            session=session.name,
            sql=sql,
            transaction=transaction,
            params=params_pb,
            param_types=param_types,
            partition_options=partition_options,
        )

        trace_attributes = {"db.statement": sql}
        with trace_call(
            f"CloudSpanner.{type(self).__name__}.partition_query",
            session,
            trace_attributes,
            observability_options=getattr(database, "observability_options", None),
            metadata=metadata,
        ) as span, MetricsCapture(self._resource_info):
            nth_request = getattr(database, "_next_nth_request", 0)
            attempt = AtomicCounter()

            async def attempt_tracking_method():
                all_metadata = database.metadata_with_request_id(
                    nth_request, attempt.increment(), metadata, span
                )
                partition_query_method = functools.partial(
                    api.partition_query,
                    request=partition_query_request,
                    metadata=all_metadata,
                    retry=retry,
                    timeout=timeout,
                )
                return await partition_query_method()

            response = await _retry(
                attempt_tracking_method,
                allowed_exceptions={InternalServerError: _check_rst_stream_error},
            )

        return [partition.partition_token for partition in response.partitions]

    @CrossSync.convert
    async def _begin_transaction(
        self, mutation: Mutation = None, transaction_tag: str = None
    ) -> bytes:
        """Begins a transaction on the database."""
        if self._transaction_id is not None:
            raise ValueError("Transaction has already begun.")
        if not self._multi_use:
            raise ValueError("Cannot begin a single-use transaction.")
        if self._read_request_count > 0:
            raise ValueError("Read-only transaction already pending")

        session = self._session
        database = session._database
        api = database.spanner_api

        metadata = _metadata_with_prefix(database.name)
        if not self._read_only and database._route_to_leader_enabled:
            metadata.append(
                _metadata_with_leader_aware_routing(database._route_to_leader_enabled)
            )

        begin_request_kwargs = {
            "session": session.name,
            "options": self._build_transaction_selector_pb().begin,
            "mutation_key": mutation,
        }

        request_options = begin_request_kwargs.get("request_options")
        client_context = _merge_client_context(
            database._instance._client._client_context, self._client_context
        )
        request_options = _merge_request_options(request_options, client_context)

        if transaction_tag:
            if request_options is None:
                request_options = RequestOptions()
            request_options.transaction_tag = transaction_tag

        if request_options:
            begin_request_kwargs["request_options"] = request_options

        with trace_call(
            name=f"CloudSpanner.{type(self).__name__}.begin",
            session=session,
            observability_options=getattr(database, "observability_options", None),
            metadata=metadata,
        ) as span, MetricsCapture(self._resource_info):
            nth_request = getattr(database, "_next_nth_request", 0)
            attempt = AtomicCounter()

            async def wrapped_method():
                begin_transaction_request = BeginTransactionRequest(
                    **begin_request_kwargs
                )
                call_metadata, error_augmenter = database.with_error_augmentation(
                    nth_request, attempt.increment(), metadata, span
                )
                begin_transaction_method = functools.partial(
                    api.begin_transaction,
                    request=begin_transaction_request,
                    metadata=call_metadata,
                )
                with error_augmenter:
                    return await begin_transaction_method()

            async def before_next_retry(nth_retry, delay_in_seconds):
                add_span_event(
                    span=span,
                    event_name="Transaction Begin Attempt Failed. Retrying",
                    event_attributes={
                        "attempt": nth_retry,
                        "sleep_seconds": delay_in_seconds,
                    },
                )

            transaction_pb: Transaction = await _retry(
                wrapped_method,
                before_next_retry=before_next_retry,
                allowed_exceptions={
                    InternalServerError: _check_rst_stream_error,
                    Aborted: None,
                },
            )

        self._update_for_transaction_pb(transaction_pb)
        return self._transaction_id

    def _build_transaction_options_pb(self) -> TransactionOptions:
        """Builds and returns the transaction options for this snapshot."""
        raise NotImplementedError

    def _build_transaction_selector_pb(self) -> TransactionSelector:
        """Builds and returns a transaction selector for this snapshot."""
        if self._transaction_id is not None:
            return TransactionSelector(id=self._transaction_id)

        options = self._build_transaction_options_pb()
        if not self._multi_use:
            return TransactionSelector(single_use=options)

        return TransactionSelector(begin=options)

    def _update_for_result_set_pb(
        self, result_set_pb: Union[ResultSet, PartialResultSet]
    ) -> None:
        """Updates the snapshot for the given result set."""
        if result_set_pb.metadata and result_set_pb.metadata.transaction:
            self._update_for_transaction_pb(result_set_pb.metadata.transaction)

    def _update_for_transaction_pb(self, transaction_pb: Transaction) -> None:
        """Updates the snapshot for the given transaction."""
        if self._transaction_id is None and transaction_pb.id:
            self._transaction_id = transaction_pb.id

        if transaction_pb._pb.HasField("precommit_token"):
            self._update_for_precommit_token_pb_unsafe(transaction_pb.precommit_token)

    @CrossSync.convert
    async def _update_for_precommit_token_pb(
        self, precommit_token_pb: MultiplexedSessionPrecommitToken
    ) -> None:
        """Updates the snapshot for the given multiplexed session precommit token."""
        async with self._lock:
            self._update_for_precommit_token_pb_unsafe(precommit_token_pb)

    def _update_for_precommit_token_pb_unsafe(
        self, precommit_token_pb: MultiplexedSessionPrecommitToken
    ) -> None:
        """Updates the snapshot for the given multiplexed session precommit token."""
        if (
            self._precommit_token is None
            or precommit_token_pb.seq_num > self._precommit_token.seq_num
        ):
            self._precommit_token = precommit_token_pb


class Snapshot(_SnapshotBase):
    """Allow a set of reads / SQL statements with shared staleness."""

    def __init__(
        self,
        session,
        read_timestamp=None,
        min_read_timestamp=None,
        max_staleness=None,
        exact_staleness=None,
        multi_use=False,
        transaction_id=None,
        client_context=None,
    ):
        super(Snapshot, self).__init__(session, client_context=client_context)
        opts = [read_timestamp, min_read_timestamp, max_staleness, exact_staleness]
        flagged = [opt for opt in opts if opt is not None]
        if len(flagged) > 1:
            raise ValueError("Supply zero or one options.")

        if multi_use:
            if min_read_timestamp is not None or max_staleness is not None:
                raise ValueError(
                    "'multi_use' is incompatible with 'min_read_timestamp' / 'max_staleness'"
                )

        self._transaction_read_timestamp = None
        self._strong = len(flagged) == 0
        self._read_timestamp = read_timestamp
        self._min_read_timestamp = min_read_timestamp
        self._max_staleness = max_staleness
        self._exact_staleness = exact_staleness
        self._multi_use = multi_use
        self._transaction_id = transaction_id

    def _build_transaction_options_pb(self) -> TransactionOptions:
        """Builds and returns transaction options for this snapshot."""
        read_only_pb_args = dict(return_read_timestamp=True)

        if self._read_timestamp:
            read_only_pb_args["read_timestamp"] = self._read_timestamp
        elif self._min_read_timestamp:
            read_only_pb_args["min_read_timestamp"] = self._min_read_timestamp
        elif self._max_staleness:
            read_only_pb_args["max_staleness"] = self._max_staleness
        elif self._exact_staleness:
            read_only_pb_args["exact_staleness"] = self._exact_staleness
        else:
            read_only_pb_args["strong"] = True

        read_only_pb = TransactionOptions.ReadOnly(**read_only_pb_args)
        return TransactionOptions(read_only=read_only_pb)

    def _update_for_transaction_pb(self, transaction_pb: Transaction) -> None:
        """Updates the snapshot for the given transaction."""
        super(Snapshot, self)._update_for_transaction_pb(transaction_pb)
        if transaction_pb.read_timestamp is not None:
            self._transaction_read_timestamp = transaction_pb.read_timestamp
