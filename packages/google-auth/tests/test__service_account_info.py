# Copyright 2016 Google LLC
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

import base64
import json
import os
from unittest import mock

import pytest  # type: ignore

from google.auth import _service_account_info
from google.auth import crypt


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SERVICE_ACCOUNT_JSON_FILE = os.path.join(DATA_DIR, "service_account.json")
GDCH_SERVICE_ACCOUNT_ES256_JSON_FILE = os.path.join(
    DATA_DIR, "gdch_service_account.json"
)
GDCH_SERVICE_ACCOUNT_ES384_JSON_FILE = os.path.join(
    DATA_DIR, "es384_service_account.json"
)

with open(SERVICE_ACCOUNT_JSON_FILE, "r") as fh:
    SERVICE_ACCOUNT_INFO = json.load(fh)

with open(GDCH_SERVICE_ACCOUNT_ES256_JSON_FILE, "r") as fh:
    GDCH_SERVICE_ACCOUNT_ES256_INFO = json.load(fh)

with open(GDCH_SERVICE_ACCOUNT_ES384_JSON_FILE, "r") as fh:
    GDCH_SERVICE_ACCOUNT_ES384_INFO = json.load(fh)


def test_from_dict():
    signer = _service_account_info.from_dict(SERVICE_ACCOUNT_INFO)
    assert isinstance(signer, crypt.RSASigner)
    assert signer.key_id == SERVICE_ACCOUNT_INFO["private_key_id"]


def test_from_dict_es256_signer():
    signer = _service_account_info.from_dict(
        GDCH_SERVICE_ACCOUNT_ES256_INFO, use_rsa_signer=False
    )
    assert isinstance(signer, crypt.EsSigner)
    assert signer.key_id == GDCH_SERVICE_ACCOUNT_ES256_INFO["private_key_id"]


def test_from_dict_es384_signer():
    signer = _service_account_info.from_dict(
        GDCH_SERVICE_ACCOUNT_ES384_INFO, use_rsa_signer=False
    )
    assert isinstance(signer, crypt.EsSigner)
    assert signer.key_id == GDCH_SERVICE_ACCOUNT_ES384_INFO["private_key_id"]
    assert signer.algorithm == "ES384"


def test_from_dict_bad_private_key():
    info = SERVICE_ACCOUNT_INFO.copy()
    info["private_key"] = "garbage"

    with pytest.raises(ValueError) as excinfo:
        _service_account_info.from_dict(info)

    assert excinfo.match(r"(?i)(key|PEM)")


def test_from_dict_bad_format():
    with pytest.raises(ValueError) as excinfo:
        _service_account_info.from_dict({}, require=("meep",))

    assert excinfo.match(r"missing fields")


def test_from_filename():
    info, signer = _service_account_info.from_filename(SERVICE_ACCOUNT_JSON_FILE)

    for key, value in SERVICE_ACCOUNT_INFO.items():
        assert info[key] == value

    assert isinstance(signer, crypt.RSASigner)
    assert signer.key_id == SERVICE_ACCOUNT_INFO["private_key_id"]


def test_from_filename_es256_signer():
    _, signer = _service_account_info.from_filename(
        GDCH_SERVICE_ACCOUNT_ES256_JSON_FILE, use_rsa_signer=False
    )

    assert isinstance(signer, crypt.EsSigner)
    assert signer.key_id == GDCH_SERVICE_ACCOUNT_ES256_INFO["private_key_id"]


def test_from_filename_es384_signer():
    _, signer = _service_account_info.from_filename(
        GDCH_SERVICE_ACCOUNT_ES384_JSON_FILE, use_rsa_signer=False
    )

    assert isinstance(signer, crypt.EsSigner)
    assert signer.key_id == GDCH_SERVICE_ACCOUNT_ES384_INFO["private_key_id"]
    assert signer.algorithm == "ES384"


def test_from_dict_mldsa_signer_auto_detect_upgrade_required(monkeypatch):
    if crypt.pqc is not None:
        monkeypatch.setattr(crypt.pqc, "mldsa", None)
    else:
        mock_pqc = mock.Mock()
        mock_pqc.mldsa = None
        mock_pqc.is_mldsa_key = lambda key: True
        mock_pqc.PqcSigner.from_service_account_info = mock.Mock(
            side_effect=RuntimeError(
                "Post-Quantum ML-DSA Service Account keys require cryptography>=47.0.0. "
                "Please upgrade your cryptography library (pip install 'cryptography>=47.0.0')."
            )
        )
        monkeypatch.setattr(crypt, "pqc", mock_pqc)

    der_bytes = (
        b"\x30\x20\x02\x01\x00\x30\x0b"
        b"\x06\x09\x60\x86\x48\x01\x65\x03\x04\x03\x12"
        b"\x04\x0a\x04\x08\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    b64_key = base64.b64encode(der_bytes).decode("ascii")
    mldsa_pem = f"-----BEGIN PRIVATE KEY-----\n{b64_key}\n-----END PRIVATE KEY-----"
    info = {
        "private_key": mldsa_pem,
        "private_key_id": "test_mldsa_key_id",
        "client_email": "test@example.com",
    }
    with pytest.raises(RuntimeError) as excinfo:
        _service_account_info.from_dict(info)

    assert (
        "Post-Quantum ML-DSA Service Account keys require cryptography>=47.0.0"
        in str(excinfo.value)
    )
    assert (
        "Please upgrade your cryptography library (pip install 'cryptography>=47.0.0')"
        in str(excinfo.value)
    )


def test_from_dict_mldsa_signer_auto_detect_success(monkeypatch):
    class MockMLDSA65PrivateKey:
        pass

    mock_mldsa = mock.Mock()
    mock_mldsa.MLDSA65PrivateKey = MockMLDSA65PrivateKey

    der_bytes = (
        b"\x30\x20\x02\x01\x00\x30\x0b"
        b"\x06\x09\x60\x86\x48\x01\x65\x03\x04\x03\x12"
        b"\x04\x0a\x04\x08\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    b64_key = base64.b64encode(der_bytes).decode("ascii")
    mldsa_pem = f"-----BEGIN PRIVATE KEY-----\n{b64_key}\n-----END PRIVATE KEY-----"
    info = {
        "private_key": mldsa_pem,
        "private_key_id": "test_mldsa_key_id",
        "client_email": "test@example.com",
    }

    if crypt.pqc is not None:
        monkeypatch.setattr(crypt.pqc, "mldsa", mock_mldsa)
        monkeypatch.setattr(
            crypt.pqc.serialization,
            "load_pem_private_key",
            lambda key, password, backend: MockMLDSA65PrivateKey(),
        )
    else:
        mock_pqc = mock.Mock()
        mock_pqc.mldsa = mock_mldsa
        mock_pqc.is_mldsa_key = lambda key: True
        mock_pqc.PqcSigner.from_service_account_info = mock.Mock(
            return_value=mock.Mock(key_id="test_mldsa_key_id", algorithm="ML-DSA-65")
        )
        monkeypatch.setattr(crypt, "pqc", mock_pqc)

    signer = _service_account_info.from_dict(info)
    assert signer.key_id == "test_mldsa_key_id"
    assert signer.algorithm == "ML-DSA-65"
