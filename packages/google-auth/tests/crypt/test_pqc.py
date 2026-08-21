# Copyright 2026 Google LLC
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

from unittest import mock

import pytest

from google.auth.crypt import pqc


PEM_MLDSA_KEY = "-----BEGIN PRIVATE KEY-----\ndGVzdG1sZHNh\n-----END PRIVATE KEY-----"
PEM_MLDSA_44 = PEM_MLDSA_KEY
PEM_MLDSA_65 = PEM_MLDSA_KEY
PEM_MLDSA_87 = PEM_MLDSA_KEY
PEM_NOT_MLDSA = (
    "-----BEGIN PRIVATE KEY-----\ndGVzdGtleW5vdG1sZHNh\n-----END PRIVATE KEY-----"
)


class TestIsMldsaKey:
    def test_is_mldsa_key_invalid_inputs(self):
        assert pqc.is_mldsa_key(None) is False
        assert pqc.is_mldsa_key(12345) is False
        assert pqc.is_mldsa_key({}) is False
        assert pqc.is_mldsa_key("not a key") is False

    def test_is_mldsa_key_without_mldsa(self, monkeypatch):
        monkeypatch.setattr(pqc, "mldsa", None)
        assert pqc.is_mldsa_key(PEM_MLDSA_65) is False

    def test_is_mldsa_key_with_mldsa_module(self, monkeypatch):
        class MockMLDSA65PrivateKey:
            pass

        mock_mldsa = mock.Mock()
        mock_mldsa.MLDSA65PrivateKey = MockMLDSA65PrivateKey

        monkeypatch.setattr(pqc, "mldsa", mock_mldsa)
        monkeypatch.setattr(
            pqc.serialization,
            "load_pem_private_key",
            lambda key, password, backend: MockMLDSA65PrivateKey(),
        )

        assert pqc.is_mldsa_key(PEM_MLDSA_65) is True


class TestPqcSignerWithoutCryptography47:
    def test_from_string_raises_runtime_error(self, monkeypatch):
        monkeypatch.setattr(pqc, "mldsa", None)
        with pytest.raises(RuntimeError) as excinfo:
            pqc.PqcSigner.from_string(PEM_MLDSA_65)

        assert (
            "Post-Quantum ML-DSA Service Account keys require cryptography>=47.0.0"
            in str(excinfo.value)
        )
        assert (
            "Please upgrade your cryptography library (pip install 'cryptography>=47.0.0')"
            in str(excinfo.value)
        )

    def test_setstate_raises_runtime_error(self, monkeypatch):
        monkeypatch.setattr(pqc, "mldsa", None)
        signer_state = {"_key": PEM_MLDSA_65.encode("utf-8"), "_key_id": "test_id"}
        # Instantiate without __init__
        signer = pqc.PqcSigner.__new__(pqc.PqcSigner)
        with pytest.raises(RuntimeError) as excinfo:
            signer.__setstate__(signer_state)

        assert (
            "Post-Quantum ML-DSA Service Account keys require cryptography>=47.0.0"
            in str(excinfo.value)
        )


class TestPqcVerifierWithoutCryptography47:
    def test_from_string_raises_runtime_error(self, monkeypatch):
        monkeypatch.setattr(pqc, "mldsa", None)
        with pytest.raises(RuntimeError) as excinfo:
            pqc.PqcVerifier.from_string("pubkey")

        assert (
            "Post-Quantum ML-DSA Service Account keys require cryptography>=47.0.0"
            in str(excinfo.value)
        )


