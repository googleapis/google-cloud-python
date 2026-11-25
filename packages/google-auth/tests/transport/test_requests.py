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

import copy
import datetime
import functools
import http.client as http_client
import json
import os
import pickle
import ssl
import threading
from unittest import mock

import freezegun
import pytest  # type: ignore
import requests
import requests.adapters

import google.auth.credentials
import google.auth.transport._custom_tls_signer
import google.auth.transport._mtls_helper
import google.auth.transport.requests
from google.auth import environment_vars, exceptions
from google.oauth2 import service_account
from tests.transport import compliance


@pytest.fixture
def frozen_time():
    with freezegun.freeze_time("1970-01-01 00:00:00", tick=False) as frozen:
        yield frozen


@pytest.fixture
def es256_cert_and_key():
    with open(os.path.join(pytest.data_dir, "es256_public_cert.pem"), "rb") as fh:
        cert = fh.read()
    with open(os.path.join(pytest.data_dir, "es256_privatekey.pem"), "rb") as fh:
        key = fh.read()
    return cert, key


@pytest.fixture
def workload_cert_config(tmpdir, monkeypatch):
    cert_file = tmpdir.join("public_cert.pem")
    cert_file.write_binary(pytest.public_cert_bytes)
    config_file = tmpdir.join("certificate_config.json")
    config_file.write(
        json.dumps(
            {
                "cert_configs": {
                    "workload": {
                        "cert_path": str(cert_file),
                        "key_path": os.path.join(pytest.data_dir, "privatekey.pem"),
                    }
                }
            }
        )
    )
    monkeypatch.setenv(environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_file))
    monkeypatch.delenv(
        environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE, raising=False
    )
    monkeypatch.delenv(
        environment_vars.CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE,
        raising=False,
    )
    return cert_file


CERT_MOCK_VAL = b"-----BEGIN CERTIFICATE-----\nMIIDIzCCAgugAwIBAgIJAMfISuBQ5m+5MA0GCSqGSIb3DQEBBQUAMBUxEzARBgNV\nBAMTCnVuaXQtdGVzdHMwHhcNMTExMjA2MTYyNjAyWhcNMjExMjAzMTYyNjAyWjAV\nMRMwEQYDVQQDEwp1bml0LXRlc3RzMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB\nCgKCAQEA4ej0p7bQ7L/r4rVGUz9RN4VQWoej1Bg1mYWIDYslvKrk1gpj7wZgkdmM\n7oVK2OfgrSj/FCTkInKPqaCR0gD7K80q+mLBrN3PUkDrJQZpvRZIff3/xmVU1Wer\nuQLFJjnFb2dqu0s/FY/2kWiJtBCakXvXEOb7zfbINuayL+MSsCGSdVYsSliS5qQp\ngyDap+8b5fpXZVJkq92hrcNtbkg7hCYUJczt8n9hcCTJCfUpApvaFQ18pe+zpyl4\n+WzkP66I28hniMQyUlA1hBiskT7qiouq0m8IOodhv2fagSZKjOTTU2xkSBc//fy3\nZpsL7WqgsZS7Q+0VRK8gKfqkxg5OYQIDAQABo3YwdDAdBgNVHQ4EFgQU2RQ8yO+O\ngN8oVW2SW7RLrfYd9jEwRQYDVR0jBD4wPIAU2RQ8yO+OgN8oVW2SW7RLrfYd9jGh\nGaQXMBUxEzARBgNVBAMTCnVuaXQtdGVzdHOCCQDHyErgUOZvuTAMBgNVHRMEBTAD\nAQH/MA0GCSqGSIb3DQEBBQUAA4IBAQBRv+M/6+FiVu7KXNjFI5pSN17OcW5QUtPr\nodJMlWrJBtynn/TA1oJlYu3yV5clc/71Vr/AxuX5xGP+IXL32YDF9lTUJXG/uUGk\n+JETpKmQviPbRsvzYhz4pf6ZIOZMc3/GIcNq92ECbseGO+yAgyWUVKMmZM0HqXC9\novNslqe0M8C1sLm1zAR5z/h/litE7/8O2ietija3Q/qtl2TOXJdCA6sgjJX2WUql\nybrC55ct18NKf3qhpcEkGQvFU40rVYApJpi98DiZPYFdx1oBDp/f4uZ3ojpxRVFT\ncDwcJLfNRCPUhormsY7fDS9xSyThiHsW9mjJYdcaKQkwYZ0F11yB\n-----END CERTIFICATE-----\n"
KEY_MOCK_VAL = b"-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIHeMEkGCSqGSIb3DQEFDTA8MBsGCSqGSIb3DQEFDDAOBAj9XnJ2h78QVAICCAAw\nHQYJYIZIAWUDBAECBBBeiiOF2LnLzq/wjb/viwMwBIGQk28Zkfj2EIk42bgc7UzC\nSf98qssCVhsIYz0Xa3eSATg8Cpn83YieaBeyxdk/tXTnrOhxMV/vt7T98kWhaGbH\n5Z9CdGVLfes0UFvVJqrlk6vcf2sOnLCGbrn78HS+ayrGOCRSCd/7+dnEiB/7Um1B\nMk6BBJHsLEnZZSHyfrw8jvYgVmcSBy/WdY0pqldD/+4D\n-----END ENCRYPTED PRIVATE KEY-----\n"


