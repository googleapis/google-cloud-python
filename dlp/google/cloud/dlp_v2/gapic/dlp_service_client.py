# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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
"""Accesses the google.privacy.dlp.v2 DlpService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.cloud.dlp_v2.gapic import dlp_service_client_config
from google.cloud.dlp_v2.gapic import enums
from google.cloud.dlp_v2.gapic.transports import dlp_service_grpc_transport
from google.cloud.dlp_v2.proto import dlp_pb2
from google.cloud.dlp_v2.proto import dlp_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-dlp', ).version


class DlpServiceClient(object):
    """
    The Cloud Data Loss Prevention (DLP) API is a service that allows clients
    to detect the presence of Personally Identifiable Information (PII) and other
    privacy-sensitive data in user-supplied, unstructured data streams, like text
    blocks or images.
    The service also includes methods for sensitive data redaction and
    scheduling of data scans on Google Cloud Platform based data sets.

    To learn more about concepts and find how-to guides see
    https://cloud.google.com/dlp/docs/.
    """

    SERVICE_ADDRESS = 'dlp.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.privacy.dlp.v2.DlpService'

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
            DlpServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def organization_path(cls, organization):
        """Return a fully-qualified organization string."""
        return google.api_core.path_template.expand(
            'organizations/{organization}',
            organization=organization,
        )

    @classmethod
    def organization_deidentify_template_path(cls, organization,
                                              deidentify_template):
        """Return a fully-qualified organization_deidentify_template string."""
        return google.api_core.path_template.expand(
            'organizations/{organization}/deidentifyTemplates/{deidentify_template}',
            organization=organization,
            deidentify_template=deidentify_template,
        )

    @classmethod
    def project_deidentify_template_path(cls, project, deidentify_template):
        """Return a fully-qualified project_deidentify_template string."""
        return google.api_core.path_template.expand(
            'projects/{project}/deidentifyTemplates/{deidentify_template}',
            project=project,
            deidentify_template=deidentify_template,
        )

    @classmethod
    def organization_inspect_template_path(cls, organization,
                                           inspect_template):
        """Return a fully-qualified organization_inspect_template string."""
        return google.api_core.path_template.expand(
            'organizations/{organization}/inspectTemplates/{inspect_template}',
            organization=organization,
            inspect_template=inspect_template,
        )

    @classmethod
    def project_inspect_template_path(cls, project, inspect_template):
        """Return a fully-qualified project_inspect_template string."""
        return google.api_core.path_template.expand(
            'projects/{project}/inspectTemplates/{inspect_template}',
            project=project,
            inspect_template=inspect_template,
        )

    @classmethod
    def project_job_trigger_path(cls, project, job_trigger):
        """Return a fully-qualified project_job_trigger string."""
        return google.api_core.path_template.expand(
            'projects/{project}/jobTriggers/{job_trigger}',
            project=project,
            job_trigger=job_trigger,
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project,
        )

    @classmethod
    def dlp_job_path(cls, project, dlp_job):
        """Return a fully-qualified dlp_job string."""
        return google.api_core.path_template.expand(
            'projects/{project}/dlpJobs/{dlp_job}',
            project=project,
            dlp_job=dlp_job,
        )

    @classmethod
    def organization_stored_info_type_path(cls, organization,
                                           stored_info_type):
        """Return a fully-qualified organization_stored_info_type string."""
        return google.api_core.path_template.expand(
            'organizations/{organization}/storedInfoTypes/{stored_info_type}',
            organization=organization,
            stored_info_type=stored_info_type,
        )

    @classmethod
    def project_stored_info_type_path(cls, project, stored_info_type):
        """Return a fully-qualified project_stored_info_type string."""
        return google.api_core.path_template.expand(
            'projects/{project}/storedInfoTypes/{stored_info_type}',
            project=project,
            stored_info_type=stored_info_type,
        )

    def __init__(self,
                 transport=None,
                 channel=None,
                 credentials=None,
                 client_config=dlp_service_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            transport (Union[~.DlpServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.DlpServiceGrpcTransport]): A transport
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
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config:
            warnings.warn('The `client_config` argument is deprecated.',
                          PendingDeprecationWarning)
        if channel:
            warnings.warn(
                'The `channel` argument is deprecated; use '
                '`transport` instead.', PendingDeprecationWarning)

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=dlp_service_grpc_transport.
                    DlpServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.')
                self.transport = transport
        else:
            self.transport = dlp_service_grpc_transport.DlpServiceGrpcTransport(
                address=self.SERVICE_ADDRESS,
                channel=channel,
                credentials=credentials,
            )

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def inspect_content(self,
                        parent,
                        inspect_config=None,
                        item=None,
                        inspect_template_name=None,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Finds potentially sensitive info in content.
        This method has limits on input size, processing time, and output size.

        When no InfoTypes or CustomInfoTypes are specified in this request, the
        system will automatically choose what detectors to run. By default this may
        be all types, but may change over time as detectors are updated.

        For how to guides, see https://cloud.google.com/dlp/docs/inspecting-images
        and https://cloud.google.com/dlp/docs/inspecting-text,

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.inspect_content(parent)

        Args:
            parent (str): The parent resource name, for example projects/my-project-id.
            inspect_config (Union[dict, ~google.cloud.dlp_v2.types.InspectConfig]): Configuration for the inspector. What specified here will override
                the template referenced by the inspect_template_name argument.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.InspectConfig`
            item (Union[dict, ~google.cloud.dlp_v2.types.ContentItem]): The item to inspect.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.ContentItem`
            inspect_template_name (str): Optional template to use. Any configuration directly specified in
                inspect_config will override those set in the template. Singular fields
                that are set in this request will replace their corresponding fields in the
                template. Repeated fields are appended. Singular sub-messages and groups
                are recursively merged.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.InspectContentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'inspect_content' not in self._inner_api_calls:
            self._inner_api_calls[
                'inspect_content'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.inspect_content,
                    default_retry=self._method_configs['InspectContent'].retry,
                    default_timeout=self._method_configs['InspectContent'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.InspectContentRequest(
            parent=parent,
            inspect_config=inspect_config,
            item=item,
            inspect_template_name=inspect_template_name,
        )
        return self._inner_api_calls['inspect_content'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def redact_image(self,
                     parent,
                     inspect_config=None,
                     image_redaction_configs=None,
                     include_findings=None,
                     byte_item=None,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Redacts potentially sensitive info from an image.
        This method has limits on input size, processing time, and output size.
        See https://cloud.google.com/dlp/docs/redacting-sensitive-data-images to
        learn more.

        When no InfoTypes or CustomInfoTypes are specified in this request, the
        system will automatically choose what detectors to run. By default this may
        be all types, but may change over time as detectors are updated.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.redact_image(parent)

        Args:
            parent (str): The parent resource name, for example projects/my-project-id.
            inspect_config (Union[dict, ~google.cloud.dlp_v2.types.InspectConfig]): Configuration for the inspector.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.InspectConfig`
            image_redaction_configs (list[Union[dict, ~google.cloud.dlp_v2.types.ImageRedactionConfig]]): The configuration for specifying what content to redact from images.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.ImageRedactionConfig`
            include_findings (bool): Whether the response should include findings along with the redacted
                image.
            byte_item (Union[dict, ~google.cloud.dlp_v2.types.ByteContentItem]): The content must be PNG, JPEG, SVG or BMP.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.ByteContentItem`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.RedactImageResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'redact_image' not in self._inner_api_calls:
            self._inner_api_calls[
                'redact_image'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.redact_image,
                    default_retry=self._method_configs['RedactImage'].retry,
                    default_timeout=self._method_configs['RedactImage'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.RedactImageRequest(
            parent=parent,
            inspect_config=inspect_config,
            image_redaction_configs=image_redaction_configs,
            include_findings=include_findings,
            byte_item=byte_item,
        )
        return self._inner_api_calls['redact_image'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def deidentify_content(self,
                           parent,
                           deidentify_config=None,
                           inspect_config=None,
                           item=None,
                           inspect_template_name=None,
                           deidentify_template_name=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        De-identifies potentially sensitive info from a ContentItem.
        This method has limits on input size and output size.
        See https://cloud.google.com/dlp/docs/deidentify-sensitive-data to
        learn more.

        When no InfoTypes or CustomInfoTypes are specified in this request, the
        system will automatically choose what detectors to run. By default this may
        be all types, but may change over time as detectors are updated.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.deidentify_content(parent)

        Args:
            parent (str): The parent resource name, for example projects/my-project-id.
            deidentify_config (Union[dict, ~google.cloud.dlp_v2.types.DeidentifyConfig]): Configuration for the de-identification of the content item.
                Items specified here will override the template referenced by the
                deidentify_template_name argument.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.DeidentifyConfig`
            inspect_config (Union[dict, ~google.cloud.dlp_v2.types.InspectConfig]): Configuration for the inspector.
                Items specified here will override the template referenced by the
                inspect_template_name argument.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.InspectConfig`
            item (Union[dict, ~google.cloud.dlp_v2.types.ContentItem]): The item to de-identify. Will be treated as text.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.ContentItem`
            inspect_template_name (str): Optional template to use. Any configuration directly specified in
                inspect_config will override those set in the template. Singular fields
                that are set in this request will replace their corresponding fields in the
                template. Repeated fields are appended. Singular sub-messages and groups
                are recursively merged.
            deidentify_template_name (str): Optional template to use. Any configuration directly specified in
                deidentify_config will override those set in the template. Singular fields
                that are set in this request will replace their corresponding fields in the
                template. Repeated fields are appended. Singular sub-messages and groups
                are recursively merged.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.DeidentifyContentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'deidentify_content' not in self._inner_api_calls:
            self._inner_api_calls[
                'deidentify_content'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.deidentify_content,
                    default_retry=self._method_configs['DeidentifyContent'].
                    retry,
                    default_timeout=self._method_configs['DeidentifyContent'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.DeidentifyContentRequest(
            parent=parent,
            deidentify_config=deidentify_config,
            inspect_config=inspect_config,
            item=item,
            inspect_template_name=inspect_template_name,
            deidentify_template_name=deidentify_template_name,
        )
        return self._inner_api_calls['deidentify_content'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def reidentify_content(self,
                           parent,
                           reidentify_config=None,
                           inspect_config=None,
                           item=None,
                           inspect_template_name=None,
                           reidentify_template_name=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Re-identifies content that has been de-identified.
        See
        https://cloud.google.com/dlp/docs/pseudonymization#re-identification_in_free_text_code_example
        to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.reidentify_content(parent)

        Args:
            parent (str): The parent resource name.
            reidentify_config (Union[dict, ~google.cloud.dlp_v2.types.DeidentifyConfig]): Configuration for the re-identification of the content item.
                This field shares the same proto message type that is used for
                de-identification, however its usage here is for the reversal of the
                previous de-identification. Re-identification is performed by examining
                the transformations used to de-identify the items and executing the
                reverse. This requires that only reversible transformations
                be provided here. The reversible transformations are:

                 - ``CryptoReplaceFfxFpeConfig``
                   If a dict is provided, it must be of the same form as the protobuf
                   message :class:`~google.cloud.dlp_v2.types.DeidentifyConfig`
            inspect_config (Union[dict, ~google.cloud.dlp_v2.types.InspectConfig]): Configuration for the inspector.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.InspectConfig`
            item (Union[dict, ~google.cloud.dlp_v2.types.ContentItem]): The item to re-identify. Will be treated as text.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.ContentItem`
            inspect_template_name (str): Optional template to use. Any configuration directly specified in
                ``inspect_config`` will override those set in the template. Singular fields
                that are set in this request will replace their corresponding fields in the
                template. Repeated fields are appended. Singular sub-messages and groups
                are recursively merged.
            reidentify_template_name (str): Optional template to use. References an instance of ``DeidentifyTemplate``.
                Any configuration directly specified in ``reidentify_config`` or
                ``inspect_config`` will override those set in the template. Singular fields
                that are set in this request will replace their corresponding fields in the
                template. Repeated fields are appended. Singular sub-messages and groups
                are recursively merged.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.ReidentifyContentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'reidentify_content' not in self._inner_api_calls:
            self._inner_api_calls[
                'reidentify_content'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.reidentify_content,
                    default_retry=self._method_configs['ReidentifyContent'].
                    retry,
                    default_timeout=self._method_configs['ReidentifyContent'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.ReidentifyContentRequest(
            parent=parent,
            reidentify_config=reidentify_config,
            inspect_config=inspect_config,
            item=item,
            inspect_template_name=inspect_template_name,
            reidentify_template_name=reidentify_template_name,
        )
        return self._inner_api_calls['reidentify_content'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_info_types(self,
                        language_code=None,
                        filter_=None,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Returns a list of the sensitive information types that the DLP API
        supports. See https://cloud.google.com/dlp/docs/infotypes-reference to
        learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> response = client.list_info_types()

        Args:
            language_code (str): Optional BCP-47 language code for localized infoType friendly
                names. If omitted, or if localized strings are not available,
                en-US strings will be returned.
            filter_ (str): Optional filter to only return infoTypes supported by certain parts of the
                API. Defaults to supported_by=INSPECT.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.ListInfoTypesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'list_info_types' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_info_types'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_info_types,
                    default_retry=self._method_configs['ListInfoTypes'].retry,
                    default_timeout=self._method_configs['ListInfoTypes'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.ListInfoTypesRequest(
            language_code=language_code,
            filter=filter_,
        )
        return self._inner_api_calls['list_info_types'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_inspect_template(
            self,
            parent,
            inspect_template=None,
            template_id=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Creates an InspectTemplate for re-using frequently used configuration
        for inspecting content, images, and storage.
        See https://cloud.google.com/dlp/docs/creating-templates to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.organization_path('[ORGANIZATION]')
            >>>
            >>> response = client.create_inspect_template(parent)

        Args:
            parent (str): The parent resource name, for example projects/my-project-id or
                organizations/my-org-id.
            inspect_template (Union[dict, ~google.cloud.dlp_v2.types.InspectTemplate]): The InspectTemplate to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.InspectTemplate`
            template_id (str): The template id can contain uppercase and lowercase letters,
                numbers, and hyphens; that is, it must match the regular
                expression: ``[a-zA-Z\\d-]+``. The maximum length is 100
                characters. Can be empty to allow the system to generate one.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.InspectTemplate` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'create_inspect_template' not in self._inner_api_calls:
            self._inner_api_calls[
                'create_inspect_template'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.create_inspect_template,
                    default_retry=self.
                    _method_configs['CreateInspectTemplate'].retry,
                    default_timeout=self.
                    _method_configs['CreateInspectTemplate'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.CreateInspectTemplateRequest(
            parent=parent,
            inspect_template=inspect_template,
            template_id=template_id,
        )
        return self._inner_api_calls['create_inspect_template'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_inspect_template(
            self,
            name,
            inspect_template=None,
            update_mask=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Updates the InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.organization_inspect_template_path('[ORGANIZATION]', '[INSPECT_TEMPLATE]')
            >>>
            >>> response = client.update_inspect_template(name)

        Args:
            name (str): Resource name of organization and inspectTemplate to be updated, for
                example ``organizations/433245324/inspectTemplates/432452342`` or
                projects/project-id/inspectTemplates/432452342.
            inspect_template (Union[dict, ~google.cloud.dlp_v2.types.InspectTemplate]): New InspectTemplate value.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.InspectTemplate`
            update_mask (Union[dict, ~google.cloud.dlp_v2.types.FieldMask]): Mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.InspectTemplate` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'update_inspect_template' not in self._inner_api_calls:
            self._inner_api_calls[
                'update_inspect_template'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.update_inspect_template,
                    default_retry=self.
                    _method_configs['UpdateInspectTemplate'].retry,
                    default_timeout=self.
                    _method_configs['UpdateInspectTemplate'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.UpdateInspectTemplateRequest(
            name=name,
            inspect_template=inspect_template,
            update_mask=update_mask,
        )
        return self._inner_api_calls['update_inspect_template'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def get_inspect_template(self,
                             name=None,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT,
                             metadata=None):
        """
        Gets an InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> response = client.get_inspect_template()

        Args:
            name (str): Resource name of the organization and inspectTemplate to be read, for
                example ``organizations/433245324/inspectTemplates/432452342`` or
                projects/project-id/inspectTemplates/432452342.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.InspectTemplate` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_inspect_template' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_inspect_template'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_inspect_template,
                    default_retry=self._method_configs['GetInspectTemplate'].
                    retry,
                    default_timeout=self._method_configs['GetInspectTemplate'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.GetInspectTemplateRequest(name=name, )
        return self._inner_api_calls['get_inspect_template'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_inspect_templates(self,
                               parent,
                               page_size=None,
                               order_by=None,
                               retry=google.api_core.gapic_v1.method.DEFAULT,
                               timeout=google.api_core.gapic_v1.method.DEFAULT,
                               metadata=None):
        """
        Lists InspectTemplates.
        See https://cloud.google.com/dlp/docs/creating-templates to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.organization_path('[ORGANIZATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_inspect_templates(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_inspect_templates(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The parent resource name, for example projects/my-project-id or
                organizations/my-org-id.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): Optional comma separated list of fields to order by,
                followed by ``asc`` or ``desc`` postfix. This list is case-insensitive,
                default sorting order is ascending, redundant space characters are
                insignificant.

                Example: ``name asc,update_time, create_time desc``

                Supported fields are:

                - ``create_time``: corresponds to time the template was created.
                - ``update_time``: corresponds to time the template was last updated.
                - ``name``: corresponds to template's name.
                - ``display_name``: corresponds to template's display name.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.dlp_v2.types.InspectTemplate` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'list_inspect_templates' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_inspect_templates'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_inspect_templates,
                    default_retry=self._method_configs['ListInspectTemplates'].
                    retry,
                    default_timeout=self.
                    _method_configs['ListInspectTemplates'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.ListInspectTemplatesRequest(
            parent=parent,
            page_size=page_size,
            order_by=order_by,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls['list_inspect_templates'],
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='inspect_templates',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def delete_inspect_template(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Deletes an InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.organization_inspect_template_path('[ORGANIZATION]', '[INSPECT_TEMPLATE]')
            >>>
            >>> client.delete_inspect_template(name)

        Args:
            name (str): Resource name of the organization and inspectTemplate to be deleted, for
                example ``organizations/433245324/inspectTemplates/432452342`` or
                projects/project-id/inspectTemplates/432452342.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if 'delete_inspect_template' not in self._inner_api_calls:
            self._inner_api_calls[
                'delete_inspect_template'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.delete_inspect_template,
                    default_retry=self.
                    _method_configs['DeleteInspectTemplate'].retry,
                    default_timeout=self.
                    _method_configs['DeleteInspectTemplate'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.DeleteInspectTemplateRequest(name=name, )
        self._inner_api_calls['delete_inspect_template'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_deidentify_template(
            self,
            parent,
            deidentify_template=None,
            template_id=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Creates a DeidentifyTemplate for re-using frequently used configuration
        for de-identifying content, images, and storage.
        See https://cloud.google.com/dlp/docs/creating-templates-deid to learn
        more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.organization_path('[ORGANIZATION]')
            >>>
            >>> response = client.create_deidentify_template(parent)

        Args:
            parent (str): The parent resource name, for example projects/my-project-id or
                organizations/my-org-id.
            deidentify_template (Union[dict, ~google.cloud.dlp_v2.types.DeidentifyTemplate]): The DeidentifyTemplate to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.DeidentifyTemplate`
            template_id (str): The template id can contain uppercase and lowercase letters,
                numbers, and hyphens; that is, it must match the regular
                expression: ``[a-zA-Z\\d-]+``. The maximum length is 100
                characters. Can be empty to allow the system to generate one.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.DeidentifyTemplate` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'create_deidentify_template' not in self._inner_api_calls:
            self._inner_api_calls[
                'create_deidentify_template'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.create_deidentify_template,
                    default_retry=self.
                    _method_configs['CreateDeidentifyTemplate'].retry,
                    default_timeout=self.
                    _method_configs['CreateDeidentifyTemplate'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.CreateDeidentifyTemplateRequest(
            parent=parent,
            deidentify_template=deidentify_template,
            template_id=template_id,
        )
        return self._inner_api_calls['create_deidentify_template'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_deidentify_template(
            self,
            name,
            deidentify_template=None,
            update_mask=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Updates the DeidentifyTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates-deid to learn
        more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.organization_deidentify_template_path('[ORGANIZATION]', '[DEIDENTIFY_TEMPLATE]')
            >>>
            >>> response = client.update_deidentify_template(name)

        Args:
            name (str): Resource name of organization and deidentify template to be updated, for
                example ``organizations/433245324/deidentifyTemplates/432452342`` or
                projects/project-id/deidentifyTemplates/432452342.
            deidentify_template (Union[dict, ~google.cloud.dlp_v2.types.DeidentifyTemplate]): New DeidentifyTemplate value.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.DeidentifyTemplate`
            update_mask (Union[dict, ~google.cloud.dlp_v2.types.FieldMask]): Mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.DeidentifyTemplate` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'update_deidentify_template' not in self._inner_api_calls:
            self._inner_api_calls[
                'update_deidentify_template'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.update_deidentify_template,
                    default_retry=self.
                    _method_configs['UpdateDeidentifyTemplate'].retry,
                    default_timeout=self.
                    _method_configs['UpdateDeidentifyTemplate'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.UpdateDeidentifyTemplateRequest(
            name=name,
            deidentify_template=deidentify_template,
            update_mask=update_mask,
        )
        return self._inner_api_calls['update_deidentify_template'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def get_deidentify_template(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Gets a DeidentifyTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates-deid to learn
        more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.organization_deidentify_template_path('[ORGANIZATION]', '[DEIDENTIFY_TEMPLATE]')
            >>>
            >>> response = client.get_deidentify_template(name)

        Args:
            name (str): Resource name of the organization and deidentify template to be read, for
                example ``organizations/433245324/deidentifyTemplates/432452342`` or
                projects/project-id/deidentifyTemplates/432452342.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.DeidentifyTemplate` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_deidentify_template' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_deidentify_template'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_deidentify_template,
                    default_retry=self.
                    _method_configs['GetDeidentifyTemplate'].retry,
                    default_timeout=self.
                    _method_configs['GetDeidentifyTemplate'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.GetDeidentifyTemplateRequest(name=name, )
        return self._inner_api_calls['get_deidentify_template'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_deidentify_templates(
            self,
            parent,
            page_size=None,
            order_by=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Lists DeidentifyTemplates.
        See https://cloud.google.com/dlp/docs/creating-templates-deid to learn
        more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.organization_path('[ORGANIZATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_deidentify_templates(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_deidentify_templates(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The parent resource name, for example projects/my-project-id or
                organizations/my-org-id.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): Optional comma separated list of fields to order by,
                followed by ``asc`` or ``desc`` postfix. This list is case-insensitive,
                default sorting order is ascending, redundant space characters are
                insignificant.

                Example: ``name asc,update_time, create_time desc``

                Supported fields are:

                - ``create_time``: corresponds to time the template was created.
                - ``update_time``: corresponds to time the template was last updated.
                - ``name``: corresponds to template's name.
                - ``display_name``: corresponds to template's display name.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.dlp_v2.types.DeidentifyTemplate` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'list_deidentify_templates' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_deidentify_templates'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_deidentify_templates,
                    default_retry=self.
                    _method_configs['ListDeidentifyTemplates'].retry,
                    default_timeout=self.
                    _method_configs['ListDeidentifyTemplates'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.ListDeidentifyTemplatesRequest(
            parent=parent,
            page_size=page_size,
            order_by=order_by,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls['list_deidentify_templates'],
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='deidentify_templates',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def delete_deidentify_template(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Deletes a DeidentifyTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates-deid to learn
        more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.organization_deidentify_template_path('[ORGANIZATION]', '[DEIDENTIFY_TEMPLATE]')
            >>>
            >>> client.delete_deidentify_template(name)

        Args:
            name (str): Resource name of the organization and deidentify template to be deleted,
                for example ``organizations/433245324/deidentifyTemplates/432452342`` or
                projects/project-id/deidentifyTemplates/432452342.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if 'delete_deidentify_template' not in self._inner_api_calls:
            self._inner_api_calls[
                'delete_deidentify_template'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.delete_deidentify_template,
                    default_retry=self.
                    _method_configs['DeleteDeidentifyTemplate'].retry,
                    default_timeout=self.
                    _method_configs['DeleteDeidentifyTemplate'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.DeleteDeidentifyTemplateRequest(name=name, )
        self._inner_api_calls['delete_deidentify_template'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_dlp_job(self,
                       parent,
                       inspect_job=None,
                       risk_job=None,
                       job_id=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Creates a new job to inspect storage or calculate risk metrics.
        See https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis to learn more.

        When no InfoTypes or CustomInfoTypes are specified in inspect jobs, the
        system will automatically choose what detectors to run. By default this may
        be all types, but may change over time as detectors are updated.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.create_dlp_job(parent)

        Args:
            parent (str): The parent resource name, for example projects/my-project-id.
            inspect_job (Union[dict, ~google.cloud.dlp_v2.types.InspectJobConfig]): If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.InspectJobConfig`
            risk_job (Union[dict, ~google.cloud.dlp_v2.types.RiskAnalysisJobConfig]): If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.RiskAnalysisJobConfig`
            job_id (str): The job id can contain uppercase and lowercase letters,
                numbers, and hyphens; that is, it must match the regular
                expression: ``[a-zA-Z\\d-]+``. The maximum length is 100
                characters. Can be empty to allow the system to generate one.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.DlpJob` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'create_dlp_job' not in self._inner_api_calls:
            self._inner_api_calls[
                'create_dlp_job'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.create_dlp_job,
                    default_retry=self._method_configs['CreateDlpJob'].retry,
                    default_timeout=self._method_configs['CreateDlpJob'].
                    timeout,
                    client_info=self._client_info,
                )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            inspect_job=inspect_job,
            risk_job=risk_job,
        )

        request = dlp_pb2.CreateDlpJobRequest(
            parent=parent,
            inspect_job=inspect_job,
            risk_job=risk_job,
            job_id=job_id,
        )
        return self._inner_api_calls['create_dlp_job'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_dlp_jobs(self,
                      parent,
                      filter_=None,
                      page_size=None,
                      type_=None,
                      order_by=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Lists DlpJobs that match the specified filter in the request.
        See https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_dlp_jobs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_dlp_jobs(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The parent resource name, for example projects/my-project-id.
            filter_ (str): Optional. Allows filtering.

                Supported syntax:

                * Filter expressions are made up of one or more restrictions.
                * Restrictions can be combined by ``AND`` or ``OR`` logical operators. A
                  sequence of restrictions implicitly uses ``AND``.
                * A restriction has the form of ``<field> <operator> <value>``.
                * Supported fields/values for inspect jobs:
                  - `state` - PENDING|RUNNING|CANCELED|FINISHED|FAILED
                  - `inspected_storage` - DATASTORE|CLOUD_STORAGE|BIGQUERY
                  - `trigger_name` - The resource name of the trigger that created job.
                * Supported fields for risk analysis jobs:
                  - `state` - RUNNING|CANCELED|FINISHED|FAILED
                * The operator must be ``=`` or ``!=``.

                Examples:

                * inspected_storage = cloud_storage AND state = done
                * inspected_storage = cloud_storage OR inspected_storage = bigquery
                * inspected_storage = cloud_storage AND (state = done OR state = canceled)

                The length of this field should be no more than 500 characters.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            type_ (~google.cloud.dlp_v2.types.DlpJobType): The type of job. Defaults to ``DlpJobType.INSPECT``
            order_by (str): Optional comma separated list of fields to order by,
                followed by ``asc`` or ``desc`` postfix. This list is case-insensitive,
                default sorting order is ascending, redundant space characters are
                insignificant.

                Example: ``name asc, end_time asc, create_time desc``

                Supported fields are:

                - ``create_time``: corresponds to time the job was created.
                - ``end_time``: corresponds to time the job ended.
                - ``name``: corresponds to job's name.
                - ``state``: corresponds to ``state``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.dlp_v2.types.DlpJob` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'list_dlp_jobs' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_dlp_jobs'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_dlp_jobs,
                    default_retry=self._method_configs['ListDlpJobs'].retry,
                    default_timeout=self._method_configs['ListDlpJobs'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.ListDlpJobsRequest(
            parent=parent,
            filter=filter_,
            page_size=page_size,
            type=type_,
            order_by=order_by,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls['list_dlp_jobs'],
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='jobs',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_dlp_job(self,
                    name,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT,
                    metadata=None):
        """
        Gets the latest state of a long-running DlpJob.
        See https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.dlp_job_path('[PROJECT]', '[DLP_JOB]')
            >>>
            >>> response = client.get_dlp_job(name)

        Args:
            name (str): The name of the DlpJob resource.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.DlpJob` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_dlp_job' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_dlp_job'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_dlp_job,
                    default_retry=self._method_configs['GetDlpJob'].retry,
                    default_timeout=self._method_configs['GetDlpJob'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.GetDlpJobRequest(name=name, )
        return self._inner_api_calls['get_dlp_job'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_dlp_job(self,
                       name,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Deletes a long-running DlpJob. This method indicates that the client is
        no longer interested in the DlpJob result. The job will be cancelled if
        possible.
        See https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.dlp_job_path('[PROJECT]', '[DLP_JOB]')
            >>>
            >>> client.delete_dlp_job(name)

        Args:
            name (str): The name of the DlpJob resource to be deleted.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if 'delete_dlp_job' not in self._inner_api_calls:
            self._inner_api_calls[
                'delete_dlp_job'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.delete_dlp_job,
                    default_retry=self._method_configs['DeleteDlpJob'].retry,
                    default_timeout=self._method_configs['DeleteDlpJob'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.DeleteDlpJobRequest(name=name, )
        self._inner_api_calls['delete_dlp_job'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def cancel_dlp_job(self,
                       name,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Starts asynchronous cancellation on a long-running DlpJob. The server
        makes a best effort to cancel the DlpJob, but success is not
        guaranteed.
        See https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.dlp_job_path('[PROJECT]', '[DLP_JOB]')
            >>>
            >>> client.cancel_dlp_job(name)

        Args:
            name (str): The name of the DlpJob resource to be cancelled.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if 'cancel_dlp_job' not in self._inner_api_calls:
            self._inner_api_calls[
                'cancel_dlp_job'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.cancel_dlp_job,
                    default_retry=self._method_configs['CancelDlpJob'].retry,
                    default_timeout=self._method_configs['CancelDlpJob'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.CancelDlpJobRequest(name=name, )
        self._inner_api_calls['cancel_dlp_job'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_job_triggers(self,
                          parent,
                          page_size=None,
                          order_by=None,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        Lists job triggers.
        See https://cloud.google.com/dlp/docs/creating-job-triggers to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_job_triggers(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_job_triggers(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The parent resource name, for example ``projects/my-project-id``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): Optional comma separated list of triggeredJob fields to order by,
                followed by ``asc`` or ``desc`` postfix. This list is case-insensitive,
                default sorting order is ascending, redundant space characters are
                insignificant.

                Example: ``name asc,update_time, create_time desc``

                Supported fields are:

                - ``create_time``: corresponds to time the JobTrigger was created.
                - ``update_time``: corresponds to time the JobTrigger was last updated.
                - ``name``: corresponds to JobTrigger's name.
                - ``display_name``: corresponds to JobTrigger's display name.
                - ``status``: corresponds to JobTrigger's status.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.dlp_v2.types.JobTrigger` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'list_job_triggers' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_job_triggers'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_job_triggers,
                    default_retry=self._method_configs['ListJobTriggers'].
                    retry,
                    default_timeout=self._method_configs['ListJobTriggers'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.ListJobTriggersRequest(
            parent=parent,
            page_size=page_size,
            order_by=order_by,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls['list_job_triggers'],
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='job_triggers',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_job_trigger(self,
                        name,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Gets a job trigger.
        See https://cloud.google.com/dlp/docs/creating-job-triggers to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.project_job_trigger_path('[PROJECT]', '[JOB_TRIGGER]')
            >>>
            >>> response = client.get_job_trigger(name)

        Args:
            name (str): Resource name of the project and the triggeredJob, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.JobTrigger` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_job_trigger' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_job_trigger'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_job_trigger,
                    default_retry=self._method_configs['GetJobTrigger'].retry,
                    default_timeout=self._method_configs['GetJobTrigger'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.GetJobTriggerRequest(name=name, )
        return self._inner_api_calls['get_job_trigger'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_job_trigger(self,
                           name,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Deletes a job trigger.
        See https://cloud.google.com/dlp/docs/creating-job-triggers to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> # TODO: Initialize ``name``:
            >>> name = ''
            >>>
            >>> client.delete_job_trigger(name)

        Args:
            name (str): Resource name of the project and the triggeredJob, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if 'delete_job_trigger' not in self._inner_api_calls:
            self._inner_api_calls[
                'delete_job_trigger'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.delete_job_trigger,
                    default_retry=self._method_configs['DeleteJobTrigger'].
                    retry,
                    default_timeout=self._method_configs['DeleteJobTrigger'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.DeleteJobTriggerRequest(name=name, )
        self._inner_api_calls['delete_job_trigger'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_job_trigger(self,
                           name,
                           job_trigger=None,
                           update_mask=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Updates a job trigger.
        See https://cloud.google.com/dlp/docs/creating-job-triggers to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.project_job_trigger_path('[PROJECT]', '[JOB_TRIGGER]')
            >>>
            >>> response = client.update_job_trigger(name)

        Args:
            name (str): Resource name of the project and the triggeredJob, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.
            job_trigger (Union[dict, ~google.cloud.dlp_v2.types.JobTrigger]): New JobTrigger value.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.JobTrigger`
            update_mask (Union[dict, ~google.cloud.dlp_v2.types.FieldMask]): Mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.JobTrigger` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'update_job_trigger' not in self._inner_api_calls:
            self._inner_api_calls[
                'update_job_trigger'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.update_job_trigger,
                    default_retry=self._method_configs['UpdateJobTrigger'].
                    retry,
                    default_timeout=self._method_configs['UpdateJobTrigger'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.UpdateJobTriggerRequest(
            name=name,
            job_trigger=job_trigger,
            update_mask=update_mask,
        )
        return self._inner_api_calls['update_job_trigger'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_job_trigger(self,
                           parent,
                           job_trigger=None,
                           trigger_id=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Creates a job trigger to run DLP actions such as scanning storage for
        sensitive information on a set schedule.
        See https://cloud.google.com/dlp/docs/creating-job-triggers to learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.create_job_trigger(parent)

        Args:
            parent (str): The parent resource name, for example projects/my-project-id.
            job_trigger (Union[dict, ~google.cloud.dlp_v2.types.JobTrigger]): The JobTrigger to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.JobTrigger`
            trigger_id (str): The trigger id can contain uppercase and lowercase letters,
                numbers, and hyphens; that is, it must match the regular
                expression: ``[a-zA-Z\\d-]+``. The maximum length is 100
                characters. Can be empty to allow the system to generate one.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.JobTrigger` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'create_job_trigger' not in self._inner_api_calls:
            self._inner_api_calls[
                'create_job_trigger'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.create_job_trigger,
                    default_retry=self._method_configs['CreateJobTrigger'].
                    retry,
                    default_timeout=self._method_configs['CreateJobTrigger'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.CreateJobTriggerRequest(
            parent=parent,
            job_trigger=job_trigger,
            trigger_id=trigger_id,
        )
        return self._inner_api_calls['create_job_trigger'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_stored_info_type(
            self,
            parent,
            config=None,
            stored_info_type_id=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Creates a pre-built stored infoType to be used for inspection.
        See https://cloud.google.com/dlp/docs/creating-stored-infotypes to
        learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.organization_path('[ORGANIZATION]')
            >>>
            >>> response = client.create_stored_info_type(parent)

        Args:
            parent (str): The parent resource name, for example projects/my-project-id or
                organizations/my-org-id.
            config (Union[dict, ~google.cloud.dlp_v2.types.StoredInfoTypeConfig]): Configuration of the storedInfoType to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.StoredInfoTypeConfig`
            stored_info_type_id (str): The storedInfoType ID can contain uppercase and lowercase letters,
                numbers, and hyphens; that is, it must match the regular
                expression: ``[a-zA-Z\\d-]+``. The maximum length is 100
                characters. Can be empty to allow the system to generate one.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.StoredInfoType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'create_stored_info_type' not in self._inner_api_calls:
            self._inner_api_calls[
                'create_stored_info_type'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.create_stored_info_type,
                    default_retry=self._method_configs['CreateStoredInfoType'].
                    retry,
                    default_timeout=self.
                    _method_configs['CreateStoredInfoType'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.CreateStoredInfoTypeRequest(
            parent=parent,
            config=config,
            stored_info_type_id=stored_info_type_id,
        )
        return self._inner_api_calls['create_stored_info_type'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_stored_info_type(
            self,
            name,
            config=None,
            update_mask=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Updates the stored infoType by creating a new version. The existing version
        will continue to be used until the new version is ready.
        See https://cloud.google.com/dlp/docs/creating-stored-infotypes to
        learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.organization_stored_info_type_path('[ORGANIZATION]', '[STORED_INFO_TYPE]')
            >>>
            >>> response = client.update_stored_info_type(name)

        Args:
            name (str): Resource name of organization and storedInfoType to be updated, for
                example ``organizations/433245324/storedInfoTypes/432452342`` or
                projects/project-id/storedInfoTypes/432452342.
            config (Union[dict, ~google.cloud.dlp_v2.types.StoredInfoTypeConfig]): Updated configuration for the storedInfoType. If not provided, a new
                version of the storedInfoType will be created with the existing
                configuration.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.StoredInfoTypeConfig`
            update_mask (Union[dict, ~google.cloud.dlp_v2.types.FieldMask]): Mask to control which fields get updated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.StoredInfoType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'update_stored_info_type' not in self._inner_api_calls:
            self._inner_api_calls[
                'update_stored_info_type'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.update_stored_info_type,
                    default_retry=self._method_configs['UpdateStoredInfoType'].
                    retry,
                    default_timeout=self.
                    _method_configs['UpdateStoredInfoType'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.UpdateStoredInfoTypeRequest(
            name=name,
            config=config,
            update_mask=update_mask,
        )
        return self._inner_api_calls['update_stored_info_type'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def get_stored_info_type(self,
                             name,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT,
                             metadata=None):
        """
        Gets a stored infoType.
        See https://cloud.google.com/dlp/docs/creating-stored-infotypes to
        learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.organization_stored_info_type_path('[ORGANIZATION]', '[STORED_INFO_TYPE]')
            >>>
            >>> response = client.get_stored_info_type(name)

        Args:
            name (str): Resource name of the organization and storedInfoType to be read, for
                example ``organizations/433245324/storedInfoTypes/432452342`` or
                projects/project-id/storedInfoTypes/432452342.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2.types.StoredInfoType` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_stored_info_type' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_stored_info_type'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_stored_info_type,
                    default_retry=self._method_configs['GetStoredInfoType'].
                    retry,
                    default_timeout=self._method_configs['GetStoredInfoType'].
                    timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.GetStoredInfoTypeRequest(name=name, )
        return self._inner_api_calls['get_stored_info_type'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_stored_info_types(self,
                               parent,
                               page_size=None,
                               order_by=None,
                               retry=google.api_core.gapic_v1.method.DEFAULT,
                               timeout=google.api_core.gapic_v1.method.DEFAULT,
                               metadata=None):
        """
        Lists stored infoTypes.
        See https://cloud.google.com/dlp/docs/creating-stored-infotypes to
        learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> parent = client.organization_path('[ORGANIZATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_stored_info_types(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_stored_info_types(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The parent resource name, for example projects/my-project-id or
                organizations/my-org-id.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): Optional comma separated list of fields to order by,
                followed by ``asc`` or ``desc`` postfix. This list is case-insensitive,
                default sorting order is ascending, redundant space characters are
                insignificant.

                Example: ``name asc, display_name, create_time desc``

                Supported fields are:

                - ``create_time``: corresponds to time the most recent version of the
                  resource was created.
                - ``state``: corresponds to the state of the resource.
                - ``name``: corresponds to resource name.
                - ``display_name``: corresponds to info type's display name.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.dlp_v2.types.StoredInfoType` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'list_stored_info_types' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_stored_info_types'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_stored_info_types,
                    default_retry=self._method_configs['ListStoredInfoTypes'].
                    retry,
                    default_timeout=self.
                    _method_configs['ListStoredInfoTypes'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.ListStoredInfoTypesRequest(
            parent=parent,
            page_size=page_size,
            order_by=order_by,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls['list_stored_info_types'],
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='stored_info_types',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def delete_stored_info_type(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Deletes a stored infoType.
        See https://cloud.google.com/dlp/docs/creating-stored-infotypes to
        learn more.

        Example:
            >>> from google.cloud import dlp_v2
            >>>
            >>> client = dlp_v2.DlpServiceClient()
            >>>
            >>> name = client.organization_stored_info_type_path('[ORGANIZATION]', '[STORED_INFO_TYPE]')
            >>>
            >>> client.delete_stored_info_type(name)

        Args:
            name (str): Resource name of the organization and storedInfoType to be deleted, for
                example ``organizations/433245324/storedInfoTypes/432452342`` or
                projects/project-id/storedInfoTypes/432452342.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if 'delete_stored_info_type' not in self._inner_api_calls:
            self._inner_api_calls[
                'delete_stored_info_type'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.delete_stored_info_type,
                    default_retry=self._method_configs['DeleteStoredInfoType'].
                    retry,
                    default_timeout=self.
                    _method_configs['DeleteStoredInfoType'].timeout,
                    client_info=self._client_info,
                )

        request = dlp_pb2.DeleteStoredInfoTypeRequest(name=name, )
        self._inner_api_calls['delete_stored_info_type'](
            request, retry=retry, timeout=timeout, metadata=metadata)
