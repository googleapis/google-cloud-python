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
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dialogflow_v2.services.answer_records import pagers
from google.cloud.dialogflow_v2.types import answer_record
from google.cloud.dialogflow_v2.types import answer_record as gcd_answer_record
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import AnswerRecordsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AnswerRecordsGrpcAsyncIOTransport
from .client import AnswerRecordsClient


class AnswerRecordsAsyncClient:
    """Service for managing
    [AnswerRecords][google.cloud.dialogflow.v2.AnswerRecord].
    """

    _client: AnswerRecordsClient

    DEFAULT_ENDPOINT = AnswerRecordsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AnswerRecordsClient.DEFAULT_MTLS_ENDPOINT

    answer_record_path = staticmethod(AnswerRecordsClient.answer_record_path)
    parse_answer_record_path = staticmethod(
        AnswerRecordsClient.parse_answer_record_path
    )
    common_billing_account_path = staticmethod(
        AnswerRecordsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AnswerRecordsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AnswerRecordsClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AnswerRecordsClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AnswerRecordsClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AnswerRecordsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AnswerRecordsClient.common_project_path)
    parse_common_project_path = staticmethod(
        AnswerRecordsClient.parse_common_project_path
    )
    common_location_path = staticmethod(AnswerRecordsClient.common_location_path)
    parse_common_location_path = staticmethod(
        AnswerRecordsClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AnswerRecordsAsyncClient: The constructed client.
        """
        return AnswerRecordsClient.from_service_account_info.__func__(AnswerRecordsAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AnswerRecordsAsyncClient: The constructed client.
        """
        return AnswerRecordsClient.from_service_account_file.__func__(AnswerRecordsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AnswerRecordsTransport:
        """Returns the transport used by the client instance.

        Returns:
            AnswerRecordsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AnswerRecordsClient).get_transport_class, type(AnswerRecordsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, AnswerRecordsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the answer records client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AnswerRecordsTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = AnswerRecordsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_answer_records(
        self,
        request: answer_record.ListAnswerRecordsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAnswerRecordsAsyncPager:
        r"""Returns the list of all answer records in the
        specified project in reverse chronological order.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.ListAnswerRecordsRequest`):
                The request object. Request message for
                [AnswerRecords.ListAnswerRecords][google.cloud.dialogflow.v2.AnswerRecords.ListAnswerRecords].
            parent (:class:`str`):
                Required. The project to list all answer records for in
                reverse chronological order. Format:
                ``projects/<Project ID>/locations/<Location ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.services.answer_records.pagers.ListAnswerRecordsAsyncPager:
                Response message for
                [AnswerRecords.ListAnswerRecords][google.cloud.dialogflow.v2.AnswerRecords.ListAnswerRecords].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = answer_record.ListAnswerRecordsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_answer_records,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListAnswerRecordsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_answer_record(
        self,
        request: gcd_answer_record.UpdateAnswerRecordRequest = None,
        *,
        answer_record: gcd_answer_record.AnswerRecord = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_answer_record.AnswerRecord:
        r"""Updates the specified answer record.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.UpdateAnswerRecordRequest`):
                The request object. Request message for
                [AnswerRecords.UpdateAnswerRecord][google.cloud.dialogflow.v2.AnswerRecords.UpdateAnswerRecord].
            answer_record (:class:`google.cloud.dialogflow_v2.types.AnswerRecord`):
                Required. Answer record to update.
                This corresponds to the ``answer_record`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to control which
                fields get updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.AnswerRecord:
                Answer records are records to manage answer history and feedbacks for
                   Dialogflow.

                   Currently, answer record includes:

                   -  human agent assistant article suggestion
                   -  human agent assistant faq article

                   It doesn't include:

                   -  DetectIntent intent matching
                   -  DetectIntent knowledge

                   Answer records are not related to the conversation
                   history in the Dialogflow Console. A Record is
                   generated even when the end-user disables
                   conversation history in the console. Records are
                   created when there's a human agent assistant
                   suggestion generated.

                   A typical workflow for customers provide feedback to
                   an answer is:

                   1. For human agent assistant, customers get
                      suggestion via ListSuggestions API. Together with
                      the answers,
                      [AnswerRecord.name][google.cloud.dialogflow.v2.AnswerRecord.name]
                      are returned to the customers.
                   2. The customer uses the
                      [AnswerRecord.name][google.cloud.dialogflow.v2.AnswerRecord.name]
                      to call the [UpdateAnswerRecord][] method to send
                      feedback about a specific answer that they believe
                      is wrong.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([answer_record, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_answer_record.UpdateAnswerRecordRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if answer_record is not None:
            request.answer_record = answer_record
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_answer_record,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("answer_record.name", request.answer_record.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AnswerRecordsAsyncClient",)
