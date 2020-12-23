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

import abc
import typing

from google import auth
from google.auth import credentials  # type: ignore

from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise
from google.protobuf import empty_pb2 as empty  # type: ignore


class RecaptchaEnterpriseServiceTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for RecaptchaEnterpriseService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "recaptchaenterprise.googleapis.com",
        credentials: credentials.Credentials = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def create_assessment(
        self,
    ) -> typing.Callable[
        [recaptchaenterprise.CreateAssessmentRequest], recaptchaenterprise.Assessment
    ]:
        raise NotImplementedError

    @property
    def annotate_assessment(
        self,
    ) -> typing.Callable[
        [recaptchaenterprise.AnnotateAssessmentRequest],
        recaptchaenterprise.AnnotateAssessmentResponse,
    ]:
        raise NotImplementedError

    @property
    def create_key(
        self,
    ) -> typing.Callable[
        [recaptchaenterprise.CreateKeyRequest], recaptchaenterprise.Key
    ]:
        raise NotImplementedError

    @property
    def list_keys(
        self,
    ) -> typing.Callable[
        [recaptchaenterprise.ListKeysRequest], recaptchaenterprise.ListKeysResponse
    ]:
        raise NotImplementedError

    @property
    def get_key(
        self,
    ) -> typing.Callable[[recaptchaenterprise.GetKeyRequest], recaptchaenterprise.Key]:
        raise NotImplementedError

    @property
    def update_key(
        self,
    ) -> typing.Callable[
        [recaptchaenterprise.UpdateKeyRequest], recaptchaenterprise.Key
    ]:
        raise NotImplementedError

    @property
    def delete_key(
        self,
    ) -> typing.Callable[[recaptchaenterprise.DeleteKeyRequest], empty.Empty]:
        raise NotImplementedError


__all__ = ("RecaptchaEnterpriseServiceTransport",)
