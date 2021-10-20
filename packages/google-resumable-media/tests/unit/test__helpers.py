# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import hashlib
import http.client

import mock
import pytest

from google.resumable_media import _helpers
from google.resumable_media import common


def test_do_nothing():
    ret_val = _helpers.do_nothing()
    assert ret_val is None


class Test_header_required(object):
    def _success_helper(self, **kwargs):
        name = "some-header"
        value = "The Right Hand Side"
        headers = {name: value, "other-name": "other-value"}
        response = mock.Mock(headers=headers, spec=["headers"])
        result = _helpers.header_required(response, name, _get_headers, **kwargs)
        assert result == value

    def test_success(self):
        self._success_helper()

    def test_success_with_callback(self):
        callback = mock.Mock(spec=[])
        self._success_helper(callback=callback)
        callback.assert_not_called()

    def _failure_helper(self, **kwargs):
        response = mock.Mock(headers={}, spec=["headers"])
        name = "any-name"
        with pytest.raises(common.InvalidResponse) as exc_info:
            _helpers.header_required(response, name, _get_headers, **kwargs)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 2
        assert error.args[1] == name

    def test_failure(self):
        self._failure_helper()

    def test_failure_with_callback(self):
        callback = mock.Mock(spec=[])
        self._failure_helper(callback=callback)
        callback.assert_called_once_with()


class Test_require_status_code(object):
    @staticmethod
    def _get_status_code(response):
        return response.status_code

    def test_success(self):
        status_codes = (http.client.OK, http.client.CREATED)
        acceptable = (
            http.client.OK,
            int(http.client.OK),
            http.client.CREATED,
            int(http.client.CREATED),
        )
        for value in acceptable:
            response = _make_response(value)
            status_code = _helpers.require_status_code(
                response, status_codes, self._get_status_code
            )
            assert value == status_code

    def test_success_with_callback(self):
        status_codes = (http.client.OK,)
        response = _make_response(http.client.OK)
        callback = mock.Mock(spec=[])
        status_code = _helpers.require_status_code(
            response, status_codes, self._get_status_code, callback=callback
        )
        assert status_code == http.client.OK
        callback.assert_not_called()

    def test_failure(self):
        status_codes = (http.client.CREATED, http.client.NO_CONTENT)
        response = _make_response(http.client.OK)
        with pytest.raises(common.InvalidResponse) as exc_info:
            _helpers.require_status_code(response, status_codes, self._get_status_code)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 5
        assert error.args[1] == response.status_code
        assert error.args[3:] == status_codes

    def test_failure_with_callback(self):
        status_codes = (http.client.OK,)
        response = _make_response(http.client.NOT_FOUND)
        callback = mock.Mock(spec=[])
        with pytest.raises(common.InvalidResponse) as exc_info:
            _helpers.require_status_code(
                response, status_codes, self._get_status_code, callback=callback
            )

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 4
        assert error.args[1] == response.status_code
        assert error.args[3:] == status_codes
        callback.assert_called_once_with()

    def test_retryable_failure_without_callback(self):
        status_codes = (http.client.OK,)
        retryable_responses = [
            _make_response(status_code) for status_code in common.RETRYABLE
        ]
        callback = mock.Mock(spec=[])
        for retryable_response in retryable_responses:
            with pytest.raises(common.InvalidResponse) as exc_info:
                _helpers.require_status_code(
                    retryable_response,
                    status_codes,
                    self._get_status_code,
                    callback=callback,
                )

            error = exc_info.value
            assert error.response is retryable_response
            assert len(error.args) == 4
            assert error.args[1] == retryable_response.status_code
            assert error.args[3:] == status_codes
            callback.assert_not_called()


class Test_calculate_retry_wait(object):
    @mock.patch("random.randint", return_value=125)
    def test_past_limit(self, randint_mock):
        base_wait, wait_time = _helpers.calculate_retry_wait(70.0, 64.0)

        assert base_wait == 64.0
        assert wait_time == 64.125
        randint_mock.assert_called_once_with(0, 1000)

    @mock.patch("random.randint", return_value=250)
    def test_at_limit(self, randint_mock):
        base_wait, wait_time = _helpers.calculate_retry_wait(50.0, 50.0)

        assert base_wait == 50.0
        assert wait_time == 50.25
        randint_mock.assert_called_once_with(0, 1000)

    @mock.patch("random.randint", return_value=875)
    def test_under_limit(self, randint_mock):
        base_wait, wait_time = _helpers.calculate_retry_wait(16.0, 33.0)

        assert base_wait == 32.0
        assert wait_time == 32.875
        randint_mock.assert_called_once_with(0, 1000)

    @mock.patch("random.randint", return_value=875)
    def test_custom_multiplier(self, randint_mock):
        base_wait, wait_time = _helpers.calculate_retry_wait(16.0, 64.0, 3)

        assert base_wait == 48.0
        assert wait_time == 48.875
        randint_mock.assert_called_once_with(0, 1000)


