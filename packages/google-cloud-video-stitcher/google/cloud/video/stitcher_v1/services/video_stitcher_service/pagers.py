# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

from google.cloud.video.stitcher_v1.types import (
    ad_tag_details,
    cdn_keys,
    slates,
    stitch_details,
    video_stitcher_service,
)


class ListCdnKeysPager:
    """A pager for iterating through ``list_cdn_keys`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListCdnKeysResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``cdn_keys`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCdnKeys`` requests and continue to iterate
    through the ``cdn_keys`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListCdnKeysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., video_stitcher_service.ListCdnKeysResponse],
        request: video_stitcher_service.ListCdnKeysRequest,
        response: video_stitcher_service.ListCdnKeysResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListCdnKeysRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListCdnKeysResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListCdnKeysRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[video_stitcher_service.ListCdnKeysResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[cdn_keys.CdnKey]:
        for page in self.pages:
            yield from page.cdn_keys

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListCdnKeysAsyncPager:
    """A pager for iterating through ``list_cdn_keys`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListCdnKeysResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``cdn_keys`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListCdnKeys`` requests and continue to iterate
    through the ``cdn_keys`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListCdnKeysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[video_stitcher_service.ListCdnKeysResponse]],
        request: video_stitcher_service.ListCdnKeysRequest,
        response: video_stitcher_service.ListCdnKeysResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListCdnKeysRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListCdnKeysResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListCdnKeysRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[video_stitcher_service.ListCdnKeysResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[cdn_keys.CdnKey]:
        async def async_generator():
            async for page in self.pages:
                for response in page.cdn_keys:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVodStitchDetailsPager:
    """A pager for iterating through ``list_vod_stitch_details`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListVodStitchDetailsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``vod_stitch_details`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListVodStitchDetails`` requests and continue to iterate
    through the ``vod_stitch_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListVodStitchDetailsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., video_stitcher_service.ListVodStitchDetailsResponse],
        request: video_stitcher_service.ListVodStitchDetailsRequest,
        response: video_stitcher_service.ListVodStitchDetailsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListVodStitchDetailsRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListVodStitchDetailsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListVodStitchDetailsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[video_stitcher_service.ListVodStitchDetailsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[stitch_details.VodStitchDetail]:
        for page in self.pages:
            yield from page.vod_stitch_details

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVodStitchDetailsAsyncPager:
    """A pager for iterating through ``list_vod_stitch_details`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListVodStitchDetailsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``vod_stitch_details`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListVodStitchDetails`` requests and continue to iterate
    through the ``vod_stitch_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListVodStitchDetailsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[video_stitcher_service.ListVodStitchDetailsResponse]
        ],
        request: video_stitcher_service.ListVodStitchDetailsRequest,
        response: video_stitcher_service.ListVodStitchDetailsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListVodStitchDetailsRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListVodStitchDetailsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListVodStitchDetailsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[video_stitcher_service.ListVodStitchDetailsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[stitch_details.VodStitchDetail]:
        async def async_generator():
            async for page in self.pages:
                for response in page.vod_stitch_details:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVodAdTagDetailsPager:
    """A pager for iterating through ``list_vod_ad_tag_details`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``vod_ad_tag_details`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListVodAdTagDetails`` requests and continue to iterate
    through the ``vod_ad_tag_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., video_stitcher_service.ListVodAdTagDetailsResponse],
        request: video_stitcher_service.ListVodAdTagDetailsRequest,
        response: video_stitcher_service.ListVodAdTagDetailsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListVodAdTagDetailsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[video_stitcher_service.ListVodAdTagDetailsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[ad_tag_details.VodAdTagDetail]:
        for page in self.pages:
            yield from page.vod_ad_tag_details

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListVodAdTagDetailsAsyncPager:
    """A pager for iterating through ``list_vod_ad_tag_details`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``vod_ad_tag_details`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListVodAdTagDetails`` requests and continue to iterate
    through the ``vod_ad_tag_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[video_stitcher_service.ListVodAdTagDetailsResponse]
        ],
        request: video_stitcher_service.ListVodAdTagDetailsRequest,
        response: video_stitcher_service.ListVodAdTagDetailsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListVodAdTagDetailsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[video_stitcher_service.ListVodAdTagDetailsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[ad_tag_details.VodAdTagDetail]:
        async def async_generator():
            async for page in self.pages:
                for response in page.vod_ad_tag_details:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListLiveAdTagDetailsPager:
    """A pager for iterating through ``list_live_ad_tag_details`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``live_ad_tag_details`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListLiveAdTagDetails`` requests and continue to iterate
    through the ``live_ad_tag_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., video_stitcher_service.ListLiveAdTagDetailsResponse],
        request: video_stitcher_service.ListLiveAdTagDetailsRequest,
        response: video_stitcher_service.ListLiveAdTagDetailsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListLiveAdTagDetailsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[video_stitcher_service.ListLiveAdTagDetailsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[ad_tag_details.LiveAdTagDetail]:
        for page in self.pages:
            yield from page.live_ad_tag_details

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListLiveAdTagDetailsAsyncPager:
    """A pager for iterating through ``list_live_ad_tag_details`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``live_ad_tag_details`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListLiveAdTagDetails`` requests and continue to iterate
    through the ``live_ad_tag_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[video_stitcher_service.ListLiveAdTagDetailsResponse]
        ],
        request: video_stitcher_service.ListLiveAdTagDetailsRequest,
        response: video_stitcher_service.ListLiveAdTagDetailsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListLiveAdTagDetailsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[video_stitcher_service.ListLiveAdTagDetailsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[ad_tag_details.LiveAdTagDetail]:
        async def async_generator():
            async for page in self.pages:
                for response in page.live_ad_tag_details:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSlatesPager:
    """A pager for iterating through ``list_slates`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListSlatesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``slates`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSlates`` requests and continue to iterate
    through the ``slates`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListSlatesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., video_stitcher_service.ListSlatesResponse],
        request: video_stitcher_service.ListSlatesRequest,
        response: video_stitcher_service.ListSlatesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListSlatesRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListSlatesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListSlatesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[video_stitcher_service.ListSlatesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[slates.Slate]:
        for page in self.pages:
            yield from page.slates

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSlatesAsyncPager:
    """A pager for iterating through ``list_slates`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.video.stitcher_v1.types.ListSlatesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``slates`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSlates`` requests and continue to iterate
    through the ``slates`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.video.stitcher_v1.types.ListSlatesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[video_stitcher_service.ListSlatesResponse]],
        request: video_stitcher_service.ListSlatesRequest,
        response: video_stitcher_service.ListSlatesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.video.stitcher_v1.types.ListSlatesRequest):
                The initial request object.
            response (google.cloud.video.stitcher_v1.types.ListSlatesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = video_stitcher_service.ListSlatesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[video_stitcher_service.ListSlatesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[slates.Slate]:
        async def async_generator():
            async for page in self.pages:
                for response in page.slates:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
