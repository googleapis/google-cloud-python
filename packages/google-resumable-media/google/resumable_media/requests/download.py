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
_SINGLE_GET_CHUNK_SIZE = 8192
_HASH_HEADER = u"x-goog-hash"
_MISSING_MD5 = u"""\
No MD5 checksum was returned from the service while downloading {}
(which happens for composite objects), so client-side content integrity
checking is not being performed."""
_CHECKSUM_MISMATCH = u"""\
Checksum mismatch while downloading:

  {}

The X-Goog-Hash header indicated an MD5 checksum of:

  {}

but the actual MD5 checksum of the downloaded contents was:

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

    Attributes:
        media_url (str): The URL containing the media to be downloaded.
        start (Optional[int]): The first byte in a range to be downloaded.
        end (Optional[int]): The last byte in a range to be downloaded.
    """

    def _get_expected_md5(self, response):
        """Get the expected MD5 hash from the response headers.

        Args:
            response (~requests.Response): The HTTP response object.

        Returns:
            Optional[str]: The expected MD5 hash of the response, if it
            can be detected from the ``X-Goog-Hash`` header.
        """
        headers = self._get_headers(response)
        expected_md5_hash = _parse_md5_header(headers.get(_HASH_HEADER), response)

        if expected_md5_hash is None:
            msg = _MISSING_MD5.format(self.media_url)
            _LOGGER.info(msg)

        return expected_md5_hash

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
        expected_md5_hash = self._get_expected_md5(response)

        if expected_md5_hash is None:
            md5_hash = _DoNothingHash()
        else:
            md5_hash = hashlib.md5()
        with response:
            # NOTE: This might "donate" ``md5_hash`` to the decoder and replace
            #       it with a ``_DoNothingHash``.
            local_hash = _add_decoder(response.raw, md5_hash)
            body_iter = response.iter_content(
                chunk_size=_SINGLE_GET_CHUNK_SIZE, decode_unicode=False
            )
            for chunk in body_iter:
                self._stream.write(chunk)
                local_hash.update(chunk)

        if expected_md5_hash is None:
            return

        actual_md5_hash = base64.b64encode(md5_hash.digest())
        # NOTE: ``b64encode`` returns ``bytes``, but ``expected_md5_hash``
        #       came from a header, so it will be ``str``.
        actual_md5_hash = actual_md5_hash.decode(u"utf-8")
        if actual_md5_hash != expected_md5_hash:
            msg = _CHECKSUM_MISMATCH.format(
                self.media_url, expected_md5_hash, actual_md5_hash
            )
            raise common.DataCorruption(response, msg)

    def consume(self, transport):
        """Consume the resource to be downloaded.

        If a ``stream`` is attached to this download, then the downloaded
        resource will be written to the stream.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.

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
        }
        if self._stream is not None:
            request_kwargs[u"stream"] = True

        result = _helpers.http_request(transport, method, url, **request_kwargs)

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

    def consume_next_chunk(self, transport):
        """Consume the next chunk of the resource to be downloaded.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.

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
        )
        self._process_response(result)
        return result


def _parse_md5_header(header_value, response):
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

    Returns:
        Optional[str]: The expected MD5 hash of the response, if it
        can be detected from the ``X-Goog-Hash`` header.

    Raises:
        ~google.resumable_media.common.InvalidResponse: If there are
            multiple ``md5`` checksums in ``header_value``.
    """
    if header_value is None:
        return None

    matches = []
    for checksum in header_value.split(u","):
        name, value = checksum.split(u"=", 1)
        if name == u"md5":
            matches.append(value)

    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        raise common.InvalidResponse(
            response,
            u"X-Goog-Hash header had multiple ``md5`` values.",
            header_value,
            matches,
        )


class _DoNothingHash(object):
    """Do-nothing hash object.

    Intended as a stand-in for ``hashlib.md5`` in cases where it
    isn't necessary to compute the hash.
    """

    def update(self, unused_chunk):
        """Do-nothing ``update`` method.

        Intended to match the interface of ``hashlib.md5``.

        Args:
            unused_chunk (bytes): A chunk of data.
        """


def _add_decoder(response_raw, md5_hash):
    """Patch the ``_decoder`` on a ``urllib3`` response.

    This is so that we can intercept the compressed bytes before they are
    decoded.

    Only patches if the content encoding is ``gzip``.

    Args:
        response_raw (urllib3.response.HTTPResponse): The raw response for
            an HTTP request.
        md5_hash (Union[_DoNothingHash, hashlib.md5]): A hash function which
            will get updated when it encounters compressed bytes.

    Returns:
        Union[_DoNothingHash, hashlib.md5]: Either the original ``md5_hash``
        if ``_decoder`` is not patched. Otherwise, returns a ``_DoNothingHash``
        since the caller will no longer need to hash to decoded bytes.
    """
    encoding = response_raw.headers.get(u"content-encoding", u"").lower()
    if encoding != u"gzip":
        return md5_hash

    response_raw._decoder = _GzipDecoder(md5_hash)
    return _DoNothingHash()


class _GzipDecoder(urllib3.response.GzipDecoder):
    """Custom subclass of ``urllib3`` decoder for ``gzip``-ed bytes.

    Allows an MD5 hash function to see the compressed bytes before they are
    decoded. This way the hash of the compressed value can be computed.

    Args:
        md5_hash (Union[_DoNothingHash, hashlib.md5]): A hash function which
            will get updated when it encounters compressed bytes.
    """

    def __init__(self, md5_hash):
        super(_GzipDecoder, self).__init__()
        self._md5_hash = md5_hash

    def decompress(self, data):
        """Decompress the bytes.

        Args:
            data (bytes): The compressed bytes to be decompressed.

        Returns:
            bytes: The decompressed bytes from ``data``.
        """
        self._md5_hash.update(data)
        return super(_GzipDecoder, self).decompress(data)
