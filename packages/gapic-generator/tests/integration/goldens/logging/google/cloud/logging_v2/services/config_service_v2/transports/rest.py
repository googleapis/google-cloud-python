# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.logging_v2.types import logging_config
from google.protobuf import empty_pb2  # type: ignore

from .base import ConfigServiceV2Transport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ConfigServiceV2RestInterceptor:
    """Interceptor for ConfigServiceV2.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ConfigServiceV2RestTransport.

    .. code-block:: python
        class MyCustomConfigServiceV2Interceptor(ConfigServiceV2RestInterceptor):
            def pre_create_bucket(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_bucket(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_exclusion(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_exclusion(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_sink(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_sink(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_view(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_view(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_bucket(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_exclusion(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_sink(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_view(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_bucket(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_bucket(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cmek_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cmek_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_exclusion(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_exclusion(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_sink(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_sink(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_view(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_view(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_buckets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_buckets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_exclusions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_exclusions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sinks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sinks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_views(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_views(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_bucket(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_update_bucket(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_bucket(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cmek_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cmek_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_exclusion(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_exclusion(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_sink(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_sink(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_view(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_view(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ConfigServiceV2RestTransport(interceptor=MyCustomConfigServiceV2Interceptor())
        client = ConfigServiceV2Client(transport=transport)


    """
    def pre_create_bucket(self, request: logging_config.CreateBucketRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.CreateBucketRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_bucket

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_create_bucket(self, response: logging_config.LogBucket) -> logging_config.LogBucket:
        """Post-rpc interceptor for create_bucket

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_create_exclusion(self, request: logging_config.CreateExclusionRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.CreateExclusionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_exclusion

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_create_exclusion(self, response: logging_config.LogExclusion) -> logging_config.LogExclusion:
        """Post-rpc interceptor for create_exclusion

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_create_sink(self, request: logging_config.CreateSinkRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.CreateSinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_sink

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_create_sink(self, response: logging_config.LogSink) -> logging_config.LogSink:
        """Post-rpc interceptor for create_sink

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_create_view(self, request: logging_config.CreateViewRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.CreateViewRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_view

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_create_view(self, response: logging_config.LogView) -> logging_config.LogView:
        """Post-rpc interceptor for create_view

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_delete_bucket(self, request: logging_config.DeleteBucketRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.DeleteBucketRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_bucket

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def pre_delete_exclusion(self, request: logging_config.DeleteExclusionRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.DeleteExclusionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_exclusion

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def pre_delete_sink(self, request: logging_config.DeleteSinkRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.DeleteSinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_sink

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def pre_delete_view(self, request: logging_config.DeleteViewRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.DeleteViewRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_view

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def pre_get_bucket(self, request: logging_config.GetBucketRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.GetBucketRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_bucket

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_get_bucket(self, response: logging_config.LogBucket) -> logging_config.LogBucket:
        """Post-rpc interceptor for get_bucket

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_get_cmek_settings(self, request: logging_config.GetCmekSettingsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.GetCmekSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cmek_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_get_cmek_settings(self, response: logging_config.CmekSettings) -> logging_config.CmekSettings:
        """Post-rpc interceptor for get_cmek_settings

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_get_exclusion(self, request: logging_config.GetExclusionRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.GetExclusionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_exclusion

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_get_exclusion(self, response: logging_config.LogExclusion) -> logging_config.LogExclusion:
        """Post-rpc interceptor for get_exclusion

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_get_sink(self, request: logging_config.GetSinkRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.GetSinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_sink

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_get_sink(self, response: logging_config.LogSink) -> logging_config.LogSink:
        """Post-rpc interceptor for get_sink

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_get_view(self, request: logging_config.GetViewRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.GetViewRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_view

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_get_view(self, response: logging_config.LogView) -> logging_config.LogView:
        """Post-rpc interceptor for get_view

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_list_buckets(self, request: logging_config.ListBucketsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.ListBucketsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_buckets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_list_buckets(self, response: logging_config.ListBucketsResponse) -> logging_config.ListBucketsResponse:
        """Post-rpc interceptor for list_buckets

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_list_exclusions(self, request: logging_config.ListExclusionsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.ListExclusionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_exclusions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_list_exclusions(self, response: logging_config.ListExclusionsResponse) -> logging_config.ListExclusionsResponse:
        """Post-rpc interceptor for list_exclusions

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_list_sinks(self, request: logging_config.ListSinksRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.ListSinksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_sinks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_list_sinks(self, response: logging_config.ListSinksResponse) -> logging_config.ListSinksResponse:
        """Post-rpc interceptor for list_sinks

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_list_views(self, request: logging_config.ListViewsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.ListViewsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_views

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_list_views(self, response: logging_config.ListViewsResponse) -> logging_config.ListViewsResponse:
        """Post-rpc interceptor for list_views

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_undelete_bucket(self, request: logging_config.UndeleteBucketRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.UndeleteBucketRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undelete_bucket

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def pre_update_bucket(self, request: logging_config.UpdateBucketRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.UpdateBucketRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_bucket

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_update_bucket(self, response: logging_config.LogBucket) -> logging_config.LogBucket:
        """Post-rpc interceptor for update_bucket

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_update_cmek_settings(self, request: logging_config.UpdateCmekSettingsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.UpdateCmekSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_cmek_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_update_cmek_settings(self, response: logging_config.CmekSettings) -> logging_config.CmekSettings:
        """Post-rpc interceptor for update_cmek_settings

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_update_exclusion(self, request: logging_config.UpdateExclusionRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.UpdateExclusionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_exclusion

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_update_exclusion(self, response: logging_config.LogExclusion) -> logging_config.LogExclusion:
        """Post-rpc interceptor for update_exclusion

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_update_sink(self, request: logging_config.UpdateSinkRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.UpdateSinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_sink

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_update_sink(self, response: logging_config.LogSink) -> logging_config.LogSink:
        """Post-rpc interceptor for update_sink

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response
    def pre_update_view(self, request: logging_config.UpdateViewRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[logging_config.UpdateViewRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_view

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConfigServiceV2 server.
        """
        return request, metadata

    def post_update_view(self, response: logging_config.LogView) -> logging_config.LogView:
        """Post-rpc interceptor for update_view

        Override in a subclass to manipulate the response
        after it is returned by the ConfigServiceV2 server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ConfigServiceV2RestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ConfigServiceV2RestInterceptor


class ConfigServiceV2RestTransport(ConfigServiceV2Transport):
    """REST backend transport for ConfigServiceV2.

    Service for configuring sinks used to route log entries.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    NOTE: This REST transport functionality is currently in a beta
    state (preview). We welcome your feedback via an issue in this
    library's source repository. Thank you!
    """

    def __init__(self, *,
            host: str = 'logging.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            client_cert_source_for_mtls: Optional[Callable[[
                ], Tuple[bytes, bytes]]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            url_scheme: str = 'https',
            interceptor: Optional[ConfigServiceV2RestInterceptor] = None,
            api_audience: Optional[str] = None,
            ) -> None:
        """Instantiate the transport.

       NOTE: This REST transport functionality is currently in a beta
       state (preview). We welcome your feedback via a GitHub issue in
       this library's repository. Thank you!

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(f"Unexpected hostname structure: {host}")  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST)
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ConfigServiceV2RestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateBucket(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("CreateBucket")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
            "bucketId" : "",        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.CreateBucketRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogBucket:
            r"""Call the create bucket method over HTTP.

            Args:
                request (~.logging_config.CreateBucketRequest):
                    The request object. The parameters to ``CreateBucket``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogBucket:
                    Describes a repository of logs.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2/{parent=*/*/locations/*}/buckets',
                'body': 'bucket',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=projects/*/locations/*}/buckets',
                'body': 'bucket',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=organizations/*/locations/*}/buckets',
                'body': 'bucket',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=folders/*/locations/*}/buckets',
                'body': 'bucket',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=billingAccounts/*/locations/*}/buckets',
                'body': 'bucket',
            },
            ]
            request, metadata = self._interceptor.pre_create_bucket(request, metadata)
            pb_request = logging_config.CreateBucketRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogBucket()
            pb_resp = logging_config.LogBucket.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_bucket(resp)
            return resp

    class _CreateExclusion(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("CreateExclusion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.CreateExclusionRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogExclusion:
            r"""Call the create exclusion method over HTTP.

            Args:
                request (~.logging_config.CreateExclusionRequest):
                    The request object. The parameters to ``CreateExclusion``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogExclusion:
                    Specifies a set of log entries that
                are not to be stored in Logging. If your
                GCP resource receives a large volume of
                logs, you can use exclusions to reduce
                your chargeable logs. Exclusions are
                processed after log sinks, so you can
                export log entries before they are
                excluded. Note that organization-level
                and folder-level exclusions don't apply
                to child resources, and that you can't
                exclude audit log entries.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2/{parent=*/*}/exclusions',
                'body': 'exclusion',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=projects/*}/exclusions',
                'body': 'exclusion',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=organizations/*}/exclusions',
                'body': 'exclusion',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=folders/*}/exclusions',
                'body': 'exclusion',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=billingAccounts/*}/exclusions',
                'body': 'exclusion',
            },
            ]
            request, metadata = self._interceptor.pre_create_exclusion(request, metadata)
            pb_request = logging_config.CreateExclusionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogExclusion()
            pb_resp = logging_config.LogExclusion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_exclusion(resp)
            return resp

    class _CreateSink(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("CreateSink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.CreateSinkRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogSink:
            r"""Call the create sink method over HTTP.

            Args:
                request (~.logging_config.CreateSinkRequest):
                    The request object. The parameters to ``CreateSink``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogSink:
                    Describes a sink used to export log
                entries to one of the following
                destinations in any project: a Cloud
                Storage bucket, a BigQuery dataset, or a
                Cloud Pub/Sub topic. A logs filter
                controls which log entries are exported.
                The sink must be created within a
                project, organization, billing account,
                or folder.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2/{parent=*/*}/sinks',
                'body': 'sink',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=projects/*}/sinks',
                'body': 'sink',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=organizations/*}/sinks',
                'body': 'sink',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=folders/*}/sinks',
                'body': 'sink',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=billingAccounts/*}/sinks',
                'body': 'sink',
            },
            ]
            request, metadata = self._interceptor.pre_create_sink(request, metadata)
            pb_request = logging_config.CreateSinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogSink()
            pb_resp = logging_config.LogSink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_sink(resp)
            return resp

    class _CreateView(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("CreateView")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
            "viewId" : "",        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.CreateViewRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogView:
            r"""Call the create view method over HTTP.

            Args:
                request (~.logging_config.CreateViewRequest):
                    The request object. The parameters to ``CreateView``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogView:
                    Describes a view over logs in a
                bucket.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2/{parent=*/*/locations/*/buckets/*}/views',
                'body': 'view',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=projects/*/locations/*/buckets/*}/views',
                'body': 'view',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=organizations/*/locations/*/buckets/*}/views',
                'body': 'view',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=folders/*/locations/*/buckets/*}/views',
                'body': 'view',
            },
{
                'method': 'post',
                'uri': '/v2/{parent=billingAccounts/*/locations/*/buckets/*}/views',
                'body': 'view',
            },
            ]
            request, metadata = self._interceptor.pre_create_view(request, metadata)
            pb_request = logging_config.CreateViewRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogView()
            pb_resp = logging_config.LogView.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_view(resp)
            return resp

    class _DeleteBucket(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("DeleteBucket")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.DeleteBucketRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ):
            r"""Call the delete bucket method over HTTP.

            Args:
                request (~.logging_config.DeleteBucketRequest):
                    The request object. The parameters to ``DeleteBucket``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/v2/{name=*/*/locations/*/buckets/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=projects/*/locations/*/buckets/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=organizations/*/locations/*/buckets/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=folders/*/locations/*/buckets/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=billingAccounts/*/locations/*/buckets/*}',
            },
            ]
            request, metadata = self._interceptor.pre_delete_bucket(request, metadata)
            pb_request = logging_config.DeleteBucketRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteExclusion(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("DeleteExclusion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.DeleteExclusionRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ):
            r"""Call the delete exclusion method over HTTP.

            Args:
                request (~.logging_config.DeleteExclusionRequest):
                    The request object. The parameters to ``DeleteExclusion``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/v2/{name=*/*/exclusions/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=projects/*/exclusions/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=organizations/*/exclusions/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=folders/*/exclusions/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=billingAccounts/*/exclusions/*}',
            },
            ]
            request, metadata = self._interceptor.pre_delete_exclusion(request, metadata)
            pb_request = logging_config.DeleteExclusionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteSink(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("DeleteSink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.DeleteSinkRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ):
            r"""Call the delete sink method over HTTP.

            Args:
                request (~.logging_config.DeleteSinkRequest):
                    The request object. The parameters to ``DeleteSink``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/v2/{sink_name=*/*/sinks/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{sink_name=projects/*/sinks/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{sink_name=organizations/*/sinks/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{sink_name=folders/*/sinks/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{sink_name=billingAccounts/*/sinks/*}',
            },
            ]
            request, metadata = self._interceptor.pre_delete_sink(request, metadata)
            pb_request = logging_config.DeleteSinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteView(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("DeleteView")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.DeleteViewRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ):
            r"""Call the delete view method over HTTP.

            Args:
                request (~.logging_config.DeleteViewRequest):
                    The request object. The parameters to ``DeleteView``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/v2/{name=*/*/locations/*/buckets/*/views/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=projects/*/locations/*/buckets/*/views/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=organizations/*/locations/*/buckets/*/views/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=folders/*/locations/*/buckets/*/views/*}',
            },
{
                'method': 'delete',
                'uri': '/v2/{name=billingAccounts/*/locations/*/buckets/*/views/*}',
            },
            ]
            request, metadata = self._interceptor.pre_delete_view(request, metadata)
            pb_request = logging_config.DeleteViewRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetBucket(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("GetBucket")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.GetBucketRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogBucket:
            r"""Call the get bucket method over HTTP.

            Args:
                request (~.logging_config.GetBucketRequest):
                    The request object. The parameters to ``GetBucket``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogBucket:
                    Describes a repository of logs.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2/{name=*/*/locations/*/buckets/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=projects/*/locations/*/buckets/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=organizations/*/locations/*/buckets/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=folders/*/locations/*/buckets/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=billingAccounts/*/buckets/*}',
            },
            ]
            request, metadata = self._interceptor.pre_get_bucket(request, metadata)
            pb_request = logging_config.GetBucketRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogBucket()
            pb_resp = logging_config.LogBucket.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_bucket(resp)
            return resp

    class _GetCmekSettings(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("GetCmekSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.GetCmekSettingsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.CmekSettings:
            r"""Call the get cmek settings method over HTTP.

            Args:
                request (~.logging_config.GetCmekSettingsRequest):
                    The request object. The parameters to
                [GetCmekSettings][google.logging.v2.ConfigServiceV2.GetCmekSettings].

                See `Enabling CMEK for Logs
                Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
                for more information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.CmekSettings:
                    Describes the customer-managed encryption key (CMEK)
                settings associated with a project, folder,
                organization, billing account, or flexible resource.

                Note: CMEK for the Logs Router can currently only be
                configured for GCP organizations. Once configured, it
                applies to all projects and folders in the GCP
                organization.

                See `Enabling CMEK for Logs
                Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
                for more information.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2/{name=*/*}/cmekSettings',
            },
{
                'method': 'get',
                'uri': '/v2/{name=organizations/*}/cmekSettings',
            },
            ]
            request, metadata = self._interceptor.pre_get_cmek_settings(request, metadata)
            pb_request = logging_config.GetCmekSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.CmekSettings()
            pb_resp = logging_config.CmekSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_cmek_settings(resp)
            return resp

    class _GetExclusion(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("GetExclusion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.GetExclusionRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogExclusion:
            r"""Call the get exclusion method over HTTP.

            Args:
                request (~.logging_config.GetExclusionRequest):
                    The request object. The parameters to ``GetExclusion``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogExclusion:
                    Specifies a set of log entries that
                are not to be stored in Logging. If your
                GCP resource receives a large volume of
                logs, you can use exclusions to reduce
                your chargeable logs. Exclusions are
                processed after log sinks, so you can
                export log entries before they are
                excluded. Note that organization-level
                and folder-level exclusions don't apply
                to child resources, and that you can't
                exclude audit log entries.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2/{name=*/*/exclusions/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=projects/*/exclusions/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=organizations/*/exclusions/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=folders/*/exclusions/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=billingAccounts/*/exclusions/*}',
            },
            ]
            request, metadata = self._interceptor.pre_get_exclusion(request, metadata)
            pb_request = logging_config.GetExclusionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogExclusion()
            pb_resp = logging_config.LogExclusion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_exclusion(resp)
            return resp

    class _GetSink(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("GetSink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.GetSinkRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogSink:
            r"""Call the get sink method over HTTP.

            Args:
                request (~.logging_config.GetSinkRequest):
                    The request object. The parameters to ``GetSink``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogSink:
                    Describes a sink used to export log
                entries to one of the following
                destinations in any project: a Cloud
                Storage bucket, a BigQuery dataset, or a
                Cloud Pub/Sub topic. A logs filter
                controls which log entries are exported.
                The sink must be created within a
                project, organization, billing account,
                or folder.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2/{sink_name=*/*/sinks/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{sink_name=projects/*/sinks/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{sink_name=organizations/*/sinks/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{sink_name=folders/*/sinks/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{sink_name=billingAccounts/*/sinks/*}',
            },
            ]
            request, metadata = self._interceptor.pre_get_sink(request, metadata)
            pb_request = logging_config.GetSinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogSink()
            pb_resp = logging_config.LogSink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_sink(resp)
            return resp

    class _GetView(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("GetView")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.GetViewRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogView:
            r"""Call the get view method over HTTP.

            Args:
                request (~.logging_config.GetViewRequest):
                    The request object. The parameters to ``GetView``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogView:
                    Describes a view over logs in a
                bucket.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2/{name=*/*/locations/*/buckets/*/views/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=projects/*/locations/*/buckets/*/views/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=organizations/*/locations/*/buckets/*/views/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=folders/*/locations/*/buckets/*/views/*}',
            },
{
                'method': 'get',
                'uri': '/v2/{name=billingAccounts/*/buckets/*/views/*}',
            },
            ]
            request, metadata = self._interceptor.pre_get_view(request, metadata)
            pb_request = logging_config.GetViewRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogView()
            pb_resp = logging_config.LogView.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_view(resp)
            return resp

    class _ListBuckets(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("ListBuckets")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.ListBucketsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.ListBucketsResponse:
            r"""Call the list buckets method over HTTP.

            Args:
                request (~.logging_config.ListBucketsRequest):
                    The request object. The parameters to ``ListBuckets``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.ListBucketsResponse:
                    The response from ListBuckets.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2/{parent=*/*/locations/*}/buckets',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=projects/*/locations/*}/buckets',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=organizations/*/locations/*}/buckets',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=folders/*/locations/*}/buckets',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=billingAccounts/*/locations/*}/buckets',
            },
            ]
            request, metadata = self._interceptor.pre_list_buckets(request, metadata)
            pb_request = logging_config.ListBucketsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.ListBucketsResponse()
            pb_resp = logging_config.ListBucketsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_buckets(resp)
            return resp

    class _ListExclusions(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("ListExclusions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.ListExclusionsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.ListExclusionsResponse:
            r"""Call the list exclusions method over HTTP.

            Args:
                request (~.logging_config.ListExclusionsRequest):
                    The request object. The parameters to ``ListExclusions``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.ListExclusionsResponse:
                    Result returned from ``ListExclusions``.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2/{parent=*/*}/exclusions',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=projects/*}/exclusions',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=organizations/*}/exclusions',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=folders/*}/exclusions',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=billingAccounts/*}/exclusions',
            },
            ]
            request, metadata = self._interceptor.pre_list_exclusions(request, metadata)
            pb_request = logging_config.ListExclusionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.ListExclusionsResponse()
            pb_resp = logging_config.ListExclusionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_exclusions(resp)
            return resp

    class _ListSinks(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("ListSinks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.ListSinksRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.ListSinksResponse:
            r"""Call the list sinks method over HTTP.

            Args:
                request (~.logging_config.ListSinksRequest):
                    The request object. The parameters to ``ListSinks``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.ListSinksResponse:
                    Result returned from ``ListSinks``.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2/{parent=*/*}/sinks',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=projects/*}/sinks',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=organizations/*}/sinks',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=folders/*}/sinks',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=billingAccounts/*}/sinks',
            },
            ]
            request, metadata = self._interceptor.pre_list_sinks(request, metadata)
            pb_request = logging_config.ListSinksRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.ListSinksResponse()
            pb_resp = logging_config.ListSinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sinks(resp)
            return resp

    class _ListViews(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("ListViews")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.ListViewsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.ListViewsResponse:
            r"""Call the list views method over HTTP.

            Args:
                request (~.logging_config.ListViewsRequest):
                    The request object. The parameters to ``ListViews``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.ListViewsResponse:
                    The response from ListViews.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v2/{parent=*/*/locations/*/buckets/*}/views',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=projects/*/locations/*/buckets/*}/views',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=organizations/*/locations/*/buckets/*}/views',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=folders/*/locations/*/buckets/*}/views',
            },
{
                'method': 'get',
                'uri': '/v2/{parent=billingAccounts/*/locations/*/buckets/*}/views',
            },
            ]
            request, metadata = self._interceptor.pre_list_views(request, metadata)
            pb_request = logging_config.ListViewsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.ListViewsResponse()
            pb_resp = logging_config.ListViewsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_views(resp)
            return resp

    class _UndeleteBucket(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("UndeleteBucket")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.UndeleteBucketRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ):
            r"""Call the undelete bucket method over HTTP.

            Args:
                request (~.logging_config.UndeleteBucketRequest):
                    The request object. The parameters to ``UndeleteBucket``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v2/{name=*/*/locations/*/buckets/*}:undelete',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v2/{name=projects/*/locations/*/buckets/*}:undelete',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v2/{name=organizations/*/locations/*/buckets/*}:undelete',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v2/{name=folders/*/locations/*/buckets/*}:undelete',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v2/{name=billingAccounts/*/locations/*/buckets/*}:undelete',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_undelete_bucket(request, metadata)
            pb_request = logging_config.UndeleteBucketRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _UpdateBucket(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("UpdateBucket")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
            "updateMask" : {},        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.UpdateBucketRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogBucket:
            r"""Call the update bucket method over HTTP.

            Args:
                request (~.logging_config.UpdateBucketRequest):
                    The request object. The parameters to ``UpdateBucket``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogBucket:
                    Describes a repository of logs.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/v2/{name=*/*/locations/*/buckets/*}',
                'body': 'bucket',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=projects/*/locations/*/buckets/*}',
                'body': 'bucket',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=organizations/*/locations/*/buckets/*}',
                'body': 'bucket',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=folders/*/locations/*/buckets/*}',
                'body': 'bucket',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=billingAccounts/*/locations/*/buckets/*}',
                'body': 'bucket',
            },
            ]
            request, metadata = self._interceptor.pre_update_bucket(request, metadata)
            pb_request = logging_config.UpdateBucketRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogBucket()
            pb_resp = logging_config.LogBucket.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_bucket(resp)
            return resp

    class _UpdateCmekSettings(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("UpdateCmekSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.UpdateCmekSettingsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.CmekSettings:
            r"""Call the update cmek settings method over HTTP.

            Args:
                request (~.logging_config.UpdateCmekSettingsRequest):
                    The request object. The parameters to
                [UpdateCmekSettings][google.logging.v2.ConfigServiceV2.UpdateCmekSettings].

                See `Enabling CMEK for Logs
                Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
                for more information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.CmekSettings:
                    Describes the customer-managed encryption key (CMEK)
                settings associated with a project, folder,
                organization, billing account, or flexible resource.

                Note: CMEK for the Logs Router can currently only be
                configured for GCP organizations. Once configured, it
                applies to all projects and folders in the GCP
                organization.

                See `Enabling CMEK for Logs
                Router <https://cloud.google.com/logging/docs/routing/managed-encryption>`__
                for more information.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/v2/{name=*/*}/cmekSettings',
                'body': 'cmek_settings',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=organizations/*}/cmekSettings',
                'body': 'cmek_settings',
            },
            ]
            request, metadata = self._interceptor.pre_update_cmek_settings(request, metadata)
            pb_request = logging_config.UpdateCmekSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.CmekSettings()
            pb_resp = logging_config.CmekSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_cmek_settings(resp)
            return resp

    class _UpdateExclusion(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("UpdateExclusion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
            "updateMask" : {},        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.UpdateExclusionRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogExclusion:
            r"""Call the update exclusion method over HTTP.

            Args:
                request (~.logging_config.UpdateExclusionRequest):
                    The request object. The parameters to ``UpdateExclusion``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogExclusion:
                    Specifies a set of log entries that
                are not to be stored in Logging. If your
                GCP resource receives a large volume of
                logs, you can use exclusions to reduce
                your chargeable logs. Exclusions are
                processed after log sinks, so you can
                export log entries before they are
                excluded. Note that organization-level
                and folder-level exclusions don't apply
                to child resources, and that you can't
                exclude audit log entries.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/v2/{name=*/*/exclusions/*}',
                'body': 'exclusion',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=projects/*/exclusions/*}',
                'body': 'exclusion',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=organizations/*/exclusions/*}',
                'body': 'exclusion',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=folders/*/exclusions/*}',
                'body': 'exclusion',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=billingAccounts/*/exclusions/*}',
                'body': 'exclusion',
            },
            ]
            request, metadata = self._interceptor.pre_update_exclusion(request, metadata)
            pb_request = logging_config.UpdateExclusionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogExclusion()
            pb_resp = logging_config.LogExclusion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_exclusion(resp)
            return resp

    class _UpdateSink(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("UpdateSink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.UpdateSinkRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogSink:
            r"""Call the update sink method over HTTP.

            Args:
                request (~.logging_config.UpdateSinkRequest):
                    The request object. The parameters to ``UpdateSink``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogSink:
                    Describes a sink used to export log
                entries to one of the following
                destinations in any project: a Cloud
                Storage bucket, a BigQuery dataset, or a
                Cloud Pub/Sub topic. A logs filter
                controls which log entries are exported.
                The sink must be created within a
                project, organization, billing account,
                or folder.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'put',
                'uri': '/v2/{sink_name=*/*/sinks/*}',
                'body': 'sink',
            },
{
                'method': 'put',
                'uri': '/v2/{sink_name=projects/*/sinks/*}',
                'body': 'sink',
            },
{
                'method': 'put',
                'uri': '/v2/{sink_name=organizations/*/sinks/*}',
                'body': 'sink',
            },
{
                'method': 'put',
                'uri': '/v2/{sink_name=folders/*/sinks/*}',
                'body': 'sink',
            },
{
                'method': 'put',
                'uri': '/v2/{sink_name=billingAccounts/*/sinks/*}',
                'body': 'sink',
            },
{
                'method': 'patch',
                'uri': '/v2/{sink_name=projects/*/sinks/*}',
                'body': 'sink',
            },
{
                'method': 'patch',
                'uri': '/v2/{sink_name=organizations/*/sinks/*}',
                'body': 'sink',
            },
{
                'method': 'patch',
                'uri': '/v2/{sink_name=folders/*/sinks/*}',
                'body': 'sink',
            },
{
                'method': 'patch',
                'uri': '/v2/{sink_name=billingAccounts/*/sinks/*}',
                'body': 'sink',
            },
            ]
            request, metadata = self._interceptor.pre_update_sink(request, metadata)
            pb_request = logging_config.UpdateSinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogSink()
            pb_resp = logging_config.LogSink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_sink(resp)
            return resp

    class _UpdateView(ConfigServiceV2RestStub):
        def __hash__(self):
            return hash("UpdateView")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: logging_config.UpdateViewRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> logging_config.LogView:
            r"""Call the update view method over HTTP.

            Args:
                request (~.logging_config.UpdateViewRequest):
                    The request object. The parameters to ``UpdateView``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.logging_config.LogView:
                    Describes a view over logs in a
                bucket.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/v2/{name=*/*/locations/*/buckets/*/views/*}',
                'body': 'view',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=projects/*/locations/*/buckets/*/views/*}',
                'body': 'view',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=organizations/*/locations/*/buckets/*/views/*}',
                'body': 'view',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=folders/*/locations/*/buckets/*/views/*}',
                'body': 'view',
            },
{
                'method': 'patch',
                'uri': '/v2/{name=billingAccounts/*/locations/*/buckets/*/views/*}',
                'body': 'view',
            },
            ]
            request, metadata = self._interceptor.pre_update_view(request, metadata)
            pb_request = logging_config.UpdateViewRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = logging_config.LogView()
            pb_resp = logging_config.LogView.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_view(resp)
            return resp

    @property
    def create_bucket(self) -> Callable[
            [logging_config.CreateBucketRequest],
            logging_config.LogBucket]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBucket(self._session, self._host, self._interceptor) # type: ignore

    @property
    def create_exclusion(self) -> Callable[
            [logging_config.CreateExclusionRequest],
            logging_config.LogExclusion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateExclusion(self._session, self._host, self._interceptor) # type: ignore

    @property
    def create_sink(self) -> Callable[
            [logging_config.CreateSinkRequest],
            logging_config.LogSink]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSink(self._session, self._host, self._interceptor) # type: ignore

    @property
    def create_view(self) -> Callable[
            [logging_config.CreateViewRequest],
            logging_config.LogView]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateView(self._session, self._host, self._interceptor) # type: ignore

    @property
    def delete_bucket(self) -> Callable[
            [logging_config.DeleteBucketRequest],
            empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBucket(self._session, self._host, self._interceptor) # type: ignore

    @property
    def delete_exclusion(self) -> Callable[
            [logging_config.DeleteExclusionRequest],
            empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteExclusion(self._session, self._host, self._interceptor) # type: ignore

    @property
    def delete_sink(self) -> Callable[
            [logging_config.DeleteSinkRequest],
            empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSink(self._session, self._host, self._interceptor) # type: ignore

    @property
    def delete_view(self) -> Callable[
            [logging_config.DeleteViewRequest],
            empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteView(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_bucket(self) -> Callable[
            [logging_config.GetBucketRequest],
            logging_config.LogBucket]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBucket(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_cmek_settings(self) -> Callable[
            [logging_config.GetCmekSettingsRequest],
            logging_config.CmekSettings]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCmekSettings(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_exclusion(self) -> Callable[
            [logging_config.GetExclusionRequest],
            logging_config.LogExclusion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetExclusion(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_sink(self) -> Callable[
            [logging_config.GetSinkRequest],
            logging_config.LogSink]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSink(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_view(self) -> Callable[
            [logging_config.GetViewRequest],
            logging_config.LogView]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetView(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_buckets(self) -> Callable[
            [logging_config.ListBucketsRequest],
            logging_config.ListBucketsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBuckets(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_exclusions(self) -> Callable[
            [logging_config.ListExclusionsRequest],
            logging_config.ListExclusionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListExclusions(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_sinks(self) -> Callable[
            [logging_config.ListSinksRequest],
            logging_config.ListSinksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSinks(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_views(self) -> Callable[
            [logging_config.ListViewsRequest],
            logging_config.ListViewsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListViews(self._session, self._host, self._interceptor) # type: ignore

    @property
    def undelete_bucket(self) -> Callable[
            [logging_config.UndeleteBucketRequest],
            empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeleteBucket(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_bucket(self) -> Callable[
            [logging_config.UpdateBucketRequest],
            logging_config.LogBucket]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBucket(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_cmek_settings(self) -> Callable[
            [logging_config.UpdateCmekSettingsRequest],
            logging_config.CmekSettings]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCmekSettings(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_exclusion(self) -> Callable[
            [logging_config.UpdateExclusionRequest],
            logging_config.LogExclusion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateExclusion(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_sink(self) -> Callable[
            [logging_config.UpdateSinkRequest],
            logging_config.LogSink]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSink(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_view(self) -> Callable[
            [logging_config.UpdateViewRequest],
            logging_config.LogView]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateView(self._session, self._host, self._interceptor) # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__=(
    'ConfigServiceV2RestTransport',
)
