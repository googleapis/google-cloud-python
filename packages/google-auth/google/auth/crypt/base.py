# Copyright 2016 Google Inc.
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

"""Base classes for cryptographic signers and verifiers."""

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class Verifier(object):
    """Abstract base class for crytographic signature verifiers."""

    @abc.abstractmethod
    def verify(self, message, signature):
        """Verifies a message against a cryptographic signature.

        Args:
            message (Union[str, bytes]): The message to verify.
            signature (Union[str, bytes]): The cryptography signature to check.

        Returns:
            bool: True if message was signed by the private key associated
            with the public key that this object was constructed with.
        """
        # pylint: disable=missing-raises-doc,redundant-returns-doc
        # (pylint doesn't recognize that this is abstract)
        raise NotImplementedError('Verify must be implemented')


@six.add_metaclass(abc.ABCMeta)
class Signer(object):
    """Abstract base class for cryptographic signers."""

    @abc.abstractproperty
    def key_id(self):
        """Optional[str]: The key ID used to identify this private key."""
        raise NotImplementedError('Key id must be implemented')

    @abc.abstractmethod
    def sign(self, message):
        """Signs a message.

        Args:
            message (Union[str, bytes]): The message to be signed.

        Returns:
            bytes: The signature of the message.
        """
        # pylint: disable=missing-raises-doc,redundant-returns-doc
        # (pylint doesn't recognize that this is abstract)
        raise NotImplementedError('Sign must be implemented')
