#!/usr/bin/env python
"""Upload and download support for apitools."""
from __future__ import print_function

import email.generator as email_generator
import email.mime.multipart as mime_multipart
import email.mime.nonmultipart as mime_nonmultipart
import io
import json
import mimetypes
import os
import threading

from six.moves import http_client

from _gcloud_vendor.apitools.base.py import exceptions
from _gcloud_vendor.apitools.base.py import http_wrapper
from _gcloud_vendor.apitools.base.py import util

__all__ = [
    'Download',
    'Upload',
]

_RESUMABLE_UPLOAD_THRESHOLD = 5 << 20
_SIMPLE_UPLOAD = 'simple'
_RESUMABLE_UPLOAD = 'resumable'


class _Transfer(object):
  """Generic bits common to Uploads and Downloads."""

  def __init__(self, stream, close_stream=False, chunksize=None,
               auto_transfer=True, http=None):
    self.__bytes_http = None
    self.__close_stream = close_stream
    self.__http = http
    self.__stream = stream
    self.__url = None

    self.auto_transfer = auto_transfer
    self.chunksize = chunksize or 1048576

  def __repr__(self):
    return str(self)

  @property
  def close_stream(self):
    return self.__close_stream

  @property
  def http(self):
    return self.__http

  @property
  def bytes_http(self):
    return self.__bytes_http or self.http

  @bytes_http.setter
  def bytes_http(self, value):
    self.__bytes_http = value

  @property
  def stream(self):
    return self.__stream

  @property
  def url(self):
    return self.__url

  def _Initialize(self, http, url):
    """Initialize this download by setting self.http and self.url.

    We want the user to be able to override self.http by having set
    the value in the constructor; in that case, we ignore the provided
    http.

    Args:
      http: An httplib2.Http instance or None.
      url: The url for this transfer.

    Returns:
      None. Initializes self.
    """
    self.EnsureUninitialized()
    if self.http is None:
      self.__http = http or http_wrapper.GetHttp()
    self.__url = url

  @property
  def initialized(self):
    return self.url is not None and self.http is not None

  @property
  def _type_name(self):
    return type(self).__name__

  def EnsureInitialized(self):
    if not self.initialized:
      raise exceptions.TransferInvalidError(
          'Cannot use uninitialized %s', self._type_name)

  def EnsureUninitialized(self):
    if self.initialized:
      raise exceptions.TransferInvalidError(
          'Cannot re-initialize %s', self._type_name)

  def __del__(self):
    if self.__close_stream:
      self.__stream.close()

  def _ExecuteCallback(self, callback, response):
    # TODO(craigcitro): Push these into a queue.
    if callback is not None:
      threading.Thread(target=callback, args=(response, self)).start()


