"""Exceptions for generated client libraries."""


class Error(Exception):
    """Base class for all exceptions."""


class CommunicationError(Error):
    """Any communication error talking to an API server."""


class HttpError(CommunicationError):
    """Error making a request. Soon to be HttpError.

    :type response: dict
    :param response: headers from the response which returned the error

    :type content: bytes
    :param content: payload of the response which returned the error

    :type url: string
    :param url: URL of the response which returned the error
    """
    def __init__(self, response, content, url):
        super(HttpError, self).__init__()
        self.response = response
        self.content = content
        self.url = url

    def __str__(self):
        content = self.content.decode('ascii', 'replace')
        return 'HttpError accessing <%s>: response: <%s>, content <%s>' % (
            self.url, self.response, content)

    @property
    def status_code(self):
        """Status code for the response.

        :rtype: integer
        :returns: the code
        """
        return int(self.response['status'])

    @classmethod
    def from_response(cls, http_response):
        """Factory:  construct an exception from a response.

        :type http_response: :class:`gcloud.streaming.http_wrapper.Response`
        :param http_response: the response which returned the error

        :rtype: :class:`HttpError`
        """
        return cls(http_response.info, http_response.content,
                   http_response.request_url)


class TransferError(CommunicationError):
    """Errors related to transfers."""


class TransferRetryError(TransferError):
    """Retryable errors related to transfers."""


class TransferInvalidError(TransferError):
    """The given transfer is invalid."""


class RequestError(CommunicationError):
    """The request was not successful."""


class RetryAfterError(HttpError):
    """The response contained a retry-after header.

    :type response: dict
    :param response: headers from the response which returned the error

    :type content: bytes
    :param content: payload of the response which returned the error

    :type url: string
    :param url: URL of the response which returned the error

    :type retry_after: integer
    :param retry_after: seconds to wait before retrying
    """
    def __init__(self, response, content, url, retry_after):
        super(RetryAfterError, self).__init__(response, content, url)
        self.retry_after = int(retry_after)

    @classmethod
    def from_response(cls, http_response):
        """Factory:  construct an exception from a response.

        :type http_response: :class:`gcloud.streaming.http_wrapper.Response`
        :param http_response: the response which returned the error

        :rtype: :class:`RetryAfterError`
        """
        return cls(http_response.info, http_response.content,
                   http_response.request_url, http_response.retry_after)


class BadStatusCodeError(HttpError):
    """The request completed but returned a bad status code."""
