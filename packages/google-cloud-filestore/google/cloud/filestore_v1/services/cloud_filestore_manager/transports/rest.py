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

import dataclasses
import json  # type: ignore
import re
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.filestore_v1.types import cloud_filestore_service

from .base import CloudFilestoreManagerTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class CloudFilestoreManagerRestInterceptor:
    """Interceptor for CloudFilestoreManager.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CloudFilestoreManagerRestTransport.

    .. code-block:: python
        class MyCustomCloudFilestoreManagerInterceptor(CloudFilestoreManagerRestInterceptor):
            def pre_create_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restore_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restore_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CloudFilestoreManagerRestTransport(interceptor=MyCustomCloudFilestoreManagerInterceptor())
        client = CloudFilestoreManagerClient(transport=transport)


    """

    def pre_create_backup(
        self,
        request: cloud_filestore_service.CreateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_filestore_service.CreateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_create_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_instance(
        self,
        request: cloud_filestore_service.CreateInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        cloud_filestore_service.CreateInstanceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_create_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_instance

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup(
        self,
        request: cloud_filestore_service.DeleteBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_filestore_service.DeleteBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_delete_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_instance(
        self,
        request: cloud_filestore_service.DeleteInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        cloud_filestore_service.DeleteInstanceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_delete_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_instance

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup(
        self,
        request: cloud_filestore_service.GetBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_filestore_service.GetBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_get_backup(
        self, response: cloud_filestore_service.Backup
    ) -> cloud_filestore_service.Backup:
        """Post-rpc interceptor for get_backup

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_instance(
        self,
        request: cloud_filestore_service.GetInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_filestore_service.GetInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_get_instance(
        self, response: cloud_filestore_service.Instance
    ) -> cloud_filestore_service.Instance:
        """Post-rpc interceptor for get_instance

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_backups(
        self,
        request: cloud_filestore_service.ListBackupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_filestore_service.ListBackupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_list_backups(
        self, response: cloud_filestore_service.ListBackupsResponse
    ) -> cloud_filestore_service.ListBackupsResponse:
        """Post-rpc interceptor for list_backups

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_instances(
        self,
        request: cloud_filestore_service.ListInstancesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_filestore_service.ListInstancesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_list_instances(
        self, response: cloud_filestore_service.ListInstancesResponse
    ) -> cloud_filestore_service.ListInstancesResponse:
        """Post-rpc interceptor for list_instances

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_restore_instance(
        self,
        request: cloud_filestore_service.RestoreInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        cloud_filestore_service.RestoreInstanceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for restore_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_restore_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for restore_instance

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup(
        self,
        request: cloud_filestore_service.UpdateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_filestore_service.UpdateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_update_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_instance(
        self,
        request: cloud_filestore_service.UpdateInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        cloud_filestore_service.UpdateInstanceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudFilestoreManager server.
        """
        return request, metadata

    def post_update_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_instance

        Override in a subclass to manipulate the response
        after it is returned by the CloudFilestoreManager server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CloudFilestoreManagerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CloudFilestoreManagerRestInterceptor


class CloudFilestoreManagerRestTransport(CloudFilestoreManagerTransport):
    """REST backend transport for CloudFilestoreManager.

    Configures and manages Cloud Filestore resources.

    Cloud Filestore Manager v1.

    The ``file.googleapis.com`` service implements the Cloud Filestore
    API and defines the following resource model for managing instances:

    -  The service works with a collection of cloud projects, named:
       ``/projects/*``
    -  Each project has a collection of available locations, named:
       ``/locations/*``
    -  Each location has a collection of instances and backups, named:
       ``/instances/*`` and ``/backups/*`` respectively.
    -  As such, Cloud Filestore instances are resources of the form:
       ``/projects/{project_number}/locations/{location_id}/instances/{instance_id}``
       and backups are resources of the form:
       ``/projects/{project_number}/locations/{location_id}/backup/{backup_id}``

    Note that location_id must be a GCP ``zone`` for instances and but
    to a GCP ``region`` for backups; for example:

    -  ``projects/12345/locations/us-central1-c/instances/my-filestore``
    -  ``projects/12345/locations/us-central1/backups/my-backup``

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "file.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CloudFilestoreManagerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

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
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or CloudFilestoreManagerRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateBackup(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("CreateBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "backupId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.CreateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup method over HTTP.

            Args:
                request (~.cloud_filestore_service.CreateBackupRequest):
                    The request object. CreateBackupRequest creates a backup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/backups",
                    "body": "backup",
                },
            ]
            request, metadata = self._interceptor.pre_create_backup(request, metadata)
            pb_request = cloud_filestore_service.CreateBackupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_backup(resp)
            return resp

    class _CreateInstance(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("CreateInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "instanceId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.CreateInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create instance method over HTTP.

            Args:
                request (~.cloud_filestore_service.CreateInstanceRequest):
                    The request object. CreateInstanceRequest creates an
                instance.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/instances",
                    "body": "instance",
                },
            ]
            request, metadata = self._interceptor.pre_create_instance(request, metadata)
            pb_request = cloud_filestore_service.CreateInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_instance(resp)
            return resp

    class _DeleteBackup(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("DeleteBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.DeleteBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup method over HTTP.

            Args:
                request (~.cloud_filestore_service.DeleteBackupRequest):
                    The request object. DeleteBackupRequest deletes a backup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/backups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_backup(request, metadata)
            pb_request = cloud_filestore_service.DeleteBackupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_backup(resp)
            return resp

    class _DeleteInstance(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("DeleteInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.DeleteInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete instance method over HTTP.

            Args:
                request (~.cloud_filestore_service.DeleteInstanceRequest):
                    The request object. DeleteInstanceRequest deletes an
                instance.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/instances/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_instance(request, metadata)
            pb_request = cloud_filestore_service.DeleteInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_instance(resp)
            return resp

    class _GetBackup(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("GetBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.GetBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_filestore_service.Backup:
            r"""Call the get backup method over HTTP.

            Args:
                request (~.cloud_filestore_service.GetBackupRequest):
                    The request object. GetBackupRequest gets the state of a
                backup.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_filestore_service.Backup:
                    A Cloud Filestore backup.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/backups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_backup(request, metadata)
            pb_request = cloud_filestore_service.GetBackupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = cloud_filestore_service.Backup()
            pb_resp = cloud_filestore_service.Backup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup(resp)
            return resp

    class _GetInstance(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("GetInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.GetInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_filestore_service.Instance:
            r"""Call the get instance method over HTTP.

            Args:
                request (~.cloud_filestore_service.GetInstanceRequest):
                    The request object. GetInstanceRequest gets the state of
                an instance.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_filestore_service.Instance:
                    A Cloud Filestore instance.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/instances/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_instance(request, metadata)
            pb_request = cloud_filestore_service.GetInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = cloud_filestore_service.Instance()
            pb_resp = cloud_filestore_service.Instance.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_instance(resp)
            return resp

    class _ListBackups(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("ListBackups")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.ListBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_filestore_service.ListBackupsResponse:
            r"""Call the list backups method over HTTP.

            Args:
                request (~.cloud_filestore_service.ListBackupsRequest):
                    The request object. ListBackupsRequest lists backups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_filestore_service.ListBackupsResponse:
                    ListBackupsResponse is the result of
                ListBackupsRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/backups",
                },
            ]
            request, metadata = self._interceptor.pre_list_backups(request, metadata)
            pb_request = cloud_filestore_service.ListBackupsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = cloud_filestore_service.ListBackupsResponse()
            pb_resp = cloud_filestore_service.ListBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backups(resp)
            return resp

    class _ListInstances(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("ListInstances")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.ListInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_filestore_service.ListInstancesResponse:
            r"""Call the list instances method over HTTP.

            Args:
                request (~.cloud_filestore_service.ListInstancesRequest):
                    The request object. ListInstancesRequest lists instances.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_filestore_service.ListInstancesResponse:
                    ListInstancesResponse is the result
                of ListInstancesRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/instances",
                },
            ]
            request, metadata = self._interceptor.pre_list_instances(request, metadata)
            pb_request = cloud_filestore_service.ListInstancesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = cloud_filestore_service.ListInstancesResponse()
            pb_resp = cloud_filestore_service.ListInstancesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_instances(resp)
            return resp

    class _RestoreInstance(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("RestoreInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.RestoreInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restore instance method over HTTP.

            Args:
                request (~.cloud_filestore_service.RestoreInstanceRequest):
                    The request object. RestoreInstanceRequest restores an
                existing instances's file share from a
                backup.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/instances/*}:restore",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_restore_instance(
                request, metadata
            )
            pb_request = cloud_filestore_service.RestoreInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_restore_instance(resp)
            return resp

    class _UpdateBackup(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("UpdateBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_filestore_service.UpdateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup method over HTTP.

            Args:
                request (~.cloud_filestore_service.UpdateBackupRequest):
                    The request object. UpdateBackupRequest updates
                description and/or labels for a backup.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{backup.name=projects/*/locations/*/backups/*}",
                    "body": "backup",
                },
            ]
            request, metadata = self._interceptor.pre_update_backup(request, metadata)
            pb_request = cloud_filestore_service.UpdateBackupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_backup(resp)
            return resp

    class _UpdateInstance(CloudFilestoreManagerRestStub):
        def __hash__(self):
            return hash("UpdateInstance")

        def __call__(
            self,
            request: cloud_filestore_service.UpdateInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update instance method over HTTP.

            Args:
                request (~.cloud_filestore_service.UpdateInstanceRequest):
                    The request object. UpdateInstanceRequest updates the
                settings of an instance.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{instance.name=projects/*/locations/*/instances/*}",
                    "body": "instance",
                },
            ]
            request, metadata = self._interceptor.pre_update_instance(request, metadata)
            pb_request = cloud_filestore_service.UpdateInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_instance(resp)
            return resp

    @property
    def create_backup(
        self,
    ) -> Callable[
        [cloud_filestore_service.CreateBackupRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.CreateInstanceRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup(
        self,
    ) -> Callable[
        [cloud_filestore_service.DeleteBackupRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.DeleteInstanceRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup(
        self,
    ) -> Callable[
        [cloud_filestore_service.GetBackupRequest], cloud_filestore_service.Backup
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.GetInstanceRequest], cloud_filestore_service.Instance
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backups(
        self,
    ) -> Callable[
        [cloud_filestore_service.ListBackupsRequest],
        cloud_filestore_service.ListBackupsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_instances(
        self,
    ) -> Callable[
        [cloud_filestore_service.ListInstancesRequest],
        cloud_filestore_service.ListInstancesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def restore_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.RestoreInstanceRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestoreInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup(
        self,
    ) -> Callable[
        [cloud_filestore_service.UpdateBackupRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.UpdateInstanceRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CloudFilestoreManagerRestTransport",)
