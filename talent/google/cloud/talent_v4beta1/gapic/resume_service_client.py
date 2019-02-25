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
"""Accesses the google.cloud.talent.v4beta1 ResumeService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.talent_v4beta1.gapic import enums
from google.cloud.talent_v4beta1.gapic import resume_service_client_config
from google.cloud.talent_v4beta1.gapic.transports import resume_service_grpc_transport
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
from google.cloud.talent_v4beta1.proto import resume_service_pb2
from google.cloud.talent_v4beta1.proto import resume_service_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-talent").version


class ResumeServiceClient(object):
    """A service that handles resume parsing."""

    SERVICE_ADDRESS = "jobs.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.talent.v4beta1.ResumeService"

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
            ResumeServiceClient: The constructed client.
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
            transport (Union[~.ResumeServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.ResumeServiceGrpcTransport]): A transport
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
            client_config = resume_service_client_config.config

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
                    default_class=resume_service_grpc_transport.ResumeServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = resume_service_grpc_transport.ResumeServiceGrpcTransport(
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
    def parse_resume(
        self,
        parent,
        resume,
        region_code=None,
        language_code=None,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Parses a resume into a ``Profile``. The API attempts to fill out the
        following profile fields if present within the resume:

        -  personNames
        -  addresses
        -  emailAddress
        -  phoneNumbers
        -  personalUris
        -  employmentRecords
        -  educationRecords
        -  skills

        Note that some attributes in these fields may not be populated if
        they're not present within the resume or unrecognizable by the resume
        parser.

        This API does not save the resume or profile. To create a profile from
        this resume, clients need to call the CreateProfile method again with
        the profile returned.

        The following list of formats are supported:

        -  PDF
        -  TXT
        -  DOC
        -  RTF
        -  DOCX
        -  PNG (only when ``ParseResumeRequest.enable_ocr`` is set to ``true``,
           otherwise an error is thrown)

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.ResumeServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `resume`:
            >>> resume = b''
            >>>
            >>> response = client.parse_resume(parent, resume)

        Args:
            parent (str): Required.

                The resource name of the project.

                The format is "projects/{project\_id}", for example,
                "projects/api-test-project".
            resume (bytes): Required.

                The bytes of the resume file in common format, for example, PDF, TXT.
                UTF-8 encoding is required if the resume is text-based, otherwise an error
                is thrown.
            region_code (str): Optional.

                The region code indicating where the resume is from. Values
                are as per the ISO-3166-2 format. For example, US, FR, DE.

                This value is optional, but providing this value improves the resume
                parsing quality and performance.

                An error is thrown if the regionCode is invalid.
            language_code (str): Optional.

                The language code of contents in the resume.

                Language codes must be in BCP-47 format, such as "en-US" or "sr-Latn".
                For more information, see `Tags for Identifying
                Languages <https://tools.ietf.org/html/bcp47>`__\ {: class="external"
                target="\_blank" }.
            options_ (Union[dict, ~google.cloud.talent_v4beta1.types.ParseResumeOptions]): Optional.

                Options that change how the resume parse is performed.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.ParseResumeOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types.ParseResumeResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "parse_resume" not in self._inner_api_calls:
            self._inner_api_calls[
                "parse_resume"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.parse_resume,
                default_retry=self._method_configs["ParseResume"].retry,
                default_timeout=self._method_configs["ParseResume"].timeout,
                client_info=self._client_info,
            )

        request = resume_service_pb2.ParseResumeRequest(
            parent=parent,
            resume=resume,
            region_code=region_code,
            language_code=language_code,
            options=options_,
        )
        return self._inner_api_calls["parse_resume"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
