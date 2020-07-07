# Copyright 2017 Google Inc.
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

"""Support for downloading media from Google APIs."""

import base64
import hashlib
import logging

import urllib3.response

from google.resumable_media import _download
from google.resumable_media import common
from google.resumable_media.requests import _helpers


_LOGGER = logging.getLogger(__name__)
_HASH_HEADER = u"x-goog-hash"
_MISSING_CHECKSUM = u"""\
No {checksum_type} checksum was returned from the service while downloading {}
(which happens for composite objects), so client-side content integrity
checking is not being performed."""
_CHECKSUM_MISMATCH = u"""\
Checksum mismatch while downloading:

  {}

The X-Goog-Hash header indicated an {checksum_type} checksum of:

  {}

but the actual {checksum_type} checksum of the downloaded contents was:

  {}
"""


class Download(_helpers.RequestsMixin, _download.Download):
    """Helper to manage downloading a resource from a Google API.

    "Slices" of the resource can be retrieved by specifying a range
    with ``start`` and / or ``end``. However, in typical usage, neither
    ``start`` nor ``end`` is expected to be provided.

    Args:
        media_url (str): The URL containing the media to be downloaded.
        stream (IO[bytes]): A write-able stream (i.e. file-like object) that
            the downloaded resource can be written to.
        start (int): The first byte in a range to be downloaded. If not
            provided, but ``end`` is provided, will download from the
            beginning to ``end`` of the media.
        end (int): The last byte in a range to be downloaded. If not
            provided, but ``start`` is provided, will download from the
            ``start`` to the end of the media.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.
        checksum Optional([str]): The type of checksum to compute to verify
            the integrity of the object. The response headers must contain
            a checksum of the requested type. If the headers lack an
            appropriate checksum (for instance in the case of transcoded or
            ranged downloads where the remote service does not know the
            correct checksum) an INFO-level log will be emitted. Supported
            values are "md5", "crc32c" and None. The default is "md5".

    Attributes:
        media_url (str): The URL containing the media to be downloaded.
        start (Optional[int]): The first byte in a range to be downloaded.
        end (Optional[int]): The last byte in a range to be downloaded.
    """

    def _write_to_stream(self, response):
        """Write response body to a write-able stream.

        .. note:

            This method assumes that the ``_stream`` attribute is set on the
            current download.

        Args:
            response (~requests.Response): The HTTP response object.

        Raises:
            ~google.resumable_media.common.DataCorruption: If the download's
                checksum doesn't agree with server-computed checksum.
        """

        # `_get_expected_checksum()` may return None even if a checksum was
        # requested, in which case it will emit an info log _MISSING_CHECKSUM.
        # If an invalid checksum type is specified, this will raise ValueError.
        expected_checksum, checksum_object = _get_expected_checksum(
            response, self._get_headers, self.media_url, checksum_type=self.checksum
        )

        with response:
            # NOTE: In order to handle compressed streams gracefully, we try
            # to insert our checksum object into the decompression stream. If
            # the stream is indeed compressed, this will delegate the checksum
            # object to the decoder and return a _DoNothingHash here.
            local_checksum_object = _add_decoder(response.raw, checksum_object)
            body_iter = response.iter_content(
                chunk_size=_helpers._SINGLE_GET_CHUNK_SIZE, decode_unicode=False
            )
            for chunk in body_iter:
                self._stream.write(chunk)
                local_checksum_object.update(chunk)

        if expected_checksum is None:
            return
        else:
            actual_checksum = base64.b64encode(checksum_object.digest())
            # NOTE: ``b64encode`` returns ``bytes``, but ``expected_checksum``
            #       came from a header, so it will be ``str``.
            actual_checksum = actual_checksum.decode(u"utf-8")
            if actual_checksum != expected_checksum:
                msg = _CHECKSUM_MISMATCH.format(
                    self.media_url,
                    expected_checksum,
                    actual_checksum,
                    checksum_type=self.checksum.upper(),
                )
                raise common.DataCorruption(response, msg)

    def consume(
        self,
        transport,
        timeout=(_helpers._DEFAULT_CONNECT_TIMEOUT, _helpers._DEFAULT_READ_TIMEOUT),
    ):
        """Consume the resource to be downloaded.

        If a ``stream`` is attached to this download, then the downloaded
        resource will be written to the stream.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.
            timeout (Optional[Union[float, Tuple[float, float]]]):
                The number of seconds to wait for the server response.
                Depending on the retry strategy, a request may be repeated
                several times using the same timeout each time.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.

        Raises:
            ~google.resumable_media.common.DataCorruption: If the download's
                checksum doesn't agree with server-computed checksum.
            ValueError: If the current :class:`Download` has already
                finished.
        """
        method, url, payload, headers = self._prepare_request()
        # NOTE: We assume "payload is None" but pass it along anyway.
        request_kwargs = {
            u"data": payload,
            u"headers": headers,
            u"retry_strategy": self._retry_strategy,
            u"timeout": timeout,
        }
        if self._stream is not None:
            request_kwargs[u"stream"] = True

        result = _helpers.http_request(transport, method, url, **request_kwargs)

        self._process_response(result)

        if self._stream is not None:
            self._write_to_stream(result)

        return result


