# Copyright 2020 Google LLC
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

"""Helper functions for getting mTLS cert and key, for internal use only."""

import json
import logging
from os import path
import re
import subprocess

CONTEXT_AWARE_METADATA_PATH = "~/.secureConnect/context_aware_metadata.json"
_CERT_PROVIDER_COMMAND = "cert_provider_command"
_CERT_REGEX = re.compile(
    b"-----BEGIN CERTIFICATE-----.+-----END CERTIFICATE-----\r?\n?", re.DOTALL
)

# support various format of key files, e.g.
# "-----BEGIN PRIVATE KEY-----...",
# "-----BEGIN EC PRIVATE KEY-----...",
# "-----BEGIN RSA PRIVATE KEY-----..."
_KEY_REGEX = re.compile(
    b"-----BEGIN [A-Z ]*PRIVATE KEY-----.+-----END [A-Z ]*PRIVATE KEY-----\r?\n?",
    re.DOTALL,
)

_LOGGER = logging.getLogger(__name__)


def _check_dca_metadata_path(metadata_path):
    """Checks for context aware metadata. If it exists, returns the absolute path;
    otherwise returns None.

    Args:
        metadata_path (str): context aware metadata path.

    Returns:
        str: absolute path if exists and None otherwise.
    """
    metadata_path = path.expanduser(metadata_path)
    if not path.exists(metadata_path):
        _LOGGER.debug("%s is not found, skip client SSL authentication.", metadata_path)
        return None
    return metadata_path


def _read_dca_metadata_file(metadata_path):
    """Loads context aware metadata from the given path.

    Args:
        metadata_path (str): context aware metadata path.

    Returns:
        Dict[str, str]: The metadata.

    Raises:
        ValueError: If failed to parse metadata as JSON.
    """
    with open(metadata_path) as f:
        metadata = json.load(f)

    return metadata


def get_client_ssl_credentials(metadata_json):
    """Returns the client side mTLS cert and key.

    Args:
        metadata_json (Dict[str, str]): metadata JSON file which contains the cert
            provider command.

    Returns:
        Tuple[bytes, bytes]: client certificate and key, both in PEM format.

    Raises:
        OSError: If the cert provider command failed to run.
        RuntimeError: If the cert provider command has a runtime error.
        ValueError: If the metadata json file doesn't contain the cert provider
            command or if the command doesn't produce both the client certificate
            and client key.
    """
    # TODO: implement an in-memory cache of cert and key so we don't have to
    # run cert provider command every time.

    # Check the cert provider command existence in the metadata json file.
    if _CERT_PROVIDER_COMMAND not in metadata_json:
        raise ValueError("Cert provider command is not found")

    # Execute the command. It throws OsError in case of system failure.
    command = metadata_json[_CERT_PROVIDER_COMMAND]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check cert provider command execution error.
    if process.returncode != 0:
        raise RuntimeError(
            "Cert provider command returns non-zero status code %s" % process.returncode
        )

    # Extract certificate (chain) and key.
    cert_match = re.findall(_CERT_REGEX, stdout)
    if len(cert_match) != 1:
        raise ValueError("Client SSL certificate is missing or invalid")
    key_match = re.findall(_KEY_REGEX, stdout)
    if len(key_match) != 1:
        raise ValueError("Client SSL key is missing or invalid")
    return cert_match[0], key_match[0]


def get_client_cert_and_key(client_cert_callback=None):
    """Returns the client side certificate and private key. The function first
    tries to get certificate and key from client_cert_callback; if the callback
    is None or doesn't provide certificate and key, the function tries application
    default SSL credentials.

    Args:
        client_cert_callback (Optional[Callable[[], (bytes, bytes)]]): An
            optional callback which returns client certificate bytes and private
            key bytes both in PEM format.

    Returns:
        Tuple[bool, bytes, bytes]:
            A boolean indicating if cert and key are obtained, the cert bytes
            and key bytes both in PEM format.

    Raises:
        OSError: If the cert provider command failed to run.
        RuntimeError: If the cert provider command has a runtime error.
        ValueError: If the metadata json file doesn't contain the cert provider
            command or if the command doesn't produce both the client certificate
            and client key.
    """
    if client_cert_callback:
        cert, key = client_cert_callback()
        return True, cert, key

    metadata_path = _check_dca_metadata_path(CONTEXT_AWARE_METADATA_PATH)
    if metadata_path:
        metadata = _read_dca_metadata_file(metadata_path)
        cert, key = get_client_ssl_credentials(metadata)
        return True, cert, key

    return False, None, None
