# pylint: disable=too-many-lines

# Copyright 2016 Google Inc. All rights reserved.
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

"""Upload and download support for apitools."""

import email.generator as email_generator
import email.mime.multipart as mime_multipart
import email.mime.nonmultipart as mime_nonmultipart
import mimetypes
import os

import six
from six.moves import http_client

from gcloud._helpers import _to_bytes
from gcloud.streaming.buffered_stream import BufferedStream
from gcloud.streaming.exceptions import CommunicationError
from gcloud.streaming.exceptions import HttpError
from gcloud.streaming.exceptions import TransferInvalidError
from gcloud.streaming.exceptions import TransferRetryError
from gcloud.streaming.http_wrapper import get_http
from gcloud.streaming.http_wrapper import make_api_request
from gcloud.streaming.http_wrapper import Request
from gcloud.streaming.http_wrapper import RESUME_INCOMPLETE
from gcloud.streaming.stream_slice import StreamSlice
from gcloud.streaming.util import acceptable_mime_type


RESUMABLE_UPLOAD_THRESHOLD = 5 << 20
SIMPLE_UPLOAD = 'simple'
RESUMABLE_UPLOAD = 'resumable'


_DEFAULT_CHUNKSIZE = 1 << 20


class _Transfer(object):
    """Generic bits common to Uploads and Downloads.

    :type stream: file-like object
    :param stream: stream to/from which data is downloaded/uploaded.

    :type close_stream: boolean
    :param close_stream: should this instance close the stream when deleted

    :type chunksize: integer
    :param chunksize: the size of chunks used to download/upload a file.

    :type auto_transfer: boolean
    :param auto_transfer: should this instance automatically begin transfering
                          data when initialized

    :type http: :class:`httplib2.Http` (or workalike)
    :param http: Http instance used to perform requests.

    :type num_retries: integer
    :param num_retries: how many retries should the transfer attempt
    """

    _num_retries = None

    def __init__(self, stream, close_stream=False,
                 chunksize=_DEFAULT_CHUNKSIZE, auto_transfer=True,
                 http=None, num_retries=5):
        self._bytes_http = None
        self._close_stream = close_stream
        self._http = http
        self._stream = stream
        self._url = None

        # Let the @property do validation.
        self.num_retries = num_retries

        self.auto_transfer = auto_transfer
        self.chunksize = chunksize

    def __repr__(self):
        return str(self)

    @property
    def close_stream(self):
        """Should this instance close the stream when deleted.

        :rtype: boolean
        :returns: Boolean indicated if the stream should be closed.
        """
        return self._close_stream

    @property
    def http(self):
        """Http instance used to perform requests.

        :rtype: :class:`httplib2.Http` (or workalike)
        :returns: The HTTP object used for requests.
        """
        return self._http

    @property
    def bytes_http(self):
        """Http instance used to perform binary requests.

        Defaults to :attr:`http`.

        :rtype: :class:`httplib2.Http` (or workalike)
        :returns: The HTTP object used for binary requests.
        """
        return self._bytes_http or self.http

    @bytes_http.setter
    def bytes_http(self, value):
        """Update Http instance used to perform binary requests.

        :type value: :class:`httplib2.Http` (or workalike)
        :param value: new instance
        """
        self._bytes_http = value

    @property
    def num_retries(self):
        """How many retries should the transfer attempt

        :rtype: integer
        :returns: The number of retries allowed.
        """
        return self._num_retries

    @num_retries.setter
    def num_retries(self, value):
        """Update how many retries should the transfer attempt

        :type value: integer
        """
        if not isinstance(value, six.integer_types):
            raise ValueError("num_retries: pass an integer")

        if value < 0:
            raise ValueError(
                'Cannot have negative value for num_retries')
        self._num_retries = value

    @property
    def stream(self):
        """Stream to/from which data is downloaded/uploaded.

        :rtype: file-like object
        :returns: The stream that sends/receives data.
        """
        return self._stream

    @property
    def url(self):
        """URL to / from which data is downloaded/uploaded.

        :rtype: string
        :returns: The URL where data is sent/received.
        """
        return self._url

    def _initialize(self, http, url):
        """Initialize this download by setting :attr:`http` and :attr`url`.

        Allow the user to be able to pre-initialize :attr:`http` by setting
        the value in the constructor; in that case, we ignore the provided
        http.

        :type http: :class:`httplib2.Http` (or a worklike) or None.
        :param http: the Http instance to use to make requests.

        :type url: string
        :param url: The url for this transfer.
        """
        self._ensure_uninitialized()
        if self.http is None:
            self._http = http or get_http()
        self._url = url

    @property
    def initialized(self):
        """Has the instance been initialized

        :rtype: boolean
        :returns: Boolean indicating if the current transfer
                  has been initialized.
        """
        return self.url is not None and self.http is not None

    def _ensure_initialized(self):
        """Helper:  assert that the instance is initialized.

        :raises: :exc:`gcloud.streaming.exceptions.TransferInvalidError`
                 if the instance is not initialized.
        """
        if not self.initialized:
            raise TransferInvalidError(
                'Cannot use uninitialized %s', type(self).__name__)

    def _ensure_uninitialized(self):
        """Helper:  assert that the instance is not initialized.

        :raises: :exc:`gcloud.streaming.exceptions.TransferInvalidError`
                 if the instance is already initialized.
        """
        if self.initialized:
            raise TransferInvalidError(
                'Cannot re-initialize %s', type(self).__name__)

    def __del__(self):
        if self._close_stream:
            self._stream.close()


