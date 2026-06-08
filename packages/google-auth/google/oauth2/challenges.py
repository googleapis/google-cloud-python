# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Challenges for reauthentication.
"""

import abc
import base64
import getpass
import hashlib
import json
import sys

from google.auth import _helpers
from google.auth import exceptions
from google.oauth2 import webauthn_handler_factory
from google.oauth2.webauthn_types import (
    AuthenticationExtensionsClientInputs,
    GetRequest,
    PublicKeyCredentialDescriptor,
)

REAUTH_ORIGIN = "https://accounts.google.com"
SAML_CHALLENGE_MESSAGE = (
    "Please run `gcloud auth login` to complete reauthentication with SAML."
)
WEBAUTHN_TIMEOUT_MS = 120000  # Two minute timeout
U2F_AUTHENTICATION_TYPE = "navigator.id.getAssertion"


def get_user_password(text):
    """Get password from user.

    Override this function with a different logic if you are using this library
    outside a CLI.

    Args:
        text (str): message for the password prompt.

    Returns:
        str: password string.
    """
    return getpass.getpass(text)


class ReauthChallenge(metaclass=abc.ABCMeta):
    """Base class for reauth challenges."""

    @property
    @abc.abstractmethod
    def name(self):  # pragma: NO COVER
        """Returns the name of the challenge."""
        raise NotImplementedError("name property must be implemented")

    @property
    @abc.abstractmethod
    def is_locally_eligible(self):  # pragma: NO COVER
        """Returns true if a challenge is supported locally on this machine."""
        raise NotImplementedError("is_locally_eligible property must be implemented")

    @abc.abstractmethod
    def obtain_challenge_input(self, metadata):  # pragma: NO COVER
        """Performs logic required to obtain credentials and returns it.

        Args:
            metadata (Mapping): challenge metadata returned in the 'challenges' field in
                the initial reauth request. Includes the 'challengeType' field
                and other challenge-specific fields.

        Returns:
            response that will be send to the reauth service as the content of
            the 'proposalResponse' field in the request body. Usually a dict
            with the keys specific to the challenge. For example,
            ``{'credential': password}`` for password challenge.
        """
        raise NotImplementedError("obtain_challenge_input method must be implemented")


class PasswordChallenge(ReauthChallenge):
    """Challenge that asks for user's password."""

    @property
    def name(self):
        return "PASSWORD"

    @property
    def is_locally_eligible(self):
        return True

    @_helpers.copy_docstring(ReauthChallenge)
    def obtain_challenge_input(self, unused_metadata):
        passwd = get_user_password("Please enter your password:")
        if not passwd:
            passwd = " "  # avoid the server crashing in case of no password :D
        return {"credential": passwd}


