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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import path_template
from google.api_core import gapic_v1
from requests import __version__ as requests_version
import dataclasses
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.compute_v1.types import compute

from .base import InstancesTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


@dataclasses.dataclass
class InstancesRestStub:
    _session: AuthorizedSession
    _host: str


class InstancesRestTransport(InstancesTransport):
    """REST backend transport for Instances.

    The Instances API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    _STUBS: Dict[str, InstancesRestStub] = {}

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
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
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._prep_wrapped_messages(client_info)

    class _AddAccessConfig(InstancesRestStub):
        def __hash__(self):
            return hash("AddAccessConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {
            "networkInterface": "",
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
            request: compute.AddAccessConfigInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the add access config method over HTTP.

            Args:
                request (~.compute.AddAccessConfigInstanceRequest):
                    The request object. A request message for
                Instances.AddAccessConfig. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/addAccessConfig",
                    "body": "access_config_resource",
                },
            ]

            request_kwargs = compute.AddAccessConfigInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.AccessConfig.to_json(
                compute.AccessConfig(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.AddAccessConfigInstanceRequest.to_json(
                    compute.AddAccessConfigInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _AddResourcePolicies(InstancesRestStub):
        def __hash__(self):
            return hash("AddResourcePolicies")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.AddResourcePoliciesInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the add resource policies method over HTTP.

            Args:
                request (~.compute.AddResourcePoliciesInstanceRequest):
                    The request object. A request message for
                Instances.AddResourcePolicies. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/addResourcePolicies",
                    "body": "instances_add_resource_policies_request_resource",
                },
            ]

            request_kwargs = compute.AddResourcePoliciesInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstancesAddResourcePoliciesRequest.to_json(
                compute.InstancesAddResourcePoliciesRequest(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.AddResourcePoliciesInstanceRequest.to_json(
                    compute.AddResourcePoliciesInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _AggregatedList(InstancesRestStub):
        def __hash__(self):
            return hash("AggregatedList")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.AggregatedListInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceAggregatedList:
            r"""Call the aggregated list method over HTTP.

            Args:
                request (~.compute.AggregatedListInstancesRequest):
                    The request object. A request message for
                Instances.AggregatedList. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceAggregatedList:

            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/aggregated/instances",
                },
            ]

            request_kwargs = compute.AggregatedListInstancesRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.AggregatedListInstancesRequest.to_json(
                    compute.AggregatedListInstancesRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.InstanceAggregatedList.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _AttachDisk(InstancesRestStub):
        def __hash__(self):
            return hash("AttachDisk")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.AttachDiskInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the attach disk method over HTTP.

            Args:
                request (~.compute.AttachDiskInstanceRequest):
                    The request object. A request message for
                Instances.AttachDisk. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/attachDisk",
                    "body": "attached_disk_resource",
                },
            ]

            request_kwargs = compute.AttachDiskInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.AttachedDisk.to_json(
                compute.AttachedDisk(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.AttachDiskInstanceRequest.to_json(
                    compute.AttachDiskInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _BulkInsert(InstancesRestStub):
        def __hash__(self):
            return hash("BulkInsert")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.BulkInsertInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the bulk insert method over HTTP.

            Args:
                request (~.compute.BulkInsertInstanceRequest):
                    The request object. A request message for
                Instances.BulkInsert. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/bulkInsert",
                    "body": "bulk_insert_instance_resource_resource",
                },
            ]

            request_kwargs = compute.BulkInsertInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.BulkInsertInstanceResource.to_json(
                compute.BulkInsertInstanceResource(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.BulkInsertInstanceRequest.to_json(
                    compute.BulkInsertInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _Delete(InstancesRestStub):
        def __hash__(self):
            return hash("Delete")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.DeleteInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteInstanceRequest):
                    The request object. A request message for
                Instances.Delete. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "delete",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}",
                },
            ]

            request_kwargs = compute.DeleteInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.DeleteInstanceRequest.to_json(
                    compute.DeleteInstanceRequest(transcoded_request["query_params"]),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _DeleteAccessConfig(InstancesRestStub):
        def __hash__(self):
            return hash("DeleteAccessConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {
            "accessConfig": "",
            "networkInterface": "",
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
            request: compute.DeleteAccessConfigInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete access config method over HTTP.

            Args:
                request (~.compute.DeleteAccessConfigInstanceRequest):
                    The request object. A request message for
                Instances.DeleteAccessConfig. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/deleteAccessConfig",
                },
            ]

            request_kwargs = compute.DeleteAccessConfigInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.DeleteAccessConfigInstanceRequest.to_json(
                    compute.DeleteAccessConfigInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _DetachDisk(InstancesRestStub):
        def __hash__(self):
            return hash("DetachDisk")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {
            "deviceName": "",
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
            request: compute.DetachDiskInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the detach disk method over HTTP.

            Args:
                request (~.compute.DetachDiskInstanceRequest):
                    The request object. A request message for
                Instances.DetachDisk. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/detachDisk",
                },
            ]

            request_kwargs = compute.DetachDiskInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.DetachDiskInstanceRequest.to_json(
                    compute.DetachDiskInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _Get(InstancesRestStub):
        def __hash__(self):
            return hash("Get")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.GetInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Instance:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetInstanceRequest):
                    The request object. A request message for Instances.Get.
                See the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Instance:
                    Represents an Instance resource. An
                instance is a virtual machine that is
                hosted on Google Cloud Platform. For
                more information, read Virtual Machine
                Instances.

            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}",
                },
            ]

            request_kwargs = compute.GetInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.GetInstanceRequest.to_json(
                    compute.GetInstanceRequest(transcoded_request["query_params"]),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Instance.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _GetEffectiveFirewalls(InstancesRestStub):
        def __hash__(self):
            return hash("GetEffectiveFirewalls")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {
            "networkInterface": "",
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
            request: compute.GetEffectiveFirewallsInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstancesGetEffectiveFirewallsResponse:
            r"""Call the get effective firewalls method over HTTP.

            Args:
                request (~.compute.GetEffectiveFirewallsInstanceRequest):
                    The request object. A request message for
                Instances.GetEffectiveFirewalls. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstancesGetEffectiveFirewallsResponse:

            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/getEffectiveFirewalls",
                },
            ]

            request_kwargs = compute.GetEffectiveFirewallsInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.GetEffectiveFirewallsInstanceRequest.to_json(
                    compute.GetEffectiveFirewallsInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.InstancesGetEffectiveFirewallsResponse.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _GetGuestAttributes(InstancesRestStub):
        def __hash__(self):
            return hash("GetGuestAttributes")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.GetGuestAttributesInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.GuestAttributes:
            r"""Call the get guest attributes method over HTTP.

            Args:
                request (~.compute.GetGuestAttributesInstanceRequest):
                    The request object. A request message for
                Instances.GetGuestAttributes. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.GuestAttributes:
                    A guest attributes entry.
            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/getGuestAttributes",
                },
            ]

            request_kwargs = compute.GetGuestAttributesInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.GetGuestAttributesInstanceRequest.to_json(
                    compute.GetGuestAttributesInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.GuestAttributes.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _GetIamPolicy(InstancesRestStub):
        def __hash__(self):
            return hash("GetIamPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.GetIamPolicyInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.compute.GetIamPolicyInstanceRequest):
                    The request object. A request message for
                Instances.GetIamPolicy. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions; each ``role``
                can be an IAM predefined role or a user-created custom
                role. For some types of Google Cloud resources, a
                ``binding`` can also specify a ``condition``, which is a
                logical expression that allows access to a resource only
                if the expression evaluates to ``true``. A condition can
                add constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.
                **JSON example:** { "bindings": [ { "role":
                "roles/resourcemanager.organizationAdmin", "members": [
                "user:mike@example.com", "group:admins@example.com",
                "domain:google.com",
                "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                ] }, { "role":
                "roles/resourcemanager.organizationViewer", "members": [
                "user:eve@example.com" ], "condition": { "title":
                "expirable access", "description": "Does not grant
                access after Sep 2020", "expression": "request.time <
                timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag":
                "BwWWja0YfJA=", "version": 3 } **YAML example:**
                bindings: - members: - user:mike@example.com -
                group:admins@example.com - domain:google.com -
                serviceAccount:my-project-id@appspot.gserviceaccount.com
                role: roles/resourcemanager.organizationAdmin - members:
                - user:eve@example.com role:
                roles/resourcemanager.organizationViewer condition:
                title: expirable access description: Does not grant
                access after Sep 2020 expression: request.time <
                timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA=
                version: 3 For a description of IAM and its features,
                see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{resource}/getIamPolicy",
                },
            ]

            request_kwargs = compute.GetIamPolicyInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.GetIamPolicyInstanceRequest.to_json(
                    compute.GetIamPolicyInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Policy.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _GetScreenshot(InstancesRestStub):
        def __hash__(self):
            return hash("GetScreenshot")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.GetScreenshotInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Screenshot:
            r"""Call the get screenshot method over HTTP.

            Args:
                request (~.compute.GetScreenshotInstanceRequest):
                    The request object. A request message for
                Instances.GetScreenshot. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Screenshot:
                    An instance's screenshot.
            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/screenshot",
                },
            ]

            request_kwargs = compute.GetScreenshotInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.GetScreenshotInstanceRequest.to_json(
                    compute.GetScreenshotInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Screenshot.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _GetSerialPortOutput(InstancesRestStub):
        def __hash__(self):
            return hash("GetSerialPortOutput")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.GetSerialPortOutputInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.SerialPortOutput:
            r"""Call the get serial port output method over HTTP.

            Args:
                request (~.compute.GetSerialPortOutputInstanceRequest):
                    The request object. A request message for
                Instances.GetSerialPortOutput. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.SerialPortOutput:
                    An instance serial console output.
            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/serialPort",
                },
            ]

            request_kwargs = compute.GetSerialPortOutputInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.GetSerialPortOutputInstanceRequest.to_json(
                    compute.GetSerialPortOutputInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.SerialPortOutput.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _GetShieldedInstanceIdentity(InstancesRestStub):
        def __hash__(self):
            return hash("GetShieldedInstanceIdentity")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.GetShieldedInstanceIdentityInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.ShieldedInstanceIdentity:
            r"""Call the get shielded instance
        identity method over HTTP.

            Args:
                request (~.compute.GetShieldedInstanceIdentityInstanceRequest):
                    The request object. A request message for
                Instances.GetShieldedInstanceIdentity.
                See the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.ShieldedInstanceIdentity:
                    A Shielded Instance Identity.
            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/getShieldedInstanceIdentity",
                },
            ]

            request_kwargs = compute.GetShieldedInstanceIdentityInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.GetShieldedInstanceIdentityInstanceRequest.to_json(
                    compute.GetShieldedInstanceIdentityInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.ShieldedInstanceIdentity.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _Insert(InstancesRestStub):
        def __hash__(self):
            return hash("Insert")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.InsertInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertInstanceRequest):
                    The request object. A request message for
                Instances.Insert. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances",
                    "body": "instance_resource",
                },
            ]

            request_kwargs = compute.InsertInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.Instance.to_json(
                compute.Instance(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.InsertInstanceRequest.to_json(
                    compute.InsertInstanceRequest(transcoded_request["query_params"]),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _List(InstancesRestStub):
        def __hash__(self):
            return hash("List")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.ListInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListInstancesRequest):
                    The request object. A request message for Instances.List.
                See the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceList:
                    Contains a list of instances.
            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances",
                },
            ]

            request_kwargs = compute.ListInstancesRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.ListInstancesRequest.to_json(
                    compute.ListInstancesRequest(transcoded_request["query_params"]),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.InstanceList.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _ListReferrers(InstancesRestStub):
        def __hash__(self):
            return hash("ListReferrers")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.ListReferrersInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.InstanceListReferrers:
            r"""Call the list referrers method over HTTP.

            Args:
                request (~.compute.ListReferrersInstancesRequest):
                    The request object. A request message for
                Instances.ListReferrers. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.InstanceListReferrers:
                    Contains a list of instance
                referrers.

            """

            http_options = [
                {
                    "method": "get",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/referrers",
                },
            ]

            request_kwargs = compute.ListReferrersInstancesRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.ListReferrersInstancesRequest.to_json(
                    compute.ListReferrersInstancesRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.InstanceListReferrers.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _RemoveResourcePolicies(InstancesRestStub):
        def __hash__(self):
            return hash("RemoveResourcePolicies")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.RemoveResourcePoliciesInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the remove resource policies method over HTTP.

            Args:
                request (~.compute.RemoveResourcePoliciesInstanceRequest):
                    The request object. A request message for
                Instances.RemoveResourcePolicies. See
                the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/removeResourcePolicies",
                    "body": "instances_remove_resource_policies_request_resource",
                },
            ]

            request_kwargs = compute.RemoveResourcePoliciesInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstancesRemoveResourcePoliciesRequest.to_json(
                compute.InstancesRemoveResourcePoliciesRequest(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.RemoveResourcePoliciesInstanceRequest.to_json(
                    compute.RemoveResourcePoliciesInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _Reset(InstancesRestStub):
        def __hash__(self):
            return hash("Reset")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.ResetInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the reset method over HTTP.

            Args:
                request (~.compute.ResetInstanceRequest):
                    The request object. A request message for
                Instances.Reset. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/reset",
                },
            ]

            request_kwargs = compute.ResetInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.ResetInstanceRequest.to_json(
                    compute.ResetInstanceRequest(transcoded_request["query_params"]),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SendDiagnosticInterrupt(InstancesRestStub):
        def __hash__(self):
            return hash("SendDiagnosticInterrupt")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SendDiagnosticInterruptInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.SendDiagnosticInterruptInstanceResponse:
            r"""Call the send diagnostic interrupt method over HTTP.

            Args:
                request (~.compute.SendDiagnosticInterruptInstanceRequest):
                    The request object. A request message for
                Instances.SendDiagnosticInterrupt. See
                the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.SendDiagnosticInterruptInstanceResponse:
                    A response message for
                Instances.SendDiagnosticInterrupt. See
                the method description for details.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/sendDiagnosticInterrupt",
                },
            ]

            request_kwargs = compute.SendDiagnosticInterruptInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SendDiagnosticInterruptInstanceRequest.to_json(
                    compute.SendDiagnosticInterruptInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.SendDiagnosticInterruptInstanceResponse.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetDeletionProtection(InstancesRestStub):
        def __hash__(self):
            return hash("SetDeletionProtection")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetDeletionProtectionInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set deletion protection method over HTTP.

            Args:
                request (~.compute.SetDeletionProtectionInstanceRequest):
                    The request object. A request message for
                Instances.SetDeletionProtection. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{resource}/setDeletionProtection",
                },
            ]

            request_kwargs = compute.SetDeletionProtectionInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetDeletionProtectionInstanceRequest.to_json(
                    compute.SetDeletionProtectionInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetDiskAutoDelete(InstancesRestStub):
        def __hash__(self):
            return hash("SetDiskAutoDelete")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {
            "autoDelete": False,
            "deviceName": "",
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
            request: compute.SetDiskAutoDeleteInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set disk auto delete method over HTTP.

            Args:
                request (~.compute.SetDiskAutoDeleteInstanceRequest):
                    The request object. A request message for
                Instances.SetDiskAutoDelete. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setDiskAutoDelete",
                },
            ]

            request_kwargs = compute.SetDiskAutoDeleteInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetDiskAutoDeleteInstanceRequest.to_json(
                    compute.SetDiskAutoDeleteInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetIamPolicy(InstancesRestStub):
        def __hash__(self):
            return hash("SetIamPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetIamPolicyInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.compute.SetIamPolicyInstanceRequest):
                    The request object. A request message for
                Instances.SetIamPolicy. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions; each ``role``
                can be an IAM predefined role or a user-created custom
                role. For some types of Google Cloud resources, a
                ``binding`` can also specify a ``condition``, which is a
                logical expression that allows access to a resource only
                if the expression evaluates to ``true``. A condition can
                add constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.
                **JSON example:** { "bindings": [ { "role":
                "roles/resourcemanager.organizationAdmin", "members": [
                "user:mike@example.com", "group:admins@example.com",
                "domain:google.com",
                "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                ] }, { "role":
                "roles/resourcemanager.organizationViewer", "members": [
                "user:eve@example.com" ], "condition": { "title":
                "expirable access", "description": "Does not grant
                access after Sep 2020", "expression": "request.time <
                timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag":
                "BwWWja0YfJA=", "version": 3 } **YAML example:**
                bindings: - members: - user:mike@example.com -
                group:admins@example.com - domain:google.com -
                serviceAccount:my-project-id@appspot.gserviceaccount.com
                role: roles/resourcemanager.organizationAdmin - members:
                - user:eve@example.com role:
                roles/resourcemanager.organizationViewer condition:
                title: expirable access description: Does not grant
                access after Sep 2020 expression: request.time <
                timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA=
                version: 3 For a description of IAM and its features,
                see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{resource}/setIamPolicy",
                    "body": "zone_set_policy_request_resource",
                },
            ]

            request_kwargs = compute.SetIamPolicyInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.ZoneSetPolicyRequest.to_json(
                compute.ZoneSetPolicyRequest(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetIamPolicyInstanceRequest.to_json(
                    compute.SetIamPolicyInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Policy.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetLabels(InstancesRestStub):
        def __hash__(self):
            return hash("SetLabels")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetLabelsInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set labels method over HTTP.

            Args:
                request (~.compute.SetLabelsInstanceRequest):
                    The request object. A request message for
                Instances.SetLabels. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setLabels",
                    "body": "instances_set_labels_request_resource",
                },
            ]

            request_kwargs = compute.SetLabelsInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstancesSetLabelsRequest.to_json(
                compute.InstancesSetLabelsRequest(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetLabelsInstanceRequest.to_json(
                    compute.SetLabelsInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetMachineResources(InstancesRestStub):
        def __hash__(self):
            return hash("SetMachineResources")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetMachineResourcesInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set machine resources method over HTTP.

            Args:
                request (~.compute.SetMachineResourcesInstanceRequest):
                    The request object. A request message for
                Instances.SetMachineResources. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setMachineResources",
                    "body": "instances_set_machine_resources_request_resource",
                },
            ]

            request_kwargs = compute.SetMachineResourcesInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstancesSetMachineResourcesRequest.to_json(
                compute.InstancesSetMachineResourcesRequest(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetMachineResourcesInstanceRequest.to_json(
                    compute.SetMachineResourcesInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetMachineType(InstancesRestStub):
        def __hash__(self):
            return hash("SetMachineType")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetMachineTypeInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set machine type method over HTTP.

            Args:
                request (~.compute.SetMachineTypeInstanceRequest):
                    The request object. A request message for
                Instances.SetMachineType. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setMachineType",
                    "body": "instances_set_machine_type_request_resource",
                },
            ]

            request_kwargs = compute.SetMachineTypeInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstancesSetMachineTypeRequest.to_json(
                compute.InstancesSetMachineTypeRequest(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetMachineTypeInstanceRequest.to_json(
                    compute.SetMachineTypeInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetMetadata(InstancesRestStub):
        def __hash__(self):
            return hash("SetMetadata")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetMetadataInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set metadata method over HTTP.

            Args:
                request (~.compute.SetMetadataInstanceRequest):
                    The request object. A request message for
                Instances.SetMetadata. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setMetadata",
                    "body": "metadata_resource",
                },
            ]

            request_kwargs = compute.SetMetadataInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.Metadata.to_json(
                compute.Metadata(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetMetadataInstanceRequest.to_json(
                    compute.SetMetadataInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetMinCpuPlatform(InstancesRestStub):
        def __hash__(self):
            return hash("SetMinCpuPlatform")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetMinCpuPlatformInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set min cpu platform method over HTTP.

            Args:
                request (~.compute.SetMinCpuPlatformInstanceRequest):
                    The request object. A request message for
                Instances.SetMinCpuPlatform. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setMinCpuPlatform",
                    "body": "instances_set_min_cpu_platform_request_resource",
                },
            ]

            request_kwargs = compute.SetMinCpuPlatformInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstancesSetMinCpuPlatformRequest.to_json(
                compute.InstancesSetMinCpuPlatformRequest(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetMinCpuPlatformInstanceRequest.to_json(
                    compute.SetMinCpuPlatformInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetScheduling(InstancesRestStub):
        def __hash__(self):
            return hash("SetScheduling")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetSchedulingInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set scheduling method over HTTP.

            Args:
                request (~.compute.SetSchedulingInstanceRequest):
                    The request object. A request message for
                Instances.SetScheduling. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setScheduling",
                    "body": "scheduling_resource",
                },
            ]

            request_kwargs = compute.SetSchedulingInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.Scheduling.to_json(
                compute.Scheduling(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetSchedulingInstanceRequest.to_json(
                    compute.SetSchedulingInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetServiceAccount(InstancesRestStub):
        def __hash__(self):
            return hash("SetServiceAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetServiceAccountInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set service account method over HTTP.

            Args:
                request (~.compute.SetServiceAccountInstanceRequest):
                    The request object. A request message for
                Instances.SetServiceAccount. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setServiceAccount",
                    "body": "instances_set_service_account_request_resource",
                },
            ]

            request_kwargs = compute.SetServiceAccountInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstancesSetServiceAccountRequest.to_json(
                compute.InstancesSetServiceAccountRequest(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetServiceAccountInstanceRequest.to_json(
                    compute.SetServiceAccountInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetShieldedInstanceIntegrityPolicy(InstancesRestStub):
        def __hash__(self):
            return hash("SetShieldedInstanceIntegrityPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetShieldedInstanceIntegrityPolicyInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set shielded instance
        integrity policy method over HTTP.

            Args:
                request (~.compute.SetShieldedInstanceIntegrityPolicyInstanceRequest):
                    The request object. A request message for
                Instances.SetShieldedInstanceIntegrityPolicy.
                See the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "patch",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setShieldedInstanceIntegrityPolicy",
                    "body": "shielded_instance_integrity_policy_resource",
                },
            ]

            request_kwargs = compute.SetShieldedInstanceIntegrityPolicyInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.ShieldedInstanceIntegrityPolicy.to_json(
                compute.ShieldedInstanceIntegrityPolicy(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetShieldedInstanceIntegrityPolicyInstanceRequest.to_json(
                    compute.SetShieldedInstanceIntegrityPolicyInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SetTags(InstancesRestStub):
        def __hash__(self):
            return hash("SetTags")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SetTagsInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set tags method over HTTP.

            Args:
                request (~.compute.SetTagsInstanceRequest):
                    The request object. A request message for
                Instances.SetTags. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setTags",
                    "body": "tags_resource",
                },
            ]

            request_kwargs = compute.SetTagsInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.Tags.to_json(
                compute.Tags(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SetTagsInstanceRequest.to_json(
                    compute.SetTagsInstanceRequest(transcoded_request["query_params"]),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _SimulateMaintenanceEvent(InstancesRestStub):
        def __hash__(self):
            return hash("SimulateMaintenanceEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.SimulateMaintenanceEventInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the simulate maintenance
        event method over HTTP.

            Args:
                request (~.compute.SimulateMaintenanceEventInstanceRequest):
                    The request object. A request message for
                Instances.SimulateMaintenanceEvent. See
                the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/simulateMaintenanceEvent",
                },
            ]

            request_kwargs = compute.SimulateMaintenanceEventInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.SimulateMaintenanceEventInstanceRequest.to_json(
                    compute.SimulateMaintenanceEventInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _Start(InstancesRestStub):
        def __hash__(self):
            return hash("Start")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.StartInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the start method over HTTP.

            Args:
                request (~.compute.StartInstanceRequest):
                    The request object. A request message for
                Instances.Start. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/start",
                },
            ]

            request_kwargs = compute.StartInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.StartInstanceRequest.to_json(
                    compute.StartInstanceRequest(transcoded_request["query_params"]),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _StartWithEncryptionKey(InstancesRestStub):
        def __hash__(self):
            return hash("StartWithEncryptionKey")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.StartWithEncryptionKeyInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the start with encryption key method over HTTP.

            Args:
                request (~.compute.StartWithEncryptionKeyInstanceRequest):
                    The request object. A request message for
                Instances.StartWithEncryptionKey. See
                the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/startWithEncryptionKey",
                    "body": "instances_start_with_encryption_key_request_resource",
                },
            ]

            request_kwargs = compute.StartWithEncryptionKeyInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.InstancesStartWithEncryptionKeyRequest.to_json(
                compute.InstancesStartWithEncryptionKeyRequest(
                    transcoded_request["body"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.StartWithEncryptionKeyInstanceRequest.to_json(
                    compute.StartWithEncryptionKeyInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _Stop(InstancesRestStub):
        def __hash__(self):
            return hash("Stop")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.StopInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the stop method over HTTP.

            Args:
                request (~.compute.StopInstanceRequest):
                    The request object. A request message for Instances.Stop.
                See the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/stop",
                },
            ]

            request_kwargs = compute.StopInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.StopInstanceRequest.to_json(
                    compute.StopInstanceRequest(transcoded_request["query_params"]),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _TestIamPermissions(InstancesRestStub):
        def __hash__(self):
            return hash("TestIamPermissions")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.TestIamPermissionsInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.TestPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.compute.TestIamPermissionsInstanceRequest):
                    The request object. A request message for
                Instances.TestIamPermissions. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TestPermissionsResponse:

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{resource}/testIamPermissions",
                    "body": "test_permissions_request_resource",
                },
            ]

            request_kwargs = compute.TestIamPermissionsInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.TestPermissionsRequest.to_json(
                compute.TestPermissionsRequest(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.TestIamPermissionsInstanceRequest.to_json(
                    compute.TestIamPermissionsInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.TestPermissionsResponse.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _Update(InstancesRestStub):
        def __hash__(self):
            return hash("Update")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.UpdateInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the update method over HTTP.

            Args:
                request (~.compute.UpdateInstanceRequest):
                    The request object. A request message for
                Instances.Update. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "put",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}",
                    "body": "instance_resource",
                },
            ]

            request_kwargs = compute.UpdateInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.Instance.to_json(
                compute.Instance(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.UpdateInstanceRequest.to_json(
                    compute.UpdateInstanceRequest(transcoded_request["query_params"]),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _UpdateAccessConfig(InstancesRestStub):
        def __hash__(self):
            return hash("UpdateAccessConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {
            "networkInterface": "",
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
            request: compute.UpdateAccessConfigInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the update access config method over HTTP.

            Args:
                request (~.compute.UpdateAccessConfigInstanceRequest):
                    The request object. A request message for
                Instances.UpdateAccessConfig. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "post",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/updateAccessConfig",
                    "body": "access_config_resource",
                },
            ]

            request_kwargs = compute.UpdateAccessConfigInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.AccessConfig.to_json(
                compute.AccessConfig(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.UpdateAccessConfigInstanceRequest.to_json(
                    compute.UpdateAccessConfigInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _UpdateDisplayDevice(InstancesRestStub):
        def __hash__(self):
            return hash("UpdateDisplayDevice")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.UpdateDisplayDeviceInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the update display device method over HTTP.

            Args:
                request (~.compute.UpdateDisplayDeviceInstanceRequest):
                    The request object. A request message for
                Instances.UpdateDisplayDevice. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "patch",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/updateDisplayDevice",
                    "body": "display_device_resource",
                },
            ]

            request_kwargs = compute.UpdateDisplayDeviceInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.DisplayDevice.to_json(
                compute.DisplayDevice(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.UpdateDisplayDeviceInstanceRequest.to_json(
                    compute.UpdateDisplayDeviceInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _UpdateNetworkInterface(InstancesRestStub):
        def __hash__(self):
            return hash("UpdateNetworkInterface")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {
            "networkInterface": "",
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
            request: compute.UpdateNetworkInterfaceInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the update network interface method over HTTP.

            Args:
                request (~.compute.UpdateNetworkInterfaceInstanceRequest):
                    The request object. A request message for
                Instances.UpdateNetworkInterface. See
                the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "patch",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/updateNetworkInterface",
                    "body": "network_interface_resource",
                },
            ]

            request_kwargs = compute.UpdateNetworkInterfaceInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.NetworkInterface.to_json(
                compute.NetworkInterface(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.UpdateNetworkInterfaceInstanceRequest.to_json(
                    compute.UpdateNetworkInterfaceInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    class _UpdateShieldedInstanceConfig(InstancesRestStub):
        def __hash__(self):
            return hash("UpdateShieldedInstanceConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: compute.UpdateShieldedInstanceConfigInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the update shielded instance
        config method over HTTP.

            Args:
                request (~.compute.UpdateShieldedInstanceConfigInstanceRequest):
                    The request object. A request message for
                Instances.UpdateShieldedInstanceConfig.
                See the method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

            """

            http_options = [
                {
                    "method": "patch",
                    "uri": "/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/updateShieldedInstanceConfig",
                    "body": "shielded_instance_config_resource",
                },
            ]

            request_kwargs = compute.UpdateShieldedInstanceConfigInstanceRequest.to_dict(
                request
            )
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.ShieldedInstanceConfig.to_json(
                compute.ShieldedInstanceConfig(transcoded_request["body"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                compute.UpdateShieldedInstanceConfigInstanceRequest.to_json(
                    compute.UpdateShieldedInstanceConfigInstanceRequest(
                        transcoded_request["query_params"]
                    ),
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                # Replace with proper schema configuration (http/https) logic
                "https://{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)
            # Return the response
            return compute.Operation.from_json(
                response.content, ignore_unknown_fields=True
            )

    @property
    def add_access_config(
        self,
    ) -> Callable[[compute.AddAccessConfigInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("add_access_config")
        if not stub:
            stub = self._STUBS["add_access_config"] = self._AddAccessConfig(
                self._session, self._host
            )

        return stub

    @property
    def add_resource_policies(
        self,
    ) -> Callable[[compute.AddResourcePoliciesInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("add_resource_policies")
        if not stub:
            stub = self._STUBS["add_resource_policies"] = self._AddResourcePolicies(
                self._session, self._host
            )

        return stub

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListInstancesRequest], compute.InstanceAggregatedList
    ]:
        stub = self._STUBS.get("aggregated_list")
        if not stub:
            stub = self._STUBS["aggregated_list"] = self._AggregatedList(
                self._session, self._host
            )

        return stub

    @property
    def attach_disk(
        self,
    ) -> Callable[[compute.AttachDiskInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("attach_disk")
        if not stub:
            stub = self._STUBS["attach_disk"] = self._AttachDisk(
                self._session, self._host
            )

        return stub

    @property
    def bulk_insert(
        self,
    ) -> Callable[[compute.BulkInsertInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("bulk_insert")
        if not stub:
            stub = self._STUBS["bulk_insert"] = self._BulkInsert(
                self._session, self._host
            )

        return stub

    @property
    def delete(self) -> Callable[[compute.DeleteInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("delete")
        if not stub:
            stub = self._STUBS["delete"] = self._Delete(self._session, self._host)

        return stub

    @property
    def delete_access_config(
        self,
    ) -> Callable[[compute.DeleteAccessConfigInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("delete_access_config")
        if not stub:
            stub = self._STUBS["delete_access_config"] = self._DeleteAccessConfig(
                self._session, self._host
            )

        return stub

    @property
    def detach_disk(
        self,
    ) -> Callable[[compute.DetachDiskInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("detach_disk")
        if not stub:
            stub = self._STUBS["detach_disk"] = self._DetachDisk(
                self._session, self._host
            )

        return stub

    @property
    def get(self) -> Callable[[compute.GetInstanceRequest], compute.Instance]:
        stub = self._STUBS.get("get")
        if not stub:
            stub = self._STUBS["get"] = self._Get(self._session, self._host)

        return stub

    @property
    def get_effective_firewalls(
        self,
    ) -> Callable[
        [compute.GetEffectiveFirewallsInstanceRequest],
        compute.InstancesGetEffectiveFirewallsResponse,
    ]:
        stub = self._STUBS.get("get_effective_firewalls")
        if not stub:
            stub = self._STUBS["get_effective_firewalls"] = self._GetEffectiveFirewalls(
                self._session, self._host
            )

        return stub

    @property
    def get_guest_attributes(
        self,
    ) -> Callable[[compute.GetGuestAttributesInstanceRequest], compute.GuestAttributes]:
        stub = self._STUBS.get("get_guest_attributes")
        if not stub:
            stub = self._STUBS["get_guest_attributes"] = self._GetGuestAttributes(
                self._session, self._host
            )

        return stub

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[compute.GetIamPolicyInstanceRequest], compute.Policy]:
        stub = self._STUBS.get("get_iam_policy")
        if not stub:
            stub = self._STUBS["get_iam_policy"] = self._GetIamPolicy(
                self._session, self._host
            )

        return stub

    @property
    def get_screenshot(
        self,
    ) -> Callable[[compute.GetScreenshotInstanceRequest], compute.Screenshot]:
        stub = self._STUBS.get("get_screenshot")
        if not stub:
            stub = self._STUBS["get_screenshot"] = self._GetScreenshot(
                self._session, self._host
            )

        return stub

    @property
    def get_serial_port_output(
        self,
    ) -> Callable[
        [compute.GetSerialPortOutputInstanceRequest], compute.SerialPortOutput
    ]:
        stub = self._STUBS.get("get_serial_port_output")
        if not stub:
            stub = self._STUBS["get_serial_port_output"] = self._GetSerialPortOutput(
                self._session, self._host
            )

        return stub

    @property
    def get_shielded_instance_identity(
        self,
    ) -> Callable[
        [compute.GetShieldedInstanceIdentityInstanceRequest],
        compute.ShieldedInstanceIdentity,
    ]:
        stub = self._STUBS.get("get_shielded_instance_identity")
        if not stub:
            stub = self._STUBS[
                "get_shielded_instance_identity"
            ] = self._GetShieldedInstanceIdentity(self._session, self._host)

        return stub

    @property
    def insert(self) -> Callable[[compute.InsertInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("insert")
        if not stub:
            stub = self._STUBS["insert"] = self._Insert(self._session, self._host)

        return stub

    @property
    def list(self) -> Callable[[compute.ListInstancesRequest], compute.InstanceList]:
        stub = self._STUBS.get("list")
        if not stub:
            stub = self._STUBS["list"] = self._List(self._session, self._host)

        return stub

    @property
    def list_referrers(
        self,
    ) -> Callable[
        [compute.ListReferrersInstancesRequest], compute.InstanceListReferrers
    ]:
        stub = self._STUBS.get("list_referrers")
        if not stub:
            stub = self._STUBS["list_referrers"] = self._ListReferrers(
                self._session, self._host
            )

        return stub

    @property
    def remove_resource_policies(
        self,
    ) -> Callable[[compute.RemoveResourcePoliciesInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("remove_resource_policies")
        if not stub:
            stub = self._STUBS[
                "remove_resource_policies"
            ] = self._RemoveResourcePolicies(self._session, self._host)

        return stub

    @property
    def reset(self) -> Callable[[compute.ResetInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("reset")
        if not stub:
            stub = self._STUBS["reset"] = self._Reset(self._session, self._host)

        return stub

    @property
    def send_diagnostic_interrupt(
        self,
    ) -> Callable[
        [compute.SendDiagnosticInterruptInstanceRequest],
        compute.SendDiagnosticInterruptInstanceResponse,
    ]:
        stub = self._STUBS.get("send_diagnostic_interrupt")
        if not stub:
            stub = self._STUBS[
                "send_diagnostic_interrupt"
            ] = self._SendDiagnosticInterrupt(self._session, self._host)

        return stub

    @property
    def set_deletion_protection(
        self,
    ) -> Callable[[compute.SetDeletionProtectionInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_deletion_protection")
        if not stub:
            stub = self._STUBS["set_deletion_protection"] = self._SetDeletionProtection(
                self._session, self._host
            )

        return stub

    @property
    def set_disk_auto_delete(
        self,
    ) -> Callable[[compute.SetDiskAutoDeleteInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_disk_auto_delete")
        if not stub:
            stub = self._STUBS["set_disk_auto_delete"] = self._SetDiskAutoDelete(
                self._session, self._host
            )

        return stub

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[compute.SetIamPolicyInstanceRequest], compute.Policy]:
        stub = self._STUBS.get("set_iam_policy")
        if not stub:
            stub = self._STUBS["set_iam_policy"] = self._SetIamPolicy(
                self._session, self._host
            )

        return stub

    @property
    def set_labels(
        self,
    ) -> Callable[[compute.SetLabelsInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_labels")
        if not stub:
            stub = self._STUBS["set_labels"] = self._SetLabels(
                self._session, self._host
            )

        return stub

    @property
    def set_machine_resources(
        self,
    ) -> Callable[[compute.SetMachineResourcesInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_machine_resources")
        if not stub:
            stub = self._STUBS["set_machine_resources"] = self._SetMachineResources(
                self._session, self._host
            )

        return stub

    @property
    def set_machine_type(
        self,
    ) -> Callable[[compute.SetMachineTypeInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_machine_type")
        if not stub:
            stub = self._STUBS["set_machine_type"] = self._SetMachineType(
                self._session, self._host
            )

        return stub

    @property
    def set_metadata(
        self,
    ) -> Callable[[compute.SetMetadataInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_metadata")
        if not stub:
            stub = self._STUBS["set_metadata"] = self._SetMetadata(
                self._session, self._host
            )

        return stub

    @property
    def set_min_cpu_platform(
        self,
    ) -> Callable[[compute.SetMinCpuPlatformInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_min_cpu_platform")
        if not stub:
            stub = self._STUBS["set_min_cpu_platform"] = self._SetMinCpuPlatform(
                self._session, self._host
            )

        return stub

    @property
    def set_scheduling(
        self,
    ) -> Callable[[compute.SetSchedulingInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_scheduling")
        if not stub:
            stub = self._STUBS["set_scheduling"] = self._SetScheduling(
                self._session, self._host
            )

        return stub

    @property
    def set_service_account(
        self,
    ) -> Callable[[compute.SetServiceAccountInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_service_account")
        if not stub:
            stub = self._STUBS["set_service_account"] = self._SetServiceAccount(
                self._session, self._host
            )

        return stub

    @property
    def set_shielded_instance_integrity_policy(
        self,
    ) -> Callable[
        [compute.SetShieldedInstanceIntegrityPolicyInstanceRequest], compute.Operation
    ]:
        stub = self._STUBS.get("set_shielded_instance_integrity_policy")
        if not stub:
            stub = self._STUBS[
                "set_shielded_instance_integrity_policy"
            ] = self._SetShieldedInstanceIntegrityPolicy(self._session, self._host)

        return stub

    @property
    def set_tags(self) -> Callable[[compute.SetTagsInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("set_tags")
        if not stub:
            stub = self._STUBS["set_tags"] = self._SetTags(self._session, self._host)

        return stub

    @property
    def simulate_maintenance_event(
        self,
    ) -> Callable[[compute.SimulateMaintenanceEventInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("simulate_maintenance_event")
        if not stub:
            stub = self._STUBS[
                "simulate_maintenance_event"
            ] = self._SimulateMaintenanceEvent(self._session, self._host)

        return stub

    @property
    def start(self) -> Callable[[compute.StartInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("start")
        if not stub:
            stub = self._STUBS["start"] = self._Start(self._session, self._host)

        return stub

    @property
    def start_with_encryption_key(
        self,
    ) -> Callable[[compute.StartWithEncryptionKeyInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("start_with_encryption_key")
        if not stub:
            stub = self._STUBS[
                "start_with_encryption_key"
            ] = self._StartWithEncryptionKey(self._session, self._host)

        return stub

    @property
    def stop(self) -> Callable[[compute.StopInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("stop")
        if not stub:
            stub = self._STUBS["stop"] = self._Stop(self._session, self._host)

        return stub

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [compute.TestIamPermissionsInstanceRequest], compute.TestPermissionsResponse
    ]:
        stub = self._STUBS.get("test_iam_permissions")
        if not stub:
            stub = self._STUBS["test_iam_permissions"] = self._TestIamPermissions(
                self._session, self._host
            )

        return stub

    @property
    def update(self) -> Callable[[compute.UpdateInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("update")
        if not stub:
            stub = self._STUBS["update"] = self._Update(self._session, self._host)

        return stub

    @property
    def update_access_config(
        self,
    ) -> Callable[[compute.UpdateAccessConfigInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("update_access_config")
        if not stub:
            stub = self._STUBS["update_access_config"] = self._UpdateAccessConfig(
                self._session, self._host
            )

        return stub

    @property
    def update_display_device(
        self,
    ) -> Callable[[compute.UpdateDisplayDeviceInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("update_display_device")
        if not stub:
            stub = self._STUBS["update_display_device"] = self._UpdateDisplayDevice(
                self._session, self._host
            )

        return stub

    @property
    def update_network_interface(
        self,
    ) -> Callable[[compute.UpdateNetworkInterfaceInstanceRequest], compute.Operation]:
        stub = self._STUBS.get("update_network_interface")
        if not stub:
            stub = self._STUBS[
                "update_network_interface"
            ] = self._UpdateNetworkInterface(self._session, self._host)

        return stub

    @property
    def update_shielded_instance_config(
        self,
    ) -> Callable[
        [compute.UpdateShieldedInstanceConfigInstanceRequest], compute.Operation
    ]:
        stub = self._STUBS.get("update_shielded_instance_config")
        if not stub:
            stub = self._STUBS[
                "update_shielded_instance_config"
            ] = self._UpdateShieldedInstanceConfig(self._session, self._host)

        return stub

    def close(self):
        self._session.close()


__all__ = ("InstancesRestTransport",)