class Download(_Transfer):
    """Represent a single download.

    :type stream: file-like object
    :param stream: stream to/from which data is downloaded/uploaded.

    :type kwds: dict
    :param kwds:  keyword arguments:  all except ``total_size`` are passed
                  through to :meth:`_Transfer.__init__()`.
    """
    _ACCEPTABLE_STATUSES = set((
        http_client.OK,
        http_client.NO_CONTENT,
        http_client.PARTIAL_CONTENT,
        http_client.REQUESTED_RANGE_NOT_SATISFIABLE,
    ))

    def __init__(self, stream, **kwds):
        total_size = kwds.pop('total_size', None)
        super(Download, self).__init__(stream, **kwds)
        self._initial_response = None
        self._progress = 0
        self._total_size = total_size
        self._encoding = None

    @classmethod
    def from_file(cls, filename, overwrite=False, auto_transfer=True, **kwds):
        """Create a new download object from a filename.

        :type filename: string
        :param filename: path/filename for the target file

        :type overwrite: boolean
        :param overwrite: should an existing file be overwritten

        :type auto_transfer: boolean
        :param auto_transfer: should the transfer be started immediately

        :type kwds: dict
        :param kwds:  keyword arguments:  passed
                      through to :meth:`_Transfer.__init__()`.

        :rtype: :class:`Download`
        :returns: The download initiated from the file passed.
        """
        path = os.path.expanduser(filename)
        if os.path.exists(path) and not overwrite:
            raise ValueError(
                'File %s exists and overwrite not specified' % path)
        return cls(open(path, 'wb'), close_stream=True,
                   auto_transfer=auto_transfer, **kwds)

    @classmethod
    def from_stream(cls, stream, auto_transfer=True, total_size=None, **kwds):
        """Create a new Download object from a stream.

        :type stream: writable file-like object
        :param stream: the target file

        :type total_size: integer or None
        :param total_size: total size of the file to be downloaded

        :type auto_transfer: boolean
        :param auto_transfer: should the transfer be started immediately

        :type kwds: dict
        :param kwds:  keyword arguments:  passed
                      through to :meth:`_Transfer.__init__()`.

        :rtype: :class:`Download`
        :returns: The download initiated from the stream passed.
        """
        return cls(stream, auto_transfer=auto_transfer, total_size=total_size,
                   **kwds)

    @property
    def progress(self):
        """Number of bytes have been downloaded.

        :rtype: integer >= 0
        :returns: The number of downloaded bytes.
        """
        return self._progress

    @property
    def total_size(self):
        """Total number of bytes to be downloaded.

        :rtype: integer or None
        :returns: The total number of bytes to download.
        """
        return self._total_size

    @property
    def encoding(self):
        """'Content-Encoding' used to transfer the file

        :rtype: string or None
        :returns: The encoding of the downloaded content.
        """
        return self._encoding

    def __repr__(self):
        if not self.initialized:
            return 'Download (uninitialized)'
        else:
            return 'Download with %d/%s bytes transferred from url %s' % (
                self.progress, self.total_size, self.url)

    def configure_request(self, http_request, url_builder):
        """Update http_request/url_builder with download-appropriate values.

        :type http_request: :class:`gcloud.streaming.http_wrapper.Request`
        :param http_request: the request to be updated

        :type url_builder: instance with settable 'query_params' attribute.
        :param url_builder: transfer policy object to be updated
        """
        url_builder.query_params['alt'] = 'media'
        http_request.headers['Range'] = 'bytes=0-%d' % (self.chunksize - 1,)

    def _set_total(self, info):
        """Update 'total_size' based on data from a response.

        :type info: mapping
        :param info: response headers
        """
        if 'content-range' in info:
            _, _, total = info['content-range'].rpartition('/')
            if total != '*':
                self._total_size = int(total)
        # Note "total_size is None" means we don't know it; if no size
        # info was returned on our initial range request, that means we
        # have a 0-byte file. (That last statement has been verified
        # empirically, but is not clearly documented anywhere.)
        if self.total_size is None:
            self._total_size = 0

    def initialize_download(self, http_request, http):
        """Initialize this download.

        If the instance has :attr:`auto_transfer` enabled, begins the
        download immediately.

        :type http_request: :class:`gcloud.streaming.http_wrapper.Request`
        :param http_request: the request to use to initialize this download.

        :type http: :class:`httplib2.Http` (or workalike)
        :param http: Http instance for this request.
        """
        self._ensure_uninitialized()
        url = http_request.url
        if self.auto_transfer:
            end_byte = self._compute_end_byte(0)
            self._set_range_header(http_request, 0, end_byte)
            response = make_api_request(
                self.bytes_http or http, http_request)
            if response.status_code not in self._ACCEPTABLE_STATUSES:
                raise HttpError.from_response(response)
            self._initial_response = response
            self._set_total(response.info)
            url = response.info.get('content-location', response.request_url)
        self._initialize(http, url)
        # Unless the user has requested otherwise, we want to just
        # go ahead and pump the bytes now.
        if self.auto_transfer:
            self.stream_file(use_chunks=True)

    def _normalize_start_end(self, start, end=None):
        """Validate / fix up byte range.

        :type start: integer
        :param start: start byte of the range:  if negative, used as an
                      offset from the end.

        :type end: integer
        :param end: end byte of the range.

        :rtype: tuple, (start, end)
        :returns:  the normalized start, end pair.
        :raises: :exc:`gcloud.streaming.exceptions.TransferInvalidError`
                 for invalid combinations of start, end.
        """
        if end is not None:
            if start < 0:
                raise TransferInvalidError(
                    'Cannot have end index with negative start index')
            elif start >= self.total_size:
                raise TransferInvalidError(
                    'Cannot have start index greater than total size')
            end = min(end, self.total_size - 1)
            if end < start:
                raise TransferInvalidError(
                    'Range requested with end[%s] < start[%s]' % (end, start))
            return start, end
        else:
            if start < 0:
                start = max(0, start + self.total_size)
            return start, self.total_size - 1

    @staticmethod
    def _set_range_header(request, start, end=None):
        """Update the 'Range' header in a request to match a byte range.

        :type request: :class:`gcloud.streaming.http_wrapper.Request`
        :param request: the request to update

        :type start: integer
        :param start: start byte of the range:  if negative, used as an
                      offset from the end.

        :type end: integer
        :param end: end byte of the range.
        """
        if start < 0:
            request.headers['range'] = 'bytes=%d' % start
        elif end is None:
            request.headers['range'] = 'bytes=%d-' % start
        else:
            request.headers['range'] = 'bytes=%d-%d' % (start, end)

    def _compute_end_byte(self, start, end=None, use_chunks=True):
        """Compute the last byte to fetch for this request.

        Based on the HTTP spec for Range and Content-Range.

        .. note::
           This is potentially confusing in several ways:
           - the value for the last byte is 0-based, eg "fetch 10 bytes
             from the beginning" would return 9 here.
           - if we have no information about size, and don't want to
             use the chunksize, we'll return None.

        :type start: integer
        :param start: start byte of the range.

        :type end: integer or None
        :param end: suggested last byte of the range.

        :type use_chunks: boolean
        :param use_chunks: If False, ignore :attr:`chunksize`.

        :rtype: str
        :returns: Last byte to use in a 'Range' header, or None.
        """
        end_byte = end

        if start < 0 and not self.total_size:
            return end_byte

        if use_chunks:
            alternate = start + self.chunksize - 1
            if end_byte is not None:
                end_byte = min(end_byte, alternate)
            else:
                end_byte = alternate

        if self.total_size:
            alternate = self.total_size - 1
            if end_byte is not None:
                end_byte = min(end_byte, alternate)
            else:
                end_byte = alternate

        return end_byte

    def _get_chunk(self, start, end):
        """Retrieve a chunk of the file.

        :type start: integer
        :param start: start byte of the range.

        :type end: integer or None
        :param end: end byte of the range.

        :rtype: :class:`gcloud.streaming.http_wrapper.Response`
        :returns: response from the chunk request.
        """
        self._ensure_initialized()
        request = Request(url=self.url)
        self._set_range_header(request, start, end=end)
        return make_api_request(
            self.bytes_http, request, retries=self.num_retries)

    def _process_response(self, response):
        """Update attribtes and writing stream, based on response.

        :type response: :class:`gcloud.streaming.http_wrapper.Response`
        :param response: response from a download request.

        :rtype: :class:`gcloud.streaming.http_wrapper.Response`
        :returns: the response
        :raises: :exc:`gcloud.streaming.exceptions.HttpError` for
                 missing / unauthorized responses;
                 :exc:`gcloud.streaming.exceptions.TransferRetryError`
                 for other error responses.
        """
        if response.status_code not in self._ACCEPTABLE_STATUSES:
            # We distinguish errors that mean we made a mistake in setting
            # up the transfer versus something we should attempt again.
            if response.status_code in (http_client.FORBIDDEN,
                                        http_client.NOT_FOUND):
                raise HttpError.from_response(response)
            else:
                raise TransferRetryError(response.content)
        if response.status_code in (http_client.OK,
                                    http_client.PARTIAL_CONTENT):
            self.stream.write(response.content)
            self._progress += response.length
            if response.info and 'content-encoding' in response.info:
                self._encoding = response.info['content-encoding']
        elif response.status_code == http_client.NO_CONTENT:
            # It's important to write something to the stream for the case
            # of a 0-byte download to a file, as otherwise python won't
            # create the file.
            self.stream.write('')
        return response

    def get_range(self, start, end=None, use_chunks=True):
        """Retrieve a given byte range from this download, inclusive.

        Writes retrieved bytes into :attr:`stream`.

        Range must be of one of these three forms:
        * 0 <= start, end = None: Fetch from start to the end of the file.
        * 0 <= start <= end: Fetch the bytes from start to end.
        * start < 0, end = None: Fetch the last -start bytes of the file.

        (These variations correspond to those described in the HTTP 1.1
        protocol for range headers in RFC 2616, sec. 14.35.1.)

        :type start: integer
        :param start: Where to start fetching bytes. (See above.)

        :type end: integer or ``None``
        :param end: Where to stop fetching bytes. (See above.)

        :type use_chunks: boolean
        :param use_chunks: If False, ignore :attr:`chunksize`
                           and fetch this range in a single request.
                           If True, streams via chunks.

        :raises: :exc:`gcloud.streaming.exceptions.TransferRetryError`
                 if a request returns an empty response.
        """
        self._ensure_initialized()
        progress_end_normalized = False
        if self.total_size is not None:
            progress, end_byte = self._normalize_start_end(start, end)
            progress_end_normalized = True
        else:
            progress = start
            end_byte = end
        while (not progress_end_normalized or end_byte is None or
               progress <= end_byte):
            end_byte = self._compute_end_byte(progress, end=end_byte,
                                              use_chunks=use_chunks)
            response = self._get_chunk(progress, end_byte)
            if not progress_end_normalized:
                self._set_total(response.info)
                progress, end_byte = self._normalize_start_end(start, end)
                progress_end_normalized = True
            response = self._process_response(response)
            progress += response.length
            if response.length == 0:
                raise TransferRetryError(
                    'Zero bytes unexpectedly returned in download response')

    def stream_file(self, use_chunks=True):
        """Stream the entire download.

        Writes retrieved bytes into :attr:`stream`.

        :type use_chunks: boolean
        :param use_chunks: If False, ignore :attr:`chunksize`
                           and stream this download in a single request.
                           If True, streams via chunks.
        """
        self._ensure_initialized()
        while True:
            if self._initial_response is not None:
                response = self._initial_response
                self._initial_response = None
            else:
                end_byte = self._compute_end_byte(self.progress,
                                                  use_chunks=use_chunks)
                response = self._get_chunk(self.progress, end_byte)
            if self.total_size is None:
                self._set_total(response.info)
            response = self._process_response(response)
            if (response.status_code == http_client.OK or
                    self.progress >= self.total_size):
                break