class Download(_Transfer):
  """Data for a single download.

  Public attributes:
    chunksize: default chunksize to use for transfers.
  """
  _ACCEPTABLE_STATUSES = set((
      http_client.OK,
      http_client.NO_CONTENT,
      http_client.PARTIAL_CONTENT,
      http_client.REQUESTED_RANGE_NOT_SATISFIABLE,
  ))
  _REQUIRED_SERIALIZATION_KEYS = set((
      'auto_transfer', 'progress', 'total_size', 'url'))

  def __init__(self, *args, **kwds):
    super(Download, self).__init__(*args, **kwds)
    self.__initial_response = None
    self.__progress = 0
    self.__total_size = None

  @property
  def progress(self):
    return self.__progress

  @classmethod
  def FromFile(cls, filename, overwrite=False, auto_transfer=True):
    """Create a new download object from a filename."""
    path = os.path.expanduser(filename)
    if os.path.exists(path) and not overwrite:
      raise exceptions.InvalidUserInputError(
          'File %s exists and overwrite not specified' % path)
    return cls(open(path, 'wb'), close_stream=True, auto_transfer=auto_transfer)

  @classmethod
  def FromStream(cls, stream, auto_transfer=True):
    """Create a new Download object from a stream."""
    return cls(stream, auto_transfer=auto_transfer)

  @classmethod
  def FromData(cls, stream, json_data, http=None, auto_transfer=None):
    """Create a new Download object from a stream and serialized data."""
    info = json.loads(json_data)
    missing_keys = cls._REQUIRED_SERIALIZATION_KEYS - set(info.keys())
    if missing_keys:
      raise exceptions.InvalidDataError(
          'Invalid serialization data, missing keys: %s' % (
              ', '.join(missing_keys)))
    download = cls.FromStream(stream)
    if auto_transfer is not None:
      download.auto_transfer = auto_transfer
    else:
      download.auto_transfer = info['auto_transfer']
    setattr(download, '_Download__progress', info['progress'])
    setattr(download, '_Download__total_size', info['total_size'])
    download._Initialize(http, info['url'])  # pylint: disable=protected-access
    return download

  @property
  def serialization_data(self):
    self.EnsureInitialized()
    return {
        'auto_transfer': self.auto_transfer,
        'progress': self.progress,
        'total_size': self.total_size,
        'url': self.url,
    }

  @property
  def total_size(self):
    return self.__total_size

  def __str__(self):
    if not self.initialized:
      return 'Download (uninitialized)'
    else:
      return 'Download with %d/%s bytes transferred from url %s' % (
          self.progress, self.total_size, self.url)

  def ConfigureRequest(self, http_request, url_builder):
    url_builder.query_params['alt'] = 'media'
    http_request.headers['Range'] = 'bytes=0-%d' % (self.chunksize - 1,)

  def __SetTotal(self, info):
    if 'content-range' in info:
      _, _, total = info['content-range'].rpartition('/')
      if total != '*':
        self.__total_size = int(total)
    # Note "total_size is None" means we don't know it; if no size
    # info was returned on our initial range request, that means we
    # have a 0-byte file. (That last statement has been verified
    # empirically, but is not clearly documented anywhere.)
    if self.total_size is None:
      self.__total_size = 0

  def InitializeDownload(self, http_request, http=None, client=None):
    """Initialize this download by making a request.

    Args:
      http_request: The HttpRequest to use to initialize this download.
      http: The httplib2.Http instance for this request.
      client: If provided, let this client process the final URL before
          sending any additional requests. If client is provided and
          http is not, client.http will be used instead.
    """
    self.EnsureUninitialized()
    if http is None and client is None:
      raise exceptions.UserError('Must provide client or http.')
    http = http or client.http
    if client is not None:
      http_request.url = client.FinalizeTransferUrl(http_request.url)
    response = http_wrapper.MakeRequest(self.bytes_http or http, http_request)
    if response.status_code not in self._ACCEPTABLE_STATUSES:
      raise exceptions.HttpError.FromResponse(response)
    self.__initial_response = response
    self.__SetTotal(response.info)
    url = response.info.get('content-location', response.request_url)
    if client is not None:
      url = client.FinalizeTransferUrl(url)
    self._Initialize(http, url)
    # Unless the user has requested otherwise, we want to just
    # go ahead and pump the bytes now.
    if self.auto_transfer:
      self.StreamInChunks()

  @staticmethod
  def _ArgPrinter(response, unused_download):
    if 'content-range' in response.info:
      print('Received %s' % response.info['content-range'])
    else:
      print('Received %d bytes' % len(response))

  @staticmethod
  def _CompletePrinter(*unused_args):
    print('Download complete')

  def __NormalizeStartEnd(self, start, end=None):
    if end is not None:
      if start < 0:
        raise exceptions.TransferInvalidError(
            'Cannot have end index with negative start index')
      elif start >= self.total_size:
        raise exceptions.TransferInvalidError(
            'Cannot have start index greater than total size')
      end = min(end, self.total_size - 1)
      if end < start:
        raise exceptions.TransferInvalidError(
            'Range requested with end[%s] < start[%s]' % (end, start))
      return start, end
    else:
      if start < 0:
        start = max(0, start + self.total_size)
      return start, self.total_size

  def __SetRangeHeader(self, request, start, end=None):
    if start < 0:
      request.headers['range'] = 'bytes=%d' % start
    elif end is None:
      request.headers['range'] = 'bytes=%d-' % start
    else:
      request.headers['range'] = 'bytes=%d-%d' % (start, end)

  def __GetChunk(self, start, end=None, additional_headers=None):
    """Retrieve a chunk, and return the full response."""
    self.EnsureInitialized()
    end_byte = min(end or start + self.chunksize, self.total_size)
    request = http_wrapper.Request(url=self.url)
    self.__SetRangeHeader(request, start, end=end_byte)
    if additional_headers is not None:
      request.headers.update(additional_headers)
    return http_wrapper.MakeRequest(self.bytes_http, request)

  def __ProcessResponse(self, response):
    """Process this response (by updating self and writing to self.stream)."""
    if response.status_code not in self._ACCEPTABLE_STATUSES:
      raise exceptions.TransferInvalidError(response.content)
    if response.status_code in (http_client.OK, http_client.PARTIAL_CONTENT):
      self.stream.write(response.content)
      self.__progress += len(response)
    elif response.status_code == http_client.NO_CONTENT:
      # It's important to write something to the stream for the case
      # of a 0-byte download to a file, as otherwise python won't
      # create the file.
      self.stream.write('')
    return response

  def GetRange(self, start, end=None, additional_headers=None):
    """Retrieve a given byte range from this download, inclusive.

    Range must be of one of these three forms:
    * 0 <= start, end = None: Fetch from start to the end of the file.
    * 0 <= start <= end: Fetch the bytes from start to end.
    * start < 0, end = None: Fetch the last -start bytes of the file.

    (These variations correspond to those described in the HTTP 1.1
    protocol for range headers in RFC 2616, sec. 14.35.1.)

    Args:
      start: (int) Where to start fetching bytes. (See above.)
      end: (int, optional) Where to stop fetching bytes. (See above.)
      additional_headers: (bool, optional) Any additional headers to
          pass with the request.

    Returns:
      None. Streams bytes into self.stream.
    """
    self.EnsureInitialized()
    progress, end = self.__NormalizeStartEnd(start, end)
    while progress < end:
      chunk_end = min(progress + self.chunksize, end)
      response = self.__GetChunk(progress, end=chunk_end,
                                 additional_headers=additional_headers)
      response = self.__ProcessResponse(response)
      progress += len(response)
      if not response:
        raise exceptions.TransferInvalidError(
            'Zero bytes unexpectedly returned in download response')

  def StreamInChunks(self, callback=None, finish_callback=None,
                     additional_headers=None):
    """Stream the entire download."""
    callback = callback or self._ArgPrinter
    finish_callback = finish_callback or self._CompletePrinter

    self.EnsureInitialized()
    while True:
      if self.__initial_response is not None:
        response = self.__initial_response
        self.__initial_response = None
      else:
        response = self.__GetChunk(self.progress,
                                   additional_headers=additional_headers)
      response = self.__ProcessResponse(response)
      self._ExecuteCallback(callback, response)
      if (response.status_code == http_client.OK or
          self.progress >= self.total_size):
        break
    self._ExecuteCallback(finish_callback, response)


