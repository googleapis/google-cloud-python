# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

from typing import Any, Callable, Iterable

from google.cloud.osconfig_v1.types import patch_deployments
from google.cloud.osconfig_v1.types import patch_jobs


class ListPatchJobsPager:
    """A pager for iterating through ``list_patch_jobs`` requests.

    This class thinly wraps an initial
    :class:`~.patch_jobs.ListPatchJobsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``patch_jobs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPatchJobs`` requests and continue to iterate
    through the ``patch_jobs`` field on the
    corresponding responses.

    All the usual :class:`~.patch_jobs.ListPatchJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [patch_jobs.ListPatchJobsRequest], patch_jobs.ListPatchJobsResponse
        ],
        request: patch_jobs.ListPatchJobsRequest,
        response: patch_jobs.ListPatchJobsResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.patch_jobs.ListPatchJobsRequest`):
                The initial request object.
            response (:class:`~.patch_jobs.ListPatchJobsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = patch_jobs.ListPatchJobsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[patch_jobs.ListPatchJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[patch_jobs.PatchJob]:
        for page in self.pages:
            yield from page.patch_jobs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPatchJobInstanceDetailsPager:
    """A pager for iterating through ``list_patch_job_instance_details`` requests.

    This class thinly wraps an initial
    :class:`~.patch_jobs.ListPatchJobInstanceDetailsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``patch_job_instance_details`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPatchJobInstanceDetails`` requests and continue to iterate
    through the ``patch_job_instance_details`` field on the
    corresponding responses.

    All the usual :class:`~.patch_jobs.ListPatchJobInstanceDetailsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [patch_jobs.ListPatchJobInstanceDetailsRequest],
            patch_jobs.ListPatchJobInstanceDetailsResponse,
        ],
        request: patch_jobs.ListPatchJobInstanceDetailsRequest,
        response: patch_jobs.ListPatchJobInstanceDetailsResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.patch_jobs.ListPatchJobInstanceDetailsRequest`):
                The initial request object.
            response (:class:`~.patch_jobs.ListPatchJobInstanceDetailsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = patch_jobs.ListPatchJobInstanceDetailsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[patch_jobs.ListPatchJobInstanceDetailsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[patch_jobs.PatchJobInstanceDetails]:
        for page in self.pages:
            yield from page.patch_job_instance_details

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPatchDeploymentsPager:
    """A pager for iterating through ``list_patch_deployments`` requests.

    This class thinly wraps an initial
    :class:`~.patch_deployments.ListPatchDeploymentsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``patch_deployments`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPatchDeployments`` requests and continue to iterate
    through the ``patch_deployments`` field on the
    corresponding responses.

    All the usual :class:`~.patch_deployments.ListPatchDeploymentsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [patch_deployments.ListPatchDeploymentsRequest],
            patch_deployments.ListPatchDeploymentsResponse,
        ],
        request: patch_deployments.ListPatchDeploymentsRequest,
        response: patch_deployments.ListPatchDeploymentsResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.patch_deployments.ListPatchDeploymentsRequest`):
                The initial request object.
            response (:class:`~.patch_deployments.ListPatchDeploymentsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = patch_deployments.ListPatchDeploymentsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[patch_deployments.ListPatchDeploymentsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[patch_deployments.PatchDeployment]:
        for page in self.pages:
            yield from page.patch_deployments

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