class TestRequestResponse(compliance.RequestResponseTests):
    def make_request(self):
        return google.auth.transport.requests.Request()

    def test_timeout(self):
        http = mock.create_autospec(requests.Session, instance=True)
        request = google.auth.transport.requests.Request(http)
        request(url="http://example.com", method="GET", timeout=5)

        assert http.request.call_args[1]["timeout"] == 5

    def test_session_closed_on_del(self):
        http = mock.create_autospec(requests.Session, instance=True)
        request = google.auth.transport.requests.Request(http)
        request.__del__()
        http.close.assert_called_with()

        http = mock.create_autospec(requests.Session, instance=True)
        http.close.side_effect = TypeError("test injected TypeError")
        request = google.auth.transport.requests.Request(http)
        request.__del__()
        http.close.assert_called_with()

    @pytest.mark.parametrize(
        "mount_prefix",
        ["https://", "https://iamcredentials.mtls.googleapis.com/"],
    )
    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_origin_mount_and_reuse(
        self, mock_send, mount_prefix, workload_cert_config
    ):
        mock_send.return_value = make_response()
        session = requests.Session()
        base_adapter = requests.adapters.HTTPAdapter(
            max_retries=3, pool_connections=4, pool_maxsize=8, pool_block=True
        )
        session.mount(mount_prefix, base_adapter)
        https_adapter = session.adapters["https://"]
        request = google.auth.transport.requests.Request(session)

        request("https://oauth2.googleapis.com/token")
        # Verify mounting replaces session.adapters rather than mutating it in place.
        adapters_iter = iter(session.adapters.items())
        next(adapters_iter)
        request("https://iamcredentials.mtls.googleapis.com/v1/token")
        list(adapters_iter)
        adapters_after_mount = session.adapters
        adapters_snapshot = session.adapters.copy()
        request("https://iamcredentials.mtls.googleapis.com/v1/token")
        assert session.adapters is adapters_after_mount
        assert session.adapters == adapters_snapshot
        request("https://STS.mtls.googleapis.com")

        mtls_adapter = session.adapters["https://iamcredentials.mtls.googleapis.com/"]
        assert isinstance(
            mtls_adapter, google.auth.transport.requests._MutualTlsAdapter
        )
        assert mtls_adapter.max_retries.total == 3
        assert mtls_adapter._pool_connections == 4
        assert mtls_adapter._pool_maxsize == 8
        assert mtls_adapter._pool_block is True
        assert session.adapters["https://sts.mtls.googleapis.com/"] is mtls_adapter
        sent_adapters = [call.args[0] for call in mock_send.call_args_list]
        assert sent_adapters == [
            https_adapter,
            mtls_adapter,
            mtls_adapter,
            mtls_adapter,
        ]

    @pytest.mark.parametrize(
        "mount_prefix,adapter_cls",
        [
            ("https://", requests.adapters.BaseAdapter),
            (
                "https://iamcredentials.mtls.googleapis.com/",
                requests.adapters.BaseAdapter,
            ),
            (
                "https://iamcredentials.mtls.googleapis.com/v1/token",
                requests.adapters.BaseAdapter,
            ),
            ("https://", google.auth.transport.requests._MutualTlsAdapter),
            (
                "https://iamcredentials.mtls.googleapis.com/v1/",
                requests.adapters.HTTPAdapter,
            ),
        ],
    )
    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_preserves_custom_adapter(
        self,
        mock_send,
        mount_prefix,
        adapter_cls,
        workload_cert_config,
    ):
        mock_send.return_value = make_response()
        session = requests.Session()
        if adapter_cls is google.auth.transport.requests._MutualTlsAdapter:
            custom_adapter = adapter_cls(
                pytest.public_cert_bytes, pytest.private_key_bytes
            )
        elif adapter_cls is requests.adapters.BaseAdapter:
            custom_adapter = AdapterStub([make_response()])
        else:
            custom_adapter = adapter_cls()
        session.mount(mount_prefix, custom_adapter)
        adapters_before = session.adapters
        adapters_snapshot = session.adapters.copy()
        request = google.auth.transport.requests.Request(session)

        request("https://IAMCREDENTIALS.mtls.googleapis.com/v1/token")

        assert session.adapters is adapters_before
        assert session.adapters == adapters_snapshot
        assert (
            session.get_adapter("https://iamcredentials.mtls.googleapis.com/v1/token")
            is custom_adapter
        )
        assert request._mtls_adapter is None

    @pytest.mark.parametrize(
        "use_cert,request_kwargs",
        [
            ("false", {}),
            ("true", {"cert": ("cert.pem", "key.pem")}),
        ],
    )
    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_skips_when_disabled_or_explicit_cert(
        self,
        mock_send,
        use_cert,
        request_kwargs,
        workload_cert_config,
        monkeypatch,
    ):
        mock_send.return_value = make_response()
        monkeypatch.setenv(environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE, use_cert)
        session = requests.Session()
        request = google.auth.transport.requests.Request(session)

        request("https://iamcredentials.mtls.googleapis.com/v1/token", **request_kwargs)

        assert "https://iamcredentials.mtls.googleapis.com/" not in session.adapters
        assert request._mtls_adapter is None

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    @mock.patch.object(
        google.auth.transport._mtls_helper,
        "get_client_cert_and_key",
        return_value=(False, None, None),
    )
    def test_mtls_no_cert_caches_unavailable(
        self, mock_get_cert, mock_send, monkeypatch
    ):
        mock_send.return_value = make_response()
        monkeypatch.setenv(environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE, "true")
        session = requests.Session()
        request = google.auth.transport.requests.Request(session)

        request("https://iamcredentials.mtls.googleapis.com/v1/token")
        request("https://iamcredentials.mtls.googleapis.com/v1/token")

        assert "https://iamcredentials.mtls.googleapis.com/" not in session.adapters
        assert request._mtls_unavailable is True
        mock_get_cert.assert_called_once()

    @pytest.mark.parametrize(
        "cert_bytes,expected_cause",
        [
            (None, FileNotFoundError),
            (b"invalid", exceptions.ClientCertError),
            (
                b"-----BEGIN CERTIFICATE-----\ninvalid\n-----END CERTIFICATE-----\n",
                exceptions.MutualTLSChannelError,
            ),
        ],
    )
    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_error_raises_transport_error_and_recovers(
        self, mock_send, cert_bytes, expected_cause, workload_cert_config
    ):
        mock_send.return_value = make_response()
        if cert_bytes is None:
            workload_cert_config.remove()
        else:
            workload_cert_config.write_binary(cert_bytes)

        request = google.auth.transport.requests.Request(requests.Session())
        with pytest.raises(exceptions.TransportError) as exc_info:
            request("https://iamcredentials.mtls.googleapis.com/v1/token")
        assert isinstance(exc_info.value.__cause__, expected_cause)
        assert request._mtls_unavailable is False

        workload_cert_config.write_binary(pytest.public_cert_bytes)
        request("https://iamcredentials.mtls.googleapis.com/v1/token")
        assert isinstance(
            request._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )

    @pytest.mark.parametrize(
        "request_kwargs",
        [
            {"verify": "/nonexistent/path/ca.pem"},
            {"cert": ("/nonexistent/path/cert.pem", "/nonexistent/path/key.pem")},
        ],
    )
    def test_session_request_missing_cert_or_ca_raises_oserror(self, request_kwargs):
        request = google.auth.transport.requests.Request(requests.Session())

        with pytest.raises(OSError) as exc_info:
            request("https://oauth2.googleapis.com/token", **request_kwargs)

        assert not isinstance(exc_info.value, exceptions.TransportError)

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_deepcopy(self, mock_send, workload_cert_config):
        mock_send.return_value = make_response()
        request = google.auth.transport.requests.Request(requests.Session())
        request("https://iamcredentials.mtls.googleapis.com/v1/token")

        copied_request = copy.deepcopy(request)
        copied_request("https://iamcredentials.mtls.googleapis.com/v1/token")

        assert copied_request.session is not request.session
        assert copied_request._mtls_lock is not request._mtls_lock
        assert copied_request._mtls_adapter is not request._mtls_adapter
        assert (
            copied_request._mtls_adapter._ctx_poolmanager
            is request._mtls_adapter._ctx_poolmanager
        )
        assert (
            copied_request._mtls_adapter._ctx_proxymanager
            is request._mtls_adapter._ctx_proxymanager
        )
        assert (
            copied_request._mtls_adapter.poolmanager
            is not request._mtls_adapter.poolmanager
        )
        assert mock_send.call_args_list[1].args[0] is copied_request._mtls_adapter

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_pickle(self, mock_send, workload_cert_config):
        mock_send.return_value = make_response()
        request = google.auth.transport.requests.Request(requests.Session())
        request("https://iamcredentials.mtls.googleapis.com/v1/token")
        prefix = "https://iamcredentials.mtls.googleapis.com/"
        assert isinstance(
            request._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )

        unpickled_request = pickle.loads(pickle.dumps(request))

        assert unpickled_request.session is not request.session
        assert unpickled_request._mtls_lock is not request._mtls_lock
        assert unpickled_request._mtls_adapter is None
        assert unpickled_request._mtls_unavailable is False
        assert (
            type(unpickled_request.session.adapters[prefix])
            is requests.adapters.HTTPAdapter
        )

        unpickled_request("https://iamcredentials.mtls.googleapis.com/v1/token")
        assert isinstance(
            unpickled_request._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )
        assert (
            unpickled_request.session.adapters[prefix]
            is unpickled_request._mtls_adapter
        )
        assert mock_send.call_args_list[1].args[0] is unpickled_request._mtls_adapter

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_legacy_pickle(self, mock_send, workload_cert_config):
        mock_send.return_value = make_response()
        request = google.auth.transport.requests.Request(requests.Session())
        with mock.patch.object(
            google.auth.transport.requests.Request,
            "__getstate__",
            return_value={"session": request.session},
        ):
            legacy_pickled = pickle.dumps(request)
        unpickled_legacy = pickle.loads(legacy_pickled)
        assert unpickled_legacy._mtls_adapter is None
        assert unpickled_legacy._mtls_unavailable is False

        unpickled_legacy("https://iamcredentials.mtls.googleapis.com/v1/token")
        prefix = "https://iamcredentials.mtls.googleapis.com/"
        assert isinstance(
            unpickled_legacy._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )
        assert (
            unpickled_legacy.session.adapters[prefix] is unpickled_legacy._mtls_adapter
        )
        assert mock_send.call_args.args[0] is unpickled_legacy._mtls_adapter

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_request_verify_false(self, mock_send, workload_cert_config):
        mock_send.return_value = make_response()
        request = google.auth.transport.requests.Request(requests.Session())

        response = request(
            "https://iamcredentials.mtls.googleapis.com/v1/token", verify=False
        )

        assert response.status == http_client.OK
        mock_send.assert_called_once()
        assert isinstance(
            mock_send.call_args.args[0],
            google.auth.transport.requests._MutualTlsAdapter,
        )
        assert mock_send.call_args.kwargs["verify"] is False

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_single_origin_rotation(
        self, mock_send, es256_cert_and_key
    ):
        mock_send.return_value = make_response()
        active_pair = [pytest.public_cert_bytes, pytest.private_key_bytes]
        source_calls = 0

        def cert_source():
            nonlocal source_calls
            source_calls += 1
            return active_pair[0], active_pair[1]

        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=cert_source
        )
        session = requests.Session()
        base_adapter = requests.adapters.HTTPAdapter(
            max_retries=3, pool_connections=4, pool_maxsize=8, pool_block=True
        )
        session.mount("https://", base_adapter)
        request = google.auth.transport.requests.Request(
            session, cert_manager=cert_manager
        )
        assert request._cert_manager is cert_manager

        request("https://oauth2.googleapis.com/token")
        assert cert_manager.generation_id == 0
        assert source_calls == 0

        url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        prefix = "https://iamcredentials.mtls.googleapis.com/"
        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "secure_cert_key_paths",
            wraps=google.auth.transport._mtls_helper.secure_cert_key_paths,
        ) as cert_key_spy:
            request(url)
            assert cert_manager.generation_id == 1
            assert source_calls == 1
            adapter_gen1 = request._mtls_adapter
            assert isinstance(
                adapter_gen1, google.auth.transport.requests._MutualTlsAdapter
            )
            assert session.adapters[prefix] is adapter_gen1
            assert adapter_gen1.max_retries.total == 3
            assert adapter_gen1._pool_connections == 4
            assert adapter_gen1._pool_maxsize == 8
            assert adapter_gen1._pool_block is True

            adapters_after_gen1 = session.adapters
            request(url)
            assert session.adapters is adapters_after_gen1
            assert request._mtls_adapter is adapter_gen1
            assert source_calls == 1

            active_pair[:] = list(es256_cert_and_key)
            assert cert_manager.refresh() is True
            assert cert_manager.generation_id == 2

            # Verify rotation swaps session.adapters atomically rather than in place.
            adapters_iter = iter(session.adapters.items())
            next(adapters_iter)
            request(url)
            list(adapters_iter)

        assert cert_key_spy.call_args_list == [
            mock.call(pytest.public_cert_bytes, pytest.private_key_bytes),
            mock.call(*es256_cert_and_key),
        ]
        adapter_gen2 = request._mtls_adapter
        assert isinstance(
            adapter_gen2, google.auth.transport.requests._MutualTlsAdapter
        )
        assert adapter_gen2 is not adapter_gen1
        assert adapter_gen2._ctx_poolmanager is not adapter_gen1._ctx_poolmanager
        assert session.adapters[prefix] is adapter_gen2
        assert adapter_gen2.max_retries.total == 3
        assert adapter_gen2._pool_connections == 4
        assert adapter_gen2._pool_maxsize == 8
        assert adapter_gen2._pool_block is True
        assert request._adapter_generation_id == 2
        assert [call.args[0] for call in mock_send.call_args_list] == [
            base_adapter,
            adapter_gen1,
            adapter_gen1,
            adapter_gen2,
        ]

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_multi_origin_rotation(
        self, mock_send, es256_cert_and_key
    ):
        mock_send.return_value = make_response()
        active_pair = [pytest.public_cert_bytes, pytest.private_key_bytes]
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (active_pair[0], active_pair[1])
        )
        assert cert_manager.refresh() is True

        session = requests.Session()
        base_adapter = requests.adapters.HTTPAdapter(
            max_retries=2, pool_connections=5, pool_maxsize=6, pool_block=True
        )
        session.mount("https://iamcredentials.mtls.googleapis.com/", base_adapter)
        request = google.auth.transport.requests.Request(
            session, cert_manager=cert_manager
        )

        iam_url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        sts_url = "https://sts.mtls.googleapis.com/v1/token"
        oauth_url = "https://oauth2.mtls.googleapis.com/token"
        iam_prefix = "https://iamcredentials.mtls.googleapis.com/"
        sts_prefix = "https://sts.mtls.googleapis.com/"
        oauth_prefix = "https://oauth2.mtls.googleapis.com/"

        request(iam_url)
        adapter_gen1 = request._mtls_adapter
        request(sts_url)
        assert session.adapters[iam_prefix] is adapter_gen1
        assert session.adapters[sts_prefix] is adapter_gen1

        active_pair[:] = list(es256_cert_and_key)
        assert cert_manager.refresh() is True

        request(iam_url)
        adapter_gen2 = request._mtls_adapter
        assert adapter_gen2 is not adapter_gen1
        assert session.adapters[iam_prefix] is adapter_gen2
        assert session.adapters[sts_prefix] is adapter_gen2

        adapters_after_gen2 = session.adapters
        request(sts_url)
        assert session.adapters is adapters_after_gen2

        # Rotate again and trigger the swap from a new third origin.
        active_pair[:] = [pytest.public_cert_bytes, pytest.private_key_bytes]
        assert cert_manager.refresh() is True

        request(oauth_url)
        adapter_gen3 = request._mtls_adapter
        assert adapter_gen3 is not adapter_gen2
        assert adapter_gen3.max_retries.total == 2
        assert adapter_gen3._pool_connections == 5
        assert adapter_gen3._pool_maxsize == 6
        assert adapter_gen3._pool_block is True
        assert session.adapters[iam_prefix] is adapter_gen3
        assert session.adapters[sts_prefix] is adapter_gen3
        assert session.adapters[oauth_prefix] is adapter_gen3

        request(iam_url)
        request(sts_url)
        assert [call.args[0] for call in mock_send.call_args_list] == [
            adapter_gen1,
            adapter_gen1,
            adapter_gen2,
            adapter_gen2,
            adapter_gen3,
            adapter_gen3,
            adapter_gen3,
        ]

    @pytest.mark.parametrize(
        "mount_prefix,custom_adapter_factory",
        [
            ("https://", lambda: AdapterStub([make_response(), make_response()])),
            (
                "https://iamcredentials.mtls.googleapis.com/",
                lambda: google.auth.transport.requests._MutualTlsAdapter(
                    pytest.public_cert_bytes, pytest.private_key_bytes
                ),
            ),
            (
                "https://iamcredentials.mtls.googleapis.com/v1/",
                lambda: requests.adapters.HTTPAdapter(),
            ),
        ],
    )
    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_preserves_custom_and_subpath_adapters(
        self, mock_send, mount_prefix, custom_adapter_factory, es256_cert_and_key
    ):
        mock_send.return_value = make_response()
        active_pair = [pytest.public_cert_bytes, pytest.private_key_bytes]
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (active_pair[0], active_pair[1])
        )
        assert cert_manager.refresh() is True

        session = requests.Session()
        custom_adapter = custom_adapter_factory()
        session.mount(mount_prefix, custom_adapter)
        adapters_before = session.adapters
        adapters_snapshot = session.adapters.copy()

        request = google.auth.transport.requests.Request(
            session, cert_manager=cert_manager
        )
        url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        request(url)

        active_pair[:] = list(es256_cert_and_key)
        assert cert_manager.refresh() is True
        request(url)

        assert session.adapters is adapters_before
        assert session.adapters == adapters_snapshot
        assert session.get_adapter(url) is custom_adapter
        assert request._mtls_adapter is None

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_rotation_leaves_other_custom_origin_intact(
        self, mock_send, es256_cert_and_key
    ):
        mock_send.return_value = make_response()
        active_pair = [pytest.public_cert_bytes, pytest.private_key_bytes]
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (active_pair[0], active_pair[1])
        )
        assert cert_manager.refresh() is True

        session = requests.Session()
        custom_mtls_adapter = google.auth.transport.requests._MutualTlsAdapter(
            pytest.public_cert_bytes, pytest.private_key_bytes
        )
        sts_prefix = "https://sts.mtls.googleapis.com/"
        iam_prefix = "https://iamcredentials.mtls.googleapis.com/"
        session.mount(sts_prefix, custom_mtls_adapter)

        request = google.auth.transport.requests.Request(
            session, cert_manager=cert_manager
        )
        request("https://iamcredentials.mtls.googleapis.com/v1/token")
        adapter_gen1 = request._mtls_adapter
        request("https://sts.mtls.googleapis.com/v1/token")

        active_pair[:] = list(es256_cert_and_key)
        assert cert_manager.refresh() is True
        request("https://iamcredentials.mtls.googleapis.com/v1/token")
        adapter_gen2 = request._mtls_adapter

        assert adapter_gen2 is not adapter_gen1
        assert session.adapters[iam_prefix] is adapter_gen2
        assert session.adapters[sts_prefix] is custom_mtls_adapter

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    @mock.patch.object(
        google.auth.transport._mtls_helper,
        "get_client_ssl_credentials",
        return_value=(False, None, None, None),
    )
    def test_mtls_cert_manager_no_default_cert_skips_mount(
        self, mock_get_ssl, mock_send
    ):
        mock_send.return_value = make_response()
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager()
        session = requests.Session()
        request = google.auth.transport.requests.Request(
            session, cert_manager=cert_manager
        )

        request("https://iamcredentials.mtls.googleapis.com/v1/token")

        assert "https://iamcredentials.mtls.googleapis.com/" not in session.adapters
        assert request._mtls_adapter is None
        assert request._mtls_unavailable is False
        mock_get_ssl.assert_called_once_with(generate_encrypted_key=False)

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_initial_load_error_raises_and_recovers(self, mock_send):
        mock_send.return_value = make_response()
        active_pair = [b"invalid", b"invalid"]
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (active_pair[0], active_pair[1])
        )
        request = google.auth.transport.requests.Request(
            requests.Session(), cert_manager=cert_manager
        )
        url = "https://iamcredentials.mtls.googleapis.com/v1/token"

        with pytest.raises(exceptions.TransportError) as exc_info:
            request(url)
        assert isinstance(exc_info.value.__cause__, exceptions.ClientCertError)
        assert request._mtls_adapter is None

        active_pair[:] = [pytest.public_cert_bytes, pytest.private_key_bytes]
        request(url)
        assert isinstance(
            request._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )
        assert mock_send.call_args.args[0] is request._mtls_adapter

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_explicit_cert_kwarg_and_env_override(
        self, mock_send, monkeypatch
    ):
        mock_send.return_value = make_response()
        monkeypatch.setenv(environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE, "false")
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (
                pytest.public_cert_bytes,
                pytest.private_key_bytes,
            )
        )
        session = requests.Session()
        request = google.auth.transport.requests.Request(
            session, cert_manager=cert_manager
        )
        url = "https://iamcredentials.mtls.googleapis.com/v1/token"

        # Explicit cert= kwarg bypasses mTLS adapter configuration.
        request(url, cert=("cert.pem", "key.pem"))
        assert "https://iamcredentials.mtls.googleapis.com/" not in session.adapters
        assert request._mtls_adapter is None

        # Without cert= kwarg, an explicit cert_manager mounts even if the env var is false.
        request(url)
        assert isinstance(
            request._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )
        assert mock_send.call_args.args[0] is request._mtls_adapter

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_deepcopy_and_copy_rotate(
        self, mock_send, es256_cert_and_key
    ):
        mock_send.return_value = make_response()
        active_pair = [pytest.public_cert_bytes, pytest.private_key_bytes]
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (active_pair[0], active_pair[1])
        )
        assert cert_manager.refresh() is True

        url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        prefix = "https://iamcredentials.mtls.googleapis.com/"
        request = google.auth.transport.requests.Request(
            requests.Session(), cert_manager=cert_manager
        )
        request(url)
        orig_gen1 = request._mtls_adapter

        copied_request = copy.deepcopy(request)
        assert copied_request._cert_manager is cert_manager
        assert copied_request.session is not request.session
        assert copied_request._mtls_lock is not request._mtls_lock
        assert copied_request._mtls_adapter is not orig_gen1
        assert copied_request.session.adapters[prefix] is copied_request._mtls_adapter
        assert copied_request._adapter_generation_id == 1

        copied_gen1 = copied_request._mtls_adapter
        copied_request(url)
        assert copied_request._mtls_adapter is copied_gen1

        active_pair[:] = list(es256_cert_and_key)
        assert cert_manager.refresh() is True

        copied_request(url)
        copied_gen2 = copied_request._mtls_adapter
        assert copied_gen2 is not copied_gen1
        assert copied_request.session.adapters[prefix] is copied_gen2
        assert copied_request._adapter_generation_id == 2
        # Original request has its own session and still holds gen 1 until called.
        assert request._mtls_adapter is orig_gen1

        request(url)
        orig_gen2 = request._mtls_adapter
        assert orig_gen2 is not orig_gen1
        assert orig_gen2 is not copied_gen2
        assert request.session.adapters[prefix] is orig_gen2
        assert request._adapter_generation_id == 2

        shallow_request = copy.copy(request)
        assert shallow_request._cert_manager is cert_manager
        assert shallow_request.session is request.session
        assert shallow_request._mtls_lock is request._mtls_lock

        active_pair[:] = [pytest.public_cert_bytes, pytest.private_key_bytes]
        assert cert_manager.refresh() is True
        shallow_request(url)
        gen3_adapter = shallow_request._mtls_adapter
        assert gen3_adapter is not orig_gen2
        assert request._mtls_adapter is gen3_adapter
        assert shallow_request.session.adapters[prefix] is gen3_adapter
        assert shallow_request._adapter_generation_id == 3

        # Alternating back to the original Request on the next rotation stays in sync.
        active_pair[:] = list(es256_cert_and_key)
        assert cert_manager.refresh() is True
        request(url)
        gen4_adapter = request._mtls_adapter
        assert gen4_adapter is not gen3_adapter
        assert shallow_request._mtls_adapter is gen4_adapter
        assert request.session.adapters[prefix] is gen4_adapter
        assert request._adapter_generation_id == 4

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_deepcopy_serializes_with_rotation(
        self, mock_send, es256_cert_and_key
    ):
        mock_send.return_value = make_response()
        active_pair = [pytest.public_cert_bytes, pytest.private_key_bytes]
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (active_pair[0], active_pair[1])
        )
        assert cert_manager.refresh() is True

        url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        prefix = "https://iamcredentials.mtls.googleapis.com/"
        request = google.auth.transport.requests.Request(
            requests.Session(), cert_manager=cert_manager
        )
        request(url)

        active_pair[:] = list(es256_cert_and_key)
        assert cert_manager.refresh() is True

        in_rotation = threading.Event()
        allow_finish = threading.Event()
        orig_secure = google.auth.transport._mtls_helper.secure_cert_key_paths

        def blocking_secure(cert, key, passphrase=None):
            in_rotation.set()
            allow_finish.wait(timeout=5)
            return orig_secure(cert, key, passphrase)

        copied_holder = []
        copy_done = threading.Event()

        def do_deepcopy():
            copied_holder.append(copy.deepcopy(request))
            copy_done.set()

        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "secure_cert_key_paths",
            side_effect=blocking_secure,
        ):
            rotate_thread = threading.Thread(target=request, args=(url,))
            rotate_thread.start()
            assert in_rotation.wait(timeout=5)

            copy_thread = threading.Thread(target=do_deepcopy)
            copy_thread.start()
            # Deepcopy must block on _mtls_lock until the rotation finishes.
            assert not copy_done.wait(timeout=0.05)

            allow_finish.set()
            rotate_thread.join()
            copy_thread.join()

        copied_request = copied_holder[0]
        assert copied_request._adapter_generation_id == 2
        assert copied_request.session.adapters[prefix] is copied_request._mtls_adapter

        # Copied request continues rotating cleanly on future generations.
        active_pair[:] = [pytest.public_cert_bytes, pytest.private_key_bytes]
        assert cert_manager.refresh() is True
        copied_gen2 = copied_request._mtls_adapter
        copied_request(url)
        assert copied_request._mtls_adapter is not copied_gen2
        assert copied_request._adapter_generation_id == 3

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_cold_start_coalesces_concurrent_requests(
        self, mock_send
    ):
        mock_send.return_value = make_response()
        source_calls = 0

        def slow_cert_source():
            nonlocal source_calls
            source_calls += 1
            threading.Event().wait(0.05)
            return pytest.public_cert_bytes, pytest.private_key_bytes

        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=slow_cert_source
        )
        base_request = google.auth.transport.requests.Request(
            requests.Session(), cert_manager=cert_manager
        )
        num_threads = 4
        request_instances = [copy.deepcopy(base_request) for _ in range(num_threads)]
        url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        barrier = threading.Barrier(num_threads)
        errors = []

        def worker(req):
            try:
                barrier.wait(timeout=5)
                req(url)
            except Exception as exc:  # pragma: NO COVER
                errors.append(exc)

        with mock.patch.object(
            cert_manager, "refresh", wraps=cert_manager.refresh
        ) as refresh_spy:
            threads = [
                threading.Thread(target=worker, args=(req,))
                for req in request_instances
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        assert not errors
        assert source_calls == 1
        assert refresh_spy.call_count >= 1
        assert all(
            call == mock.call(expected_generation=0)
            for call in refresh_spy.call_args_list
        )
        assert all(req._adapter_generation_id == 1 for req in request_instances)

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_rotation_adapter_error_keeps_previous_adapter(
        self, mock_send, es256_cert_and_key
    ):
        mock_send.return_value = make_response()
        active_pair = [pytest.public_cert_bytes, pytest.private_key_bytes]
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (active_pair[0], active_pair[1])
        )
        url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        prefix = "https://iamcredentials.mtls.googleapis.com/"
        request = google.auth.transport.requests.Request(
            requests.Session(), cert_manager=cert_manager
        )
        request(url)
        adapter_gen1 = request._mtls_adapter

        # Rotate to a valid cert paired with a mismatched key so refresh() advances
        # generation_id, but _MutualTlsAdapter raises MutualTLSChannelError.
        active_pair[:] = [es256_cert_and_key[0], pytest.private_key_bytes]
        assert cert_manager.refresh() is True

        with pytest.raises(exceptions.TransportError) as exc_info:
            request(url)
        assert isinstance(exc_info.value.__cause__, exceptions.MutualTLSChannelError)
        assert request._mtls_adapter is adapter_gen1
        assert request._adapter_generation_id == 1
        assert request.session.adapters[prefix] is adapter_gen1

        # Recover cleanly on the next valid rotation.
        active_pair[:] = [pytest.public_cert_bytes, pytest.private_key_bytes]
        assert cert_manager.refresh() is True
        request(url)
        assert request._mtls_adapter is not adapter_gen1
        assert request._adapter_generation_id == 3
        assert request.session.adapters[prefix] is request._mtls_adapter
        assert mock_send.call_args.args[0] is request._mtls_adapter

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_released_pickle_resets_adapter(self, mock_send, workload_cert_config):
        mock_send.return_value = make_response()
        url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        prefix = "https://iamcredentials.mtls.googleapis.com/"
        request = google.auth.transport.requests.Request(requests.Session())
        request(url)
        assert isinstance(
            request._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )

        # Simulate a pickle produced by released google-auth where __getstate__
        # preserved _mtls_adapter (which reduces to plain HTTPAdapter on unpickle).
        released_state = {
            "session": request.session,
            "_mtls_adapter": request._mtls_adapter,
            "_mtls_unavailable": False,
            "_mtls_lock": None,
        }
        with mock.patch.object(
            google.auth.transport.requests.Request,
            "__getstate__",
            return_value=released_state,
        ):
            released_pickled = pickle.dumps(request)

        unpickled = pickle.loads(released_pickled)
        assert unpickled._cert_manager is None
        assert unpickled._mtls_adapter is None
        assert unpickled._adapter_generation_id is None
        assert unpickled._mtls_unavailable is False
        assert type(unpickled.session.adapters[prefix]) is requests.adapters.HTTPAdapter

        unpickled(url)
        assert isinstance(
            unpickled._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )
        assert unpickled.session.adapters[prefix] is unpickled._mtls_adapter
        assert mock_send.call_args.args[0] is unpickled._mtls_adapter

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_pickle_with_closure(
        self, mock_send, workload_cert_config
    ):
        mock_send.return_value = make_response()
        cert = pytest.public_cert_bytes
        key = pytest.private_key_bytes
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (cert, key)
        )
        assert cert_manager.refresh() is True

        url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        prefix = "https://iamcredentials.mtls.googleapis.com/"
        request = google.auth.transport.requests.Request(
            requests.Session(), cert_manager=cert_manager
        )
        request(url)
        assert isinstance(
            request._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )

        unpickled_request = pickle.loads(pickle.dumps(request))
        assert unpickled_request._cert_manager is None
        assert unpickled_request._mtls_adapter is None
        assert unpickled_request._adapter_generation_id is None
        assert unpickled_request._mtls_lock is not request._mtls_lock
        assert (
            type(unpickled_request.session.adapters[prefix])
            is requests.adapters.HTTPAdapter
        )

        unpickled_request(url)
        assert isinstance(
            unpickled_request._mtls_adapter,
            google.auth.transport.requests._MutualTlsAdapter,
        )
        assert (
            unpickled_request.session.adapters[prefix]
            is unpickled_request._mtls_adapter
        )
        assert mock_send.call_args.args[0] is unpickled_request._mtls_adapter

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_attached_after_static_mount(
        self, mock_send, workload_cert_config, es256_cert_and_key
    ):
        mock_send.return_value = make_response()
        url = "https://iamcredentials.mtls.googleapis.com/v1/token"
        prefix = "https://iamcredentials.mtls.googleapis.com/"
        request = google.auth.transport.requests.Request(requests.Session())

        request(url)
        static_adapter = request._mtls_adapter
        assert isinstance(
            static_adapter, google.auth.transport.requests._MutualTlsAdapter
        )

        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: es256_cert_and_key
        )
        assert cert_manager.refresh() is True
        request._cert_manager = cert_manager

        request(url)
        managed_adapter = request._mtls_adapter
        assert managed_adapter is not static_adapter
        assert request.session.adapters[prefix] is managed_adapter
        assert request._adapter_generation_id == 1
        assert [call.args[0] for call in mock_send.call_args_list] == [
            static_adapter,
            managed_adapter,
        ]

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_mtls_cert_manager_concurrent_rotation(self, mock_send, es256_cert_and_key):
        mock_send.return_value = make_response()
        active_pair = [pytest.public_cert_bytes, pytest.private_key_bytes]
        cert_manager = google.auth.transport._mtls_helper._MtlsCertManager(
            client_cert_source=lambda: (active_pair[0], active_pair[1])
        )
        assert cert_manager.refresh() is True

        request = google.auth.transport.requests.Request(
            requests.Session(), cert_manager=cert_manager
        )
        urls = [
            "https://iamcredentials.mtls.googleapis.com/v1/token",
            "https://sts.mtls.googleapis.com/v1/token",
        ]
        for url in urls:
            request(url)
        adapter_gen1 = request._mtls_adapter

        active_pair[:] = list(es256_cert_and_key)
        assert cert_manager.refresh() is True

        num_threads = 6
        barrier = threading.Barrier(num_threads)
        errors = []

        def worker(index):
            try:
                barrier.wait(timeout=5)
                request(urls[index % len(urls)])
            except Exception as exc:  # pragma: NO COVER
                errors.append(exc)

        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "secure_cert_key_paths",
            wraps=google.auth.transport._mtls_helper.secure_cert_key_paths,
        ) as cert_key_spy:
            threads = [
                threading.Thread(target=worker, args=(i,)) for i in range(num_threads)
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        assert not errors
        cert_key_spy.assert_called_once_with(*es256_cert_and_key)
        adapter_gen2 = request._mtls_adapter
        assert adapter_gen2 is not adapter_gen1
        sent_after_rotation = [
            call.args[0] for call in mock_send.call_args_list[len(urls) :]
        ]
        assert len(sent_after_rotation) == num_threads
        assert all(adapter is adapter_gen2 for adapter in sent_after_rotation)


class TestTimeoutGuard(object):
    def make_guard(self, *args, **kwargs):
        return google.auth.transport.requests.TimeoutGuard(*args, **kwargs)

    def test_tracks_elapsed_time_w_numeric_timeout(self, frozen_time):
        with self.make_guard(timeout=10) as guard:
            frozen_time.tick(delta=datetime.timedelta(seconds=3.8))
        assert guard.remaining_timeout == 6.2

    def test_tracks_elapsed_time_w_tuple_timeout(self, frozen_time):
        with self.make_guard(timeout=(16, 19)) as guard:
            frozen_time.tick(delta=datetime.timedelta(seconds=3.8))
        assert guard.remaining_timeout == (12.2, 15.2)

    def test_noop_if_no_timeout(self, frozen_time):
        with self.make_guard(timeout=None) as guard:
            frozen_time.tick(delta=datetime.timedelta(days=3650))
        # NOTE: no timeout error raised, despite years have passed
        assert guard.remaining_timeout is None

    def test_timeout_error_w_numeric_timeout(self, frozen_time):
        with pytest.raises(requests.exceptions.Timeout):
            with self.make_guard(timeout=10) as guard:
                frozen_time.tick(delta=datetime.timedelta(seconds=10.001))
        assert guard.remaining_timeout == pytest.approx(-0.001)

    def test_timeout_error_w_tuple_timeout(self, frozen_time):
        with pytest.raises(requests.exceptions.Timeout):
            with self.make_guard(timeout=(11, 10)) as guard:
                frozen_time.tick(delta=datetime.timedelta(seconds=10.001))
        assert guard.remaining_timeout == pytest.approx((0.999, -0.001))

    def test_custom_timeout_error_type(self, frozen_time):
        class FooError(Exception):
            pass

        with pytest.raises(FooError):
            with self.make_guard(timeout=1, timeout_error_type=FooError):
                frozen_time.tick(delta=datetime.timedelta(seconds=2))

    def test_lets_suite_errors_bubble_up(self, frozen_time):
        with pytest.raises(IndexError):
            with self.make_guard(timeout=1):
                [1, 2, 3][3]


class CredentialsStub(google.auth.credentials.Credentials):
    def __init__(self, token="token"):
        super(CredentialsStub, self).__init__()
        self.token = token

    def apply(self, headers, token=None):
        headers["authorization"] = self.token

    def before_request(self, request, method, url, headers):
        self.apply(headers)

    def refresh(self, request):
        self.token += "1"

    def with_quota_project(self, quota_project_id):
        raise NotImplementedError()


class TimeTickCredentialsStub(CredentialsStub):
    """Credentials that spend some (mocked) time when refreshing a token."""

    def __init__(self, time_tick, token="token"):
        self._time_tick = time_tick
        super(TimeTickCredentialsStub, self).__init__(token=token)

    def refresh(self, request):
        self._time_tick()
        super(TimeTickCredentialsStub, self).refresh(requests)


class AdapterStub(requests.adapters.BaseAdapter):
    def __init__(self, responses, headers=None):
        super(AdapterStub, self).__init__()
        self.responses = responses
        self.requests = []
        self.headers = headers or {}

    def send(self, request, **kwargs):
        # pylint: disable=arguments-differ
        # request is the only required argument here and the only argument
        # we care about.
        self.requests.append(request)
        return self.responses.pop(0)

    def close(self):  # pragma: NO COVER
        # pylint wants this to be here because it's abstract in the base
        # class, but requests never actually calls it.
        return


class TimeTickAdapterStub(AdapterStub):
    """Adapter that spends some (mocked) time when making a request."""

    def __init__(self, time_tick, responses, headers=None):
        self._time_tick = time_tick
        super(TimeTickAdapterStub, self).__init__(responses, headers=headers)

    def send(self, request, **kwargs):
        self._time_tick()
        return super(TimeTickAdapterStub, self).send(request, **kwargs)


class TestMutualTlsAdapter(object):
    @mock.patch.object(requests.adapters.HTTPAdapter, "init_poolmanager")
    @mock.patch.object(requests.adapters.HTTPAdapter, "proxy_manager_for")
    def test_success(self, mock_proxy_manager_for, mock_init_poolmanager):
        adapter = google.auth.transport.requests._MutualTlsAdapter(
            pytest.public_cert_bytes, pytest.private_key_bytes
        )

        assert adapter._ctx_poolmanager.check_hostname is False
        assert adapter._ctx_proxymanager.check_hostname is False

        adapter.init_poolmanager()
        mock_init_poolmanager.assert_called_with(ssl_context=adapter._ctx_poolmanager)

        adapter.proxy_manager_for()
        mock_proxy_manager_for.assert_called_with(ssl_context=adapter._ctx_proxymanager)

    def test_verify_false_compatibility(self):
        adapter = google.auth.transport.requests._MutualTlsAdapter(
            pytest.public_cert_bytes, pytest.private_key_bytes
        )

        adapter._ctx_poolmanager.verify_mode = ssl.CERT_NONE
        adapter._ctx_proxymanager.verify_mode = ssl.CERT_NONE
        assert adapter._ctx_poolmanager.verify_mode == ssl.CERT_NONE
        assert adapter._ctx_proxymanager.verify_mode == ssl.CERT_NONE

    def test_invalid_cert_or_key(self):
        with pytest.raises(exceptions.MutualTLSChannelError):
            google.auth.transport.requests._MutualTlsAdapter(
                b"invalid cert", b"invalid key"
            )

    @mock.patch("google.auth.transport.requests._mtls_helper.secure_cert_key_paths")
    def test_setup_error_raises_mutual_tls_channel_error(self, mock_secure_paths):
        mock_secure_paths.side_effect = OSError("Disk full")
        with pytest.raises(exceptions.MutualTLSChannelError) as exc_info:
            google.auth.transport.requests._MutualTlsAdapter(b"cert", b"key")
        assert "Failed to configure client certificate" in str(exc_info.value)
        assert isinstance(exc_info.value.__cause__, OSError)


def make_response(status=http_client.OK, data=None):
    response = requests.Response()
    response.status_code = status
    response._content = data
    return response


class TestAuthorizedSession(object):
    TEST_URL = "http://example.com/"
    MTLS_TEST_URL = "https://example.mtls.googleapis.com/"

    def test_constructor(self):
        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials
        )

        assert authed_session.credentials == mock.sentinel.credentials

    def test_constructor_with_auth_request(self):
        http = mock.create_autospec(requests.Session)
        auth_request = google.auth.transport.requests.Request(http)

        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials, auth_request=auth_request
        )

        assert authed_session._auth_request is auth_request

    def test_request_default_timeout(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        response = make_response()
        adapter = AdapterStub([response])

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
        authed_session.mount(self.TEST_URL, adapter)

        patcher = mock.patch("google.auth.transport.requests.requests.Session.request")
        with patcher as patched_request:
            authed_session.request("GET", self.TEST_URL)

        expected_timeout = google.auth.transport.requests._DEFAULT_TIMEOUT
        assert patched_request.call_args[1]["timeout"] == expected_timeout

    def test_request_no_refresh(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        response = make_response()
        adapter = AdapterStub([response])

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
        authed_session.mount(self.TEST_URL, adapter)

        result = authed_session.request("GET", self.TEST_URL)

        assert response == result
        assert credentials.before_request.called
        assert not credentials.refresh.called
        assert len(adapter.requests) == 1
        assert adapter.requests[0].url == self.TEST_URL
        assert adapter.requests[0].headers["authorization"] == "token"

    def test_request_refresh(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.OK)
        # First request will 401, second request will succeed.
        adapter = AdapterStub(
            [make_response(status=http_client.UNAUTHORIZED), final_response]
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.TEST_URL, adapter)

        result = authed_session.request("GET", self.TEST_URL)

        assert result == final_response
        assert credentials.before_request.call_count == 2
        assert credentials.refresh.called
        assert len(adapter.requests) == 2

        assert adapter.requests[0].url == self.TEST_URL
        assert adapter.requests[0].headers["authorization"] == "token"

        assert adapter.requests[1].url == self.TEST_URL
        assert adapter.requests[1].headers["authorization"] == "token1"

    def test_request_max_allowed_time_timeout_error(self, frozen_time):
        tick_one_second = functools.partial(
            frozen_time.tick, delta=datetime.timedelta(seconds=1.0)
        )

        credentials = mock.Mock(
            wraps=TimeTickCredentialsStub(time_tick=tick_one_second)
        )
        adapter = TimeTickAdapterStub(
            time_tick=tick_one_second, responses=[make_response(status=http_client.OK)]
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
        authed_session.mount(self.TEST_URL, adapter)

        # Because a request takes a full mocked second, max_allowed_time shorter
        # than that will cause a timeout error.
        with pytest.raises(requests.exceptions.Timeout):
            authed_session.request("GET", self.TEST_URL, max_allowed_time=0.9)

    def test_request_max_allowed_time_w_transport_timeout_no_error(self, frozen_time):
        tick_one_second = functools.partial(
            frozen_time.tick, delta=datetime.timedelta(seconds=1.0)
        )

        credentials = mock.Mock(
            wraps=TimeTickCredentialsStub(time_tick=tick_one_second)
        )
        adapter = TimeTickAdapterStub(
            time_tick=tick_one_second,
            responses=[
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ],
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
        authed_session.mount(self.TEST_URL, adapter)

        # A short configured transport timeout does not affect max_allowed_time.
        # The latter is not adjusted to it and is only concerned with the actual
        # execution time. The call below should thus not raise a timeout error.
        authed_session.request("GET", self.TEST_URL, timeout=0.5, max_allowed_time=3.1)

    def test_request_max_allowed_time_w_refresh_timeout_no_error(self, frozen_time):
        tick_one_second = functools.partial(
            frozen_time.tick, delta=datetime.timedelta(seconds=1.0)
        )

        credentials = mock.Mock(
            wraps=TimeTickCredentialsStub(time_tick=tick_one_second)
        )
        adapter = TimeTickAdapterStub(
            time_tick=tick_one_second,
            responses=[
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ],
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=1.1
        )
        authed_session.mount(self.TEST_URL, adapter)

        # A short configured refresh timeout does not affect max_allowed_time.
        # The latter is not adjusted to it and is only concerned with the actual
        # execution time. The call below should thus not raise a timeout error
        # (and `timeout` does not come into play either, as it's very long).
        authed_session.request("GET", self.TEST_URL, timeout=60, max_allowed_time=3.1)

    def test_request_timeout_w_refresh_timeout_timeout_error(self, frozen_time):
        tick_one_second = functools.partial(
            frozen_time.tick, delta=datetime.timedelta(seconds=1.0)
        )

        credentials = mock.Mock(
            wraps=TimeTickCredentialsStub(time_tick=tick_one_second)
        )
        adapter = TimeTickAdapterStub(
            time_tick=tick_one_second,
            responses=[
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ],
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=100
        )
        authed_session.mount(self.TEST_URL, adapter)

        # An UNAUTHORIZED response triggers a refresh (an extra request), thus
        # the final request that otherwise succeeds results in a timeout error
        # (all three requests together last 3 mocked seconds).
        with pytest.raises(requests.exceptions.Timeout):
            authed_session.request(
                "GET", self.TEST_URL, timeout=60, max_allowed_time=2.9
            )

    def test_authorized_session_without_default_host(self):
        credentials = mock.create_autospec(service_account.Credentials)

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)

        authed_session.credentials._create_self_signed_jwt.assert_called_once_with(None)

    def test_authorized_session_with_default_host(self):
        default_host = "pubsub.googleapis.com"
        credentials = mock.create_autospec(service_account.Credentials)

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, default_host=default_host
        )

        authed_session.credentials._create_self_signed_jwt.assert_called_once_with(
            "https://{}/".format(default_host)
        )

    def test_configure_mtls_channel_with_callback(self):
        mock_callback = mock.Mock()
        mock_callback.return_value = (
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel(mock_callback)

        assert auth_session.is_mtls
        assert isinstance(
            auth_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_with_metadata(self, mock_get_client_cert_and_key):
        mock_get_client_cert_and_key.return_value = (
            True,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel()

        assert auth_session.is_mtls
        assert isinstance(
            auth_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_closes_old_adapters(
        self, mock_get_client_cert_and_key
    ):
        mock_get_client_cert_and_key.return_value = (
            True,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        old_main_adapter = mock.Mock(spec=requests.adapters.HTTPAdapter)
        old_auth_adapter = mock.Mock(spec=requests.adapters.HTTPAdapter)

        auth_session.mount("https://", old_main_adapter)
        auth_session._auth_request_session.mount("https://", old_auth_adapter)

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel()

        old_main_adapter.close.assert_called_once()
        old_auth_adapter.close.assert_called_once()

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_mounts_adapter_to_auth_request_session(
        self, mock_get_client_cert_and_key
    ):
        mock_get_client_cert_and_key.return_value = (
            True,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel()

        assert auth_session.is_mtls
        # Main session gets the mTLS adapter
        assert isinstance(
            auth_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )
        # _auth_request_session gets a separate adapter instance
        assert isinstance(
            auth_session._auth_request_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )
        assert (
            auth_session.adapters["https://"]
            is not auth_session._auth_request_session.adapters["https://"]
        )

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_without_https_adapter(
        self, mock_get_client_cert_and_key
    ):
        mock_get_client_cert_and_key.return_value = (
            True,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )

        # Remove the 'https://' adapter to trigger InvalidSchema
        auth_session.adapters.pop("https://", None)
        auth_session._auth_request_session.adapters.pop("https://", None)

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel()

        assert auth_session.is_mtls
        # Main session gets the mTLS adapter
        assert isinstance(
            auth_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )
        # _auth_request_session gets the exact same adapter
        assert isinstance(
            auth_session._auth_request_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_without_auth_request_session(
        self, mock_get_client_cert_and_key
    ):
        mock_get_client_cert_and_key.return_value = (
            True,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock(), auth_request=mock.Mock()
        )
        assert auth_session._auth_request_session is None

        old_main_adapter = mock.Mock(spec=requests.adapters.HTTPAdapter)
        auth_session.mount("https://", old_main_adapter)

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel()

        old_main_adapter.close.assert_called_once()
        assert auth_session.is_mtls
        assert isinstance(
            auth_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )

    @mock.patch.object(google.auth.transport.requests._MutualTlsAdapter, "__init__")
    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_non_mtls(
        self, mock_get_client_cert_and_key, mock_adapter_ctor
    ):
        mock_get_client_cert_and_key.return_value = (False, None, None)

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel()
        assert auth_session._is_mtls is False

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_exceptions(self, mock_get_client_cert_and_key):
        mock_get_client_cert_and_key.side_effect = exceptions.ClientCertError()

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with pytest.raises(exceptions.MutualTLSChannelError):
            with mock.patch.dict(
                os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
            ):
                auth_session.configure_mtls_channel()
        assert auth_session._is_mtls is False

        mock_get_client_cert_and_key.side_effect = OSError("Mock file read error")
        with pytest.raises(exceptions.MutualTLSChannelError):
            with mock.patch.dict(
                os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
            ):
                auth_session.configure_mtls_channel()
        assert auth_session._is_mtls is False

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    @mock.patch("google.auth.transport.requests.create_urllib3_context", autospec=True)
    def test_configure_mtls_channel_cert_loading_exceptions(
        self, mock_create_urllib3_context, mock_get_client_cert_and_key
    ):
        import ssl

        mock_get_client_cert_and_key.return_value = (
            True,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        for exception_type in [ValueError("error"), ssl.SSLError("error")]:
            mock_ctx = mock.Mock()
            mock_ctx.load_cert_chain.side_effect = exception_type
            mock_create_urllib3_context.return_value = mock_ctx

            auth_session = google.auth.transport.requests.AuthorizedSession(
                credentials=mock.Mock()
            )
            with pytest.raises(exceptions.MutualTLSChannelError):
                with mock.patch.dict(
                    os.environ,
                    {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"},
                ):
                    auth_session.configure_mtls_channel()
            assert auth_session._is_mtls is False

            assert not auth_session.is_mtls

    @mock.patch(
        "google.auth.transport._mtls_helper._get_cert_config_path", return_value=None
    )
    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    @mock.patch.dict(
        os.environ,
        {
            "GOOGLE_API_USE_CLIENT_CERTIFICATE": "false",
            "CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE": "false",
            "GOOGLE_API_CERTIFICATE_CONFIG": "",
            "CLOUDSDK_CONTEXT_AWARE_CERTIFICATE_CONFIG_FILE_PATH": "",
        },
    )
    def test_configure_mtls_channel_without_client_cert_env(
        self, get_client_cert_and_key, mock_get_cert_config_path
    ):
        env_to_patch = {
            environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "",
            environment_vars.CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE: "",
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG: "",
            environment_vars.CLOUDSDK_CONTEXT_AWARE_CERTIFICATE_CONFIG_FILE_PATH: "",
        }
        with mock.patch.dict(os.environ, env_to_patch):
            auth_session = google.auth.transport.requests.AuthorizedSession(
                credentials=mock.Mock()
            )
            auth_session.configure_mtls_channel()
            assert not auth_session.is_mtls
            get_client_cert_and_key.assert_not_called()

            mock_callback = mock.Mock()
            auth_session.configure_mtls_channel(mock_callback)
            assert not auth_session.is_mtls
            mock_callback.assert_not_called()

    def test_close_wo_passed_in_auth_request(self):
        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials
        )
        authed_session._auth_request_session = mock.Mock(spec=["close"])

        authed_session.close()

        authed_session._auth_request_session.close.assert_called_once_with()

    def test_close_w_passed_in_auth_request(self):
        http = mock.create_autospec(requests.Session)
        auth_request = google.auth.transport.requests.Request(http)
        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials, auth_request=auth_request
        )

        authed_session.close()  # no raise

    def test_cert_rotation_when_cert_mismatch_and_mtls_enabled(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.OK)
        # First request will 401, second request will succeed.
        adapter = AdapterStub(
            [make_response(status=http_client.UNAUTHORIZED), final_response]
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.MTLS_TEST_URL, adapter)

        old_cert = b"-----BEGIN CERTIFICATE-----\nMIIBdTCCARqgAwIBAgIJAOYVvu/axMxvMAoGCCqGSM49BAMCMCcxJTAjBgNVBAMM\nHEdvb2dsZSBFbmRwb2ludCBWZXJpZmljYXRpb24wHhcNMjUwNzMwMjMwNjA4WhcN\nMjYwNzMxMjMwNjA4WjAnMSUwIwYDVQQDDBxHb29nbGUgRW5kcG9pbnQgVmVyaWZp\nY2F0aW9uMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEbtr18gkEtwPow2oqyZsU\n4KLwFaLFlRlYv55UATS3QTDykDnIufC42TJCnqFRYhwicwpE2jnUV+l9g3Voias8\nraMvMC0wCQYDVR0TBAIwADALBgNVHQ8EBAMCB4AwEwYDVR0lBAwwCgYIKwYBBQUH\nAwIwCgYIKoZIzj0EAwIDSQAwRgIhAKcjW6dmF1YCksXPgDPlPu/nSnOjb3qCcivz\n/Jxq2zoeAiEA7/aNxcEoCGS3hwMIXoaaD/vPcZOOopKSyqXCvxRooKQ=\n-----END CERTIFICATE-----\n"

        # New certificate and key to simulate rotation.
        new_cert = pytest.public_cert_bytes
        new_key = pytest.private_key_bytes

        # Set _cached_cert to a callable that returns the old certificate.
        authed_session._cached_cert = old_cert
        authed_session._is_mtls = True

        # Mock call_client_cert_callback to return the new certificate.
        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "call_client_cert_callback",
            return_value=(new_cert, new_key),
        ) as mock_callback:
            result = authed_session.request("GET", self.MTLS_TEST_URL)

        # Asserts to verify the behavior.
        assert mock_callback.called
        assert credentials.refresh.called
        assert credentials.refresh.call_count == 1
        assert result.status_code == final_response.status_code

    def test_no_cert_rotation_when_cert_match_and_mTLS_enabled(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.UNAUTHORIZED)
        adapter = AdapterStub(
            [
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.UNAUTHORIZED),
            ]
        )
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.MTLS_TEST_URL, adapter)
        authed_session._is_mtls = True

        old_cert = CERT_MOCK_VAL

        # New certificate and key to simulate rotation.
        new_cert = old_cert
        new_key = KEY_MOCK_VAL

        # Set _cached_cert to a callable that returns the old certificate.
        authed_session._cached_cert = old_cert

        # Mock call_client_cert_callback to return the new certificate.
        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "call_client_cert_callback",
            return_value=(new_cert, new_key),
        ):
            result = authed_session.request("GET", self.MTLS_TEST_URL)

        # Asserts to verify the behavior.
        assert credentials.refresh.call_count == 2
        assert result.status_code == final_response.status_code

    def test_no_cert_match_check_when_mtls_disabled(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.UNAUTHORIZED)
        adapter = AdapterStub(
            [
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.UNAUTHORIZED),
            ]
        )
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.TEST_URL, adapter)
        authed_session._is_mtls = False

        new_cert = CERT_MOCK_VAL

        # New certificate and key to simulate rotation.
        new_key = KEY_MOCK_VAL

        # Mock call_client_cert_callback to return the new certificate.
        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "call_client_cert_callback",
            return_value=(new_cert, new_key),
        ) as mock_callback:
            result = authed_session.request("GET", self.TEST_URL)

        # Asserts to verify the behavior.
        assert not mock_callback.called
        assert result.status_code == final_response.status_code

    def test_no_cert_rotation_when_no_unauthorized_response(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.UPGRADE_REQUIRED)

        # Response is set to code other than 401(Unauthorized).
        adapter = AdapterStub([make_response(status=http_client.UPGRADE_REQUIRED)])
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.MTLS_TEST_URL, adapter)

        authed_session._is_mtls = True

        result = authed_session.request("GET", self.MTLS_TEST_URL)
        assert result.status_code == final_response.status_code

        # Asserts to verify the behavior.
        assert not credentials.refresh.called
        assert credentials.refresh.call_count == 0

    def test_cert_rotation_failure_raises_error(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        # First request will 401, second request will fail to reconfigure mTLS.
        adapter = AdapterStub([make_response(status=http_client.UNAUTHORIZED)])

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.MTLS_TEST_URL, adapter)

        old_cert = b"-----BEGIN CERTIFICATE-----\nMIIBdTCCARqgAwIBAgIJAOYVvu/axMxvMAoGCCqGSM49BAMCMCcxJTAjBgNVBAMM\nHEdvb2dsZSBFbmRwb2ludCBWZXJpZmljYXRpb24wHhcNMjUwNzMwMjMwNjA4WhcN\nMjYwNzMxMjMwNjA4WjAnMSUwIwYDVQQDDBxHb29nbGUgRW5kcG9pbnQgVmVyaWZp\nY2F0aW9uMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEbtr18gkEtwPow2oqyZsU\n4KLwFaLFlRlYv55UATS3QTDykDnIufC42TJCnqFRYhwicwpE2jnUV+l9g3Voias8\nraMvMC0wCQYDVR0TBAIwADALBgNVHQ8EBAMCB4AwEwYDVR0lBAwwCgYIKwYBBQUH\nAwIwCgYIKoZIzj0EAwIDSQAwRgIhAKcjW6dmF1YCksXPgDPlPu/nSnOjb3qCcivz\n/Jxq2zoeAiEA7/aNxcEoCGS3hwMIXoaaD/vPcZOOopKSyqXCvxRooKQ=\n-----END CERTIFICATE-----\n"

        # New certificate and key to simulate rotation.
        new_cert = CERT_MOCK_VAL
        new_key = KEY_MOCK_VAL

        authed_session._cached_cert = old_cert
        authed_session._is_mtls = True

        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "call_client_cert_callback",
            return_value=(new_cert, new_key),
        ):
            with mock.patch.object(
                authed_session,
                "configure_mtls_channel",
                side_effect=Exception("Failed to reconfigure"),
            ):
                with pytest.raises(exceptions.MutualTLSChannelError):
                    authed_session.request("GET", self.MTLS_TEST_URL)

                # Assert to verify behavior
                credentials.refresh.assert_not_called()

    def test_cert_rotation_check_params_fails(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        adapter = AdapterStub(
            [
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ]
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.MTLS_TEST_URL, adapter)
        authed_session._is_mtls = True
        authed_session._cached_cert = b"cached_cert"

        with mock.patch(
            "google.auth.transport.requests._mtls_helper.check_parameters_for_unauthorized_response",
            side_effect=Exception("check_params failed"),
        ) as mock_check_params:
            response = authed_session.request("GET", self.MTLS_TEST_URL)

            mock_check_params.assert_called_once()
            assert credentials.refresh.called
            assert response.status_code == http_client.OK

    def test_cert_rotation_logic_skipped_on_other_refresh_status_codes(self):
        """
        Tests that the code can handle a refresh triggered by a status code
        other than 401 (UNAUTHORIZED). This covers the 'else' branch of the
        'if response.status_code == http_client.UNAUTHORIZED' check
        """
        credentials = mock.Mock(wraps=CredentialsStub())
        # Configure the session to treat 503 (Service Unavailable) as a refreshable error
        custom_refresh_codes = [http_client.SERVICE_UNAVAILABLE]

        # Return 503 first, then 200
        adapter = AdapterStub(
            [
                make_response(status=http_client.SERVICE_UNAVAILABLE),
                make_response(status=http_client.OK),
            ]
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_status_codes=custom_refresh_codes
        )
        authed_session.mount(self.MTLS_TEST_URL, adapter)

        # Enable mTLS to prove it is skipped despite being enabled
        authed_session._is_mtls = True

        with mock.patch(
            "google.auth.transport.requests._mtls_helper", autospec=True
        ) as mock_helper:
            authed_session.request("GET", self.MTLS_TEST_URL)

            # Assert refresh happened (Outer Check was True)
            assert credentials.refresh.called

            # Assert mTLS check logic was SKIPPED (Inner Check was False)
            assert not mock_helper.check_parameters_for_unauthorized_response.called

    @pytest.mark.parametrize(
        "non_mtls_url",
        [
            "https://storage.googleapis.com/bucket/mtls.googleapis.com",
            "https://my-service-xyz-uc.a.run.app/mtls.run.app",
        ],
    )
    def test_cert_rotation_skipped_on_non_mtls_url(self, non_mtls_url):
        """
        Tests that mTLS cert rotation is skipped on non-mTLS URLs even if
        mTLS is enabled and an UNAUTHORIZED (401) response is received.
        """
        credentials = mock.Mock(wraps=CredentialsStub())
        # First request will 401, second request will succeed.
        adapter = AdapterStub(
            [
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ]
        )
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount("https://", adapter)
        authed_session._is_mtls = True
        authed_session._cached_cert = b"cached_cert"

        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "check_parameters_for_unauthorized_response",
        ) as mock_check_params:
            authed_session.request("GET", non_mtls_url)

            # Assert refresh happened
            assert credentials.refresh.called

            # Assert mTLS check logic was SKIPPED
            assert not mock_check_params.called

    @pytest.mark.parametrize(
        "mtls_url",
        [
            "https://storage.p.googleapis.com/b/my-bucket",
            "https://my-service-123456.us-central1.mtls.run.app/v1",
        ],
    )
    def test_cert_rotation_triggered_on_mtls_url(self, mtls_url):
        """
        Tests that mTLS cert rotation IS triggered on Private Service Connect
        (PSC) and Cloud Run mTLS endpoints when an UNAUTHORIZED (401) response
        is received.
        """
        credentials = mock.Mock(wraps=CredentialsStub())
        adapter = AdapterStub(
            [
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ]
        )
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(mtls_url, adapter)
        authed_session._is_mtls = True
        authed_session._cached_cert = b"cached_cert"

        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "check_parameters_for_unauthorized_response",
            return_value=(b"new_cert", b"new_key", "old_fp", "old_fp"),
        ) as mock_check_params:
            authed_session.request("GET", mtls_url)

            # Assert mTLS check logic was called on PSC / Cloud Run mTLS endpoint
            mock_check_params.assert_called_once()
            assert credentials.refresh.called

    def test_configure_mtls_channel_subsequent_failure(self):
        # 1. Setup successful mTLS configuration
        mock_callback = mock.Mock()
        mock_callback.return_value = (
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )
        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel(mock_callback)

        assert auth_session.is_mtls
        assert isinstance(
            auth_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )

        # 2. Trigger a failure on a subsequent configuration call
        with mock.patch(
            "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
        ) as mock_get_client_cert_and_key:
            mock_get_client_cert_and_key.side_effect = exceptions.ClientCertError()

            with pytest.raises(exceptions.MutualTLSChannelError):
                with mock.patch.dict(
                    os.environ,
                    {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"},
                ):
                    auth_session.configure_mtls_channel()

        # 3. Verify it retains its previous mTLS state and MutualTlsAdapter
        assert auth_session.is_mtls
        assert isinstance(
            auth_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )

    def test_configure_mtls_channel_subsequent_disabled(self):
        # 1. Setup successful mTLS configuration
        mock_callback = mock.Mock()
        mock_callback.return_value = (
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )
        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel(mock_callback)

        assert auth_session.is_mtls

        # 2. Subsequent call returns no client certificate (disabled)
        with mock.patch(
            "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
        ) as mock_get_client_cert_and_key:
            mock_get_client_cert_and_key.return_value = (False, None, None)

            with mock.patch.dict(
                os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
            ):
                auth_session.configure_mtls_channel()

        # 3. Verify mTLS is disabled and standard HTTPAdapter is restored
        assert not auth_session.is_mtls
        assert isinstance(
            auth_session.adapters["https://"],
            requests.adapters.HTTPAdapter,
        )

    def test_unauthorized_cert_discovery_exception_proceeds_to_token_refresh(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        adapter = AdapterStub(
            [
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ]
        )
        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
        authed_session.mount(self.MTLS_TEST_URL, adapter)
        authed_session._is_mtls = True
        # Simulate discovery failure (e.g. Enterprise cert provider error or file missing)
        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "check_parameters_for_unauthorized_response",
            side_effect=Exception("Certificate discovery failed"),
        ):
            result = authed_session.request("GET", self.MTLS_TEST_URL)
        # Token refresh should still be called despite discovery failure
        credentials.refresh.assert_called_once()
        assert result.status_code == http_client.OK
        assert not authed_session._mtls_reauth_lock.locked()

    def test_cert_check_skipped_when_cert_rotated_during_request(self):
        """
        Tests that a request that receives a 401 response does not read the
        client certificate again if another thread has already rotated it
        while the request was in flight.
        """
        credentials = mock.Mock(wraps=CredentialsStub())
        adapter = AdapterStub(
            [
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ]
        )
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.MTLS_TEST_URL, adapter)
        authed_session._is_mtls = True
        authed_session._cached_cert = b"old_cert"
        send_request = adapter.send

        def send_request_and_rotate_cert(request, **kwargs):
            # Simulate another thread rotating the client certificate while
            # this request is in flight.
            authed_session._cached_cert = b"new_cert"
            return send_request(request, **kwargs)

        adapter.send = send_request_and_rotate_cert

        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "check_parameters_for_unauthorized_response",
        ) as mock_check_params:
            with mock.patch.object(
                authed_session, "configure_mtls_channel"
            ) as mock_configure_mtls_channel:
                result = authed_session.request("GET", self.MTLS_TEST_URL)

        assert result.status_code == http_client.OK
        mock_check_params.assert_not_called()
        mock_configure_mtls_channel.assert_not_called()
        credentials.refresh.assert_called_once()

    def test_reconfigure_mtls_channel_skipped_if_mtls_disabled(self):
        """
        Tests that the client certificate is not checked if another thread
        disabled mTLS while this thread was waiting for the lock.
        """
        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials
        )
        authed_session._is_mtls = False

        with mock.patch.object(
            google.auth.transport._mtls_helper,
            "check_parameters_for_unauthorized_response",
        ) as mock_check_params:
            authed_session._reconfigure_mtls_channel_if_cert_changed(b"old_cert")

        mock_check_params.assert_not_called()
        assert not authed_session._mtls_reauth_lock.locked()

    @mock.patch.object(requests.adapters.HTTPAdapter, "send", autospec=True)
    def test_concurrent_unauthorized_responses_reconfigure_mtls_channel_once(
        self, mock_send
    ):
        """
        Tests that when several threads that share an AuthorizedSession receive
        a 401 response at the same time, the client certificate is read and the
        real mTLS channel reconfiguration runs only once, and every request is
        retried successfully through the newly mounted mTLS adapter.
        """
        num_threads = 8
        old_cert = b"old_cert"
        all_requests_sent = threading.Barrier(num_threads)

        authed_session = google.auth.transport.requests.AuthorizedSession(
            CredentialsStub(), refresh_timeout=60
        )
        authed_session._is_mtls = True
        authed_session._cached_cert = old_cert
        old_adapter = authed_session.adapters["https://"]
        old_auth_adapter = authed_session._auth_request_session.adapters["https://"]

        def send(adapter, request, **kwargs):
            if isinstance(adapter, google.auth.transport.requests._MutualTlsAdapter):
                return make_response(status=http_client.OK)
            # Wait until every thread has sent its request through the old
            # adapter, so that all of them receive a 401 response.
            all_requests_sent.wait(timeout=30)
            return make_response(status=http_client.UNAUTHORIZED)

        mock_send.side_effect = send

        def check_parameters_for_unauthorized_response(cached_cert):
            cached_fingerprint = "old_fp" if cached_cert == old_cert else "new_fp"
            return (
                pytest.public_cert_bytes,
                pytest.private_key_bytes,
                cached_fingerprint,
                "new_fp",
            )

        results = []
        errors = []

        def make_request():
            try:
                results.append(authed_session.request("GET", self.MTLS_TEST_URL))
            except Exception as exc:  # pragma: NO COVER
                errors.append(exc)

        with (
            mock.patch.dict(
                os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
            ),
            mock.patch.object(
                google.auth.transport._mtls_helper,
                "check_parameters_for_unauthorized_response",
                side_effect=check_parameters_for_unauthorized_response,
            ) as mock_check_params,
            mock.patch.object(
                authed_session,
                "configure_mtls_channel",
                wraps=authed_session.configure_mtls_channel,
            ) as spy_configure_mtls_channel,
        ):
            threads = [
                threading.Thread(target=make_request) for _ in range(num_threads)
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=60)

        assert errors == []
        assert [r.status_code for r in results] == [http_client.OK] * num_threads
        mock_check_params.assert_called_once()
        spy_configure_mtls_channel.assert_called_once()
        assert authed_session.is_mtls
        assert authed_session._cached_cert == pytest.public_cert_bytes
        new_adapter = authed_session.adapters["https://"]
        new_auth_adapter = authed_session._auth_request_session.adapters["https://"]
        assert isinstance(new_adapter, google.auth.transport.requests._MutualTlsAdapter)
        assert isinstance(
            new_auth_adapter, google.auth.transport.requests._MutualTlsAdapter
        )
        assert new_adapter is not old_adapter
        assert new_auth_adapter is not old_auth_adapter
        assert not authed_session._mtls_reauth_lock.locked()

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_does_not_mutate_adapters_in_place(
        self, mock_get_client_cert_and_key
    ):
        """
        Tests that configure_mtls_channel replaces the adapters dictionaries of
        the session and of the auth request session instead of mutating them,
        so that a thread iterating over them in get_adapter() does not fail
        with "OrderedDict mutated during iteration".
        """
        mock_get_client_cert_and_key.return_value = (
            True,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        custom_adapter = AdapterStub([])
        authed_session.mount(self.MTLS_TEST_URL, custom_adapter)
        auth_session = authed_session._auth_request_session

        adapters_before = authed_session.adapters
        adapters_snapshot = adapters_before.copy()
        adapters_iter = iter(adapters_before.items())
        next(adapters_iter)
        auth_adapters_before = auth_session.adapters
        auth_adapters_snapshot = auth_adapters_before.copy()
        auth_adapters_iter = iter(auth_adapters_before.items())
        next(auth_adapters_iter)

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            authed_session.configure_mtls_channel()

        # Iterators over the previous dictionaries are still valid.
        list(adapters_iter)
        list(auth_adapters_iter)
        assert adapters_before == adapters_snapshot
        assert auth_adapters_before == auth_adapters_snapshot
        assert authed_session.adapters is not adapters_before
        assert auth_session.adapters is not auth_adapters_before
        assert isinstance(
            authed_session.get_adapter("https://example.com/"),
            google.auth.transport.requests._MutualTlsAdapter,
        )
        assert isinstance(
            auth_session.get_adapter("https://example.com/"),
            google.auth.transport.requests._MutualTlsAdapter,
        )
        # The more specific prefix mounted earlier still takes precedence.
        assert authed_session.get_adapter(self.MTLS_TEST_URL) is custom_adapter


class TestMutualTlsOffloadAdapter(object):
    @mock.patch.object(requests.adapters.HTTPAdapter, "init_poolmanager")
    @mock.patch.object(requests.adapters.HTTPAdapter, "proxy_manager_for")
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner, "load_libraries"
    )
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner,
        "attach_to_ssl_context",
    )
    def test_success(
        self,
        mock_attach_to_ssl_context,
        mock_load_libraries,
        mock_proxy_manager_for,
        mock_init_poolmanager,
    ):
        enterprise_cert_file_path = "/path/to/enterprise/cert/json"
        adapter = google.auth.transport.requests._MutualTlsOffloadAdapter(
            enterprise_cert_file_path
        )

        mock_load_libraries.assert_called_once()
        assert mock_attach_to_ssl_context.call_count == 2

        adapter.init_poolmanager()
        mock_init_poolmanager.assert_called_with(ssl_context=adapter._ctx_poolmanager)

        adapter.proxy_manager_for()
        mock_proxy_manager_for.assert_called_with(ssl_context=adapter._ctx_proxymanager)

    @mock.patch.object(requests.adapters.HTTPAdapter, "init_poolmanager")
    @mock.patch.object(requests.adapters.HTTPAdapter, "proxy_manager_for")
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner, "should_use_provider"
    )
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner, "load_libraries"
    )
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner,
        "attach_to_ssl_context",
    )
    def test_success_should_use_provider(
        self,
        mock_attach_to_ssl_context,
        mock_load_libraries,
        mock_should_use_provider,
        mock_proxy_manager_for,
        mock_init_poolmanager,
    ):
        enterprise_cert_file_path = "/path/to/enterprise/cert/json"
        adapter = google.auth.transport.requests._MutualTlsOffloadAdapter(
            enterprise_cert_file_path
        )

        mock_should_use_provider.return_value = True
        mock_load_libraries.assert_called_once()
        assert mock_attach_to_ssl_context.call_count == 2

        adapter.init_poolmanager()
        mock_init_poolmanager.assert_called_with(ssl_context=adapter._ctx_poolmanager)

        adapter.proxy_manager_for()
        mock_proxy_manager_for.assert_called_with(ssl_context=adapter._ctx_proxymanager)


