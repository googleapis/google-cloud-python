# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.cloud.talent.v4beta1 ProfileService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.talent_v4beta1.gapic import enums
from google.cloud.talent_v4beta1.gapic import profile_service_client_config
from google.cloud.talent_v4beta1.gapic.transports import profile_service_grpc_transport
from google.cloud.talent_v4beta1.proto import application_pb2
from google.cloud.talent_v4beta1.proto import application_service_pb2
from google.cloud.talent_v4beta1.proto import application_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import common_pb2
from google.cloud.talent_v4beta1.proto import company_pb2
from google.cloud.talent_v4beta1.proto import company_service_pb2
from google.cloud.talent_v4beta1.proto import company_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import completion_service_pb2
from google.cloud.talent_v4beta1.proto import completion_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import event_pb2
from google.cloud.talent_v4beta1.proto import event_service_pb2
from google.cloud.talent_v4beta1.proto import event_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import filters_pb2
from google.cloud.talent_v4beta1.proto import histogram_pb2
from google.cloud.talent_v4beta1.proto import job_pb2
from google.cloud.talent_v4beta1.proto import job_service_pb2
from google.cloud.talent_v4beta1.proto import job_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import profile_pb2
from google.cloud.talent_v4beta1.proto import profile_service_pb2
from google.cloud.talent_v4beta1.proto import profile_service_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-talent").version


