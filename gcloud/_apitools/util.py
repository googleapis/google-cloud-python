# pylint: skip-file
"""Assorted utilities shared between parts of apitools.

Pruned to include only helpers used by other vendored-in modules:

``gcloud._apidools.transfer`` uses:

- Typecheck
- AcceptableMimeType

``gcloud._apitools.http_wrapper`` uses:

- CalculateWaitForRetry
"""

import random

from gcloud._apitools import exceptions


def Typecheck(arg, arg_type, msg=None):
    if not isinstance(arg, arg_type):
        if msg is None:
            if isinstance(arg_type, tuple):
                msg = 'Type of arg is "%s", not one of %r' % (
                    type(arg), arg_type)
            else:
                msg = 'Type of arg is "%s", not "%s"' % (type(arg), arg_type)
        raise exceptions.TypecheckError(msg)
    return arg


def CalculateWaitForRetry(retry_attempt, max_wait=60):
    """Calculates amount of time to wait before a retry attempt.

    Wait time grows exponentially with the number of attempts. A
    random amount of jitter is added to spread out retry attempts from
    different clients.

    Args:
      retry_attempt: Retry attempt counter.
      max_wait: Upper bound for wait time [seconds].

    Returns:
      Number of seconds to wait before retrying request.

    """

    wait_time = 2 ** retry_attempt
    max_jitter = wait_time / 4.0
    wait_time += random.uniform(-max_jitter, max_jitter)
    return max(1, min(wait_time, max_wait))


def AcceptableMimeType(accept_patterns, mime_type):
    """Return True iff mime_type is acceptable for one of accept_patterns.

    Note that this function assumes that all patterns in accept_patterns
    will be simple types of the form "type/subtype", where one or both
    of these can be "*". We do not support parameters (i.e. "; q=") in
    patterns.

    Args:
      accept_patterns: list of acceptable MIME types.
      mime_type: the mime type we would like to match.

    Returns:
      Whether or not mime_type matches (at least) one of these patterns.
    """
    if '/' not in mime_type:
        raise exceptions.InvalidUserInputError(
            'Invalid MIME type: "%s"' % mime_type)
    unsupported_patterns = [p for p in accept_patterns if ';' in p]
    if unsupported_patterns:
        raise exceptions.GeneratedClientError(
            'MIME patterns with parameter unsupported: "%s"' % ', '.join(
                unsupported_patterns))

    def MimeTypeMatches(pattern, mime_type):
        """Return True iff mime_type is acceptable for pattern."""
        # Some systems use a single '*' instead of '*/*'.
        if pattern == '*':
            pattern = '*/*'
        return all(accept in ('*', provided) for accept, provided
                   in zip(pattern.split('/'), mime_type.split('/')))

    return any(MimeTypeMatches(pattern, mime_type)
               for pattern in accept_patterns)