def _make_response(status_code):
    return mock.Mock(status_code=status_code, spec=["status_code"])


def _get_headers(response):
    return response.headers


@pytest.mark.parametrize("checksum", ["md5", "crc32c", None])
def test__get_checksum_object(checksum):
    checksum_object = _helpers._get_checksum_object(checksum)

    checksum_types = {
        "md5": type(hashlib.md5()),
        "crc32c": type(_helpers._get_crc32c_object()),
        None: type(None),
    }
    assert isinstance(checksum_object, checksum_types[checksum])


def test__get_checksum_object_invalid():
    with pytest.raises(ValueError):
        _helpers._get_checksum_object("invalid")


@mock.patch("builtins.__import__")
def test__get_crc32_object_wo_google_crc32c_wo_crcmod(mock_import):
    mock_import.side_effect = ImportError("testing")

    with pytest.raises(ImportError):
        _helpers._get_crc32c_object()

    expected_calls = [
        mock.call("google_crc32c", mock.ANY, None, None, 0),
        mock.call("crcmod", mock.ANY, None, None, 0),
    ]
    mock_import.assert_has_calls(expected_calls)


@mock.patch("builtins.__import__")
def test__get_crc32_object_w_google_crc32c(mock_import):
    google_crc32c = mock.Mock(spec=["Checksum"])
    mock_import.return_value = google_crc32c

    found = _helpers._get_crc32c_object()

    assert found is google_crc32c.Checksum.return_value
    google_crc32c.Checksum.assert_called_once_with()

    mock_import.assert_called_once_with("google_crc32c", mock.ANY, None, None, 0)


@mock.patch("builtins.__import__")
def test__get_crc32_object_wo_google_crc32c_w_crcmod(mock_import):
    crcmod = mock.Mock(spec=["predefined", "crcmod"])
    crcmod.predefined = mock.Mock(spec=["Crc"])
    crcmod.crcmod = mock.Mock(spec=["_usingExtension"])
    mock_import.side_effect = [ImportError("testing"), crcmod, crcmod.crcmod]

    found = _helpers._get_crc32c_object()

    assert found is crcmod.predefined.Crc.return_value
    crcmod.predefined.Crc.assert_called_once_with("crc-32c")

    expected_calls = [
        mock.call("google_crc32c", mock.ANY, None, None, 0),
        mock.call("crcmod", mock.ANY, None, None, 0),
        mock.call("crcmod.crcmod", mock.ANY, {}, ["_usingExtension"], 0),
    ]
    mock_import.assert_has_calls(expected_calls)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@mock.patch("builtins.__import__")
def test__is_fast_crcmod_wo_extension_warning(mock_import):
    crcmod = mock.Mock(spec=["crcmod"])
    crcmod.crcmod = mock.Mock(spec=["_usingExtension"])
    crcmod.crcmod._usingExtension = False
    mock_import.return_value = crcmod.crcmod

    assert not _helpers._is_fast_crcmod()

    mock_import.assert_called_once_with(
        "crcmod.crcmod",
        mock.ANY,
        {},
        ["_usingExtension"],
        0,
    )


@mock.patch("builtins.__import__")
def test__is_fast_crcmod_w_extension(mock_import):
    crcmod = mock.Mock(spec=["crcmod"])
    crcmod.crcmod = mock.Mock(spec=["_usingExtension"])
    crcmod.crcmod._usingExtension = True
    mock_import.return_value = crcmod.crcmod

    assert _helpers._is_fast_crcmod()


def test__DoNothingHash():
    do_nothing_hash = _helpers._DoNothingHash()
    return_value = do_nothing_hash.update(b"some data")
    assert return_value is None