class TestAuthorizedSessionMTLSReauth:
    @mock.patch(
        "google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response"
    )
    @mock.patch("google.auth.transport.requests.requests.Session.request")
    def test_reauth_lock_acquired_on_unauthorized(
        self, mock_session_request, mock_check_params
    ):
        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        session = google.auth.transport.requests.AuthorizedSession(credentials)
        session._is_mtls = True
        mock_session_request.side_effect = [
            mock.Mock(status_code=http_client.UNAUTHORIZED),
            mock.Mock(status_code=http_client.OK),
        ]
        mock_check_params.return_value = (b"cert", b"key", "old_fp", "new_fp")
        lock_held_during_call = {"held": False}

        def mock_configure_mtls_channel(callback):
            lock_held_during_call["held"] = session._mtls_reauth_lock.locked()

        session.configure_mtls_channel = mock.Mock(
            side_effect=mock_configure_mtls_channel
        )

        session.request("GET", "https://example.mtls.googleapis.com/")

        session.configure_mtls_channel.assert_called_once()
        assert lock_held_during_call["held"] is True
        assert not session._mtls_reauth_lock.locked()

    @mock.patch(
        "google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response"
    )
    @mock.patch("google.auth.transport.requests.requests.Session.request")
    def test_reauth_skipped_when_cert_fingerprint_matches(
        self, mock_session_request, mock_check_params
    ):
        credentials = mock.Mock()
        session = google.auth.transport.requests.AuthorizedSession(credentials)
        session._is_mtls = True
        session._cached_cert = b"cert"

        mock_session_request.side_effect = [
            mock.Mock(status_code=http_client.UNAUTHORIZED),
            mock.Mock(status_code=http_client.OK),
        ]
        mock_check_params.return_value = (
            b"same_cert_bytes",
            b"same_key_bytes",
            "same_fingerprint",
            "same_fingerprint",
        )
        session.configure_mtls_channel = mock.Mock()

        session.request("GET", "https://example.mtls.googleapis.com/")

        session.configure_mtls_channel.assert_not_called()
