# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
    Union,
)

from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core import retry_async as retries_async

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
    OptionalAsyncRetry = Union[
        retries_async.AsyncRetry, gapic_v1.method._MethodDefault, None
    ]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore
    OptionalAsyncRetry = Union[retries_async.AsyncRetry, object, None]  # type: ignore

from google.cloud.oracledatabase_v1.types import (
    autonomous_database,
    autonomous_database_character_set,
    autonomous_db_backup,
    autonomous_db_version,
    db_node,
    db_server,
    db_system_shape,
    entitlement,
    exadata_infra,
    gi_version,
    oracledatabase,
    vm_cluster,
)


class ListCloudExadataInfrastructuresPager:
    """A pager for iterating through ``list_cloud_exadata_infrastructures`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListCloudExadataInfrastructuresResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``cloud_exadata_infrastructures`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCloudExadataInfrastructures`` requests and continue to iterate
    through the ``cloud_exadata_infrastructures`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListCloudExadataInfrastructuresResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListCloudExadataInfrastructuresResponse],
        request: oracledatabase.ListCloudExadataInfrastructuresRequest,
        response: oracledatabase.ListCloudExadataInfrastructuresResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListCloudExadataInfrastructuresRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListCloudExadataInfrastructuresResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListCloudExadataInfrastructuresRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListCloudExadataInfrastructuresResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[exadata_infra.CloudExadataInfrastructure]:
        for page in self.pages:
            yield from page.cloud_exadata_infrastructures

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListCloudVmClustersPager:
    """A pager for iterating through ``list_cloud_vm_clusters`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListCloudVmClustersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``cloud_vm_clusters`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCloudVmClusters`` requests and continue to iterate
    through the ``cloud_vm_clusters`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListCloudVmClustersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListCloudVmClustersResponse],
        request: oracledatabase.ListCloudVmClustersRequest,
        response: oracledatabase.ListCloudVmClustersResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListCloudVmClustersRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListCloudVmClustersResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListCloudVmClustersRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListCloudVmClustersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[vm_cluster.CloudVmCluster]:
        for page in self.pages:
            yield from page.cloud_vm_clusters

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEntitlementsPager:
    """A pager for iterating through ``list_entitlements`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListEntitlementsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``entitlements`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEntitlements`` requests and continue to iterate
    through the ``entitlements`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListEntitlementsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListEntitlementsResponse],
        request: oracledatabase.ListEntitlementsRequest,
        response: oracledatabase.ListEntitlementsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListEntitlementsRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListEntitlementsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListEntitlementsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListEntitlementsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[entitlement.Entitlement]:
        for page in self.pages:
            yield from page.entitlements

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDbServersPager:
    """A pager for iterating through ``list_db_servers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListDbServersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``db_servers`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDbServers`` requests and continue to iterate
    through the ``db_servers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListDbServersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListDbServersResponse],
        request: oracledatabase.ListDbServersRequest,
        response: oracledatabase.ListDbServersResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListDbServersRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListDbServersResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListDbServersRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListDbServersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[db_server.DbServer]:
        for page in self.pages:
            yield from page.db_servers

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDbNodesPager:
    """A pager for iterating through ``list_db_nodes`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListDbNodesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``db_nodes`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDbNodes`` requests and continue to iterate
    through the ``db_nodes`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListDbNodesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListDbNodesResponse],
        request: oracledatabase.ListDbNodesRequest,
        response: oracledatabase.ListDbNodesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListDbNodesRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListDbNodesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListDbNodesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListDbNodesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[db_node.DbNode]:
        for page in self.pages:
            yield from page.db_nodes

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListGiVersionsPager:
    """A pager for iterating through ``list_gi_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListGiVersionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``gi_versions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListGiVersions`` requests and continue to iterate
    through the ``gi_versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListGiVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListGiVersionsResponse],
        request: oracledatabase.ListGiVersionsRequest,
        response: oracledatabase.ListGiVersionsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListGiVersionsRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListGiVersionsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListGiVersionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListGiVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[gi_version.GiVersion]:
        for page in self.pages:
            yield from page.gi_versions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDbSystemShapesPager:
    """A pager for iterating through ``list_db_system_shapes`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListDbSystemShapesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``db_system_shapes`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDbSystemShapes`` requests and continue to iterate
    through the ``db_system_shapes`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListDbSystemShapesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListDbSystemShapesResponse],
        request: oracledatabase.ListDbSystemShapesRequest,
        response: oracledatabase.ListDbSystemShapesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListDbSystemShapesRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListDbSystemShapesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListDbSystemShapesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListDbSystemShapesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[db_system_shape.DbSystemShape]:
        for page in self.pages:
            yield from page.db_system_shapes

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAutonomousDatabasesPager:
    """A pager for iterating through ``list_autonomous_databases`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListAutonomousDatabasesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``autonomous_databases`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAutonomousDatabases`` requests and continue to iterate
    through the ``autonomous_databases`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListAutonomousDatabasesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListAutonomousDatabasesResponse],
        request: oracledatabase.ListAutonomousDatabasesRequest,
        response: oracledatabase.ListAutonomousDatabasesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListAutonomousDatabasesRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListAutonomousDatabasesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListAutonomousDatabasesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListAutonomousDatabasesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[autonomous_database.AutonomousDatabase]:
        for page in self.pages:
            yield from page.autonomous_databases

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAutonomousDbVersionsPager:
    """A pager for iterating through ``list_autonomous_db_versions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListAutonomousDbVersionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``autonomous_db_versions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAutonomousDbVersions`` requests and continue to iterate
    through the ``autonomous_db_versions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListAutonomousDbVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListAutonomousDbVersionsResponse],
        request: oracledatabase.ListAutonomousDbVersionsRequest,
        response: oracledatabase.ListAutonomousDbVersionsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListAutonomousDbVersionsRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListAutonomousDbVersionsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListAutonomousDbVersionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListAutonomousDbVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[autonomous_db_version.AutonomousDbVersion]:
        for page in self.pages:
            yield from page.autonomous_db_versions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAutonomousDatabaseCharacterSetsPager:
    """A pager for iterating through ``list_autonomous_database_character_sets`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseCharacterSetsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``autonomous_database_character_sets`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAutonomousDatabaseCharacterSets`` requests and continue to iterate
    through the ``autonomous_database_character_sets`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseCharacterSetsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., oracledatabase.ListAutonomousDatabaseCharacterSetsResponse
        ],
        request: oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
        response: oracledatabase.ListAutonomousDatabaseCharacterSetsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseCharacterSetsRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseCharacterSetsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest(
            request
        )
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(
        self,
    ) -> Iterator[oracledatabase.ListAutonomousDatabaseCharacterSetsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(
        self,
    ) -> Iterator[autonomous_database_character_set.AutonomousDatabaseCharacterSet]:
        for page in self.pages:
            yield from page.autonomous_database_character_sets

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAutonomousDatabaseBackupsPager:
    """A pager for iterating through ``list_autonomous_database_backups`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseBackupsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``autonomous_database_backups`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAutonomousDatabaseBackups`` requests and continue to iterate
    through the ``autonomous_database_backups`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseBackupsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., oracledatabase.ListAutonomousDatabaseBackupsResponse],
        request: oracledatabase.ListAutonomousDatabaseBackupsRequest,
        response: oracledatabase.ListAutonomousDatabaseBackupsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseBackupsRequest):
                The initial request object.
            response (google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseBackupsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = oracledatabase.ListAutonomousDatabaseBackupsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[oracledatabase.ListAutonomousDatabaseBackupsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[autonomous_db_backup.AutonomousDatabaseBackup]:
        for page in self.pages:
            yield from page.autonomous_database_backups

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