class SecurityKeyChallenge(ReauthChallenge):
    """Challenge that asks for user's security key touch."""

    @property
    def name(self):
        return "SECURITY_KEY"

    @property
    def is_locally_eligible(self):
        return True

    @_helpers.copy_docstring(ReauthChallenge)
    def obtain_challenge_input(self, metadata):
        # Check if there is an available Webauthn Handler, if not use fido2.
        try:
            factory = webauthn_handler_factory.WebauthnHandlerFactory()
            webauthn_handler = factory.get_handler()
            if webauthn_handler is not None:
                sys.stderr.write("Please insert and touch your security key\n")
                return self._obtain_challenge_input_webauthn(metadata, webauthn_handler)
        except Exception:
            # Attempt fido2 if exception in webauthn flow.
            pass

        return self._obtain_challenge_input_fido2(metadata)

    def _get_fido2_classes(self):
        try:
            from fido2.ctap import CtapError  # type: ignore
            from fido2.ctap1 import (
                APDU,  # type: ignore
                ApduError,  # type: ignore
                Ctap1,  # type: ignore
            )
            from fido2.hid import CtapHidDevice  # type: ignore
        except ImportError as caught_exc:
            raise exceptions.ReauthFailError(
                "fido2 dependency is required to use Security key reauth feature. "
                "It can be installed via `pip install fido2` or `pip install google-auth[reauth]`."
            ) from caught_exc
        return CtapHidDevice, Ctap1, APDU, ApduError, CtapError

    def _obtain_challenge_input_fido2(self, metadata):
        CtapHidDevice, Ctap1, APDU, ApduError, CtapError = self._get_fido2_classes()

        devices = list(CtapHidDevice.list_devices())
        if not devices:
            sys.stderr.write("No security key found.\n")
            return None

        sk = metadata["securityKey"]
        challenges = sk["challenges"]
        # Read both 'applicationId' and 'relyingPartyId', if they are the same, use
        # applicationId, if they are different, use relyingPartyId first and retry
        # with applicationId
        application_id = sk["applicationId"]
        relying_party_id = sk["relyingPartyId"]

        if application_id != relying_party_id:
            application_parameters = [relying_party_id, application_id]
        else:
            application_parameters = [application_id]

        sys.stderr.write("Please touch your security key.\n")
        for app_id in application_parameters:
            app_param = hashlib.sha256(app_id.encode("utf-8")).digest()
            for challenge in challenges:
                key_handle = self._urlsafe_b64decode(challenge["keyHandle"])
                challenge_bytes = self._urlsafe_b64decode(challenge["challenge"])
                client_data = self._create_u2f_client_data(challenge_bytes)
                client_param = hashlib.sha256(client_data).digest()
                for device in devices:
                    try:
                        signature = Ctap1(device).authenticate(
                            client_param, app_param, key_handle
                        )
                    except ApduError as caught_exc:
                        if caught_exc.code == APDU.WRONG_DATA:
                            continue
                        if caught_exc.code == APDU.USE_NOT_SATISFIED:
                            sys.stderr.write(
                                "Timed out while waiting for security key touch.\n"
                            )
                            return None
                        raise
                    except CtapError as caught_exc:
                        if caught_exc.code in (
                            CtapError.ERR.TIMEOUT,
                            CtapError.ERR.ACTION_TIMEOUT,
                            CtapError.ERR.KEEPALIVE_CANCEL,
                            CtapError.ERR.OPERATION_DENIED,
                        ):
                            sys.stderr.write(
                                "Timed out while waiting for security key touch.\n"
                            )
                            return None
                        raise
                    else:
                        return {
                            "securityKey": {
                                "clientData": self._unpadded_urlsafe_b64encode(
                                    client_data
                                ),
                                "signatureData": self._unpadded_urlsafe_b64encode(
                                    bytes(signature)
                                ),
                                "applicationId": app_id,
                                "keyHandle": self._unpadded_urlsafe_b64encode(
                                    key_handle
                                ),
                            }
                        }
        sys.stderr.write("Ineligible security key.\n")
        return None

    def _obtain_challenge_input_webauthn(self, metadata, webauthn_handler):
        sk = metadata.get("securityKey")
        if sk is None:
            raise exceptions.InvalidValue("securityKey is None")
        challenges = sk.get("challenges")
        application_id = sk.get("applicationId")
        relying_party_id = sk.get("relyingPartyId")
        if challenges is None or len(challenges) < 1:
            raise exceptions.InvalidValue("challenges is None or empty")
        if application_id is None:
            raise exceptions.InvalidValue("application_id is None")
        if relying_party_id is None:
            raise exceptions.InvalidValue("relying_party_id is None")

        allow_credentials = []
        for challenge in challenges:
            kh = challenge.get("keyHandle")
            if kh is None:
                raise exceptions.InvalidValue("keyHandle is None")
            key_handle = self._unpadded_urlsafe_b64recode(kh)
            allow_credentials.append(PublicKeyCredentialDescriptor(id=key_handle))

        extension = AuthenticationExtensionsClientInputs(appid=application_id)

        challenge = challenges[0].get("challenge")
        if challenge is None:
            raise exceptions.InvalidValue("challenge is None")

        get_request = GetRequest(
            origin=REAUTH_ORIGIN,
            rpid=relying_party_id,
            challenge=self._unpadded_urlsafe_b64recode(challenge),
            timeout_ms=WEBAUTHN_TIMEOUT_MS,
            allow_credentials=allow_credentials,
            user_verification="preferred",
            extensions=extension,
        )

        try:
            get_response = webauthn_handler.get(get_request)
        except Exception as e:
            sys.stderr.write("Webauthn Error: {}.\n".format(e))
            raise e

        response = {
            "clientData": get_response.response.client_data_json,
            "authenticatorData": get_response.response.authenticator_data,
            "signatureData": get_response.response.signature,
            "applicationId": application_id,
            "keyHandle": get_response.id,
            "securityKeyReplyType": 2,
        }
        return {"securityKey": response}

    def _unpadded_urlsafe_b64recode(self, s):
        """Converts standard b64 encoded string to url safe b64 encoded string
        with no padding."""
        return self._unpadded_urlsafe_b64encode(self._urlsafe_b64decode(s))

    def _create_u2f_client_data(self, challenge):
        return json.dumps(
            {
                "challenge": self._unpadded_urlsafe_b64encode(challenge),
                "origin": REAUTH_ORIGIN,
                "typ": U2F_AUTHENTICATION_TYPE,
            },
            sort_keys=True,
        ).encode()

    def _unpadded_urlsafe_b64encode(self, data):
        return base64.urlsafe_b64encode(data).decode().rstrip("=")

    def _urlsafe_b64decode(self, data):
        return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


class SamlChallenge(ReauthChallenge):
    """Challenge that asks the users to browse to their ID Providers.

    Currently SAML challenge is not supported. When obtaining the challenge
    input, exception will be raised to instruct the users to run
    `gcloud auth login` for reauthentication.
    """

    @property
    def name(self):
        return "SAML"

    @property
    def is_locally_eligible(self):
        return True

    def obtain_challenge_input(self, metadata):
        # Magic Arch has not fully supported returning a proper dedirect URL
        # for programmatic SAML users today. So we error our here and request
        # users to use gcloud to complete a login.
        raise exceptions.ReauthSamlChallengeFailError(SAML_CHALLENGE_MESSAGE)


AVAILABLE_CHALLENGES = {
    challenge.name: challenge
    for challenge in [SecurityKeyChallenge(), PasswordChallenge(), SamlChallenge()]
}
