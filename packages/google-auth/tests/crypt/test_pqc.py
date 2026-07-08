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

from google.auth.crypt import pqc


def test_pqc_signer_algorithm():
    mock_key = mock.MagicMock()
    signer = pqc.PqcSigner(mock_key, key_id="key-123")
    assert signer.key_id == "key-123"
    assert signer.algorithm == "ML-DSA-65"


def test_pqc_signer_sign():
    mock_key = mock.MagicMock()
    mock_key.sign.return_value = b"mock_pqc_signature"
    signer = pqc.PqcSigner(mock_key, key_id="key-123")

    sig = signer.sign("hello")
    assert sig == b"mock_pqc_signature"
    mock_key.sign.assert_called_once_with(b"hello")


def test_is_pqc_disabled(monkeypatch):
    assert not pqc.is_pqc_disabled()
    monkeypatch.setenv("GOOGLE_CLOUD_DISABLE_PQC", "1")
    assert pqc.is_pqc_disabled()
    monkeypatch.setenv("GOOGLE_CLOUD_DISABLE_PQC", "true")
    assert pqc.is_pqc_disabled()
    monkeypatch.setenv("GOOGLE_CLOUD_DISABLE_PQC", "0")
    assert not pqc.is_pqc_disabled()


def test_configure_ssl_context_pqc_enabled(monkeypatch):
    monkeypatch.delenv("GOOGLE_CLOUD_DISABLE_PQC", raising=False)
    mock_ctx = mock.MagicMock()
    result = pqc.configure_ssl_context_pqc(mock_ctx)
    assert result == mock_ctx
    mock_ctx.set_ecdh_curve.assert_not_called()


def test_configure_ssl_context_pqc_disabled(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_DISABLE_PQC", "1")
    mock_ctx = mock.MagicMock()
    result = pqc.configure_ssl_context_pqc(mock_ctx)
    assert result == mock_ctx
    mock_ctx.set_ecdh_curve.assert_called_once_with("prime256v1:secp384r1")

