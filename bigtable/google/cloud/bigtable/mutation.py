from grpc import StatusCode

from google.api_core.exceptions import RetryError
from google.api_core.retry import if_exception_type
from google.api_core.retry import Retry
from google.cloud.bigtable_v2.proto import (
    data_pb2 as data_v2_pb2)
from google.cloud.bigtable_v2.proto.bigtable_pb2 import MutateRowsRequest


class _BigtableRetryableError(Exception):
    """Retry-able error expected by the default retry strategy."""


DEFAULT_RETRY = Retry(
    predicate=if_exception_type(_BigtableRetryableError),
    initial=1.0,
    maximum=15.0,
    multiplier=2.0,
    deadline=120.0,  # 2 minutes
)


class MutateRowsEntry(object):
    """Create Entry using list of mutations

    Arguments:
        row_key (bytes): Key of the Row in bytes.
    """

    def __init__(self, row_key):
        self.row_key = row_key
        self.mutations = []

    def set_cell(self, row_key, family_name, column_id, value, timestamp=None):
        """Create the mutation request message for SetCell and add it to the
            list of mutations

        Arguments:
            row_key (bytes): Key of the Row.
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
            column_id (bytes):
                The qualifier of the column into which new data should be
                written. Can be any byte string, including the empty string.
            value (bytes):
                The value to be written into the specified cell.
            timestamp (int):
                (optional) The timestamp of the cell into which new data should
                be written. Use -1 for current Bigtable server time. Otherwise,
                the client should set this value itself, noting that the
                default value is a timestamp of zero if the field is left
                unspecified. Values must match the granularity of the table
                (e.g. micros, millis).
        """
        mutation = SetCellMutation(family_name, column_id, value, timestamp)
        self.mutations.append(mutation.mutation_request)

    def delete_from_column(self, row_key, family_name, column_id,
                           time_range=None):
        """Create the mutation request message for DeleteFromColumn and
            add it to the list of mutations

        Arguments:
            row_key (bytes): Key of the Row.
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
            column_id (bytes):
                The qualifier of the column into which new data should be
                written. Can be any byte string, including the empty string.
            time_range (TimestampRange):
                (optional) The range of timestamps within which cells should be
                deleted.
        """
        mutation = DeleteFromColumnMutation(family_name, column_id, time_range)
        self.mutations.append(mutation.mutation_request)

    def create_entry(self):
        """Create Entry from list of mutations

        Returns:
            `Entry <google.bigtable.v2.MutateRowsRequest.Entry>`
            A ``Entry`` message.
        """
        entry = MutateRowsRequest.Entry(row_key=self.row_key)
        for mutation in self.mutations:
            entry.mutations.add().CopyFrom(mutation)
        return entry


class MutateRows(object):
    """Create Entry using list of mutations

    Arguments:
        table_name (bytes): Key of the Row in bytes.
        client (class):
            `Client <google.cloud.bigtable_v2.BigtableClient>`
            The client class of BigtableClient.
    """

    def __init__(self, table_name, client):
        self.table_name = table_name
        self.client = client
        self.entries = []

    def add_row_mutations_entry(self, mutate_rows_entry):
        """Create list of entries of ``Entry``

        Arguments:
            mutate_rows_entry (class): Class of ``MutateRowsEntry``
        """
        entry = mutate_rows_entry.create_entry()
        self.entries.append(entry)

    def mutate_rows(self, retry=DEFAULT_RETRY):
        """Call on GAPIC API for MutateRows

        Returns:
            List[~google.rpc.status_pb2.Status].
            A list of response statuses (`google.rpc.status_pb2.Status`)
            corresponding to success or failure of each row mutation
            sent. These will be in the same order as the ``rows``.
        """
        retryable_mutate_rows = _RetryableMutateRows(
            self.table_name, self.client, self.entries)
        return retryable_mutate_rows(retry=retry)