class ProfileServiceClient(object):
    """
    A service that handles profile management, including profile CRUD,
    enumeration and search.
    """

    SERVICE_ADDRESS = "jobs.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.talent.v4beta1.ProfileService"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ProfileServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def profile_path(cls, project, tenant, profile):
        """Return a fully-qualified profile string."""
        return google.api_core.path_template.expand(
            "projects/{project}/tenants/{tenant}/profiles/{profile}",
            project=project,
            tenant=tenant,
            profile=profile,
        )

    @classmethod
    def tenant_path(cls, project, tenant):
        """Return a fully-qualified tenant string."""
        return google.api_core.path_template.expand(
            "projects/{project}/tenants/{tenant}", project=project, tenant=tenant
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.ProfileServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.ProfileServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = profile_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=profile_service_grpc_transport.ProfileServiceGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = profile_service_grpc_transport.ProfileServiceGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def list_profiles(
        self,
        parent,
        page_size=None,
        read_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists profiles by filter. The order is unspecified.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.ProfileServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_profiles(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_profiles(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the tenant under which the profile is
                created.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenants/foo".
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            read_mask (Union[dict, ~google.cloud.talent_v4beta1.types.FieldMask]): Optional. A field mask to specify the profile fields to be listed in
                response. All fields are listed if it is unset.

                Valid values are:

                -  name

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.talent_v4beta1.types.Profile` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_profiles" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_profiles"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_profiles,
                default_retry=self._method_configs["ListProfiles"].retry,
                default_timeout=self._method_configs["ListProfiles"].timeout,
                client_info=self._client_info,
            )

        request = profile_service_pb2.ListProfilesRequest(
            parent=parent, page_size=page_size, read_mask=read_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_profiles"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="profiles",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_profile(
        self,
        parent,
        profile,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates and returns a new profile.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.ProfileServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `profile`:
            >>> profile = {}
            >>>
            >>> response = client.create_profile(parent, profile)

        Args:
            parent (str): Required. The name of the tenant this profile belongs to.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenants/foo".
            profile (Union[dict, ~google.cloud.talent_v4beta1.types.Profile]): Required. The profile to be created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.Profile`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types.Profile` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_profile" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_profile"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_profile,
                default_retry=self._method_configs["CreateProfile"].retry,
                default_timeout=self._method_configs["CreateProfile"].timeout,
                client_info=self._client_info,
            )

        request = profile_service_pb2.CreateProfileRequest(
            parent=parent, profile=profile
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_profile"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_profile(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the specified profile.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.ProfileServiceClient()
            >>>
            >>> name = client.profile_path('[PROJECT]', '[TENANT]', '[PROFILE]')
            >>>
            >>> response = client.get_profile(name)

        Args:
            name (str): Required. Resource name of the profile to get.

                The format is
                "projects/{project\_id}/tenants/{tenant\_id}/profiles/{profile\_id}",
                for example, "projects/api-test-project/tenants/foo/profiles/bar".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types.Profile` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_profile" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_profile"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_profile,
                default_retry=self._method_configs["GetProfile"].retry,
                default_timeout=self._method_configs["GetProfile"].timeout,
                client_info=self._client_info,
            )

        request = profile_service_pb2.GetProfileRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_profile"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_profile(
        self,
        profile,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates the specified profile and returns the updated result.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.ProfileServiceClient()
            >>>
            >>> # TODO: Initialize `profile`:
            >>> profile = {}
            >>>
            >>> response = client.update_profile(profile)

        Args:
            profile (Union[dict, ~google.cloud.talent_v4beta1.types.Profile]): Required. Profile to be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.Profile`
            update_mask (Union[dict, ~google.cloud.talent_v4beta1.types.FieldMask]): Optional. A field mask to specify the profile fields to update.

                A full update is performed if it is unset.

                Valid values are:

                -  external\_id
                -  source
                -  uri
                -  is\_hirable
                -  create\_time
                -  update\_time
                -  resume
                -  person\_names
                -  addresses
                -  email\_addresses
                -  phone\_numbers
                -  personal\_uris
                -  additional\_contact\_info
                -  employment\_records
                -  education\_records
                -  skills
                -  activities
                -  publications
                -  patents
                -  certifications
                -  recruiting\_notes
                -  custom\_attributes
                -  group\_id
                -  external\_system
                -  source\_note
                -  primary\_responsibilities
                -  citizenships
                -  work\_authorizations
                -  employee\_types
                -  language\_code
                -  qualification\_summary
                -  allowed\_contact\_types
                -  preferred\_contact\_types
                -  contact\_availability
                -  language\_fluencies
                -  work\_preference
                -  industry\_experiences
                -  work\_environment\_experiences
                -  work\_availability
                -  security\_clearances
                -  references
                -  assessments
                -  interviews

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types.Profile` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_profile" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_profile"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_profile,
                default_retry=self._method_configs["UpdateProfile"].retry,
                default_timeout=self._method_configs["UpdateProfile"].timeout,
                client_info=self._client_info,
            )

        request = profile_service_pb2.UpdateProfileRequest(
            profile=profile, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("profile.name", profile.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_profile"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_profile(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the specified profile.
        Prerequisite: The profile has no associated applications or assignments
        associated.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.ProfileServiceClient()
            >>>
            >>> name = client.profile_path('[PROJECT]', '[TENANT]', '[PROFILE]')
            >>>
            >>> client.delete_profile(name)

        Args:
            name (str): Required. Resource name of the profile to be deleted.

                The format is
                "projects/{project\_id}/tenants/{tenant\_id}/profiles/{profile\_id}",
                for example, "projects/api-test-project/tenants/foo/profiles/bar".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_profile" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_profile"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_profile,
                default_retry=self._method_configs["DeleteProfile"].retry,
                default_timeout=self._method_configs["DeleteProfile"].timeout,
                client_info=self._client_info,
            )

        request = profile_service_pb2.DeleteProfileRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_profile"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def search_profiles(
        self,
        parent,
        request_metadata,
        profile_query=None,
        page_size=None,
        offset=None,
        disable_spell_check=None,
        order_by=None,
        case_sensitive_sort=None,
        histogram_queries=None,
        result_set_id=None,
        strict_keywords_search=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Searches for profiles within a tenant.

        For example, search by raw queries "software engineer in Mountain View"
        or search by structured filters (location filter, education filter,
        etc.).

        See ``SearchProfilesRequest`` for more information.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.ProfileServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `request_metadata`:
            >>> request_metadata = {}
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_profiles(parent, request_metadata):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_profiles(parent, request_metadata).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the tenant to search within.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenants/foo".
            request_metadata (Union[dict, ~google.cloud.talent_v4beta1.types.RequestMetadata]): Required. The meta information collected about the profile search user.
                This is used to improve the search quality of the service. These values are
                provided by users, and must be precise and consistent.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.RequestMetadata`
            profile_query (Union[dict, ~google.cloud.talent_v4beta1.types.ProfileQuery]): Optional. Search query to execute. See ``ProfileQuery`` for more
                details.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.ProfileQuery`
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            offset (int): Optional. An integer that specifies the current offset (that is,
                starting result) in search results. This field is only considered if
                ``page_token`` is unset.

                The maximum allowed value is 5000. Otherwise an error is thrown.

                For example, 0 means to search from the first profile, and 10 means to
                search from the 11th profile. This can be used for pagination, for
                example pageSize = 10 and offset = 10 means to search from the second
                page.
            disable_spell_check (bool): Optional. This flag controls the spell-check feature. If ``false``, the
                service attempts to correct a misspelled query.

                For example, "enginee" is corrected to "engineer".
            order_by (str): Optional. The criteria that determines how search results are sorted.
                Defaults is "relevance desc" if no value is specified.

                Supported options are:

                -  "relevance desc": By descending relevance, as determined by the API
                   algorithms.
                -  "update\_date desc": Sort by ``Profile.update_time`` in descending
                   order (recently updated profiles first).
                -  "create\_date desc": Sort by ``Profile.create_time`` in descending
                   order (recently created profiles first).
                -  "first\_name": Sort by ``PersonName.PersonStructuredName.given_name``
                   in ascending order.
                -  "first\_name desc": Sort by
                   ``PersonName.PersonStructuredName.given_name`` in descending order.
                -  "last\_name": Sort by ``PersonName.PersonStructuredName.family_name``
                   in ascending order.
                -  "last\_name desc": Sort by
                   ``PersonName.PersonStructuredName.family_name`` in ascending order.
            case_sensitive_sort (bool): Optional. When sort by field is based on alphabetical order, sort values
                case sensitively (based on ASCII) when the value is set to true. Default
                value is case in-sensitive sort (false).
            histogram_queries (list[Union[dict, ~google.cloud.talent_v4beta1.types.HistogramQuery]]): Optional. A list of expressions specifies histogram requests against
                matching profiles for ``SearchProfilesRequest``.

                The expression syntax looks like a function definition with optional
                parameters.

                Function syntax: function\_name(histogram\_facet[, list of buckets])

                Data types:

                -  Histogram facet: facet names with format [a-zA-Z][a-zA-Z0-9\_]+.
                -  String: string like "any string with backslash escape for quote(")."
                -  Number: whole number and floating point number like 10, -1 and -0.01.
                -  List: list of elements with comma(,) separator surrounded by square
                   brackets. For example, [1, 2, 3] and ["one", "two", "three"].

                Built-in constants:

                -  MIN (minimum number similar to java Double.MIN\_VALUE)
                -  MAX (maximum number similar to java Double.MAX\_VALUE)

                Built-in functions:

                -  bucket(start, end[, label]) Bucket build-in function creates a bucket
                   with range of \`start, end). Note that the end is exclusive. For
                   example, bucket(1, MAX, "positive number") or bucket(1, 10).

                Histogram Facets:

                -  admin1: Admin1 is a global placeholder for referring to state,
                   province, or the particular term a country uses to define the
                   geographic structure below the country level. Examples include states
                   codes such as "CA", "IL", "NY", and provinces, such as "BC".
                -  locality: Locality is a global placeholder for referring to city,
                   town, or the particular term a country uses to define the geographic
                   structure below the admin1 level. Examples include city names such as
                   "Mountain View" and "New York".
                -  extended\_locality: Extended locality is concatenated version of
                   admin1 and locality with comma separator. For example, "Mountain
                   View, CA" and "New York, NY".
                -  postal\_code: Postal code of profile which follows locale code.
                -  country: Country code (ISO-3166-1 alpha-2 code) of profile, such as
                   US, JP, GB.
                -  job\_title: Normalized job titles specified in EmploymentHistory.
                -  company\_name: Normalized company name of profiles to match on.
                -  institution: The school name. For example, "MIT", "University of
                   California, Berkeley"
                -  degree: Highest education degree in ISCED code. Each value in degree
                   covers a specific level of education, without any expansion to upper
                   nor lower levels of education degree.
                -  experience\_in\_months: experience in months. 0 means 0 month to 1
                   month (exclusive).
                -  application\_date: The application date specifies application start
                   dates. See [ApplicationDateFilter\` for more details.
                -  application\_outcome\_notes: The application outcome reason specifies
                   the reasons behind the outcome of the job application. See
                   ``ApplicationOutcomeNotesFilter`` for more details.
                -  application\_job\_title: The application job title specifies the job
                   applied for in the application. See ``ApplicationJobFilter`` for more
                   details.
                -  hirable\_status: Hirable status specifies the profile's hirable
                   status.
                -  string\_custom\_attribute: String custom attributes. Values can be
                   accessed via square bracket notation like
                   string\_custom\_attribute["key1"].
                -  numeric\_custom\_attribute: Numeric custom attributes. Values can be
                   accessed via square bracket notation like
                   numeric\_custom\_attribute["key1"].

                Example expressions:

                -  count(admin1)
                -  count(experience\_in\_months, [bucket(0, 12, "1 year"), bucket(12,
                   36, "1-3 years"), bucket(36, MAX, "3+ years")])
                -  count(string\_custom\_attribute["assigned\_recruiter"])
                -  count(numeric\_custom\_attribute["favorite\_number"], [bucket(MIN, 0,
                   "negative"), bucket(0, MAX, "non-negative")])

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.HistogramQuery`
            result_set_id (str): Optional. An id that uniquely identifies the result set of a
                ``SearchProfiles`` call. The id should be retrieved from the
                ``SearchProfilesResponse`` message returned from a previous invocation
                of ``SearchProfiles``.

                A result set is an ordered list of search results.

                If this field is not set, a new result set is computed based on the
                ``profile_query``. A new ``result_set_id`` is returned as a handle to
                access this result set.

                If this field is set, the service will ignore the resource and
                ``profile_query`` values, and simply retrieve a page of results from the
                corresponding result set. In this case, one and only one of
                ``page_token`` or ``offset`` must be set.

                A typical use case is to invoke ``SearchProfilesRequest`` without this
                field, then use the resulting ``result_set_id`` in
                ``SearchProfilesResponse`` to page through the results.
            strict_keywords_search (bool): Optional. This flag is used to indicate whether the service will attempt to
                understand synonyms and terms related to the search query or treat the
                query "as is" when it generates a set of results. By default this flag is
                set to false, thus allowing expanded results to also be returned. For
                example a search for "software engineer" might also return candidates who
                have experience in jobs similar to software engineer positions. By setting
                this flag to true, the service will only attempt to deliver candidates has
                software engineer in his/her global fields by treating "software engineer"
                as a keyword.

                It is recommended to provide a feature in the UI (such as a checkbox) to
                allow recruiters to set this flag to true if they intend to search for
                longer boolean strings.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.talent_v4beta1.types.SummarizedProfile` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "search_profiles" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_profiles"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_profiles,
                default_retry=self._method_configs["SearchProfiles"].retry,
                default_timeout=self._method_configs["SearchProfiles"].timeout,
                client_info=self._client_info,
            )

        request = profile_service_pb2.SearchProfilesRequest(
            parent=parent,
            request_metadata=request_metadata,
            profile_query=profile_query,
            page_size=page_size,
            offset=offset,
            disable_spell_check=disable_spell_check,
            order_by=order_by,
            case_sensitive_sort=case_sensitive_sort,
            histogram_queries=histogram_queries,
            result_set_id=result_set_id,
            strict_keywords_search=strict_keywords_search,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["search_profiles"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="summarized_profiles",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator
