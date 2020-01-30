# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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


import google.api_core.grpc_helpers
import google.api_core.operations_v1

from google.cloud.translate_v3beta1.proto import translation_service_pb2_grpc


class TranslationServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.translation.v3beta1 TranslationService API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-translation",
    )

    def __init__(
        self, channel=None, credentials=None, address="translate.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "translation_service_stub": translation_service_pb2_grpc.TranslationServiceStub(
                channel
            )
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="translate.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def translate_text(self):
        """Return the gRPC stub for :meth:`TranslationServiceClient.translate_text`.

        Translates input text and returns translated text.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["translation_service_stub"].TranslateText

    @property
    def detect_language(self):
        """Return the gRPC stub for :meth:`TranslationServiceClient.detect_language`.

        Detects the language of text within a request.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["translation_service_stub"].DetectLanguage

    @property
    def get_supported_languages(self):
        """Return the gRPC stub for :meth:`TranslationServiceClient.get_supported_languages`.

        Returns a list of supported languages for translation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["translation_service_stub"].GetSupportedLanguages

    @property
    def batch_translate_text(self):
        """Return the gRPC stub for :meth:`TranslationServiceClient.batch_translate_text`.

        Translates a large volume of text in asynchronous batch mode.
        This function provides real-time output as the inputs are being processed.
        If caller cancels a request, the partial results (for an input file, it's
        all or nothing) may still be available on the specified output location.

        This call returns immediately and you can
        use google.longrunning.Operation.name to poll the status of the call.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["translation_service_stub"].BatchTranslateText

    @property
    def create_glossary(self):
        """Return the gRPC stub for :meth:`TranslationServiceClient.create_glossary`.

        Creates a glossary and returns the long-running operation. Returns
        NOT\_FOUND, if the project doesn't exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["translation_service_stub"].CreateGlossary

    @property
    def list_glossaries(self):
        """Return the gRPC stub for :meth:`TranslationServiceClient.list_glossaries`.

        Lists glossaries in a project. Returns NOT\_FOUND, if the project
        doesn't exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["translation_service_stub"].ListGlossaries

    @property
    def get_glossary(self):
        """Return the gRPC stub for :meth:`TranslationServiceClient.get_glossary`.

        Gets a glossary. Returns NOT\_FOUND, if the glossary doesn't exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["translation_service_stub"].GetGlossary

    @property
    def delete_glossary(self):
        """Return the gRPC stub for :meth:`TranslationServiceClient.delete_glossary`.

        Deletes a glossary, or cancels glossary construction if the glossary
        isn't created yet. Returns NOT\_FOUND, if the glossary doesn't exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["translation_service_stub"].DeleteGlossary
