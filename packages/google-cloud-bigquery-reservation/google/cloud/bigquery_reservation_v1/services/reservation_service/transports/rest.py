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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.bigquery_reservation_v1.types import reservation as gcbr_reservation
from google.cloud.bigquery_reservation_v1.types import reservation

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import ReservationServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ReservationServiceRestInterceptor:
    """Interceptor for ReservationService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ReservationServiceRestTransport.

    .. code-block:: python
        class MyCustomReservationServiceInterceptor(ReservationServiceRestInterceptor):
            def pre_create_assignment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_assignment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_capacity_commitment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_capacity_commitment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_reservation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_reservation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_assignment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_capacity_commitment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_reservation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_bi_reservation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_bi_reservation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_capacity_commitment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_capacity_commitment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_reservation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_reservation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_assignments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_assignments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_capacity_commitments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_capacity_commitments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_reservations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_reservations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_merge_capacity_commitments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_merge_capacity_commitments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_move_assignment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_move_assignment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_all_assignments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_all_assignments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_assignments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_assignments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_split_capacity_commitment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_split_capacity_commitment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_assignment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_assignment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_bi_reservation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_bi_reservation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_capacity_commitment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_capacity_commitment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_reservation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_reservation(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ReservationServiceRestTransport(interceptor=MyCustomReservationServiceInterceptor())
        client = ReservationServiceClient(transport=transport)


    """

    def pre_create_assignment(
        self,
        request: reservation.CreateAssignmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.CreateAssignmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_assignment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_create_assignment(
        self, response: reservation.Assignment
    ) -> reservation.Assignment:
        """Post-rpc interceptor for create_assignment

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_create_capacity_commitment(
        self,
        request: reservation.CreateCapacityCommitmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.CreateCapacityCommitmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_capacity_commitment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_create_capacity_commitment(
        self, response: reservation.CapacityCommitment
    ) -> reservation.CapacityCommitment:
        """Post-rpc interceptor for create_capacity_commitment

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_create_reservation(
        self,
        request: gcbr_reservation.CreateReservationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcbr_reservation.CreateReservationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_reservation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_create_reservation(
        self, response: gcbr_reservation.Reservation
    ) -> gcbr_reservation.Reservation:
        """Post-rpc interceptor for create_reservation

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_assignment(
        self,
        request: reservation.DeleteAssignmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.DeleteAssignmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_assignment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def pre_delete_capacity_commitment(
        self,
        request: reservation.DeleteCapacityCommitmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.DeleteCapacityCommitmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_capacity_commitment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def pre_delete_reservation(
        self,
        request: reservation.DeleteReservationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.DeleteReservationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_reservation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def pre_get_bi_reservation(
        self,
        request: reservation.GetBiReservationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.GetBiReservationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_bi_reservation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_get_bi_reservation(
        self, response: reservation.BiReservation
    ) -> reservation.BiReservation:
        """Post-rpc interceptor for get_bi_reservation

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_capacity_commitment(
        self,
        request: reservation.GetCapacityCommitmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.GetCapacityCommitmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_capacity_commitment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_get_capacity_commitment(
        self, response: reservation.CapacityCommitment
    ) -> reservation.CapacityCommitment:
        """Post-rpc interceptor for get_capacity_commitment

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_get_reservation(
        self,
        request: reservation.GetReservationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.GetReservationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_reservation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_get_reservation(
        self, response: reservation.Reservation
    ) -> reservation.Reservation:
        """Post-rpc interceptor for get_reservation

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_assignments(
        self,
        request: reservation.ListAssignmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.ListAssignmentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_assignments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_list_assignments(
        self, response: reservation.ListAssignmentsResponse
    ) -> reservation.ListAssignmentsResponse:
        """Post-rpc interceptor for list_assignments

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_capacity_commitments(
        self,
        request: reservation.ListCapacityCommitmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.ListCapacityCommitmentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_capacity_commitments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_list_capacity_commitments(
        self, response: reservation.ListCapacityCommitmentsResponse
    ) -> reservation.ListCapacityCommitmentsResponse:
        """Post-rpc interceptor for list_capacity_commitments

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_list_reservations(
        self,
        request: reservation.ListReservationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.ListReservationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_reservations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_list_reservations(
        self, response: reservation.ListReservationsResponse
    ) -> reservation.ListReservationsResponse:
        """Post-rpc interceptor for list_reservations

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_merge_capacity_commitments(
        self,
        request: reservation.MergeCapacityCommitmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.MergeCapacityCommitmentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for merge_capacity_commitments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_merge_capacity_commitments(
        self, response: reservation.CapacityCommitment
    ) -> reservation.CapacityCommitment:
        """Post-rpc interceptor for merge_capacity_commitments

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_move_assignment(
        self,
        request: reservation.MoveAssignmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.MoveAssignmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for move_assignment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_move_assignment(
        self, response: reservation.Assignment
    ) -> reservation.Assignment:
        """Post-rpc interceptor for move_assignment

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_search_all_assignments(
        self,
        request: reservation.SearchAllAssignmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.SearchAllAssignmentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_all_assignments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_search_all_assignments(
        self, response: reservation.SearchAllAssignmentsResponse
    ) -> reservation.SearchAllAssignmentsResponse:
        """Post-rpc interceptor for search_all_assignments

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_search_assignments(
        self,
        request: reservation.SearchAssignmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.SearchAssignmentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_assignments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_search_assignments(
        self, response: reservation.SearchAssignmentsResponse
    ) -> reservation.SearchAssignmentsResponse:
        """Post-rpc interceptor for search_assignments

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_split_capacity_commitment(
        self,
        request: reservation.SplitCapacityCommitmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.SplitCapacityCommitmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for split_capacity_commitment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_split_capacity_commitment(
        self, response: reservation.SplitCapacityCommitmentResponse
    ) -> reservation.SplitCapacityCommitmentResponse:
        """Post-rpc interceptor for split_capacity_commitment

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_update_assignment(
        self,
        request: reservation.UpdateAssignmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.UpdateAssignmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_assignment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_update_assignment(
        self, response: reservation.Assignment
    ) -> reservation.Assignment:
        """Post-rpc interceptor for update_assignment

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_update_bi_reservation(
        self,
        request: reservation.UpdateBiReservationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.UpdateBiReservationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_bi_reservation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_update_bi_reservation(
        self, response: reservation.BiReservation
    ) -> reservation.BiReservation:
        """Post-rpc interceptor for update_bi_reservation

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_update_capacity_commitment(
        self,
        request: reservation.UpdateCapacityCommitmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[reservation.UpdateCapacityCommitmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_capacity_commitment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_update_capacity_commitment(
        self, response: reservation.CapacityCommitment
    ) -> reservation.CapacityCommitment:
        """Post-rpc interceptor for update_capacity_commitment

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response

    def pre_update_reservation(
        self,
        request: gcbr_reservation.UpdateReservationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcbr_reservation.UpdateReservationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_reservation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ReservationService server.
        """
        return request, metadata

    def post_update_reservation(
        self, response: gcbr_reservation.Reservation
    ) -> gcbr_reservation.Reservation:
        """Post-rpc interceptor for update_reservation

        Override in a subclass to manipulate the response
        after it is returned by the ReservationService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ReservationServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ReservationServiceRestInterceptor


class ReservationServiceRestTransport(ReservationServiceTransport):
    """REST backend transport for ReservationService.

    This API allows users to manage their BigQuery reservations.

    A reservation provides computational resource guarantees, in the
    form of `slots <https://cloud.google.com/bigquery/docs/slots>`__, to
    users. A slot is a unit of computational power in BigQuery, and
    serves as the basic unit of parallelism. In a scan of a
    multi-partitioned table, a single slot operates on a single
    partition of the table. A reservation resource exists as a child
    resource of the admin project and location, e.g.:
    ``projects/myproject/locations/US/reservations/reservationName``.

    A capacity commitment is a way to purchase compute capacity for
    BigQuery jobs (in the form of slots) with some committed period of
    usage. A capacity commitment resource exists as a child resource of
    the admin project and location, e.g.:
    ``projects/myproject/locations/US/capacityCommitments/id``.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "bigqueryreservation.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ReservationServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'bigqueryreservation.googleapis.com').
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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ReservationServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateAssignment(ReservationServiceRestStub):
        def __hash__(self):
            return hash("CreateAssignment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.CreateAssignmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.Assignment:
            r"""Call the create assignment method over HTTP.

            Args:
                request (~.reservation.CreateAssignmentRequest):
                    The request object. The request for
                [ReservationService.CreateAssignment][google.cloud.bigquery.reservation.v1.ReservationService.CreateAssignment].
                Note: "bigquery.reservationAssignments.create"
                permission is required on the related assignee.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.Assignment:
                    An assignment allows a project to
                submit jobs of a certain type using
                slots from the specified reservation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/reservations/*}/assignments",
                    "body": "assignment",
                },
            ]
            request, metadata = self._interceptor.pre_create_assignment(
                request, metadata
            )
            pb_request = reservation.CreateAssignmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.Assignment()
            pb_resp = reservation.Assignment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_assignment(resp)
            return resp

    class _CreateCapacityCommitment(ReservationServiceRestStub):
        def __hash__(self):
            return hash("CreateCapacityCommitment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.CreateCapacityCommitmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.CapacityCommitment:
            r"""Call the create capacity
            commitment method over HTTP.

                Args:
                    request (~.reservation.CreateCapacityCommitmentRequest):
                        The request object. The request for
                    [ReservationService.CreateCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.CreateCapacityCommitment].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.reservation.CapacityCommitment:
                        Capacity commitment is a way to
                    purchase compute capacity for BigQuery
                    jobs (in the form of slots) with some
                    committed period of usage. Annual
                    commitments renew by default.
                    Commitments can be removed after their
                    commitment end time passes.

                    In order to remove annual commitment,
                    its plan needs to be changed to monthly
                    or flex first.

                    A capacity commitment resource exists as
                    a child resource of the admin project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/capacityCommitments",
                    "body": "capacity_commitment",
                },
            ]
            request, metadata = self._interceptor.pre_create_capacity_commitment(
                request, metadata
            )
            pb_request = reservation.CreateCapacityCommitmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.CapacityCommitment()
            pb_resp = reservation.CapacityCommitment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_capacity_commitment(resp)
            return resp

    class _CreateReservation(ReservationServiceRestStub):
        def __hash__(self):
            return hash("CreateReservation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcbr_reservation.CreateReservationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcbr_reservation.Reservation:
            r"""Call the create reservation method over HTTP.

            Args:
                request (~.gcbr_reservation.CreateReservationRequest):
                    The request object. The request for
                [ReservationService.CreateReservation][google.cloud.bigquery.reservation.v1.ReservationService.CreateReservation].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcbr_reservation.Reservation:
                    A reservation is a mechanism used to
                guarantee slots to users.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/reservations",
                    "body": "reservation",
                },
            ]
            request, metadata = self._interceptor.pre_create_reservation(
                request, metadata
            )
            pb_request = gcbr_reservation.CreateReservationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = gcbr_reservation.Reservation()
            pb_resp = gcbr_reservation.Reservation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_reservation(resp)
            return resp

    class _DeleteAssignment(ReservationServiceRestStub):
        def __hash__(self):
            return hash("DeleteAssignment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.DeleteAssignmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete assignment method over HTTP.

            Args:
                request (~.reservation.DeleteAssignmentRequest):
                    The request object. The request for
                [ReservationService.DeleteAssignment][google.cloud.bigquery.reservation.v1.ReservationService.DeleteAssignment].
                Note: "bigquery.reservationAssignments.delete"
                permission is required on the related assignee.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/reservations/*/assignments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_assignment(
                request, metadata
            )
            pb_request = reservation.DeleteAssignmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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

    class _DeleteCapacityCommitment(ReservationServiceRestStub):
        def __hash__(self):
            return hash("DeleteCapacityCommitment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.DeleteCapacityCommitmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete capacity
            commitment method over HTTP.

                Args:
                    request (~.reservation.DeleteCapacityCommitmentRequest):
                        The request object. The request for
                    [ReservationService.DeleteCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.DeleteCapacityCommitment].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/capacityCommitments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_capacity_commitment(
                request, metadata
            )
            pb_request = reservation.DeleteCapacityCommitmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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

    class _DeleteReservation(ReservationServiceRestStub):
        def __hash__(self):
            return hash("DeleteReservation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.DeleteReservationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete reservation method over HTTP.

            Args:
                request (~.reservation.DeleteReservationRequest):
                    The request object. The request for
                [ReservationService.DeleteReservation][google.cloud.bigquery.reservation.v1.ReservationService.DeleteReservation].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/reservations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_reservation(
                request, metadata
            )
            pb_request = reservation.DeleteReservationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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

    class _GetBiReservation(ReservationServiceRestStub):
        def __hash__(self):
            return hash("GetBiReservation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.GetBiReservationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.BiReservation:
            r"""Call the get bi reservation method over HTTP.

            Args:
                request (~.reservation.GetBiReservationRequest):
                    The request object. A request to get a singleton BI
                reservation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.BiReservation:
                    Represents a BI Reservation.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/biReservation}",
                },
            ]
            request, metadata = self._interceptor.pre_get_bi_reservation(
                request, metadata
            )
            pb_request = reservation.GetBiReservationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.BiReservation()
            pb_resp = reservation.BiReservation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_bi_reservation(resp)
            return resp

    class _GetCapacityCommitment(ReservationServiceRestStub):
        def __hash__(self):
            return hash("GetCapacityCommitment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.GetCapacityCommitmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.CapacityCommitment:
            r"""Call the get capacity commitment method over HTTP.

            Args:
                request (~.reservation.GetCapacityCommitmentRequest):
                    The request object. The request for
                [ReservationService.GetCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.GetCapacityCommitment].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.CapacityCommitment:
                    Capacity commitment is a way to
                purchase compute capacity for BigQuery
                jobs (in the form of slots) with some
                committed period of usage. Annual
                commitments renew by default.
                Commitments can be removed after their
                commitment end time passes.

                In order to remove annual commitment,
                its plan needs to be changed to monthly
                or flex first.

                A capacity commitment resource exists as
                a child resource of the admin project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/capacityCommitments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_capacity_commitment(
                request, metadata
            )
            pb_request = reservation.GetCapacityCommitmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.CapacityCommitment()
            pb_resp = reservation.CapacityCommitment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_capacity_commitment(resp)
            return resp

    class _GetReservation(ReservationServiceRestStub):
        def __hash__(self):
            return hash("GetReservation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.GetReservationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.Reservation:
            r"""Call the get reservation method over HTTP.

            Args:
                request (~.reservation.GetReservationRequest):
                    The request object. The request for
                [ReservationService.GetReservation][google.cloud.bigquery.reservation.v1.ReservationService.GetReservation].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.Reservation:
                    A reservation is a mechanism used to
                guarantee slots to users.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/reservations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_reservation(request, metadata)
            pb_request = reservation.GetReservationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.Reservation()
            pb_resp = reservation.Reservation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_reservation(resp)
            return resp

    class _ListAssignments(ReservationServiceRestStub):
        def __hash__(self):
            return hash("ListAssignments")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.ListAssignmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.ListAssignmentsResponse:
            r"""Call the list assignments method over HTTP.

            Args:
                request (~.reservation.ListAssignmentsRequest):
                    The request object. The request for
                [ReservationService.ListAssignments][google.cloud.bigquery.reservation.v1.ReservationService.ListAssignments].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.ListAssignmentsResponse:
                    The response for
                [ReservationService.ListAssignments][google.cloud.bigquery.reservation.v1.ReservationService.ListAssignments].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/reservations/*}/assignments",
                },
            ]
            request, metadata = self._interceptor.pre_list_assignments(
                request, metadata
            )
            pb_request = reservation.ListAssignmentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.ListAssignmentsResponse()
            pb_resp = reservation.ListAssignmentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_assignments(resp)
            return resp

    class _ListCapacityCommitments(ReservationServiceRestStub):
        def __hash__(self):
            return hash("ListCapacityCommitments")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.ListCapacityCommitmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.ListCapacityCommitmentsResponse:
            r"""Call the list capacity commitments method over HTTP.

            Args:
                request (~.reservation.ListCapacityCommitmentsRequest):
                    The request object. The request for
                [ReservationService.ListCapacityCommitments][google.cloud.bigquery.reservation.v1.ReservationService.ListCapacityCommitments].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.ListCapacityCommitmentsResponse:
                    The response for
                [ReservationService.ListCapacityCommitments][google.cloud.bigquery.reservation.v1.ReservationService.ListCapacityCommitments].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/capacityCommitments",
                },
            ]
            request, metadata = self._interceptor.pre_list_capacity_commitments(
                request, metadata
            )
            pb_request = reservation.ListCapacityCommitmentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.ListCapacityCommitmentsResponse()
            pb_resp = reservation.ListCapacityCommitmentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_capacity_commitments(resp)
            return resp

    class _ListReservations(ReservationServiceRestStub):
        def __hash__(self):
            return hash("ListReservations")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.ListReservationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.ListReservationsResponse:
            r"""Call the list reservations method over HTTP.

            Args:
                request (~.reservation.ListReservationsRequest):
                    The request object. The request for
                [ReservationService.ListReservations][google.cloud.bigquery.reservation.v1.ReservationService.ListReservations].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.ListReservationsResponse:
                    The response for
                [ReservationService.ListReservations][google.cloud.bigquery.reservation.v1.ReservationService.ListReservations].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/reservations",
                },
            ]
            request, metadata = self._interceptor.pre_list_reservations(
                request, metadata
            )
            pb_request = reservation.ListReservationsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.ListReservationsResponse()
            pb_resp = reservation.ListReservationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_reservations(resp)
            return resp

    class _MergeCapacityCommitments(ReservationServiceRestStub):
        def __hash__(self):
            return hash("MergeCapacityCommitments")

        def __call__(
            self,
            request: reservation.MergeCapacityCommitmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.CapacityCommitment:
            r"""Call the merge capacity
            commitments method over HTTP.

                Args:
                    request (~.reservation.MergeCapacityCommitmentsRequest):
                        The request object. The request for
                    [ReservationService.MergeCapacityCommitments][google.cloud.bigquery.reservation.v1.ReservationService.MergeCapacityCommitments].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.reservation.CapacityCommitment:
                        Capacity commitment is a way to
                    purchase compute capacity for BigQuery
                    jobs (in the form of slots) with some
                    committed period of usage. Annual
                    commitments renew by default.
                    Commitments can be removed after their
                    commitment end time passes.

                    In order to remove annual commitment,
                    its plan needs to be changed to monthly
                    or flex first.

                    A capacity commitment resource exists as
                    a child resource of the admin project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/capacityCommitments:merge",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_merge_capacity_commitments(
                request, metadata
            )
            pb_request = reservation.MergeCapacityCommitmentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.CapacityCommitment()
            pb_resp = reservation.CapacityCommitment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_merge_capacity_commitments(resp)
            return resp

    class _MoveAssignment(ReservationServiceRestStub):
        def __hash__(self):
            return hash("MoveAssignment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.MoveAssignmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.Assignment:
            r"""Call the move assignment method over HTTP.

            Args:
                request (~.reservation.MoveAssignmentRequest):
                    The request object. The request for
                [ReservationService.MoveAssignment][google.cloud.bigquery.reservation.v1.ReservationService.MoveAssignment].

                **Note**: "bigquery.reservationAssignments.create"
                permission is required on the destination_id.

                **Note**: "bigquery.reservationAssignments.create" and
                "bigquery.reservationAssignments.delete" permission are
                required on the related assignee.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.Assignment:
                    An assignment allows a project to
                submit jobs of a certain type using
                slots from the specified reservation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/reservations/*/assignments/*}:move",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_move_assignment(request, metadata)
            pb_request = reservation.MoveAssignmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.Assignment()
            pb_resp = reservation.Assignment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_move_assignment(resp)
            return resp

    class _SearchAllAssignments(ReservationServiceRestStub):
        def __hash__(self):
            return hash("SearchAllAssignments")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.SearchAllAssignmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.SearchAllAssignmentsResponse:
            r"""Call the search all assignments method over HTTP.

            Args:
                request (~.reservation.SearchAllAssignmentsRequest):
                    The request object. The request for
                [ReservationService.SearchAllAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAllAssignments].
                Note: "bigquery.reservationAssignments.search"
                permission is required on the related assignee.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.SearchAllAssignmentsResponse:
                    The response for
                [ReservationService.SearchAllAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAllAssignments].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}:searchAllAssignments",
                },
            ]
            request, metadata = self._interceptor.pre_search_all_assignments(
                request, metadata
            )
            pb_request = reservation.SearchAllAssignmentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.SearchAllAssignmentsResponse()
            pb_resp = reservation.SearchAllAssignmentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_all_assignments(resp)
            return resp

    class _SearchAssignments(ReservationServiceRestStub):
        def __hash__(self):
            return hash("SearchAssignments")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.SearchAssignmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.SearchAssignmentsResponse:
            r"""Call the search assignments method over HTTP.

            Args:
                request (~.reservation.SearchAssignmentsRequest):
                    The request object. The request for
                [ReservationService.SearchAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAssignments].
                Note: "bigquery.reservationAssignments.search"
                permission is required on the related assignee.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.SearchAssignmentsResponse:
                    The response for
                [ReservationService.SearchAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAssignments].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}:searchAssignments",
                },
            ]
            request, metadata = self._interceptor.pre_search_assignments(
                request, metadata
            )
            pb_request = reservation.SearchAssignmentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.SearchAssignmentsResponse()
            pb_resp = reservation.SearchAssignmentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_assignments(resp)
            return resp

    class _SplitCapacityCommitment(ReservationServiceRestStub):
        def __hash__(self):
            return hash("SplitCapacityCommitment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: reservation.SplitCapacityCommitmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.SplitCapacityCommitmentResponse:
            r"""Call the split capacity commitment method over HTTP.

            Args:
                request (~.reservation.SplitCapacityCommitmentRequest):
                    The request object. The request for
                [ReservationService.SplitCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.SplitCapacityCommitment].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.SplitCapacityCommitmentResponse:
                    The response for
                [ReservationService.SplitCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.SplitCapacityCommitment].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/capacityCommitments/*}:split",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_split_capacity_commitment(
                request, metadata
            )
            pb_request = reservation.SplitCapacityCommitmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.SplitCapacityCommitmentResponse()
            pb_resp = reservation.SplitCapacityCommitmentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_split_capacity_commitment(resp)
            return resp

    class _UpdateAssignment(ReservationServiceRestStub):
        def __hash__(self):
            return hash("UpdateAssignment")

        def __call__(
            self,
            request: reservation.UpdateAssignmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.Assignment:
            r"""Call the update assignment method over HTTP.

            Args:
                request (~.reservation.UpdateAssignmentRequest):
                    The request object. The request for
                [ReservationService.UpdateAssignment][google.cloud.bigquery.reservation.v1.ReservationService.UpdateAssignment].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.Assignment:
                    An assignment allows a project to
                submit jobs of a certain type using
                slots from the specified reservation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{assignment.name=projects/*/locations/*/reservations/*/assignments/*}",
                    "body": "assignment",
                },
            ]
            request, metadata = self._interceptor.pre_update_assignment(
                request, metadata
            )
            pb_request = reservation.UpdateAssignmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.Assignment()
            pb_resp = reservation.Assignment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_assignment(resp)
            return resp

    class _UpdateBiReservation(ReservationServiceRestStub):
        def __hash__(self):
            return hash("UpdateBiReservation")

        def __call__(
            self,
            request: reservation.UpdateBiReservationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.BiReservation:
            r"""Call the update bi reservation method over HTTP.

            Args:
                request (~.reservation.UpdateBiReservationRequest):
                    The request object. A request to update a BI reservation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.reservation.BiReservation:
                    Represents a BI Reservation.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{bi_reservation.name=projects/*/locations/*/biReservation}",
                    "body": "bi_reservation",
                },
            ]
            request, metadata = self._interceptor.pre_update_bi_reservation(
                request, metadata
            )
            pb_request = reservation.UpdateBiReservationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.BiReservation()
            pb_resp = reservation.BiReservation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_bi_reservation(resp)
            return resp

    class _UpdateCapacityCommitment(ReservationServiceRestStub):
        def __hash__(self):
            return hash("UpdateCapacityCommitment")

        def __call__(
            self,
            request: reservation.UpdateCapacityCommitmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> reservation.CapacityCommitment:
            r"""Call the update capacity
            commitment method over HTTP.

                Args:
                    request (~.reservation.UpdateCapacityCommitmentRequest):
                        The request object. The request for
                    [ReservationService.UpdateCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.UpdateCapacityCommitment].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.reservation.CapacityCommitment:
                        Capacity commitment is a way to
                    purchase compute capacity for BigQuery
                    jobs (in the form of slots) with some
                    committed period of usage. Annual
                    commitments renew by default.
                    Commitments can be removed after their
                    commitment end time passes.

                    In order to remove annual commitment,
                    its plan needs to be changed to monthly
                    or flex first.

                    A capacity commitment resource exists as
                    a child resource of the admin project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{capacity_commitment.name=projects/*/locations/*/capacityCommitments/*}",
                    "body": "capacity_commitment",
                },
            ]
            request, metadata = self._interceptor.pre_update_capacity_commitment(
                request, metadata
            )
            pb_request = reservation.UpdateCapacityCommitmentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = reservation.CapacityCommitment()
            pb_resp = reservation.CapacityCommitment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_capacity_commitment(resp)
            return resp

    class _UpdateReservation(ReservationServiceRestStub):
        def __hash__(self):
            return hash("UpdateReservation")

        def __call__(
            self,
            request: gcbr_reservation.UpdateReservationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcbr_reservation.Reservation:
            r"""Call the update reservation method over HTTP.

            Args:
                request (~.gcbr_reservation.UpdateReservationRequest):
                    The request object. The request for
                [ReservationService.UpdateReservation][google.cloud.bigquery.reservation.v1.ReservationService.UpdateReservation].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcbr_reservation.Reservation:
                    A reservation is a mechanism used to
                guarantee slots to users.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{reservation.name=projects/*/locations/*/reservations/*}",
                    "body": "reservation",
                },
            ]
            request, metadata = self._interceptor.pre_update_reservation(
                request, metadata
            )
            pb_request = gcbr_reservation.UpdateReservationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = gcbr_reservation.Reservation()
            pb_resp = gcbr_reservation.Reservation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_reservation(resp)
            return resp

    @property
    def create_assignment(
        self,
    ) -> Callable[[reservation.CreateAssignmentRequest], reservation.Assignment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAssignment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_capacity_commitment(
        self,
    ) -> Callable[
        [reservation.CreateCapacityCommitmentRequest], reservation.CapacityCommitment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCapacityCommitment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_reservation(
        self,
    ) -> Callable[
        [gcbr_reservation.CreateReservationRequest], gcbr_reservation.Reservation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReservation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_assignment(
        self,
    ) -> Callable[[reservation.DeleteAssignmentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAssignment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_capacity_commitment(
        self,
    ) -> Callable[[reservation.DeleteCapacityCommitmentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCapacityCommitment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_reservation(
        self,
    ) -> Callable[[reservation.DeleteReservationRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteReservation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_bi_reservation(
        self,
    ) -> Callable[[reservation.GetBiReservationRequest], reservation.BiReservation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBiReservation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_capacity_commitment(
        self,
    ) -> Callable[
        [reservation.GetCapacityCommitmentRequest], reservation.CapacityCommitment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCapacityCommitment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_reservation(
        self,
    ) -> Callable[[reservation.GetReservationRequest], reservation.Reservation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReservation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_assignments(
        self,
    ) -> Callable[
        [reservation.ListAssignmentsRequest], reservation.ListAssignmentsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAssignments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_capacity_commitments(
        self,
    ) -> Callable[
        [reservation.ListCapacityCommitmentsRequest],
        reservation.ListCapacityCommitmentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCapacityCommitments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_reservations(
        self,
    ) -> Callable[
        [reservation.ListReservationsRequest], reservation.ListReservationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReservations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def merge_capacity_commitments(
        self,
    ) -> Callable[
        [reservation.MergeCapacityCommitmentsRequest], reservation.CapacityCommitment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MergeCapacityCommitments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def move_assignment(
        self,
    ) -> Callable[[reservation.MoveAssignmentRequest], reservation.Assignment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MoveAssignment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_all_assignments(
        self,
    ) -> Callable[
        [reservation.SearchAllAssignmentsRequest],
        reservation.SearchAllAssignmentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchAllAssignments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_assignments(
        self,
    ) -> Callable[
        [reservation.SearchAssignmentsRequest], reservation.SearchAssignmentsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchAssignments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def split_capacity_commitment(
        self,
    ) -> Callable[
        [reservation.SplitCapacityCommitmentRequest],
        reservation.SplitCapacityCommitmentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SplitCapacityCommitment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_assignment(
        self,
    ) -> Callable[[reservation.UpdateAssignmentRequest], reservation.Assignment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAssignment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_bi_reservation(
        self,
    ) -> Callable[[reservation.UpdateBiReservationRequest], reservation.BiReservation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBiReservation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_capacity_commitment(
        self,
    ) -> Callable[
        [reservation.UpdateCapacityCommitmentRequest], reservation.CapacityCommitment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCapacityCommitment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_reservation(
        self,
    ) -> Callable[
        [gcbr_reservation.UpdateReservationRequest], gcbr_reservation.Reservation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateReservation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ReservationServiceRestTransport",)
