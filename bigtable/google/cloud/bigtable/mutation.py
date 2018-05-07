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

    def set_cell(self, family_name, column_id, value, timestamp=None):
        """Create the mutation request message for SetCell and add it to the
            list of mutations

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
        set_cell_mutation = data_v2_pb2.Mutation.SetCell(
            family_name=family_name,
            column_qualifier=column_id,
            timestamp_micros=timestamp,
            value=value
        )
        mutation_message = data_v2_pb2.Mutation(set_cell=set_cell_mutation)
        self.mutations.append(mutation_message)

    def delete_from_column(self, family_name, column_id, time_range=None):
        """Create the mutation request message for DeleteFromColumn and
            add it to the list of mutations

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
        delete_from_column_mutation = data_v2_pb2.Mutation.DeleteFromColumn(
            family_name=family_name,
            column_qualifier=column_id,
            time_range=time_range
        )
        mutation_message = data_v2_pb2.Mutation(
            delete_from_column=delete_from_column_mutation)
        self.mutations.append(mutation_message)

    def delete_from_family(self, family_name):
        """Create the mutation request message for DeleteFromFamily and add
        it to the list of mutations

        Arguments:
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
        """
        delete_from_family_mutation = data_v2_pb2.Mutation.DeleteFromFamily(
            family_name=family_name
        )
        mutation_message = data_v2_pb2.Mutation(
            delete_from_family=delete_from_family_mutation)
        self.mutations.append(mutation_message)

    def delete_from_row(self):
        """Create the mutation request message for DeleteFromRow and add it
        to the list of mutations"""
        delete_from_row_mutation = data_v2_pb2.Mutation.DeleteFromRow()
        mutation_message = data_v2_pb2.Mutation(
            delete_from_row=delete_from_row_mutation)
        self.mutations.append(mutation_message)

    def create_entry(self):
        """Create a MutateRowsRequest Entry from the list of mutations

        Returns:
            `Entry <google.bigtable.v2.MutateRowsRequest.Entry>`
             An ``Entry`` for a MutateRowsRequest message.
        """
        entry = MutateRowsRequest.Entry(row_key=self.row_key)
        for mutation in self.mutations:
            entry.mutations.add().CopyFrom(mutation)
        return entry


class MutateRows(object):
    """Maintain a list of Entry's to mutate
       Corresponds to the MutateRowsRequest

    Arguments:
        table_name (str): The name of the table with rows to mutate.
        client (class):
            `Client <google.cloud.bigtable_v2.BigtableClient>`
            The client class for the GAPIC API.
    """

    def __init__(self, table_name, client):
        self.table_name = table_name
        self.client = client
        self.entries = []

    def add_row_mutations_entry(self, mutate_rows_entry):
        """Add an ``Entry`` to the list for the mutate request

        Arguments:
            mutate_rows_entry (class): Class of ``MutateRowsEntry``
        """
        entry = mutate_rows_entry.create_entry()
        self.entries.append(entry)

    def mutate(self, retry=DEFAULT_RETRY):
        """Call the GAPIC API for MutateRows

        Returns:
            List[~google.rpc.status_pb2.Status].
            A list of response statuses (`google.rpc.status_pb2.Status`)
            corresponding to success or failure of each Entry sent.
        """
        retryable_mutate_rows = _RetryableMutateRows(
            self.table_name, self.client, self.entries)
        return retryable_mutate_rows(retry=retry)


class _RetryableMutateRows(object):
    """A callable worker that can retry to mutate rows with transient errors.

    This class is a callable that can retry mutating rows that result in
    transient errors. After all rows are successful or none of the rows
    are retryable, any subsequent call on this callable will be a no-op.
    """

    RETRY_CODES = (
        StatusCode.DEADLINE_EXCEEDED.value[0],
        StatusCode.ABORTED.value[0],
        StatusCode.UNAVAILABLE.value[0],
    )

    def __init__(self, table_name, client, entries):
        self.table_name = table_name
        self.client = client
        self.responses_statuses = [None] * len(entries)
        self.retryable_entries = entries

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
        """Mutate all the rows that are eligible for retry.

        A row is eligible for retry if it has not been tried or if it resulted
        in a transient error in a previous call.
        Returns:
            `List [~google.rpc.status_pb2.Status]`
             The responses statuses, which is a list of
             Class `~google.rpc.status_pb2.Status`.
        Raises:
             One of the following:

                 * (exc) `~.table._BigtableRetryableError` if any
                   row returned a transient error.
                 * (exc) `RuntimeError` if the number of responses doesn't
                   match the number of rows that were retried
        """
        retryable_entries = []
        index_into_all_entries = []
        for index, status in enumerate(self.responses_statuses):
            if self._is_retryable(status):
                retryable_entries.append(self.retryable_entries[index])
                index_into_all_entries.append(index)

        responses = self.client.mutate_rows(
            table_name=self.table_name, entries=retryable_entries)

        num_responses = 0
        num_retryable_responses = 0
        for response in responses:
            for entry in response.entries:
                num_responses += 1
                index = index_into_all_entries[entry.index]
                self.responses_statuses[index] = entry.status
                if self._is_retryable(entry.status):
                    num_retryable_responses += 1

        if len(retryable_entries) != num_responses:
            raise RuntimeError(
                'Unexpected number of responses', num_responses,
                'Expected', len(retryable_entries))

        if num_retryable_responses:
            raise _BigtableRetryableError

        return self.responses_statuses
