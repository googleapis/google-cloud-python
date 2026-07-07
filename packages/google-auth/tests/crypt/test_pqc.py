# Copyright 2026 Google LLC
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

import cryptography
import pytest
from packaging.version import Version


def test_cryptography_pqc_mlkem_support():
    """Verifies that the cryptography package installed in google-auth supports Post-Quantum Cryptography (ML-KEM / FIPS 203)."""
    # Attempt to import ML-KEM (FIPS 203) introduced in cryptography 44.0.0
    try:
        from cryptography.hazmat.primitives.asymmetric import mlkem
    except ImportError:
        pytest.fail(
            f"PQC Compliance Failure: cryptography version {cryptography.__version__} does not support ML-KEM (FIPS 203). "
            f"google-auth requires cryptography >= 44.0.0 for PQC support."
        )

    # 1. Generate ML-KEM-768 (FIPS 203) private key and derive public key
    private_key = mlkem.MLKEM768PrivateKey.generate()
    public_key = private_key.public_key()
    assert isinstance(private_key, mlkem.MLKEM768PrivateKey)
    assert isinstance(public_key, mlkem.MLKEM768PublicKey)

    # 2. Perform Key Encapsulation (sender generates shared secret + ciphertext)
    shared_secret_sender, ciphertext = public_key.encapsulate()
    assert len(ciphertext) > 0
    assert len(shared_secret_sender) > 0

    # 3. Perform Key Decapsulation (receiver recovers shared secret from ciphertext)
    shared_secret_receiver = private_key.decapsulate(ciphertext)
    assert shared_secret_receiver == shared_secret_sender