class _RetryableMutateRows(object):

    RETRY_CODES = (
        StatusCode.DEADLINE_EXCEEDED.value[0],
        StatusCode.ABORTED.value[0],
        StatusCode.UNAVAILABLE.value[0],
    )

    def __init__(self, table_name, client, entries):
        self.table_name = table_name
        self.client = client
        self.entries = entries
        self.responses_statuses = [None] * len(self.entries)
        self.retryable_entries = []

    def __call__(self, retry=DEFAULT_RETRY):
        """Attempt to mutate all rows and retry rows with transient errors.

        Will retry the rows with transient errors until all rows succeed or
        ``deadline`` specified in the `retry` is reached.

        Arguments:
        retry (class):
            `Retry <google.api_core.retry.Retry>`
            (optional) This is a DEFAULT_RETRY class with default settings.
            It is optional by passing False to this parameter retry logic will
            bypass.

        Returns:
            List[~google.rpc.status_pb2.Status].
            A list of response statuses (`google.rpc.status_pb2.Status`)
            corresponding to success or failure of each row mutation
            sent. These will be in the same order as the ``rows``.
        """
        mutate_rows = self._do_mutate_retryable_mutate_rows
        if retry:
            mutate_rows = retry(self._do_mutate_retryable_mutate_rows)

        try:
            mutate_rows()
        except (_BigtableRetryableError, RetryError) as err:
            # - _BigtableRetryableError raised when no retry strategy is used
            #   and a retryable error on a mutation occurred.
            # - RetryError raised when retry deadline is reached.
            # In both cases, just return current `responses_statuses`.
            pass

        return self.responses_statuses

    @staticmethod
    def _is_retryable(status):
        return (status is None or
                status.code in _RetryableMutateRows.RETRY_CODES)

    def _do_mutate_retryable_mutate_rows(self):

        if not self.entries:
            return self.responses_statuses
        else:
            if not self.retryable_entries:
                responses = self.client.mutate_rows(table_name=self.table_name,
                                                    entries=self.entries)
            else:
                responses = self.client.mutate_rows(
                    table_name=self.table_name, entries=self.retryable_entries)

            num_responses = 0
            num_retryable_responses = 0
            for response in responses:
                for entry in response.entries:
                    num_responses += 1
                    index = entry.index
                    self.responses_statuses[index] = entry.status
                    if self._is_retryable(entry.status):
                        self.retryable_entries.append(self.entries[index])
                        num_retryable_responses += 1

            if len(self.entries) != num_responses:
                raise RuntimeError(
                    'Unexpected number of responses', num_responses,
                    'Expected', len(self.entries))

            if num_retryable_responses:
                raise _BigtableRetryableError

        return self.responses_statuses


class SetCellMutation(object):
    """Create the mutation request message for SetCell and add it to the list
    of mutations

    Arguments:
        family_name (str):
            The name of the family into which new data should be written.
            Must match ``[-_.a-zA-Z0-9]+``.
        column_id (bytes):
            The qualifier of the column into which new data should be
            written. Can be any byte string, including the empty string.
        value (bytes):
            The value to be written into the specified cell.
        timestamp (int):
            (optional) The timestamp of the cell into which new data should
            be written. Use -1 for current Bigtable server time. Otherwise,
            the client should set this value itself, noting that the
            default value is a timestamp of zero if the field is left
            unspecified. Values must match the granularity of the table
            (e.g. micros, millis).
    """

    def __init__(self, family_name, column_id, value, timestamp):
        super(SetCellMutation, self).__init__()
        self.family_name = family_name
        self.column_id = column_id
        self.value = value
        self.timestamp = timestamp

    @property
    def mutation_request(self):
        """message: Mutation of the SetCell."""
        set_cell_mutation = data_v2_pb2.Mutation.SetCell(
            family_name=self.family_name,
            column_qualifier=self.column_id,
            timestamp_micros=self.timestamp,
            value=self.value,
        )
        return data_v2_pb2.Mutation(set_cell=set_cell_mutation)


class DeleteFromColumnMutation(object):
    """Create the mutation request message for DeleteFromColumn and add it to
    the list of mutations

    Arguments:
        family_name (str):
            The name of the family into which new data should be written.
            Must match ``[-_.a-zA-Z0-9]+``.
        column_id (bytes):
            The qualifier of the column into which new data should be
            written. Can be any byte string, including the empty string.
        time_range (TimestampRange):
            (optional) The range of timestamps within which cells should be
            deleted.
    """

    def __init__(self, family_name, column_id, time_range):
        super(DeleteFromColumnMutation, self).__init__()
        self.family_name = family_name
        self.column_id = column_id
        self.time_range = time_range

    @property
    def mutation_request(self):
        """message: Mutation of the DeleteFromColumn."""
        delete_from_column_mutation = data_v2_pb2.Mutation.DeleteFromColumn(
            family_name=self.family_name,
            column_qualifier=self.column_id,
            time_range=self.time_range
        )
        return data_v2_pb2.Mutation(
            delete_from_column=delete_from_column_mutation)