class RawDownload(_helpers.RawRequestsMixin, _download.Download):
    """Helper to manage downloading a raw resource from a Google API.

    "Slices" of the resource can be retrieved by specifying a range
    with ``start`` and / or ``end``. However, in typical usage, neither
    ``start`` nor ``end`` is expected to be provided.

    Args:
        media_url (str): The URL containing the media to be downloaded.
        stream (IO[bytes]): A write-able stream (i.e. file-like object) that
            the downloaded resource can be written to.
        start (int): The first byte in a range to be downloaded. If not
            provided, but ``end`` is provided, will download from the
            beginning to ``end`` of the media.
        end (int): The last byte in a range to be downloaded. If not
            provided, but ``start`` is provided, will download from the
            ``start`` to the end of the media.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.
        checksum Optional([str]): The type of checksum to compute to verify
            the integrity of the object. The response headers must contain
            a checksum of the requested type. If the headers lack an
            appropriate checksum (for instance in the case of transcoded or
            ranged downloads where the remote service does not know the
            correct checksum) an INFO-level log will be emitted. Supported
            values are "md5", "crc32c" and None. The default is "md5".
    Attributes:
        media_url (str): The URL containing the media to be downloaded.
        start (Optional[int]): The first byte in a range to be downloaded.
        end (Optional[int]): The last byte in a range to be downloaded.
    """

    def _write_to_stream(self, response):
        """Write response body to a write-able stream.

        .. note:

            This method assumes that the ``_stream`` attribute is set on the
            current download.

        Args:
            response (~requests.Response): The HTTP response object.

        Raises:
            ~google.resumable_media.common.DataCorruption: If the download's
                checksum doesn't agree with server-computed checksum.
        """

        # `_get_expected_checksum()` may return None even if a checksum was
        # requested, in which case it will emit an info log _MISSING_CHECKSUM.
        # If an invalid checksum type is specified, this will raise ValueError.
        expected_checksum, checksum_object = _get_expected_checksum(
            response, self._get_headers, self.media_url, checksum_type=self.checksum
        )

        with response:
            body_iter = response.raw.stream(
                _helpers._SINGLE_GET_CHUNK_SIZE, decode_content=False
            )
            for chunk in body_iter:
                self._stream.write(chunk)
                checksum_object.update(chunk)
            response._content_consumed = True

        if expected_checksum is None:
            return
        else:
            actual_checksum = base64.b64encode(checksum_object.digest())

            # NOTE: ``b64encode`` returns ``bytes``, but ``expected_checksum``
            #       came from a header, so it will be ``str``.
            actual_checksum = actual_checksum.decode(u"utf-8")
            if actual_checksum != expected_checksum:
                msg = _CHECKSUM_MISMATCH.format(
                    self.media_url,
                    expected_checksum,
                    actual_checksum,
                    checksum_type=self.checksum.upper(),
                )
                raise common.DataCorruption(response, msg)

    def consume(
        self,
        transport,
        timeout=(_helpers._DEFAULT_CONNECT_TIMEOUT, _helpers._DEFAULT_READ_TIMEOUT),
    ):
        """Consume the resource to be downloaded.

        If a ``stream`` is attached to this download, then the downloaded
        resource will be written to the stream.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.
            timeout (Optional[Union[float, Tuple[float, float]]]):
                The number of seconds to wait for the server response.
                Depending on the retry strategy, a request may be repeated
                several times using the same timeout each time.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.

        Raises:
            ~google.resumable_media.common.DataCorruption: If the download's
                checksum doesn't agree with server-computed checksum.
            ValueError: If the current :class:`Download` has already
                finished.
        """
        method, url, payload, headers = self._prepare_request()
        # NOTE: We assume "payload is None" but pass it along anyway.
        result = _helpers.http_request(
            transport,
            method,
            url,
            data=payload,
            headers=headers,
            retry_strategy=self._retry_strategy,
            stream=True,
            timeout=timeout,
        )

        self._process_response(result)

        if self._stream is not None:
            self._write_to_stream(result)

        return result