class Test__get_expected_checksum(object):
    @pytest.mark.parametrize("template", ["crc32c={},md5={}", "crc32c={}, md5={}"])
    @pytest.mark.parametrize("checksum", ["md5", "crc32c"])
    @mock.patch("google.resumable_media._helpers._LOGGER")
    def test__w_header_present(self, _LOGGER, template, checksum):
        checksums = {"md5": "b2twdXNodGhpc2J1dHRvbg==", "crc32c": "3q2+7w=="}
        header_value = template.format(checksums["crc32c"], checksums["md5"])
        headers = {_helpers._HASH_HEADER: header_value}
        response = _mock_response(headers=headers)

        def _get_headers(response):
            return response.headers

        url = "https://example.com/"
        expected_checksum, checksum_obj = _helpers._get_expected_checksum(
            response, _get_headers, url, checksum_type=checksum
        )
        assert expected_checksum == checksums[checksum]

        checksum_types = {
            "md5": type(hashlib.md5()),
            "crc32c": type(_helpers._get_crc32c_object()),
        }
        assert isinstance(checksum_obj, checksum_types[checksum])

        _LOGGER.info.assert_not_called()

    @pytest.mark.parametrize("checksum", ["md5", "crc32c"])
    @mock.patch("google.resumable_media._helpers._LOGGER")
    def test__w_header_missing(self, _LOGGER, checksum):
        headers = {}
        response = _mock_response(headers=headers)

        def _get_headers(response):
            return response.headers

        url = "https://example.com/"
        expected_checksum, checksum_obj = _helpers._get_expected_checksum(
            response, _get_headers, url, checksum_type=checksum
        )
        assert expected_checksum is None
        assert isinstance(checksum_obj, _helpers._DoNothingHash)
        expected_msg = _helpers._MISSING_CHECKSUM.format(
            url, checksum_type=checksum.upper()
        )
        _LOGGER.info.assert_called_once_with(expected_msg)


class Test__parse_checksum_header(object):

    CRC32C_CHECKSUM = "3q2+7w=="
    MD5_CHECKSUM = "c2l4dGVlbmJ5dGVzbG9uZw=="

    def test_empty_value(self):
        header_value = None
        response = None
        md5_header = _helpers._parse_checksum_header(
            header_value, response, checksum_label="md5"
        )
        assert md5_header is None
        crc32c_header = _helpers._parse_checksum_header(
            header_value, response, checksum_label="crc32c"
        )
        assert crc32c_header is None

    def test_crc32c_only(self):
        header_value = "crc32c={}".format(self.CRC32C_CHECKSUM)
        response = None
        md5_header = _helpers._parse_checksum_header(
            header_value, response, checksum_label="md5"
        )
        assert md5_header is None
        crc32c_header = _helpers._parse_checksum_header(
            header_value, response, checksum_label="crc32c"
        )
        assert crc32c_header == self.CRC32C_CHECKSUM

    def test_md5_only(self):
        header_value = "md5={}".format(self.MD5_CHECKSUM)
        response = None
        md5_header = _helpers._parse_checksum_header(
            header_value, response, checksum_label="md5"
        )
        assert md5_header == self.MD5_CHECKSUM
        crc32c_header = _helpers._parse_checksum_header(
            header_value, response, checksum_label="crc32c"
        )
        assert crc32c_header is None

    def test_both_crc32c_and_md5(self):
        header_value = "crc32c={},md5={}".format(
            self.CRC32C_CHECKSUM, self.MD5_CHECKSUM
        )
        response = None
        md5_header = _helpers._parse_checksum_header(
            header_value, response, checksum_label="md5"
        )
        assert md5_header == self.MD5_CHECKSUM
        crc32c_header = _helpers._parse_checksum_header(
            header_value, response, checksum_label="crc32c"
        )
        assert crc32c_header == self.CRC32C_CHECKSUM

    def test_md5_multiple_matches(self):
        another_checksum = "eW91IGRpZCBXQVQgbm93Pw=="
        header_value = "md5={},md5={}".format(self.MD5_CHECKSUM, another_checksum)
        response = mock.sentinel.response

        with pytest.raises(common.InvalidResponse) as exc_info:
            _helpers._parse_checksum_header(
                header_value, response, checksum_label="md5"
            )

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 3
        assert error.args[1] == header_value
        assert error.args[2] == [self.MD5_CHECKSUM, another_checksum]


def _mock_response(headers):
    return mock.Mock(
        headers=headers,
        status_code=200,
        spec=["status_code", "headers"],
    )
