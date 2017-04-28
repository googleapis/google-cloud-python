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

"""Support for resumable uploads.

Also supported here are simple (media) uploads and multipart
uploads that contain both metadata and a small file as payload.
"""


from google.resumable_media import _upload
from google.resumable_media.requests import _helpers


class SimpleUpload(_helpers.RequestsMixin, _upload.SimpleUpload):
    """Upload a resource to a Google API.

    A **simple** media upload sends no metadata and completes the upload
    in a single request.

    Args:
        upload_url (str): The URL where the content will be uploaded.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.

    Attributes:
        upload_url (str): The URL where the content will be uploaded.
    """

    def transmit(self, transport, data, content_type):
        """Transmit the resource to be uploaded.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.
            data (bytes): The resource content to be uploaded.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.
        """
        method, url, payload, headers = self._prepare_request(
            data, content_type)
        result = _helpers.http_request(
            transport, method, url, data=payload, headers=headers)
        self._process_response(result)
        return result


class MultipartUpload(_helpers.RequestsMixin, _upload.MultipartUpload):
    """Upload a resource with metadata to a Google API.

    A **multipart** upload sends both metadata and the resource in a single
    (multipart) request.

    Args:
        upload_url (str): The URL where the content will be uploaded.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.

    Attributes:
        upload_url (str): The URL where the content will be uploaded.
    """

    def transmit(self, transport, data, metadata, content_type):
        """Transmit the resource to be uploaded.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.
            data (bytes): The resource content to be uploaded.
            metadata (Mapping[str, str]): The resource metadata, such as an
                ACL list.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.
        """
        method, url, payload, headers = self._prepare_request(
            data, metadata, content_type)
        result = _helpers.http_request(
            transport, method, url, data=payload, headers=headers)
        self._process_response(result)
        return result


class ResumableUpload(_helpers.RequestsMixin, _upload.ResumableUpload):
    """Initiate and fulfill a resumable upload to a Google API.

    A **resumable** upload sends an initial request with the resource metadata
    and then gets assigned an upload ID / upload URL to send bytes to.
    Using the upload URL, the upload is then done in chunks (determined by
    the user) until all bytes have been uploaded.

    Args:
        upload_url (str): The URL where the resumable upload will be initiated.
        chunk_size (int): The size of each chunk used to upload the resource.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the :meth:`initiate` request, e.g. headers for
            encrypted data. These **will not** be sent with
            :meth:`transmit_next_chunk` or :meth:`recover` requests.

    Attributes:
        upload_url (str): The URL where the content will be uploaded.

    Raises:
        ValueError: If ``chunk_size`` is not a multiple of
            :data:`.UPLOAD_CHUNK_SIZE`.
    """

    def initiate(self, transport, stream, metadata, content_type):
        """Initiate a resumable upload.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.
            stream (IO[bytes]): The stream (i.e. file-like object) that will
                be uploaded. The stream **must** be at the beginning (i.e.
                ``stream.tell() == 0``).
            metadata (Mapping[str, str]): The resource metadata, such as an
                ACL list.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.
        """
        method, url, payload, headers = self._prepare_initiate_request(
            stream, metadata, content_type)
        result = _helpers.http_request(
            transport, method, url, data=payload, headers=headers)
        self._process_initiate_response(result)
        return result

    def transmit_next_chunk(self, transport):
        """Transmit the next chunk of the resource to be uploaded.

        In the case of failure, an exception is thrown that preserves the
        failed response:

        .. testsetup:: bad-response

           import io

           import mock
           import requests
           from six.moves import http_client

           from google import resumable_media
           import google.resumable_media.requests.upload as upload_mod

           transport = mock.Mock(spec=[u'request'])
           fake_response = requests.Response()
           fake_response.status_code = int(http_client.BAD_REQUEST)
           transport.request.return_value = fake_response

           upload_url = u'http://test.invalid'
           upload = upload_mod.ResumableUpload(
               upload_url, resumable_media.UPLOAD_CHUNK_SIZE)
           # Fake that the upload has been initiate()-d
           data = b'data is here'
           upload._stream = io.BytesIO(data)
           upload._total_bytes = len(data)
           upload._resumable_url = u'http://test.invalid?upload_id=nope'

        .. doctest:: bad-response
           :options: +NORMALIZE_WHITESPACE

           >>> error = None
           >>> try:
           ...     upload.transmit_next_chunk(transport)
           ... except resumable_media.InvalidResponse as caught_exc:
           ...     error = caught_exc
           ...
           >>> error
           InvalidResponse('Request failed with status code', 400,
                           'Expected one of', <HTTPStatus.OK: 200>, 308)
           >>> error.response
           <Response [400]>

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.

        Raises:
            ~google.resumable_media.exceptions.InvalidResponse: If the status
                code is not 200 or 308.
        """
        method, url, payload, headers = self._prepare_request()
        result = _helpers.http_request(
            transport, method, url, data=payload, headers=headers)
        self._process_response(result)
        return result

    def recover(self, transport):
        """Recover from a failure.

        This method should be used when a :class:`ResumableUpload` is in an
        :attr:`~ResumableUpload.invalid` state due to a request failure.

        This will verify the progress with the server and make sure the
        current upload is in a valid state before :meth:`transmit_next_chunk`
        can be used again.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.
        """
        method, url, payload, headers = self._prepare_recover_request()
        # NOTE: We assume "payload is None" but pass it along anyway.
        result = _helpers.http_request(
            transport, method, url, data=payload, headers=headers)
        self._process_recover_response(result)
        return result
