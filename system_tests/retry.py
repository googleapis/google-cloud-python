import time
from functools import wraps


def retry(exception, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    :type exception: Exception or tuple
    :param exception: the exception to check. may be a tuple of
        exceptions to check

    :type tries: int
    :param tries: number of times to try (not retry) before giving up

    :type delay: int
    :param delay: initial delay between retries in seconds

    :type backoff: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry

    :type logger: logging.Logger instance
    :param logger: logger to use. If None, print

    :rtype: func
    :returns: Retry wrapper function.
    """
    def retry_decorator(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return retry_decorator
