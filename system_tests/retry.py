import time
from functools import wraps

import six


class Retry(object):
    """Retry class for retrying eventually consistent resources in testing."""

    def __init__(self, exception, tries=4, delay=3, backoff=2, logger=None):
        """Retry calling the decorated function using an exponential backoff.

        :type exception: Exception or tuple of Exceptions
        :param exception: The exception to check or may be a tuple of
                          exceptions to check.

        :type tries: int
        :param tries: Number of times to try (not retry) before giving up.

        :type delay: int
        :param delay: Initial delay between retries in seconds.

        :type backoff: int
        :param backoff: Backoff multiplier e.g. value of 2 will double the
                        delay each retry.

        :type logger: logging.Logger instance
        :param logger: Logger to use. If None, print.
        """

        self.exception = exception
        self.tries = tries
        self.delay = delay
        self.backoff = backoff
        self.logger = logger.warning if logger else six.print_

    def __call__(self, to_wrap):
        @wraps(to_wrap)
        def wrapped_function(*args, **kwargs):
            tries_counter = self.tries
            while tries_counter > 0:
                try:
                    return to_wrap(*args, **kwargs)
                except self.exception as caught_exception:
                    msg = ("%s, Trying again in %d seconds..." %
                           (str(caught_exception), self.delay))
                    self.logger(msg)

                    time.sleep(self.delay)
                    tries_counter -= 1
                    self.delay *= self.backoff
            return to_wrap(*args, **kwargs)

        return wrapped_function