class ChunkedDownload(_helpers.RequestsMixin, _download.ChunkedDownload):
    """Download a resource in chunks from a Google API.

    Args:
        media_url (str): The URL containing the media to be downloaded.
        chunk_size (int): The number of bytes to be retrieved in each
            request.
        stream (IO[bytes]): A write-able stream (i.e. file-like object) that
            will be used to concatenate chunks of the resource as they are
            downloaded.
        start (int): The first byte in a range to be downloaded. If not
            provided, defaults to ``0``.
        end (int): The last byte in a range to be downloaded. If not
            provided, will download to the end of the media.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with each request, e.g. headers for data encryption
            key headers.

    Attributes:
        media_url (str): The URL containing the media to be downloaded.
        start (Optional[int]): The first byte in a range to be downloaded.
        end (Optional[int]): The last byte in a range to be downloaded.
        chunk_size (int): The number of bytes to be retrieved in each request.

    Raises:
        ValueError: If ``start`` is negative.
    """

    def consume_next_chunk(
        self,
        transport,
        timeout=(_helpers._DEFAULT_CONNECT_TIMEOUT, _helpers._DEFAULT_READ_TIMEOUT),
    ):
        """Consume the next chunk of the resource to be downloaded.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.
            timeout (Optional[Union[float, Tuple[float, float]]]):
                The number of seconds to wait for the server response.
                Depending on the retry strategy, a request may be repeated
                several times using the same timeout each time.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.

        Raises:
            ValueError: If the current download has finished.
        """
        method, url, payload, headers = self._prepare_request()
        # NOTE: We assume "payload is None" but pass it along anyway.
        result = _helpers.http_request(
            transport,
            method,
            url,
            data=payload,
            headers=headers,
            retry_strategy=self._retry_strategy,
            timeout=timeout,
        )
        self._process_response(result)
        return result


class RawChunkedDownload(_helpers.RawRequestsMixin, _download.ChunkedDownload):
    """Download a raw resource in chunks from a Google API.

    Args:
        media_url (str): The URL containing the media to be downloaded.
        chunk_size (int): The number of bytes to be retrieved in each
            request.
        stream (IO[bytes]): A write-able stream (i.e. file-like object) that
            will be used to concatenate chunks of the resource as they are
            downloaded.
        start (int): The first byte in a range to be downloaded. If not
            provided, defaults to ``0``.
        end (int): The last byte in a range to be downloaded. If not
            provided, will download to the end of the media.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with each request, e.g. headers for data encryption
            key headers.

    Attributes:
        media_url (str): The URL containing the media to be downloaded.
        start (Optional[int]): The first byte in a range to be downloaded.
        end (Optional[int]): The last byte in a range to be downloaded.
        chunk_size (int): The number of bytes to be retrieved in each request.

    Raises:
        ValueError: If ``start`` is negative.
    """

    def consume_next_chunk(
        self,
        transport,
        timeout=(_helpers._DEFAULT_CONNECT_TIMEOUT, _helpers._DEFAULT_READ_TIMEOUT),
    ):
        """Consume the next chunk of the resource to be downloaded.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.
            timeout (Optional[Union[float, Tuple[float, float]]]):
                The number of seconds to wait for the server response.
                Depending on the retry strategy, a request may be repeated
                several times using the same timeout each time.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.

        Raises:
            ValueError: If the current download has finished.
        """
        method, url, payload, headers = self._prepare_request()
        # NOTE: We assume "payload is None" but pass it along anyway.
        result = _helpers.http_request(
            transport,
            method,
            url,
            data=payload,
            headers=headers,
            stream=True,
            retry_strategy=self._retry_strategy,
            timeout=timeout,
        )
        self._process_response(result)
        return result