class Upload(_Transfer):
    """Represent a single Upload.

    :type stream: file-like object
    :param stream: stream to/from which data is downloaded/uploaded.

    :type mime_type: string:
    :param mime_type: MIME type of the upload.

    :type total_size: integer or None
    :param total_size: Total upload size for the stream.

    :type http: :class:`httplib2.Http` (or workalike)
    :param http: Http instance used to perform requests.

    :type close_stream: boolean
    :param close_stream: should this instance close the stream when deleted

    :type auto_transfer: boolean
    :param auto_transfer: should this instance automatically begin transfering
                          data when initialized

    :type kwds: dict
    :param kwds:  keyword arguments:  all except ``total_size`` are passed
                  through to :meth:`_Transfer.__init__()`.
    """
    _REQUIRED_SERIALIZATION_KEYS = set((
        'auto_transfer', 'mime_type', 'total_size', 'url'))

    def __init__(self, stream, mime_type, total_size=None, http=None,
                 close_stream=False, auto_transfer=True,
                 **kwds):
        super(Upload, self).__init__(
            stream, close_stream=close_stream, auto_transfer=auto_transfer,
            http=http, **kwds)
        self._final_response = None
        self._server_chunk_granularity = None
        self._complete = False
        self._mime_type = mime_type
        self._progress = 0
        self._strategy = None
        self._total_size = total_size

    @classmethod
    def from_file(cls, filename, mime_type=None, auto_transfer=True, **kwds):
        """Create a new Upload object from a filename.

        :type filename: string
        :param filename: path/filename to the file being uploaded

        :type mime_type: string
        :param mime_type:  MIMEtype of the file being uploaded

        :type auto_transfer: boolean or None
        :param auto_transfer: should the transfer be started immediately

        :type kwds: dict
        :param kwds:  keyword arguments:  passed
                      through to :meth:`_Transfer.__init__()`.

        :rtype: :class:`Upload`
        :returns: The upload initiated from the file passed.
        """
        path = os.path.expanduser(filename)
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(path)
            if mime_type is None:
                raise ValueError(
                    'Could not guess mime type for %s' % path)
        size = os.stat(path).st_size
        return cls(open(path, 'rb'), mime_type, total_size=size,
                   close_stream=True, auto_transfer=auto_transfer, **kwds)

    @classmethod
    def from_stream(cls, stream, mime_type,
                    total_size=None, auto_transfer=True, **kwds):
        """Create a new Upload object from a stream.

        :type stream: writable file-like object
        :param stream: the target file

        :type mime_type: string
        :param mime_type:  MIMEtype of the file being uploaded

        :type total_size: integer or None
        :param total_size:  Size of the file being uploaded

        :type auto_transfer: boolean or None
        :param auto_transfer: should the transfer be started immediately

        :type kwds: dict
        :param kwds:  keyword arguments:  passed
                      through to :meth:`_Transfer.__init__()`.

        :rtype: :class:`Upload`
        :returns: The upload initiated from the stream passed.
        """
        if mime_type is None:
            raise ValueError(
                'No mime_type specified for stream')
        return cls(stream, mime_type, total_size=total_size,
                   close_stream=False, auto_transfer=auto_transfer, **kwds)

    @property
    def complete(self):
        """Has the entire stream been uploaded.

        :rtype: boolean
        :returns: Boolean indicated if the upload is complete.
        """
        return self._complete

    @property
    def mime_type(self):
        """MIMEtype of the file being uploaded.

        :rtype: string
        :returns: The mime-type of the upload.
        """
        return self._mime_type

    @property
    def progress(self):
        """Bytes uploaded so far

        :rtype: integer
        :returns: The amount uploaded so far.
        """
        return self._progress

    @property
    def strategy(self):
        """Upload strategy to use

        :rtype: string or None
        :returns: The strategy used to upload the data.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        """Update upload strategy to use

        :type value: string (one of :data:`SIMPLE_UPLOAD` or
                :data:`RESUMABLE_UPLOAD`)

        :raises: :exc:`ValueError` if value is not one of the two allowed
                 strings.
        """
        if value not in (SIMPLE_UPLOAD, RESUMABLE_UPLOAD):
            raise ValueError((
                'Invalid value "%s" for upload strategy, must be one of '
                '"simple" or "resumable".') % value)
        self._strategy = value

    @property
    def total_size(self):
        """Total size of the stream to be uploaded.

        :rtype: integer or None
        :returns: The total size to be uploaded.
        """
        return self._total_size

    @total_size.setter
    def total_size(self, value):
        """Update total size of the stream to be uploaded.

        :type value: integer or None
        :param value: the size
        """
        self._ensure_uninitialized()
        self._total_size = value

    def __repr__(self):
        if not self.initialized:
            return 'Upload (uninitialized)'
        else:
            return 'Upload with %d/%s bytes transferred for url %s' % (
                self.progress, self.total_size or '???', self.url)

    def _set_default_strategy(self, upload_config, http_request):
        """Determine and set the default upload strategy for this upload.

        We generally prefer simple or multipart, unless we're forced to
        use resumable. This happens when any of (1) the upload is too
        large, (2) the simple endpoint doesn't support multipart requests
        and we have metadata, or (3) there is no simple upload endpoint.

        :type upload_config: instance w/ ``max_size`` and ``accept``
                             attributes
        :param upload_config: Configuration for the upload endpoint.

        :type http_request: :class:`gcloud.streaming.http_wrapper.Request`
        :param http_request: The associated http request.
        """
        if upload_config.resumable_path is None:
            self.strategy = SIMPLE_UPLOAD
        if self.strategy is not None:
            return
        strategy = SIMPLE_UPLOAD
        if (self.total_size is not None and
                self.total_size > RESUMABLE_UPLOAD_THRESHOLD):
            strategy = RESUMABLE_UPLOAD
        if http_request.body and not upload_config.simple_multipart:
            strategy = RESUMABLE_UPLOAD
        if not upload_config.simple_path:
            strategy = RESUMABLE_UPLOAD
        self.strategy = strategy

    def configure_request(self, upload_config, http_request, url_builder):
        """Configure the request and url for this upload.

        :type upload_config: instance w/ ``max_size`` and ``accept``
                             attributes
        :param upload_config: transfer policy object to be queried

        :type http_request: :class:`gcloud.streaming.http_wrapper.Request`
        :param http_request: the request to be updated

        :type url_builder: instance with settable 'relative_path' and
                           'query_params' attributes.
        :param url_builder: transfer policy object to be updated

        :raises: :exc:`ValueError` if the requested upload is too big,
                  or does not have an acceptable MIME type.
        """
        # Validate total_size vs. max_size
        if (self.total_size and upload_config.max_size and
                self.total_size > upload_config.max_size):
            raise ValueError(
                'Upload too big: %s larger than max size %s' % (
                    self.total_size, upload_config.max_size))
        # Validate mime type
        if not acceptable_mime_type(upload_config.accept, self.mime_type):
            raise ValueError(
                'MIME type %s does not match any accepted MIME ranges %s' % (
                    self.mime_type, upload_config.accept))

        self._set_default_strategy(upload_config, http_request)
        if self.strategy == SIMPLE_UPLOAD:
            url_builder.relative_path = upload_config.simple_path
            if http_request.body:
                url_builder.query_params['uploadType'] = 'multipart'
                self._configure_multipart_request(http_request)
            else:
                url_builder.query_params['uploadType'] = 'media'
                self._configure_media_request(http_request)
        else:
            url_builder.relative_path = upload_config.resumable_path
            url_builder.query_params['uploadType'] = 'resumable'
            self._configure_resumable_request(http_request)

    def _configure_media_request(self, http_request):
        """Helper for 'configure_request': set up simple request."""
        http_request.headers['content-type'] = self.mime_type
        http_request.body = self.stream.read()
        http_request.loggable_body = '<media body>'

    def _configure_multipart_request(self, http_request):
        """Helper for 'configure_request': set up multipart request."""
        # This is a multipart/related upload.
        msg_root = mime_multipart.MIMEMultipart('related')
        # msg_root should not write out its own headers
        setattr(msg_root, '_write_headers', lambda self: None)

        # attach the body as one part
        msg = mime_nonmultipart.MIMENonMultipart(
            *http_request.headers['content-type'].split('/'))
        msg.set_payload(http_request.body)
        msg_root.attach(msg)

        # attach the media as the second part
        msg = mime_nonmultipart.MIMENonMultipart(*self.mime_type.split('/'))
        msg['Content-Transfer-Encoding'] = 'binary'
        msg.set_payload(self.stream.read())
        msg_root.attach(msg)

        # NOTE: generate multipart message as bytes, not text
        stream = six.BytesIO()
        if six.PY3:  # pragma: NO COVER  Python3
            generator_class = email_generator.BytesGenerator
        else:
            generator_class = email_generator.Generator
        generator = generator_class(stream, mangle_from_=False)
        generator.flatten(msg_root, unixfrom=False)
        http_request.body = stream.getvalue()

        multipart_boundary = msg_root.get_boundary()
        http_request.headers['content-type'] = (
            'multipart/related; boundary="%s"' % multipart_boundary)

        boundary_bytes = _to_bytes(multipart_boundary)
        body_components = http_request.body.split(boundary_bytes)
        headers, _, _ = body_components[-2].partition(b'\n\n')
        body_components[-2] = b'\n\n'.join([headers, b'<media body>\n\n--'])
        http_request.loggable_body = boundary_bytes.join(body_components)

    def _configure_resumable_request(self, http_request):
        """Helper for 'configure_request': set up resumable request."""
        http_request.headers['X-Upload-Content-Type'] = self.mime_type
        if self.total_size is not None:
            http_request.headers[
                'X-Upload-Content-Length'] = str(self.total_size)

    def refresh_upload_state(self):
        """Refresh the state of a resumable upload via query to the back-end.
        """
        if self.strategy != RESUMABLE_UPLOAD:
            return
        self._ensure_initialized()
        # NOTE: Per RFC 2616[1]/7231[2], a 'PUT' request is inappropriate
        #       here:  it is intended to be used to replace the entire
        #       resource, not to  query for a status.
        #
        #       If the back-end doesn't provide a way to query for this state
        #       via a 'GET' request, somebody should be spanked.
        #
        #       The violation is documented[3].
        #
        # [1] http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.6
        # [2] http://tools.ietf.org/html/rfc7231#section-4.3.4
        # [3]
        # https://cloud.google.com/storage/docs/json_api/v1/how-tos/upload#resume-upload
        refresh_request = Request(
            url=self.url, http_method='PUT',
            headers={'Content-Range': 'bytes */*'})
        refresh_response = make_api_request(
            self.http, refresh_request, redirections=0,
            retries=self.num_retries)
        range_header = self._get_range_header(refresh_response)
        if refresh_response.status_code in (http_client.OK,
                                            http_client.CREATED):
            self._complete = True
            self._progress = self.total_size
            self.stream.seek(self.progress)
            # If we're finished, the refresh response will contain the metadata
            # originally requested. Cache it so it can be returned in
            # StreamInChunks.
            self._final_response = refresh_response
        elif refresh_response.status_code == RESUME_INCOMPLETE:
            if range_header is None:
                self._progress = 0
            else:
                self._progress = self._last_byte(range_header) + 1
            self.stream.seek(self.progress)
        else:
            raise HttpError.from_response(refresh_response)

    @staticmethod
    def _get_range_header(response):
        """Return a 'Range' header from a response.

        :type response: :class:`gcloud.streaming.http_wrapper.Response`
        :param response: response to be queried

        :rtype: string
        :returns: The header used to determine the bytes range.
        """
        # NOTE: Per RFC 2616[1]/7233[2][3], 'Range' is a request header,
        #       not a response header.  If the back-end is actually setting
        #       'Range' on responses, somebody should be spanked:  it should
        #       be sending 'Content-Range' (including the # '/<length>'
        #       trailer).
        #
        #       The violation is documented[4].
        #
        # [1] http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        # [2] http://tools.ietf.org/html/rfc7233#section-3.1
        # [3] http://tools.ietf.org/html/rfc7233#section-4.2
        # [4]
        # https://cloud.google.com/storage/docs/json_api/v1/how-tos/upload#chunking
        return response.info.get('Range', response.info.get('range'))

    def initialize_upload(self, http_request, http):
        """Initialize this upload from the given http_request.

        :type http_request: :class:`gcloud.streaming.http_wrapper.Request`
        :param http_request: the request to be used

        :type http: :class:`httplib2.Http` (or workalike)
        :param http: Http instance for this request.

        :raises: :exc:`ValueError` if the instance has not been configured
                 with a strategy.
        :rtype: :class:`~gcloud.streaming.http_wrapper.Response`
        :returns: The response if the upload is resumable and auto transfer
                  is not used.
        """
        if self.strategy is None:
            raise ValueError(
                'No upload strategy set; did you call configure_request?')
        if self.strategy != RESUMABLE_UPLOAD:
            return
        self._ensure_uninitialized()
        http_response = make_api_request(http, http_request,
                                         retries=self.num_retries)
        if http_response.status_code != http_client.OK:
            raise HttpError.from_response(http_response)

        granularity = http_response.info.get('X-Goog-Upload-Chunk-Granularity')
        if granularity is not None:
            granularity = int(granularity)
        self._server_chunk_granularity = granularity
        url = http_response.info['location']
        self._initialize(http, url)

        # Unless the user has requested otherwise, we want to just
        # go ahead and pump the bytes now.
        if self.auto_transfer:
            return self.stream_file(use_chunks=True)
        else:
            return http_response

    @staticmethod
    def _last_byte(range_header):
        """Parse the last byte from a 'Range' header.

        :type range_header: string
        :param range_header: 'Range' header value per RFC 2616/7233

        :rtype: int
        :returns: The last byte from a range header.
        """
        _, _, end = range_header.partition('-')
        return int(end)

    def _validate_chunksize(self, chunksize=None):
        """Validate chunksize against server-specified granularity.

        Helper for :meth:`stream_file`.

        :type chunksize: integer or None
        :param chunksize: the chunk size to be tested.

        :raises: :exc:`ValueError` if ``chunksize`` is not a multiple
                 of the server-specified granulariy.
        """
        if self._server_chunk_granularity is None:
            return
        chunksize = chunksize or self.chunksize
        if chunksize % self._server_chunk_granularity:
            raise ValueError(
                'Server requires chunksize to be a multiple of %d',
                self._server_chunk_granularity)

    def stream_file(self, use_chunks=True):
        """Upload the stream.

        :type use_chunks: boolean
        :param use_chunks: If False, send the stream in a single request.
                           Otherwise, send it in chunks.

        :rtype: :class:`gcloud.streaming.http_wrapper.Response`
        :returns: The response for the final request made.
        """
        if self.strategy != RESUMABLE_UPLOAD:
            raise ValueError(
                'Cannot stream non-resumable upload')
        # final_response is set if we resumed an already-completed upload.
        response = self._final_response
        send_func = self._send_chunk if use_chunks else self._send_media_body
        if use_chunks:
            self._validate_chunksize(self.chunksize)
        self._ensure_initialized()
        while not self.complete:
            response = send_func(self.stream.tell())
            if response.status_code in (http_client.OK, http_client.CREATED):
                self._complete = True
                break
            self._progress = self._last_byte(response.info['range'])
            if self.progress + 1 != self.stream.tell():
                raise CommunicationError(
                    'Failed to transfer all bytes in chunk, upload paused at '
                    'byte %d' % self.progress)
        if self.complete and hasattr(self.stream, 'seek'):
            if not hasattr(self.stream, 'seekable') or self.stream.seekable():
                current_pos = self.stream.tell()
                self.stream.seek(0, os.SEEK_END)
                end_pos = self.stream.tell()
                self.stream.seek(current_pos)
                if current_pos != end_pos:
                    raise TransferInvalidError(
                        'Upload complete with %s '
                        'additional bytes left in stream' %
                        (int(end_pos) - int(current_pos)))
        return response

    def _send_media_request(self, request, end):
        """Peform API upload request.

        Helper for _send_media_body & _send_chunk:

        :type request: :class:`gcloud.streaming.http_wrapper.Request`
        :param request: the request to upload

        :type end: integer
        :param end: end byte of the to be uploaded

        :rtype: :class:`gcloud.streaming.http_wrapper.Response`
        :returns: the response
        :raises: :exc:`gcloud.streaming.exceptions.HttpError` if the status
                 code from the response indicates an error.
        """
        response = make_api_request(
            self.bytes_http, request, retries=self.num_retries)
        if response.status_code not in (http_client.OK, http_client.CREATED,
                                        RESUME_INCOMPLETE):
            # We want to reset our state to wherever the server left us
            # before this failed request, and then raise.
            self.refresh_upload_state()
            raise HttpError.from_response(response)
        if response.status_code == RESUME_INCOMPLETE:
            last_byte = self._last_byte(
                self._get_range_header(response))
            if last_byte + 1 != end:
                self.stream.seek(last_byte)
        return response

    def _send_media_body(self, start):
        """Send the entire stream in a single request.

        Helper for :meth:`stream_file`:

        :type start: integer
        :param start: start byte of the range.

        :rtype: :class:`gcloud.streaming.http_wrapper.Response`
        :returns: The response from the media upload request.
        """
        self._ensure_initialized()
        if self.total_size is None:
            raise TransferInvalidError(
                'Total size must be known for SendMediaBody')
        body_stream = StreamSlice(self.stream, self.total_size - start)

        request = Request(url=self.url, http_method='PUT', body=body_stream)
        request.headers['Content-Type'] = self.mime_type
        if start == self.total_size:
            # End of an upload with 0 bytes left to send; just finalize.
            range_string = 'bytes */%s' % self.total_size
        else:
            range_string = 'bytes %s-%s/%s' % (start, self.total_size - 1,
                                               self.total_size)

        request.headers['Content-Range'] = range_string

        return self._send_media_request(request, self.total_size)

    def _send_chunk(self, start):
        """Send a chunk of the stream.

        Helper for :meth:`stream_file`:

        :type start: integer
        :param start: start byte of the range.

        :rtype: :class:`gcloud.streaming.http_wrapper.Response`
        :returns: The response from the chunked upload request.
        """
        self._ensure_initialized()
        no_log_body = self.total_size is None
        if self.total_size is None:
            # For the streaming resumable case, we need to detect when
            # we're at the end of the stream.
            body_stream = BufferedStream(
                self.stream, start, self.chunksize)
            end = body_stream.stream_end_position
            if body_stream.stream_exhausted:
                self._total_size = end
            # Here, change body_stream from a stream to a string object,
            # which means reading a chunk into memory.  This works around
            # https://code.google.com/p/httplib2/issues/detail?id=176 which can
            # cause httplib2 to skip bytes on 401's for file objects.
            body_stream = body_stream.read(self.chunksize)
        else:
            end = min(start + self.chunksize, self.total_size)
            body_stream = StreamSlice(self.stream, end - start)
        request = Request(url=self.url, http_method='PUT', body=body_stream)
        request.headers['Content-Type'] = self.mime_type
        if no_log_body:
            # Disable logging of streaming body.
            request.loggable_body = '<media body>'
        if self.total_size is None:
            # Streaming resumable upload case, unknown total size.
            range_string = 'bytes %s-%s/*' % (start, end - 1)
        elif end == start:
            # End of an upload with 0 bytes left to send; just finalize.
            range_string = 'bytes */%s' % self.total_size
        else:
            # Normal resumable upload case with known sizes.
            range_string = 'bytes %s-%s/%s' % (start, end - 1, self.total_size)

        request.headers['Content-Range'] = range_string

        return self._send_media_request(request, end)