class Upload(_Transfer):
  """Data for a single Upload.

  Fields:
    stream: The stream to upload.
    mime_type: MIME type of the upload.
    total_size: (optional) Total upload size for the stream.
    close_stream: (default: False) Whether or not we should close the
        stream when finished with the upload.
    auto_transfer: (default: True) If True, stream all bytes as soon as
        the upload is created.
  """
  _REQUIRED_SERIALIZATION_KEYS = set((
      'auto_transfer', 'mime_type', 'total_size', 'url'))

  def __init__(self, stream, mime_type, total_size=None, http=None,
               close_stream=False, chunksize=None, auto_transfer=True):
    super(Upload, self).__init__(
        stream, close_stream=close_stream, chunksize=chunksize,
        auto_transfer=auto_transfer, http=http)
    self.__complete = False
    self.__mime_type = mime_type
    self.__progress = 0
    self.__server_chunk_granularity = None
    self.__strategy = None

    self.total_size = total_size

  @property
  def progress(self):
    return self.__progress

  @classmethod
  def FromFile(cls, filename, mime_type=None, auto_transfer=True):
    """Create a new Upload object from a filename."""
    path = os.path.expanduser(filename)
    if not os.path.exists(path):
      raise exceptions.NotFoundError('Could not find file %s' % path)
    if not mime_type:
      mime_type, _ = mimetypes.guess_type(path)
      if mime_type is None:
        raise exceptions.InvalidUserInputError(
            'Could not guess mime type for %s' % path)
    size = os.stat(path).st_size
    return cls(open(path, 'rb'), mime_type, total_size=size, close_stream=True,
               auto_transfer=auto_transfer)

  @classmethod
  def FromStream(cls, stream, mime_type, total_size=None, auto_transfer=True):
    """Create a new Upload object from a stream."""
    if mime_type is None:
      raise exceptions.InvalidUserInputError(
          'No mime_type specified for stream')
    return cls(stream, mime_type, total_size=total_size, close_stream=False,
               auto_transfer=auto_transfer)

  @classmethod
  def FromData(cls, stream, json_data, http, auto_transfer=None):
    """Create a new Upload of stream from serialized json_data using http."""
    info = json.loads(json_data)
    missing_keys = cls._REQUIRED_SERIALIZATION_KEYS - set(info.keys())
    if missing_keys:
      raise exceptions.InvalidDataError(
          'Invalid serialization data, missing keys: %s' % (
              ', '.join(missing_keys)))
    upload = cls.FromStream(stream, info['mime_type'],
                            total_size=info.get('total_size'))
    if isinstance(stream, io.IOBase) and not stream.seekable():
      raise exceptions.InvalidUserInputError(
          'Cannot restart resumable upload on non-seekable stream')
    if auto_transfer is not None:
      upload.auto_transfer = auto_transfer
    else:
      upload.auto_transfer = info['auto_transfer']
    upload.strategy = _RESUMABLE_UPLOAD
    upload._Initialize(http, info['url'])  # pylint: disable=protected-access
    upload._RefreshResumableUploadState()  # pylint: disable=protected-access
    upload.EnsureInitialized()
    if upload.auto_transfer:
      upload.StreamInChunks()
    return upload

  @property
  def serialization_data(self):
    self.EnsureInitialized()
    if self.strategy != _RESUMABLE_UPLOAD:
      raise exceptions.InvalidDataError(
          'Serialization only supported for resumable uploads')
    return {
        'auto_transfer': self.auto_transfer,
        'mime_type': self.mime_type,
        'total_size': self.total_size,
        'url': self.url,
    }

  @property
  def complete(self):
    return self.__complete

  @property
  def mime_type(self):
    return self.__mime_type

  def __str__(self):
    if not self.initialized:
      return 'Upload (uninitialized)'
    else:
      return 'Upload with %d/%s bytes transferred for url %s' % (
          self.progress, self.total_size or '???', self.url)

  @property
  def strategy(self):
    return self.__strategy

  @strategy.setter
  def strategy(self, value):
    if value not in (_SIMPLE_UPLOAD, _RESUMABLE_UPLOAD):
      raise exceptions.UserError((
          'Invalid value "%s" for upload strategy, must be one of '
          '"simple" or "resumable".') % value)
    self.__strategy = value

  @property
  def total_size(self):
    return self.__total_size

  @total_size.setter
  def total_size(self, value):
    self.EnsureUninitialized()
    self.__total_size = value

  def __SetDefaultUploadStrategy(self, upload_config, http_request):
    """Determine and set the default upload strategy for this upload.

    We generally prefer simple or multipart, unless we're forced to
    use resumable. This happens when any of (1) the upload is too
    large, (2) the simple endpoint doesn't support multipart requests
    and we have metadata, or (3) there is no simple upload endpoint.

    Args:
      upload_config: Configuration for the upload endpoint.
      http_request: The associated http request.

    Returns:
      None.
    """
    if self.strategy is not None:
      return
    strategy = _SIMPLE_UPLOAD
    if (self.total_size is not None and
        self.total_size > _RESUMABLE_UPLOAD_THRESHOLD):
      strategy = _RESUMABLE_UPLOAD
    if http_request.body and not upload_config.simple_multipart:
      strategy = _RESUMABLE_UPLOAD
    if not upload_config.simple_path:
      strategy = _RESUMABLE_UPLOAD
    self.strategy = strategy

  def ConfigureRequest(self, upload_config, http_request, url_builder):
    """Configure the request and url for this upload."""
    # Validate total_size vs. max_size
    if (self.total_size and upload_config.max_size and
        self.total_size > upload_config.max_size):
      raise exceptions.InvalidUserInputError(
          'Upload too big: %s larger than max size %s' % (
              self.total_size, upload_config.max_size))
    # Validate mime type
    if not util.AcceptableMimeType(upload_config.accept, self.mime_type):
      raise exceptions.InvalidUserInputError(
          'MIME type %s does not match any accepted MIME ranges %s' % (
              self.mime_type, upload_config.accept))

    self.__SetDefaultUploadStrategy(upload_config, http_request)
    if self.strategy == _SIMPLE_UPLOAD:
      url_builder.relative_path = upload_config.simple_path
      if http_request.body:
        url_builder.query_params['uploadType'] = 'multipart'
        self.__ConfigureMultipartRequest(http_request)
      else:
        url_builder.query_params['uploadType'] = 'media'
        self.__ConfigureMediaRequest(http_request)
    else:
      url_builder.relative_path = upload_config.resumable_path
      url_builder.query_params['uploadType'] = 'resumable'
      self.__ConfigureResumableRequest(http_request)

  def __ConfigureMediaRequest(self, http_request):
    """Configure http_request as a simple request for this upload."""
    http_request.headers['content-type'] = self.mime_type
    http_request.body = self.stream.read()

  def __ConfigureMultipartRequest(self, http_request):
    """Configure http_request as a multipart request for this upload."""
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

    # encode the body: note that we can't use `as_string`, because
    # it plays games with `From ` lines.
    fp = io.StringIO()
    g = email_generator.Generator(fp, mangle_from_=False)
    g.flatten(msg_root, unixfrom=False)
    http_request.body = fp.getvalue()

    multipart_boundary = msg_root.get_boundary()
    http_request.headers['content-type'] = (
        'multipart/related; boundary=%r' % multipart_boundary)

  def __ConfigureResumableRequest(self, http_request):
    http_request.headers['X-Upload-Content-Type'] = self.mime_type
    if self.total_size is not None:
      http_request.headers['X-Upload-Content-Length'] = str(self.total_size)

  def _RefreshResumableUploadState(self):
    """Talk to the server and refresh the state of this resumable upload."""
    if self.strategy != _RESUMABLE_UPLOAD:
      return
    self.EnsureInitialized()
    refresh_request = http_wrapper.Request(
        url=self.url, http_method='PUT', headers={'Content-Range': 'bytes */*'})
    refresh_response = http_wrapper.MakeRequest(
        self.http, refresh_request, redirections=0)
    range_header = refresh_response.info.get(
        'Range', refresh_response.info.get('range'))
    if refresh_response.status_code in (http_client.OK, http_client.CREATED):
      self.__complete = True
    elif refresh_response.status_code == http_wrapper.RESUME_INCOMPLETE:
      if range_header is None:
        self.__progress = 0
      else:
        self.__progress = self.__GetLastByte(range_header) + 1
      self.stream.seek(self.progress)
    else:
      raise exceptions.HttpError.FromResponse(refresh_response)

  def InitializeUpload(self, http_request, http=None, client=None):
    """Initialize this upload from the given http_request."""
    if self.strategy is None:
      raise exceptions.UserError(
          'No upload strategy set; did you call ConfigureRequest?')
    if http is None and client is None:
      raise exceptions.UserError('Must provide client or http.')
    if self.strategy != _RESUMABLE_UPLOAD:
      return
    if self.total_size is None:
      raise exceptions.InvalidUserInputError(
          'Cannot stream upload without total size')
    http = http or client.http
    if client is not None:
      http_request.url = client.FinalizeTransferUrl(http_request.url)
    self.EnsureUninitialized()
    http_response = http_wrapper.MakeRequest(http, http_request)
    if http_response.status_code != http_client.OK:
      raise exceptions.HttpError.FromResponse(http_response)

    self.__server_chunk_granularity = http_response.info.get(
        'X-Goog-Upload-Chunk-Granularity')
    self.__ValidateChunksize()
    url = http_response.info['location']
    if client is not None:
      url = client.FinalizeTransferUrl(url)
    self._Initialize(http, url)

    # Unless the user has requested otherwise, we want to just
    # go ahead and pump the bytes now.
    if self.auto_transfer:
      return self.StreamInChunks()

  def __GetLastByte(self, range_header):
    _, _, end = range_header.partition('-')
    # TODO(craigcitro): Validate start == 0?
    return int(end)

  def __ValidateChunksize(self, chunksize=None):
    if self.__server_chunk_granularity is None:
      return
    chunksize = chunksize or self.chunksize
    if chunksize % self.__server_chunk_granularity:
      raise exceptions.ConfigurationValueError(
          'Server requires chunksize to be a multiple of %d',
          self.__server_chunk_granularity)

  @staticmethod
  def _ArgPrinter(response, unused_upload):
    print('Sent %s' % response.info['range'])

  @staticmethod
  def _CompletePrinter(*unused_args):
    print('Upload complete')

  def StreamInChunks(self, callback=None, finish_callback=None,
                     additional_headers=None):
    """Send this (resumable) upload in chunks."""
    if self.strategy != _RESUMABLE_UPLOAD:
      raise exceptions.InvalidUserInputError(
          'Cannot stream non-resumable upload')
    if self.total_size is None:
      raise exceptions.InvalidUserInputError(
          'Cannot stream upload without total size')
    callback = callback or self._ArgPrinter
    finish_callback = finish_callback or self._CompletePrinter
    response = None
    self.__ValidateChunksize(self.chunksize)
    self.EnsureInitialized()
    while not self.complete:
      response = self.__SendChunk(self.stream.tell(),
                                  additional_headers=additional_headers)
      if response.status_code in (http_client.OK, http_client.CREATED):
        self.__complete = True
        break
      self.__progress = self.__GetLastByte(response.info['range'])
      if self.progress + 1 != self.stream.tell():
        # TODO(craigcitro): Add a better way to recover here.
        raise exceptions.CommunicationError(
            'Failed to transfer all bytes in chunk, upload paused at byte '
            '%d' % self.progress)
      self._ExecuteCallback(callback, response)
    self._ExecuteCallback(finish_callback, response)
    return response

  def __SendChunk(self, start, additional_headers=None, data=None):
    """Send the specified chunk."""
    self.EnsureInitialized()
    if data is None:
      data = self.stream.read(self.chunksize)
    end = start + len(data)

    request = http_wrapper.Request(url=self.url, http_method='PUT', body=data)
    request.headers['Content-Type'] = self.mime_type
    if data:
      request.headers['Content-Range'] = 'bytes %s-%s/%s' % (
          start, end - 1, self.total_size)
    if additional_headers:
      request.headers.update(additional_headers)

    response = http_wrapper.MakeRequest(self.bytes_http, request)
    if response.status_code not in (http_client.OK, http_client.CREATED,
                                    http_wrapper.RESUME_INCOMPLETE):
      raise exceptions.HttpError.FromResponse(response)
    if response.status_code in (http_client.OK, http_client.CREATED):
      return response
    # TODO(craigcitro): Add retries on no progress?
    last_byte = self.__GetLastByte(response.info['range'])
    if last_byte + 1 != end:
      new_start = last_byte + 1 - start
      response = self.__SendChunk(last_byte + 1, data=data[new_start:])
    return response
