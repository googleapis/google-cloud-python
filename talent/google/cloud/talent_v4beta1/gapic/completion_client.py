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

"""Accesses the google.cloud.talent.v4beta1 Completion API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.talent_v4beta1.gapic import completion_client_config
from google.cloud.talent_v4beta1.gapic import enums
from google.cloud.talent_v4beta1.gapic.transports import completion_grpc_transport
from google.cloud.talent_v4beta1.proto import application_pb2
from google.cloud.talent_v4beta1.proto import application_service_pb2
from google.cloud.talent_v4beta1.proto import application_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import company_pb2
from google.cloud.talent_v4beta1.proto import company_service_pb2
from google.cloud.talent_v4beta1.proto import company_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import completion_service_pb2
from google.cloud.talent_v4beta1.proto import completion_service_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-talent").version


class CompletionClient(object):
    """A service handles auto completion."""

    SERVICE_ADDRESS = "jobs.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.talent.v4beta1.Completion"

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
            CompletionClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def company_path(cls, project, tenant, company):
        """Return a fully-qualified company string."""
        return google.api_core.path_template.expand(
            "projects/{project}/tenants/{tenant}/companies/{company}",
            project=project,
            tenant=tenant,
            company=company,
        )

    @classmethod
    def company_without_tenant_path(cls, project, company):
        """Return a fully-qualified company_without_tenant string."""
        return google.api_core.path_template.expand(
            "projects/{project}/companies/{company}", project=project, company=company
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
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
            transport (Union[~.CompletionGrpcTransport,
                    Callable[[~.Credentials, type], ~.CompletionGrpcTransport]): A transport
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
            client_config = completion_client_config.config

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
                    default_class=completion_grpc_transport.CompletionGrpcTransport,
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
            self.transport = completion_grpc_transport.CompletionGrpcTransport(
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
    def complete_query(
        self,
        parent,
        query,
        page_size,
        language_codes=None,
        company=None,
        scope=None,
        type_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Completes the specified prefix with keyword suggestions.
        Intended for use by a job search auto-complete search box.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.CompletionClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `query`:
            >>> query = ''
            >>>
            >>> # TODO: Initialize `page_size`:
            >>> page_size = 0
            >>>
            >>> response = client.complete_query(parent, query, page_size)

        Args:
            parent (str): Required. Resource name of tenant the completion is performed within.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenant/foo".

                Tenant id is optional and the default tenant is used if unspecified, for
                example, "projects/api-test-project".
            query (str): Required. The query used to generate suggestions.

                The maximum number of allowed characters is 255.
            page_size (int): Required. Completion result count.

                The maximum allowed page size is 10.
            language_codes (list[str]): Optional. The list of languages of the query. This is the BCP-47
                language code, such as "en-US" or "sr-Latn". For more information, see
                `Tags for Identifying Languages <https://tools.ietf.org/html/bcp47>`__.

                For ``CompletionType.JOB_TITLE`` type, only open jobs with the same
                ``language_codes`` are returned.

                For ``CompletionType.COMPANY_NAME`` type, only companies having open
                jobs with the same ``language_codes`` are returned.

                For ``CompletionType.COMBINED`` type, only open jobs with the same
                ``language_codes`` or companies having open jobs with the same
                ``language_codes`` are returned.

                The maximum number of allowed characters is 255.
            company (str): Optional. If provided, restricts completion to specified company.

                The format is
                "projects/{project\_id}/tenants/{tenant\_id}/companies/{company\_id}",
                for example, "projects/api-test-project/tenants/foo/companies/bar".

                Tenant id is optional and the default tenant is used if unspecified, for
                example, "projects/api-test-project/companies/bar".
            scope (~google.cloud.talent_v4beta1.types.CompletionScope): Optional. The scope of the completion. The defaults is
                ``CompletionScope.PUBLIC``.
            type_ (~google.cloud.talent_v4beta1.types.CompletionType): Optional. The completion topic. The default is
                ``CompletionType.COMBINED``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types.CompleteQueryResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "complete_query" not in self._inner_api_calls:
            self._inner_api_calls[
                "complete_query"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.complete_query,
                default_retry=self._method_configs["CompleteQuery"].retry,
                default_timeout=self._method_configs["CompleteQuery"].timeout,
                client_info=self._client_info,
            )

        request = completion_service_pb2.CompleteQueryRequest(
            parent=parent,
            query=query,
            page_size=page_size,
            language_codes=language_codes,
            company=company,
            scope=scope,
            type=type_,
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

        return self._inner_api_calls["complete_query"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
