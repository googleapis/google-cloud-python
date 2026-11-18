# Copyright 2020 Google LLC
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

"""API to calculate checksums of SQL statements results."""

import hashlib
import logging
import pickle
from typing import Any, Callable, Iterator, Optional, Tuple

import grpc
from google.api_core.exceptions import Aborted, GoogleAPICallError

from google.cloud.spanner_dbapi.exceptions import InterfaceError, RetryAborted

_LOGGER = logging.getLogger(__name__)

RETRY_ABORTED_ERROR = (
    "The transaction was aborted and could not be retried due to a concurrent "
    "modification."
)


class ResultsChecksum:
    """Cumulative checksum.

    Used to calculate a total checksum of all the results
    returned by operations executed within transaction.
    Includes methods for checksums comparison.
    These checksums are used while retrying an aborted
    transaction to check if the results of a retried transaction
    are equal to the results of the original transaction.
    """

    def __init__(self):
        self.checksum = hashlib.sha256()
        self.count = 0  # counter of consumed results

    def __len__(self):
        """Return the number of consumed results.

        :rtype: :class:`int`
        :returns: The number of results.
        """
        return self.count

    def __eq__(self, other):
        """Check if checksums are equal.

        :type other: :class:`google.cloud.spanner_dbapi.checksum.ResultsChecksum`
        :param other: Another checksum to compare with this one.
        """
        return self.checksum.digest() == other.checksum.digest()

    def consume_result(self, result):
        """Add the given result into the checksum.

        :type result: Union[int, list]
        :param result: Streamed row or row count from an UPDATE operation.
        """
        self.checksum.update(pickle.dumps(result))
        self.count += 1


def _compare_checksums(original, retried):
    """Compare the given checksums.

    Raise an error if the given checksums are not equal.

    :type original: :class:`~google.cloud.spanner_dbapi.checksum.ResultsChecksum`
    :param original: results checksum of the original transaction.

    :type retried: :class:`~google.cloud.spanner_dbapi.checksum.ResultsChecksum`
    :param retried: results checksum of the retried transaction.

    :raises: :exc:`google.cloud.spanner_dbapi.exceptions.RetryAborted` in case if checksums are not equal.
    """
    if retried != original:
        raise RetryAborted(RETRY_ABORTED_ERROR)


def _extract_grpc_error_info(
    source: Any,
) -> Tuple[Optional[grpc.StatusCode], Optional[str]]:
    code_getter = getattr(source, "code", None)
    if not callable(code_getter):
        return None, None
    code = code_getter()
    if not isinstance(code, grpc.StatusCode):
        return None, None
    details_getter = getattr(source, "details", None)
    details = details_getter() if callable(details_getter) else None
    if details is None:
        return code, None
    return code, details if isinstance(details, str) else str(details)


def _get_grpc_error_info(
    error: BaseException,
) -> Tuple[Optional[grpc.StatusCode], Optional[str]]:
    """Extract (gRPC status code, message) from an error or its ``__cause__`` chain."""
    visited = set()
    current: Optional[BaseException] = error
    while current is not None and id(current) not in visited:
        visited.add(id(current))
        if isinstance(current, GoogleAPICallError):
            response = getattr(current, "response", None)
            code, response_message = _extract_grpc_error_info(response)
            if code is not None:
                return (
                    code,
                    response_message
                    if response_message is not None
                    else current.message,
                )
            if isinstance(current.grpc_status_code, grpc.StatusCode):
                return current.grpc_status_code, current.message
        code, message = _extract_grpc_error_info(current)
        if code is not None:
            return code, message if message is not None else str(current)
        current = current.__cause__
    return None, None


def _errors_equal_for_retry(
    original: Optional[BaseException],
    retried: Optional[BaseException],
) -> bool:
    """Compare two exceptions for transaction retry equivalence.

    For gRPC errors (including through wrapped ``__cause__`` exceptions),
    returns True only if both the non-OK gRPC status code and error message
    match. For non-gRPC exceptions (or ``StatusCode.OK``), falls back to
    comparing exception type and ``args``.
    """
    if original is None or retried is None:
        return False
    if original is retried:
        return True
    original_code, original_message = _get_grpc_error_info(original)
    retried_code, retried_message = _get_grpc_error_info(retried)
    if original_code is not None or retried_code is not None:
        if original_code != retried_code:
            return False
        if original_code != grpc.StatusCode.OK:
            return original_message == retried_message
    return type(original) is type(retried) and original.args == retried.args


def _close_iterator(iterator: Any) -> None:
    """Close an iterator or generator if it exposes a callable ``close()``."""
    close_method = getattr(iterator, "close", None)
    if callable(close_method):
        try:
            close_method()
        except Exception as exception:
            _LOGGER.warning("Failed to close iterator: %s", exception)


class ChecksumIterator:
    """Iterator wrapper that tracks consumed query results for transaction retries.

    When a read-write transaction is aborted by Spanner, the transaction must be
    replayed and can only continue safely if every query produces the exact same
    results that the caller has already observed. This wrapper records a running
    :class:`ResultsChecksum` of all yielded rows, the number of ``next()`` calls
    made, and whether iteration ended at EOF or raised a non-``Aborted`` error,
    allowing replay to detect concurrent modifications (changed rows, new rows
    past EOF, or differing errors) before resuming iteration.
    """

    def __init__(
        self,
        iterator: Iterator[Any],
        retry_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        if iterator is None:
            raise ValueError("iterator must not be None")
        self._iterator: Iterator[Any] = iterator
        self._retry_callback: Optional[Callable[[], None]] = retry_callback
        self._next_count: int = 0
        self._checksum: ResultsChecksum = ResultsChecksum()
        self._error: Optional[Exception] = None
        self._error_index: Optional[int] = None
        self._eof_reached: bool = False
        self._closed: bool = False

    @property
    def iterator(self) -> Iterator[Any]:
        """Return the underlying iterator."""
        return self._iterator

    @property
    def next_count(self) -> int:
        """Return the number of completed ``next()`` calls."""
        return self._next_count

    @property
    def checksum(self) -> ResultsChecksum:
        """Return the running :class:`ResultsChecksum` of yielded rows."""
        return self._checksum

    @property
    def error(self) -> Optional[Exception]:
        """Return the recorded non-``Aborted`` error, if any."""
        return self._error

    @property
    def error_index(self) -> Optional[int]:
        """Return the 0-based ``next()`` index where ``error`` occurred."""
        return self._error_index

    @property
    def eof_reached(self) -> bool:
        """Return True if ``StopIteration`` has been observed."""
        return self._eof_reached

    @property
    def is_closed(self) -> bool:
        """Return True if this iterator has been closed."""
        return self._closed

    def close(self) -> None:
        """Close this wrapper and its underlying iterator, if closeable."""
        if not self._closed:
            self._closed = True
            _close_iterator(self._iterator)

    def __iter__(self) -> "ChecksumIterator":
        return self

    def __next__(self) -> Any:
        if self._closed:
            raise InterfaceError("ChecksumIterator is already closed.")
        if self._eof_reached:
            raise StopIteration
        if self._error is not None:
            raise self._error

        while True:
            try:
                row = next(self._iterator)
            except Aborted:
                if self._retry_callback is None:
                    raise
                self._retry_callback()
                if self._closed:
                    raise InterfaceError("ChecksumIterator is already closed.")
                continue
            except StopIteration:
                self._eof_reached = True
                self._next_count += 1
                raise
            except Exception as exception:
                self._error = exception
                self._error_index = self._next_count
                self._next_count += 1
                raise

            self._checksum.consume_result(row)
            self._next_count += 1
            return row

    def retry(self, new_iterator: Iterator[Any]) -> None:
        """Replay ``next_count`` calls on ``new_iterator`` and verify parity.

        Verifies that ``new_iterator`` produces the identical prefix checksum,
        reproduces any recorded non-``Aborted`` error at ``error_index``, and
        reaches ``StopIteration`` at the exact EOF position if EOF was reached.
        On success, swaps ``self._iterator`` to ``new_iterator`` (or closes
        ``new_iterator`` if this wrapper has already been closed).

        Raises:
            Aborted: If ``new_iterator`` aborts during replay.
            RetryAborted: If results, EOF position, or errors do not match.
        """
        if new_iterator is None:
            raise RetryAborted(RETRY_ABORTED_ERROR)

        try:
            self._replay_and_verify_prefix(new_iterator)
            self._verify_terminal_state(new_iterator)
        except BaseException:
            _close_iterator(new_iterator)
            raise

        if self._closed:
            _close_iterator(new_iterator)
        else:
            self._swap_iterator(new_iterator)

    def _replay_and_verify_prefix(self, new_iterator: Iterator[Any]) -> None:
        if len(self._checksum) == 0:
            return
        new_checksum = ResultsChecksum()
        for _ in range(len(self._checksum)):
            try:
                row = next(new_iterator)
            except Aborted:
                raise
            except StopIteration:
                raise RetryAborted(RETRY_ABORTED_ERROR)
            except Exception as exception:
                raise RetryAborted(RETRY_ABORTED_ERROR, exception) from exception
            new_checksum.consume_result(row)

        _compare_checksums(self._checksum, new_checksum)

    def _verify_terminal_state(self, new_iterator: Iterator[Any]) -> None:
        if not self._eof_reached and self._error is None:
            return
        try:
            next(new_iterator)
        except Aborted:
            raise
        except StopIteration:
            if not self._eof_reached:
                raise RetryAborted(RETRY_ABORTED_ERROR)
            return
        except Exception as exception:
            if self._error is not None and _errors_equal_for_retry(
                self._error, exception
            ):
                return
            raise RetryAborted(RETRY_ABORTED_ERROR, exception) from exception

        raise RetryAborted(RETRY_ABORTED_ERROR)

    def _swap_iterator(self, new_iterator: Iterator[Any]) -> None:
        old_iterator = self._iterator
        self._iterator = new_iterator
        _close_iterator(old_iterator)