def _get_expected_checksum(response, get_headers, media_url, checksum_type):
    """Get the expected checksum and checksum object for the response.

    Args:
        response (~requests.Response): The HTTP response object.
        get_headers (callable: response->dict): returns response headers.
        media_url (str): The URL containing the media to be downloaded.
        checksum_type Optional(str): The checksum type to read from the headers,
            exactly as it will appear in the headers (case-sensitive). Must be
            "md5", "crc32c" or None.

    Returns:
        Tuple (Optional[str], object): The expected checksum of the response,
        if it can be detected from the ``X-Goog-Hash`` header, and the
        appropriate checksum object for the expected checksum.
    """
    if checksum_type not in ["md5", "crc32c", None]:
        raise ValueError("checksum must be ``'md5'``, ``'crc32c'`` or ``None``")
    elif checksum_type in ["md5", "crc32c"]:
        headers = get_headers(response)
        expected_checksum = _parse_checksum_header(
            headers.get(_HASH_HEADER), response, checksum_label=checksum_type
        )

        if expected_checksum is None:
            msg = _MISSING_CHECKSUM.format(
                media_url, checksum_type=checksum_type.upper()
            )
            _LOGGER.info(msg)
            checksum_object = _DoNothingHash()
        else:
            if checksum_type == "md5":
                checksum_object = hashlib.md5()
            else:
                checksum_object = _helpers._get_crc32c_object()
    else:
        expected_checksum = None
        checksum_object = _DoNothingHash()

    return (expected_checksum, checksum_object)


def _parse_checksum_header(header_value, response, checksum_label):
    """Parses the MD5 header from an ``X-Goog-Hash`` value.

    .. _header reference: https://cloud.google.com/storage/docs/\
                          xml-api/reference-headers#xgooghash

    Expects ``header_value`` (if not :data:`None`) to be in one of the three
    following formats:

    * ``crc32c=n03x6A==``
    * ``md5=Ojk9c3dhfxgoKVVHYwFbHQ==``
    * ``crc32c=n03x6A==,md5=Ojk9c3dhfxgoKVVHYwFbHQ==``

    See the `header reference`_ for more information.

    Args:
        header_value (Optional[str]): The ``X-Goog-Hash`` header from
            a download response.
        response (~requests.Response): The HTTP response object.
        checksum_label (str): The label of the header value to read, as in the
            examples above. Typically "md5" or "crc32c"

    Returns:
        Optional[str]: The expected checksum of the response, if it
        can be detected from the ``X-Goog-Hash`` header; otherwise, None.

    Raises:
        ~google.resumable_media.common.InvalidResponse: If there are
            multiple checksums of the requested type in ``header_value``.
    """
    if header_value is None:
        return None

    matches = []
    for checksum in header_value.split(u","):
        name, value = checksum.split(u"=", 1)
        if name == checksum_label:
            matches.append(value)

    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        raise common.InvalidResponse(
            response,
            u"X-Goog-Hash header had multiple ``{}`` values.".format(checksum_label),
            header_value,
            matches,
        )


class _DoNothingHash(object):
    """Do-nothing hash object.

    Intended as a stand-in for ``hashlib.md5`` or a crc32c checksum
    implementation in cases where it isn't necessary to compute the hash.
    """

    def update(self, unused_chunk):
        """Do-nothing ``update`` method.

        Intended to match the interface of ``hashlib.md5`` and other checksums.

        Args:
            unused_chunk (bytes): A chunk of data.
        """


def _add_decoder(response_raw, checksum):
    """Patch the ``_decoder`` on a ``urllib3`` response.

    This is so that we can intercept the compressed bytes before they are
    decoded.

    Only patches if the content encoding is ``gzip``.

    Args:
        response_raw (urllib3.response.HTTPResponse): The raw response for
            an HTTP request.
        checksum (object):
            A checksum which will be updated with compressed bytes.

    Returns:
        object: Either the original ``checksum`` if ``_decoder`` is not
        patched, or a ``_DoNothingHash`` if the decoder is patched, since the
        caller will no longer need to hash to decoded bytes.
    """
    encoding = response_raw.headers.get(u"content-encoding", u"").lower()
    if encoding != u"gzip":
        return checksum

    response_raw._decoder = _GzipDecoder(checksum)
    return _DoNothingHash()


class _GzipDecoder(urllib3.response.GzipDecoder):
    """Custom subclass of ``urllib3`` decoder for ``gzip``-ed bytes.

    Allows a checksum function to see the compressed bytes before they are
    decoded. This way the checksum of the compressed value can be computed.

    Args:
        checksum (object):
            A checksum which will be updated with compressed bytes.
    """

    def __init__(self, checksum):
        super(_GzipDecoder, self).__init__()
        self._checksum = checksum

    def decompress(self, data):
        """Decompress the bytes.

        Args:
            data (bytes): The compressed bytes to be decompressed.

        Returns:
            bytes: The decompressed bytes from ``data``.
        """
        self._checksum.update(data)
        return super(_GzipDecoder, self).decompress(data)