class TestPqcSignerWithCryptography47:
    @pytest.fixture
    def mock_mldsa_env(self, monkeypatch):
        class MockMLDSA65PrivateKey:
            def __init__(self):
                self._signed = False

            def sign(self, message):
                self._signed = True
                return b"sig-65-" + message

            def private_bytes(self, encoding, format, encryption_algorithm):
                return b"private-pem-65"

        class MockMLDSA44PrivateKey:
            def sign(self, message):
                return b"sig-44-" + message

        class MockMLDSA87PrivateKey:
            def sign(self, message):
                return b"sig-87-" + message

        mock_mldsa = mock.Mock()
        mock_mldsa.MLDSA44PrivateKey = MockMLDSA44PrivateKey
        mock_mldsa.MLDSA65PrivateKey = MockMLDSA65PrivateKey
        mock_mldsa.MLDSA87PrivateKey = MockMLDSA87PrivateKey

        monkeypatch.setattr(pqc, "mldsa", mock_mldsa)
        return (
            mock_mldsa,
            MockMLDSA44PrivateKey,
            MockMLDSA65PrivateKey,
            MockMLDSA87PrivateKey,
        )

    def test_from_string_mldsa44(self, mock_mldsa_env, monkeypatch):
        _, Mock44, _, _ = mock_mldsa_env
        monkeypatch.setattr(
            pqc.serialization,
            "load_pem_private_key",
            lambda key, password, backend: Mock44(),
        )
        signer = pqc.PqcSigner.from_string(PEM_MLDSA_44, key_id="key-44")
        assert signer.key_id == "key-44"
        assert signer.algorithm == "ML-DSA-44"

        sig = signer.sign(b"test")
        assert sig == b"sig-44-test"

    def test_from_string_mldsa65(self, mock_mldsa_env, monkeypatch):
        _, _, Mock65, _ = mock_mldsa_env
        monkeypatch.setattr(
            pqc.serialization,
            "load_pem_private_key",
            lambda key, password, backend: Mock65(),
        )
        signer = pqc.PqcSigner.from_string(PEM_MLDSA_65, key_id="key-65")
        assert signer.key_id == "key-65"
        assert signer.algorithm == "ML-DSA-65"
        assert pqc.PqcSigner.RECOMMENDED_DEFAULT_ALGORITHM == "ML-DSA-65"

        sig = signer.sign("hello")
        assert sig == b"sig-65-hello"

    def test_from_string_mldsa87(self, mock_mldsa_env, monkeypatch):
        _, _, _, Mock87 = mock_mldsa_env
        monkeypatch.setattr(
            pqc.serialization,
            "load_pem_private_key",
            lambda key, password, backend: Mock87(),
        )
        signer = pqc.PqcSigner.from_string(PEM_MLDSA_87, key_id="key-87")
        assert signer.key_id == "key-87"
        assert signer.algorithm == "ML-DSA-87"

        sig = signer.sign(b"world")
        assert sig == b"sig-87-world"

    def test_from_string_invalid_type(self, mock_mldsa_env, monkeypatch):
        monkeypatch.setattr(
            pqc.serialization,
            "load_pem_private_key",
            lambda key, password, backend: "not-an-mldsa-key",
        )
        with pytest.raises(TypeError) as excinfo:
            pqc.PqcSigner.from_string(PEM_MLDSA_65)
        assert "Expected private key of type ML-DSA" in str(excinfo.value)

    def test_pickle_getstate_setstate(self, mock_mldsa_env, monkeypatch):
        _, _, Mock65, _ = mock_mldsa_env
        key = Mock65()
        signer = pqc.PqcSigner(key, key_id="test-id")

        state = signer.__getstate__()
        assert state["_key"] == b"private-pem-65"
        assert state["_key_id"] == "test-id"

        loaded_key = Mock65()
        monkeypatch.setattr(
            pqc.serialization,
            "load_pem_private_key",
            mock.Mock(return_value=loaded_key),
        )

        new_signer = pqc.PqcSigner.__new__(pqc.PqcSigner)
        new_signer.__setstate__(state)
        assert new_signer.key_id == "test-id"
        assert new_signer.algorithm == "ML-DSA-65"


class TestPqcVerifierWithCryptography47:
    @pytest.fixture
    def mock_mldsa_env(self, monkeypatch):
        class MockMLDSA65PublicKey:
            def verify(self, signature, message):
                if signature != b"valid-sig":
                    raise ValueError("Invalid signature")

        mock_mldsa = mock.Mock()
        mock_mldsa.MLDSA65PublicKey = MockMLDSA65PublicKey
        monkeypatch.setattr(pqc, "mldsa", mock_mldsa)
        return mock_mldsa, MockMLDSA65PublicKey

    def test_from_string_and_verify(self, mock_mldsa_env, monkeypatch):
        mock_mldsa, Mock65Pub = mock_mldsa_env
        monkeypatch.setattr(
            pqc.serialization,
            "load_pem_public_key",
            lambda pub, backend: Mock65Pub(),
        )

        verifier = pqc.PqcVerifier.from_string("mock-pubkey")
        assert verifier.verify(b"msg", b"valid-sig") is True
        assert verifier.verify(b"msg", b"invalid-sig") is False

    def test_from_string_x509_cert(self, mock_mldsa_env, monkeypatch):
        mock_mldsa, Mock65Pub = mock_mldsa_env
        mock_cert = mock.Mock()
        mock_cert.public_key.return_value = Mock65Pub()
        monkeypatch.setattr(
            pqc.cryptography.x509,
            "load_pem_x509_certificate",
            lambda cert, backend: mock_cert,
        )

        cert_str = "-----BEGIN CERTIFICATE-----\nmockcert\n-----END CERTIFICATE-----"
        verifier = pqc.PqcVerifier.from_string(cert_str)
        assert verifier.verify(b"msg", b"valid-sig") is True

    def test_from_string_invalid_type(self, mock_mldsa_env, monkeypatch):
        monkeypatch.setattr(
            pqc.serialization,
            "load_pem_public_key",
            lambda pub, backend: "not-an-mldsa-pubkey",
        )
        with pytest.raises(TypeError) as excinfo:
            pqc.PqcVerifier.from_string("mock-pubkey")
        assert "Expected public key of type ML-DSA" in str(excinfo.value)
