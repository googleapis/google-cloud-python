# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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
"""Wrappers for protocol buffer enum types."""

import enum


class MqttState(enum.IntEnum):
    """
    Indicates whether an MQTT connection is enabled or disabled. See the field
    description for details.

    Attributes:
      MQTT_STATE_UNSPECIFIED (int): No MQTT state specified. If not specified, MQTT will be enabled by default.
      MQTT_ENABLED (int): Enables a MQTT connection.
      MQTT_DISABLED (int): Disables a MQTT connection.
    """
    MQTT_STATE_UNSPECIFIED = 0
    MQTT_ENABLED = 1
    MQTT_DISABLED = 2


class HttpState(enum.IntEnum):
    """
    Indicates whether DeviceService (HTTP) is enabled or disabled for the
    registry. See the field description for details.

    Attributes:
      HTTP_STATE_UNSPECIFIED (int): No HTTP state specified. If not specified, DeviceService will be
      enabled by default.
      HTTP_ENABLED (int): Enables DeviceService (HTTP) service for the registry.
      HTTP_DISABLED (int): Disables DeviceService (HTTP) service for the registry.
    """
    HTTP_STATE_UNSPECIFIED = 0
    HTTP_ENABLED = 1
    HTTP_DISABLED = 2


class PublicKeyCertificateFormat(enum.IntEnum):
    """
    The supported formats for the public key.

    Attributes:
      UNSPECIFIED_PUBLIC_KEY_CERTIFICATE_FORMAT (int): The format has not been specified. This is an invalid default value and
      must not be used.
      X509_CERTIFICATE_PEM (int): An X.509v3 certificate
      (`RFC5280 <https://www.ietf.org/rfc/rfc5280.txt>`__), encoded in base64,
      and wrapped by ``-----BEGIN CERTIFICATE-----`` and
      ``-----END CERTIFICATE-----``.
    """
    UNSPECIFIED_PUBLIC_KEY_CERTIFICATE_FORMAT = 0
    X509_CERTIFICATE_PEM = 1


class PublicKeyFormat(enum.IntEnum):
    """
    The supported formats for the public key.

    Attributes:
      UNSPECIFIED_PUBLIC_KEY_FORMAT (int): The format has not been specified. This is an invalid default value and
      must not be used.
      RSA_PEM (int): An RSA public key encoded in base64, and wrapped by
      ``-----BEGIN PUBLIC KEY-----`` and ``-----END PUBLIC KEY-----``. This
      can be used to verify ``RS256`` signatures in JWT tokens
      (`RFC7518 <https://www.ietf.org/rfc/rfc7518.txt>`__).
      RSA_X509_PEM (int): As RSA\_PEM, but wrapped in an X.509v3 certificate
      (`RFC5280 <https://www.ietf.org/rfc/rfc5280.txt>`__), encoded in base64,
      and wrapped by ``-----BEGIN CERTIFICATE-----`` and
      ``-----END CERTIFICATE-----``.
      ES256_PEM (int): Public key for the ECDSA algorithm using P-256 and SHA-256, encoded in
      base64, and wrapped by ``-----BEGIN PUBLIC KEY-----`` and
      ``-----END  PUBLIC KEY-----``. This can be used to verify JWT tokens
      with the ``ES256`` algorithm
      (`RFC7518 <https://www.ietf.org/rfc/rfc7518.txt>`__). This curve is
      defined in `OpenSSL <https://www.openssl.org/>`__ as the ``prime256v1``
      curve.
      ES256_X509_PEM (int): As ES256\_PEM, but wrapped in an X.509v3 certificate
      (`RFC5280 <https://www.ietf.org/rfc/rfc5280.txt>`__), encoded in base64,
      and wrapped by ``-----BEGIN CERTIFICATE-----`` and
      ``-----END CERTIFICATE-----``.
    """
    UNSPECIFIED_PUBLIC_KEY_FORMAT = 0
    RSA_PEM = 3
    RSA_X509_PEM = 1
    ES256_PEM = 2
    ES256_X509_PEM = 4
