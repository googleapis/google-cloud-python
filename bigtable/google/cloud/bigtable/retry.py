"""Provides function wrappers that implement retrying."""
import random
import time
import six

from google.cloud._helpers import _to_bytes
from google.cloud.bigtable._generated import (
    bigtable_pb2 as data_messages_v2_pb2)
from google.gax import config, errors
from grpc import RpcError


_MILLIS_PER_SECOND = 1000


class ReadRowsIterator():
    """Creates an iterator equivalent to a_iter, but that retries on certain
    exceptions.
    """

    def __init__(self, client, name, start_key, end_key, filter_, limit,
                 retry_options, **kwargs):
        self.client = client
        self.retry_options = retry_options
        self.name = name
        self.start_key = start_key
        self.start_key_closed = True
        self.end_key = end_key
        self.filter_ = filter_
        self.limit = limit
        self.delay_mult = retry_options.backoff_settings.retry_delay_multiplier
        self.max_delay_millis = \
            retry_options.backoff_settings.max_retry_delay_millis
        self.timeout_mult = \
            retry_options.backoff_settings.rpc_timeout_multiplier
        self.max_timeout = \
            (retry_options.backoff_settings.max_rpc_timeout_millis /
             _MILLIS_PER_SECOND)
        self.total_timeout = \
            (retry_options.backoff_settings.total_timeout_millis /
             _MILLIS_PER_SECOND)
        self.set_stream()

    def set_start_key(self, start_key):
        """
        Sets the row key at which this iterator will begin reading.
        """
        self.start_key = start_key
        self.start_key_closed = False

    def set_stream(self):
        """
        Resets the read stream by making an RPC on the 'ReadRows' endpoint.
        """
        req_pb = _create_row_request(self.name, start_key=self.start_key,
                                     start_key_closed=self.start_key_closed,
                                     end_key=self.end_key,
                                     filter_=self.filter_, limit=self.limit)
        self.stream = self.client._data_stub.ReadRows(req_pb)

    def next(self, *args, **kwargs):
        """
        Read and return the next row from the stream.
        Retry on idempotent failure.
        """
        delay = self.retry_options.backoff_settings.initial_retry_delay_millis
        exc = errors.RetryError('Retry total timeout exceeded before any'
                                'response was received')
        timeout = (self.retry_options.backoff_settings
                   .initial_rpc_timeout_millis /
                   _MILLIS_PER_SECOND)

        now = time.time()
        deadline = now + self.total_timeout
        while deadline is None or now < deadline:
            try:
                return six.next(self.stream)
            except StopIteration as stop:
                raise stop
            except RpcError as error:  # pylint: disable=broad-except
                code = config.exc_to_code(error)
                if code not in self.retry_options.retry_codes:
                    six.reraise(errors.RetryError,
                                errors.RetryError(str(error)))

                # pylint: disable=redefined-variable-type
                exc = errors.RetryError(
                    'Retry total timeout exceeded with exception', error)

                # Sleep a random number which will, on average, equal the
                # expected delay.
                to_sleep = random.uniform(0, delay * 2)
                time.sleep(to_sleep / _MILLIS_PER_SECOND)
                delay = min(delay * self.delay_mult, self.max_delay_millis)
                now = time.time()
                timeout = min(
                    timeout * self.timeout_mult, self.max_timeout,
                    deadline - now)
                self.set_stream()

        six.reraise(errors.RetryError, exc)

    def __next__(self, *args, **kwargs):
        return self.next(*args, **kwargs)

    def __iter__(self):
        return self


def _create_row_request(table_name, row_key=None, start_key=None,
                        start_key_closed=True, end_key=None, filter_=None,
                        limit=None):
    """Creates a request to read rows in a table.

    :type table_name: str
    :param table_name: The name of the table to read from.

    :type row_key: bytes
    :param row_key: (Optional) The key of a specific row to read from.

    :type start_key: bytes
    :param start_key: (Optional) The beginning of a range of row keys to
                      read from. The range will include ``start_key``. If
                      left empty, will be interpreted as the empty string.

    :type end_key: bytes
    :param end_key: (Optional) The end of a range of row keys to read from.
                    The range will not include ``end_key``. If left empty,
                    will be interpreted as an infinite string.

    :type filter_: :class:`.RowFilter`
    :param filter_: (Optional) The filter to apply to the contents of the
                    specified row(s). If unset, reads the entire table.

    :type limit: int
    :param limit: (Optional) The read will terminate after committing to N
                  rows' worth of results. The default (zero) is to return
                  all results.

    :rtype: :class:`data_messages_v2_pb2.ReadRowsRequest`
    :returns: The ``ReadRowsRequest`` protobuf corresponding to the inputs.
    :raises: :class:`ValueError <exceptions.ValueError>` if both
             ``row_key`` and one of ``start_key`` and ``end_key`` are set
    """
    request_kwargs = {'table_name': table_name}
    if (row_key is not None and
            (start_key is not None or end_key is not None)):
        raise ValueError('Row key and row range cannot be '
                         'set simultaneously')
    range_kwargs = {}
    if start_key is not None or end_key is not None:
        if start_key is not None:
            if start_key_closed:
                range_kwargs['start_key_closed'] = _to_bytes(start_key)
            else:
                range_kwargs['start_key_open'] = _to_bytes(start_key)
        if end_key is not None:
            range_kwargs['end_key_open'] = _to_bytes(end_key)
    if filter_ is not None:
        request_kwargs['filter'] = filter_.to_pb()
    if limit is not None:
        request_kwargs['rows_limit'] = limit

    message = data_messages_v2_pb2.ReadRowsRequest(**request_kwargs)

    if row_key is not None:
        message.rows.row_keys.append(_to_bytes(row_key))

    if range_kwargs:
        message.rows.row_ranges.add(**range_kwargs)

    return message
