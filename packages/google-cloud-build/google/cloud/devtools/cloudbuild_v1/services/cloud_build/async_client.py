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

from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation
from google.api_core import operation_async
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import pagers
from google.cloud.devtools.cloudbuild_v1.types import cloudbuild
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import CloudBuildTransport
from .transports.grpc_asyncio import CloudBuildGrpcAsyncIOTransport
from .client import CloudBuildClient


class CloudBuildAsyncClient:
    """Creates and manages builds on Google Cloud Platform.

    The main concept used by this API is a ``Build``, which describes
    the location of the source to build, how to build the source, and
    where to store the built artifacts, if any.

    A user can list previously-requested builds or get builds by their
    ID to determine the status of the build.
    """

    _client: CloudBuildClient

    DEFAULT_ENDPOINT = CloudBuildClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CloudBuildClient.DEFAULT_MTLS_ENDPOINT

    from_service_account_file = CloudBuildClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(CloudBuildClient).get_transport_class, type(CloudBuildClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, CloudBuildTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the cloud build client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudBuildTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = CloudBuildClient(
            credentials=credentials, transport=transport, client_options=client_options,
        )

    async def create_build(
        self,
        request: cloudbuild.CreateBuildRequest = None,
        *,
        project_id: str = None,
        build: cloudbuild.Build = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Starts a build with the specified configuration.

        This method returns a long-running ``Operation``, which includes
        the build ID. Pass the build ID to ``GetBuild`` to determine the
        build status (such as ``SUCCESS`` or ``FAILURE``).

        Args:
            request (:class:`~.cloudbuild.CreateBuildRequest`):
                The request object. Request to create a new build.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            build (:class:`~.cloudbuild.Build`):
                Required. Build resource to create.
                This corresponds to the ``build`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.cloudbuild.Build``: A build resource in the
                Cloud Build API.

                At a high level, a ``Build`` describes where to find
                source code, how to build it (for example, the builder
                image to run on the source), and where to store the
                built artifacts.

                Fields can include the following variables, which will
                be expanded when the build is created:

                -  $PROJECT_ID: the project ID of the build.
                -  $BUILD_ID: the autogenerated ID of the build.
                -  $REPO_NAME: the source repository name specified by
                   RepoSource.
                -  $BRANCH_NAME: the branch name specified by
                   RepoSource.
                -  $TAG_NAME: the tag name specified by RepoSource.
                -  $REVISION_ID or $COMMIT_SHA: the commit SHA specified
                   by RepoSource or resolved from the specified branch
                   or tag.
                -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                   $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, build]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.CreateBuildRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if build is not None:
            request.build = build

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_build,
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_build(
        self,
        request: cloudbuild.GetBuildRequest = None,
        *,
        project_id: str = None,
        id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.Build:
        r"""Returns information about a previously requested build.

        The ``Build`` that is returned includes its status (such as
        ``SUCCESS``, ``FAILURE``, or ``WORKING``), and timing
        information.

        Args:
            request (:class:`~.cloudbuild.GetBuildRequest`):
                The request object. Request to get a build.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            id (:class:`str`):
                Required. ID of the build.
                This corresponds to the ``id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloudbuild.Build:
                A build resource in the Cloud Build API.

                At a high level, a ``Build`` describes where to find
                source code, how to build it (for example, the builder
                image to run on the source), and where to store the
                built artifacts.

                Fields can include the following variables, which will
                be expanded when the build is created:

                -  $PROJECT_ID: the project ID of the build.
                -  $BUILD_ID: the autogenerated ID of the build.
                -  $REPO_NAME: the source repository name specified by
                   RepoSource.
                -  $BRANCH_NAME: the branch name specified by
                   RepoSource.
                -  $TAG_NAME: the tag name specified by RepoSource.
                -  $REVISION_ID or $COMMIT_SHA: the commit SHA specified
                   by RepoSource or resolved from the specified branch
                   or tag.
                -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                   $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.GetBuildRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if id is not None:
            request.id = id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_build,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_builds(
        self,
        request: cloudbuild.ListBuildsRequest = None,
        *,
        project_id: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBuildsAsyncPager:
        r"""Lists previously requested builds.
        Previously requested builds may still be in-progress, or
        may have finished successfully or unsuccessfully.

        Args:
            request (:class:`~.cloudbuild.ListBuildsRequest`):
                The request object. Request to list builds.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
                The raw filter text to constrain the
                results.
                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListBuildsAsyncPager:
                Response including listed builds.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, filter]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.ListBuildsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if filter is not None:
            request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_builds,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListBuildsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def cancel_build(
        self,
        request: cloudbuild.CancelBuildRequest = None,
        *,
        project_id: str = None,
        id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.Build:
        r"""Cancels a build in progress.

        Args:
            request (:class:`~.cloudbuild.CancelBuildRequest`):
                The request object. Request to cancel an ongoing build.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            id (:class:`str`):
                Required. ID of the build.
                This corresponds to the ``id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloudbuild.Build:
                A build resource in the Cloud Build API.

                At a high level, a ``Build`` describes where to find
                source code, how to build it (for example, the builder
                image to run on the source), and where to store the
                built artifacts.

                Fields can include the following variables, which will
                be expanded when the build is created:

                -  $PROJECT_ID: the project ID of the build.
                -  $BUILD_ID: the autogenerated ID of the build.
                -  $REPO_NAME: the source repository name specified by
                   RepoSource.
                -  $BRANCH_NAME: the branch name specified by
                   RepoSource.
                -  $TAG_NAME: the tag name specified by RepoSource.
                -  $REVISION_ID or $COMMIT_SHA: the commit SHA specified
                   by RepoSource or resolved from the specified branch
                   or tag.
                -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                   $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.CancelBuildRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if id is not None:
            request.id = id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_build,
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def retry_build(
        self,
        request: cloudbuild.RetryBuildRequest = None,
        *,
        project_id: str = None,
        id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new build based on the specified build.

        This method creates a new build using the original build
        request, which may or may not result in an identical build.

        For triggered builds:

        -  Triggered builds resolve to a precise revision; therefore a
           retry of a triggered build will result in a build that uses
           the same revision.

        For non-triggered builds that specify ``RepoSource``:

        -  If the original build built from the tip of a branch, the
           retried build will build from the tip of that branch, which
           may not be the same revision as the original build.
        -  If the original build specified a commit sha or revision ID,
           the retried build will use the identical source.

        For builds that specify ``StorageSource``:

        -  If the original build pulled source from Google Cloud Storage
           without specifying the generation of the object, the new
           build will use the current object, which may be different
           from the original build source.
        -  If the original build pulled source from Cloud Storage and
           specified the generation of the object, the new build will
           attempt to use the same object, which may or may not be
           available depending on the bucket's lifecycle management
           settings.

        Args:
            request (:class:`~.cloudbuild.RetryBuildRequest`):
                The request object. Specifies a build to retry.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            id (:class:`str`):
                Required. Build ID of the original
                build.
                This corresponds to the ``id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.cloudbuild.Build``: A build resource in the
                Cloud Build API.

                At a high level, a ``Build`` describes where to find
                source code, how to build it (for example, the builder
                image to run on the source), and where to store the
                built artifacts.

                Fields can include the following variables, which will
                be expanded when the build is created:

                -  $PROJECT_ID: the project ID of the build.
                -  $BUILD_ID: the autogenerated ID of the build.
                -  $REPO_NAME: the source repository name specified by
                   RepoSource.
                -  $BRANCH_NAME: the branch name specified by
                   RepoSource.
                -  $TAG_NAME: the tag name specified by RepoSource.
                -  $REVISION_ID or $COMMIT_SHA: the commit SHA specified
                   by RepoSource or resolved from the specified branch
                   or tag.
                -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                   $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.RetryBuildRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if id is not None:
            request.id = id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.retry_build,
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    async def create_build_trigger(
        self,
        request: cloudbuild.CreateBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger: cloudbuild.BuildTrigger = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.BuildTrigger:
        r"""Creates a new ``BuildTrigger``.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.CreateBuildTriggerRequest`):
                The request object. Request to create a new
                `BuildTrigger`.
            project_id (:class:`str`):
                Required. ID of the project for which
                to configure automatic builds.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger (:class:`~.cloudbuild.BuildTrigger`):
                Required. ``BuildTrigger`` to create.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloudbuild.BuildTrigger:
                Configuration for an automated build
                in response to source repository
                changes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, trigger]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.CreateBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if trigger is not None:
            request.trigger = trigger

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_build_trigger,
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_build_trigger(
        self,
        request: cloudbuild.GetBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.BuildTrigger:
        r"""Returns information about a ``BuildTrigger``.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.GetBuildTriggerRequest`):
                The request object. Returns the `BuildTrigger` with the
                specified ID.
            project_id (:class:`str`):
                Required. ID of the project that owns
                the trigger.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (:class:`str`):
                Required. Identifier (``id`` or ``name``) of the
                ``BuildTrigger`` to get.
                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloudbuild.BuildTrigger:
                Configuration for an automated build
                in response to source repository
                changes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, trigger_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.GetBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if trigger_id is not None:
            request.trigger_id = trigger_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_build_trigger,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_build_triggers(
        self,
        request: cloudbuild.ListBuildTriggersRequest = None,
        *,
        project_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBuildTriggersAsyncPager:
        r"""Lists existing ``BuildTrigger``\ s.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.ListBuildTriggersRequest`):
                The request object. Request to list existing
                `BuildTriggers`.
            project_id (:class:`str`):
                Required. ID of the project for which
                to list BuildTriggers.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListBuildTriggersAsyncPager:
                Response containing existing ``BuildTriggers``.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.ListBuildTriggersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_build_triggers,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListBuildTriggersAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_build_trigger(
        self,
        request: cloudbuild.DeleteBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.DeleteBuildTriggerRequest`):
                The request object. Request to delete a `BuildTrigger`.
            project_id (:class:`str`):
                Required. ID of the project that owns
                the trigger.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (:class:`str`):
                Required. ID of the ``BuildTrigger`` to delete.
                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, trigger_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.DeleteBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if trigger_id is not None:
            request.trigger_id = trigger_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_build_trigger,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def update_build_trigger(
        self,
        request: cloudbuild.UpdateBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        trigger: cloudbuild.BuildTrigger = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.BuildTrigger:
        r"""Updates a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.UpdateBuildTriggerRequest`):
                The request object. Request to update an existing
                `BuildTrigger`.
            project_id (:class:`str`):
                Required. ID of the project that owns
                the trigger.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (:class:`str`):
                Required. ID of the ``BuildTrigger`` to update.
                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger (:class:`~.cloudbuild.BuildTrigger`):
                Required. ``BuildTrigger`` to update.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloudbuild.BuildTrigger:
                Configuration for an automated build
                in response to source repository
                changes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, trigger_id, trigger]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.UpdateBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if trigger_id is not None:
            request.trigger_id = trigger_id
        if trigger is not None:
            request.trigger = trigger

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_build_trigger,
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def run_build_trigger(
        self,
        request: cloudbuild.RunBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        source: cloudbuild.RepoSource = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Runs a ``BuildTrigger`` at a particular source revision.

        Args:
            request (:class:`~.cloudbuild.RunBuildTriggerRequest`):
                The request object. Specifies a build trigger to run and
                the source to use.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (:class:`str`):
                Required. ID of the trigger.
                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source (:class:`~.cloudbuild.RepoSource`):
                Required. Source to build against
                this trigger.
                This corresponds to the ``source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.cloudbuild.Build``: A build resource in the
                Cloud Build API.

                At a high level, a ``Build`` describes where to find
                source code, how to build it (for example, the builder
                image to run on the source), and where to store the
                built artifacts.

                Fields can include the following variables, which will
                be expanded when the build is created:

                -  $PROJECT_ID: the project ID of the build.
                -  $BUILD_ID: the autogenerated ID of the build.
                -  $REPO_NAME: the source repository name specified by
                   RepoSource.
                -  $BRANCH_NAME: the branch name specified by
                   RepoSource.
                -  $TAG_NAME: the tag name specified by RepoSource.
                -  $REVISION_ID or $COMMIT_SHA: the commit SHA specified
                   by RepoSource or resolved from the specified branch
                   or tag.
                -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                   $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, trigger_id, source]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.RunBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if trigger_id is not None:
            request.trigger_id = trigger_id
        if source is not None:
            request.source = source

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_build_trigger,
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    async def create_worker_pool(
        self,
        request: cloudbuild.CreateWorkerPoolRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.WorkerPool:
        r"""Creates a ``WorkerPool`` to run the builds, and returns the new
        worker pool.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.CreateWorkerPoolRequest`):
                The request object. Request to create a new
                `WorkerPool`.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloudbuild.WorkerPool:
                Configuration for a WorkerPool to run
                the builds.
                Workers are machines that Cloud Build
                uses to run your builds. By default, all
                workers run in a project owned by Cloud
                Build. To have full control over the
                workers that execute your builds -- such
                as enabling them to access private
                resources on your private network -- you
                can request Cloud Build to run the
                workers in your own project by creating
                a custom workers pool.

        """
        # Create or coerce a protobuf request object.

        request = cloudbuild.CreateWorkerPoolRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_worker_pool,
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_worker_pool(
        self,
        request: cloudbuild.GetWorkerPoolRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.WorkerPool:
        r"""Returns information about a ``WorkerPool``.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.GetWorkerPoolRequest`):
                The request object. Request to get a `WorkerPool` with
                the specified name.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloudbuild.WorkerPool:
                Configuration for a WorkerPool to run
                the builds.
                Workers are machines that Cloud Build
                uses to run your builds. By default, all
                workers run in a project owned by Cloud
                Build. To have full control over the
                workers that execute your builds -- such
                as enabling them to access private
                resources on your private network -- you
                can request Cloud Build to run the
                workers in your own project by creating
                a custom workers pool.

        """
        # Create or coerce a protobuf request object.

        request = cloudbuild.GetWorkerPoolRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_worker_pool,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_worker_pool(
        self,
        request: cloudbuild.DeleteWorkerPoolRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a ``WorkerPool`` by its project ID and WorkerPool name.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.DeleteWorkerPoolRequest`):
                The request object. Request to delete a `WorkerPool`.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.

        request = cloudbuild.DeleteWorkerPoolRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_worker_pool,
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def update_worker_pool(
        self,
        request: cloudbuild.UpdateWorkerPoolRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.WorkerPool:
        r"""Update a ``WorkerPool``.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.UpdateWorkerPoolRequest`):
                The request object. Request to update a `WorkerPool`.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloudbuild.WorkerPool:
                Configuration for a WorkerPool to run
                the builds.
                Workers are machines that Cloud Build
                uses to run your builds. By default, all
                workers run in a project owned by Cloud
                Build. To have full control over the
                workers that execute your builds -- such
                as enabling them to access private
                resources on your private network -- you
                can request Cloud Build to run the
                workers in your own project by creating
                a custom workers pool.

        """
        # Create or coerce a protobuf request object.

        request = cloudbuild.UpdateWorkerPoolRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_worker_pool,
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_worker_pools(
        self,
        request: cloudbuild.ListWorkerPoolsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.ListWorkerPoolsResponse:
        r"""List project's ``WorkerPools``.

        This API is experimental.

        Args:
            request (:class:`~.cloudbuild.ListWorkerPoolsRequest`):
                The request object. Request to list `WorkerPools`.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloudbuild.ListWorkerPoolsResponse:
                Response containing existing ``WorkerPools``.
        """
        # Create or coerce a protobuf request object.

        request = cloudbuild.ListWorkerPoolsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_worker_pools,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=600.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-devtools-cloudbuild",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudBuildAsyncClient",)
