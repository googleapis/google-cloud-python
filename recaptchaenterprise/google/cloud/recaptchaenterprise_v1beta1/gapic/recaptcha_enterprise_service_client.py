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
"""Accesses the google.cloud.recaptchaenterprise.v1beta1 RecaptchaEnterpriseService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.recaptchaenterprise_v1beta1.gapic import enums
from google.cloud.recaptchaenterprise_v1beta1.gapic import (
    recaptcha_enterprise_service_client_config,
)
from google.cloud.recaptchaenterprise_v1beta1.gapic.transports import (
    recaptcha_enterprise_service_grpc_transport,
)
from google.cloud.recaptchaenterprise_v1beta1.proto import recaptchaenterprise_pb2
from google.cloud.recaptchaenterprise_v1beta1.proto import recaptchaenterprise_pb2_grpc

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-recaptchaenterprise"
).version


class RecaptchaEnterpriseServiceClient(object):
    """Service to determine the likelihood an event is legitimate."""

    SERVICE_ADDRESS = "recaptchaenterprise.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = (
        "google.cloud.recaptchaenterprise.v1beta1.RecaptchaEnterpriseService"
    )

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
            RecaptchaEnterpriseServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def assessment_path(cls, project, assessment):
        """Return a fully-qualified assessment string."""
        return google.api_core.path_template.expand(
            "projects/{project}/assessments/{assessment}",
            project=project,
            assessment=assessment,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.RecaptchaEnterpriseServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.RecaptchaEnterpriseServiceGrpcTransport]): A transport
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
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = recaptcha_enterprise_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=recaptcha_enterprise_service_grpc_transport.RecaptchaEnterpriseServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = recaptcha_enterprise_service_grpc_transport.RecaptchaEnterpriseServiceGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
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
    def create_assessment(
        self,
        parent,
        assessment,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates an Assessment of the likelihood an event is legitimate.

        Example:
            >>> from google.cloud import recaptchaenterprise_v1beta1
            >>>
            >>> client = recaptchaenterprise_v1beta1.RecaptchaEnterpriseServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `assessment`:
            >>> assessment = {}
            >>>
            >>> response = client.create_assessment(parent, assessment)

        Args:
            parent (str): Required. The name of the project in which the assessment will be
                created, in the format "projects/{project\_number}".
            assessment (Union[dict, ~google.cloud.recaptchaenterprise_v1beta1.types.Assessment]): The asessment details.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.recaptchaenterprise_v1beta1.types.Assessment`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.recaptchaenterprise_v1beta1.types.Assessment` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_assessment" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_assessment"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_assessment,
                default_retry=self._method_configs["CreateAssessment"].retry,
                default_timeout=self._method_configs["CreateAssessment"].timeout,
                client_info=self._client_info,
            )

        request = recaptchaenterprise_pb2.CreateAssessmentRequest(
            parent=parent, assessment=assessment
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

        return self._inner_api_calls["create_assessment"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def annotate_assessment(
        self,
        name,
        annotation,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Annotates a previously created Assessment to provide additional information
        on whether the event turned out to be authentic or fradulent.

        Example:
            >>> from google.cloud import recaptchaenterprise_v1beta1
            >>> from google.cloud.recaptchaenterprise_v1beta1 import enums
            >>>
            >>> client = recaptchaenterprise_v1beta1.RecaptchaEnterpriseServiceClient()
            >>>
            >>> name = client.assessment_path('[PROJECT]', '[ASSESSMENT]')
            >>>
            >>> # TODO: Initialize `annotation`:
            >>> annotation = enums.AnnotateAssessmentRequest.Annotation.ANNOTATION_UNSPECIFIED
            >>>
            >>> response = client.annotate_assessment(name, annotation)

        Args:
            name (str): Required. The resource name of the Assessment, in the format
                "projects/{project\_number}/assessments/{assessment\_id}".
            annotation (~google.cloud.recaptchaenterprise_v1beta1.types.Annotation): The annotation that will be assigned to the Event.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.recaptchaenterprise_v1beta1.types.AnnotateAssessmentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "annotate_assessment" not in self._inner_api_calls:
            self._inner_api_calls[
                "annotate_assessment"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.annotate_assessment,
                default_retry=self._method_configs["AnnotateAssessment"].retry,
                default_timeout=self._method_configs["AnnotateAssessment"].timeout,
                client_info=self._client_info,
            )

        request = recaptchaenterprise_pb2.AnnotateAssessmentRequest(
            name=name, annotation=annotation
        )
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

        return self._inner_api_calls["annotate_assessment"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
