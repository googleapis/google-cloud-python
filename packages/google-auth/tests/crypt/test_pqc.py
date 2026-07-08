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
