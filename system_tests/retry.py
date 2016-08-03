import time
from functools import wraps

import six


class RetryErrors(object):
    """Retry class for retrying given exceptions in testing."""

    def __init__(self, exception, max_tries=4, delay=1, backoff=2,
                 logger=None):
        """Retry calling the decorated function using an exponential backoff.

        :type exception: Exception or tuple of Exceptions
        :param exception: The exception to check or may be a tuple of
                          exceptions to check.

        :type max_tries: int
        :param max_tries: Number of times to try (not retry) before giving up.

        :type delay: int
        :param delay: Initial delay between retries in seconds.

        :type backoff: int
        :param backoff: Backoff multiplier e.g. value of 2 will double the
                        delay each retry.

        :type logger: logging.Logger instance
        :param logger: Logger to use. If None, print.
        """

        self.exception = exception
        self.max_tries = max_tries
        self.delay = delay
        self.backoff = backoff
        self.logger = logger.warning if logger else six.print_

    def __call__(self, to_wrap):
        @wraps(to_wrap)
        def wrapped_function(*args, **kwargs):
            tries = 0
            while tries < self.max_tries:
                try:
                    return to_wrap(*args, **kwargs)
                except self.exception as caught_exception:
                    delay = self.delay * self.backoff**tries
                    msg = ("%s, Trying again in %d seconds..." %
                           (str(caught_exception), delay))
                    self.logger(msg)

                    time.sleep(delay)
                    tries += 1
            return to_wrap(*args, **kwargs)

        return wrapped_function
