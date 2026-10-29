# Copyright 2026 Google LLC
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

"""Unit tests for OpenTelemetry standard metrics across HTTP media, fileio, and transfer_manager."""

import base64
import concurrent.futures
import datetime
import gc
import http.client
import io
import json
from unittest import mock

import google_crc32c
import pytest
import requests
from google.api_core import retry
from google.auth import credentials as auth_credentials
from google.cloud.exceptions import Forbidden, NotFound
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

from google.cloud.storage import (
    _helpers,
    _opentelemetry_metrics,
    fileio,
    transfer_manager,
)
from google.cloud.storage._media.requests import _request_helpers
from google.cloud.storage._media.requests.download import (
    ChunkedDownload,
    Download,
    RawChunkedDownload,
    RawDownload,
)
from google.cloud.storage._media.requests.upload import (
    MultipartUpload,
    ResumableUpload,
    SimpleUpload,
    XMLMPUContainer,
    XMLMPUPart,
)
from google.cloud.storage.client import Client
from google.cloud.storage.exceptions import DataCorruption, InvalidResponse
from google.cloud.storage.retry import DEFAULT_RETRY_IF_GENERATION_SPECIFIED


def _make_credentials():
    return auth_credentials.AnonymousCredentials()


def _crc32c_b64(data: bytes) -> str:
    checksum = google_crc32c.Checksum(data)
    return base64.b64encode(checksum.digest()).decode("ascii")


class _FakeRawStream:
    """Minimal urllib3-like raw response backing streaming and single-shot reads."""

    def __init__(self, chunks, error_after=None):
        self._chunks = list(chunks)
        self._buf = b"".join(self._chunks)
        self._error_after = error_after
        self.headers = {}

    def read(self, amt=None, decode_content=None):
        if amt is None:
            data, self._buf = self._buf, b""
            self._chunks = []
            return data
        data, self._buf = self._buf[:amt], self._buf[amt:]
        if not self._buf:
            self._chunks = []
        return data

    def stream(self, amt=8192, decode_content=None):
        for idx, chunk in enumerate(self._chunks):
            if self._error_after is not None and idx >= self._error_after:
                raise requests.ReadTimeout("mid-stream timeout")
            yield chunk

    def close(self):
        pass


def _media_response(
    body=b"",
    status_code=http.client.OK,
    headers=None,
    chunks=None,
    streaming=False,
    error_after=None,
):
    response = requests.Response()
    response.status_code = status_code
    if headers:
        response.headers.update(headers)
    chunk_list = list(chunks) if chunks is not None else ([body] if body else [])
    response.raw = _FakeRawStream(chunk_list, error_after=error_after)
    if streaming:
        response._content = False
    else:
        response._content = body
    response.request = requests.Request(
        "GET", "https://storage.googleapis.com/download/storage/v1/b/b1/o/o1"
    ).prepare()
    return response


def _json_response(payload=None, status_code=http.client.OK):
    hdrs = {"Content-Type": "application/json"}
    body = b"" if payload is None else json.dumps(payload).encode("utf-8")
    return _media_response(body=body, status_code=status_code, headers=hdrs)


def _collect_metrics(reader):
    data = reader.get_metrics_data()
    collected = {}
    if data is None:  # pragma: NO COVER
        return collected
    for resource_metric in data.resource_metrics:
        for scope_metric in resource_metric.scope_metrics:
            for metric in scope_metric.metrics:
                collected.setdefault(metric.name, []).extend(metric.data.data_points)
    return collected


@pytest.fixture(autouse=True)
def _enable_dev_gate(monkeypatch):
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)
    monkeypatch.setattr(_opentelemetry_metrics, "HAS_OPENTELEMETRY_METRICS", True)


@pytest.fixture
def metrics_env():
    reader = InMemoryMetricReader()
    provider = MeterProvider(metric_readers=[reader])
    session = mock.MagicMock()
    client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=session,
        enable_metrics=True,
        meter_provider=provider,
    )
    client._bucket_metadata_cache = None
    yield client, session, reader
    client.close()


def test_bind_suboperation_context_and_request_helpers_branches(metrics_env):
    client, session, reader = metrics_env
    recorder = client._metrics_recorder

    # 1. _bind_suboperation_context suppressed & inactive branches
    with _helpers._suppress_internal_metrics():
        with _helpers._bind_suboperation_context(
            client, "storage.fileio.BlobReader", "ReadObject"
        ) as st:
            assert st is None
        assert _request_helpers.resolve_transport_recorder(session) is None

    disabled_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=mock.MagicMock(),
        enable_metrics=False,
    )
    disabled_client._bucket_metadata_cache = None
    with _helpers._bind_suboperation_context(
        disabled_client, "storage.fileio.BlobReader", "ReadObject"
    ) as st:
        assert st is None
    assert _request_helpers.resolve_transport_recorder(disabled_client._http) is None
    disabled_client.close()

    # 2. resolve_transport_recorder via ContextVar vs transport attribute
    plain_transport = mock.MagicMock(spec=["request"])
    assert _request_helpers.resolve_transport_recorder(plain_transport) is None
    with _helpers._bind_suboperation_context(
        client, "storage.fileio.BlobReader", "ReadObject"
    ) as st:
        assert st is not None
        assert _helpers._SUPPRESS_BODY_SIZE.get() is True
        assert _request_helpers.resolve_transport_recorder(plain_transport) is recorder
    assert _helpers._SUPPRESS_BODY_SIZE.get() is False
    assert _request_helpers.resolve_transport_recorder(session) is recorder

    # Inactive recorder in _ACTIVE_METRICS_RECORDER falls through to transport
    inactive_rec = mock.Mock(standard_enabled=False)
    tok = _helpers._ACTIVE_METRICS_RECORDER.set(inactive_rec)
    try:
        assert _request_helpers.resolve_transport_recorder(session) is recorder
    finally:
        _helpers._ACTIVE_METRICS_RECORDER.reset(tok)

    # 3. Direct helper edge cases outside wait_and_retry
    _request_helpers.record_streaming_ttfb()  # No-op when state is None
    plain_transport.request.return_value = _json_response({"ok": True})
    direct_resp = _request_helpers.transport_request(
        plain_transport, "GET", "https://storage.googleapis.com/b1/o1"
    )
    assert direct_resp.status_code == 200
    assert _request_helpers._extract_status_code(direct_resp) == 200
    assert _request_helpers._extract_status_code(mock.Mock(status_code=True)) is None
    assert _request_helpers._extract_status_code(None) is None

    # 4. transport_request when ttfb_recorded is already True vs streaming=False
    manual_state = _request_helpers._MediaAttemptState(
        recorder=recorder,
        method="GET",
        fallback_url="https://storage.googleapis.com/b1/o1",
        streaming=False,
    )
    manual_state.ttfb_recorded = True
    st_tok = _request_helpers._MEDIA_ATTEMPT_STATE.set(manual_state)
    try:
        _request_helpers.transport_request(
            plain_transport, "GET", "https://storage.googleapis.com/b1/o1"
        )
    finally:
        _request_helpers._MEDIA_ATTEMPT_STATE.reset(st_tok)

    # 5. RequestsMixin & RawRequestsMixin._get_body branches: multi-chunk, 0-chunk, and pre-populated _content
    req_mixin = _request_helpers.RequestsMixin()
    req_chunks = _media_response(chunks=[b"ab", b"cd"], streaming=True)
    assert req_mixin._get_body(req_chunks) == b"abcd"
    assert req_mixin._get_body(req_chunks) == b"abcd"
    req_empty = _media_response(chunks=[], streaming=True)
    assert req_mixin._get_body(req_empty) == b""

    raw_mixin = _request_helpers.RawRequestsMixin()
    resp_chunks = _media_response(chunks=[b"ab", b"cd"], streaming=True)
    assert raw_mixin._get_body(resp_chunks) == b"abcd"
    # Second call exercises the `else:` branch where response._content is already bytes
    assert raw_mixin._get_body(resp_chunks) == b"abcd"
    resp_empty_stream = _media_response(chunks=[], streaming=True)
    assert raw_mixin._get_body(resp_empty_stream) == b""

    # 6. wait_and_retry edge branches:
    # - uninstrumented transport with and without retry_strategy
    fast_retry = retry.Retry(
        predicate=retry.if_exception_type(RuntimeError),
        initial=0.001,
        maximum=0.002,
        deadline=1.0,
    )
    calls = {"n": 0}

    def _flaky_uninstrumented():
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("retry me")
        return "done"

    assert (
        _request_helpers.wait_and_retry(
            _flaky_uninstrumented, fast_retry, transport=plain_transport
        )
        == "done"
    )
    assert (
        _request_helpers.wait_and_retry(
            lambda: "no-retry", None, transport=plain_transport
        )
        == "no-retry"
    )

    # - instrumented wait_and_retry without transport_request (custom callable returning None vs response,
    #   and raising exception carrying exc.response vs no response, outside & inside operation)
    assert (
        _request_helpers.wait_and_retry(
            lambda: None,
            None,
            transport=session,
            method="GET",
            url="https://storage.googleapis.com/download/storage/v1/b/b1/o/o1",
        )
        is None
    )
    assert (
        _request_helpers.wait_and_retry(
            lambda: _json_response({"ok": True}),
            None,
            transport=session,
            method="GET",
            url="https://storage.googleapis.com/download/storage/v1/b/b1/o/o1",
        ).status_code
        == 200
    )

    err_with_resp = requests.HTTPError("502 Bad Gateway")
    err_with_resp.response = _json_response({"err": "bad gateway"}, status_code=502)
    with pytest.raises(requests.HTTPError):
        _request_helpers.wait_and_retry(
            lambda: (_ for _ in ()).throw(err_with_resp),
            None,
            transport=session,
            method="GET",
            url="https://storage.googleapis.com/download/storage/v1/b/b1/o/o1",
        )

    # - streaming=True where transport_request succeeds with 200 and body is unconsumed
    session.request.return_value = _json_response({"ok": True})
    assert (
        _request_helpers.wait_and_retry(
            lambda: _request_helpers.transport_request(
                session,
                "GET",
                "https://storage.googleapis.com/download/storage/v1/b/b1/o/o1",
            ),
            None,
            transport=session,
            method="GET",
            url="https://storage.googleapis.com/download/storage/v1/b/b1/o/o1",
            streaming=True,
        ).status_code
        == 200
    )

    # 7. Missing status_code (None) must NOT record TTFB across transport_request,
    #    record_streaming_ttfb, or wait_and_retry (both success and InvalidResponse error paths)
    pts_before_nosc = _collect_metrics(reader)
    ttfb_before_nosc = sum(p.count for p in pts_before_nosc["gcp.storage.client.ttfb"])

    resp_no_sc = mock.Mock(status_code=None, headers={})
    session.request.return_value = resp_no_sc
    _request_helpers.wait_and_retry(
        lambda: _request_helpers.transport_request(
            session,
            "GET",
            "https://storage.googleapis.com/download/storage/v1/b/b1/o/o1",
        ),
        None,
        transport=session,
        method="GET",
        url="https://storage.googleapis.com/download/storage/v1/b/b1/o/o1",
        streaming=False,
    )

    def _streaming_no_sc_invalid():
        r = _request_helpers.transport_request(
            session,
            "GET",
            "https://storage.googleapis.com/download/storage/v1/b/b1/o/o1",
        )
        _request_helpers.record_streaming_ttfb()
        raise InvalidResponse(r, "missing status code")

    with pytest.raises(InvalidResponse):
        _request_helpers.wait_and_retry(
            _streaming_no_sc_invalid,
            None,
            transport=session,
            method="GET",
            url="https://storage.googleapis.com/download/storage/v1/b/b1/o/o1",
            streaming=True,
        )

    pts_after_nosc = _collect_metrics(reader)
    ttfb_after_nosc = sum(p.count for p in pts_after_nosc["gcp.storage.client.ttfb"])
    assert ttfb_after_nosc == ttfb_before_nosc


def test_media_downloads_ttfb_retries_and_416_zero_byte(metrics_env):
    client, session, reader = metrics_env
    media_url = "https://storage.googleapis.com/download/storage/v1/b/b1/o/o1?alt=media"
    fast_retry = retry.Retry(
        predicate=retry.if_exception_type(
            InvalidResponse, requests.ConnectionError, requests.Timeout
        ),
        initial=0.001,
        maximum=0.002,
        deadline=5.0,
    )

    # 1. Download (streaming to BytesIO, multi-chunk) with:
    #    - Attempt 1: ConnectTimeout before headers -> NO TTFB, TIMEOUT
    #    - Attempt 2: ConnectionError before headers -> NO TTFB, CONNECTION_ERROR
    #    - Attempt 3: HTTP 503 InvalidResponse -> header TTFB recorded, UNAVAILABLE
    #    - Attempt 4: HTTP 200 streaming ReadTimeout BEFORE chunk 1 -> NO TTFB, TIMEOUT
    #    - Attempt 5: HTTP 200 streaming ReadTimeout AFTER chunk 1 -> chunk-1 TTFB recorded, TIMEOUT
    #    - Attempt 6: HTTP 200 streaming success (2 chunks) -> chunk-1 TTFB recorded, OK
    payload = b"hello world!"
    crc_hdr = f"crc32c={_crc32c_b64(payload)}"
    session.request.side_effect = [
        requests.ConnectTimeout("connect timed out"),
        requests.ConnectionError("connection reset"),
        _media_response(b"unavailable", status_code=503, streaming=True),
        _media_response(
            chunks=[b"hello ", b"world!"],
            status_code=200,
            streaming=True,
            error_after=0,
        ),
        _media_response(
            chunks=[b"hello ", b"world!"],
            status_code=200,
            streaming=True,
            error_after=1,
        ),
        _media_response(
            chunks=[b"hello ", b"world!"],
            status_code=200,
            headers={"x-goog-generation": "1", "x-goog-hash": crc_hdr},
            streaming=True,
        ),
    ]
    out = io.BytesIO()
    with _helpers._start_storage_operation(
        client, "storage.Blob.download_to_file", "ReadObject"
    ):
        dl = Download(media_url, stream=out, checksum="crc32c")
        dl._retry_strategy = fast_retry
        dl.consume(session)

    # Because Attempt 5 wrote b"hello " before failing, out has b"hello hello world!"
    assert out.getvalue().endswith(payload)
    pts = _collect_metrics(reader)
    assert sum(p.value for p in pts["gcp.storage.client.operations"]) == 1
    assert sum(p.value for p in pts["gcp.storage.client.attempts"]) == 6
    assert sum(p.value for p in pts["gcp.storage.client.retries"]) == 5
    assert sum(p.value for p in pts["gcp.storage.client.errors"]) == 5
    err_by_type = {}
    for p in pts["gcp.storage.client.errors"]:
        et = p.attributes["error.type"]
        err_by_type[et] = err_by_type.get(et, 0) + p.value
    assert err_by_type == {
        "TIMEOUT": 3,
        "CONNECTION_ERROR": 1,
        "UNAVAILABLE": 1,
    }
    # TTFB recorded on Attempt 3 (503 headers), Attempt 5 (chunk 1), and Attempt 6 (chunk 1) = 3 total!
    assert sum(p.count for p in pts["gcp.storage.client.ttfb"]) == 3
    for h_pt in pts["http.client.request.duration"]:
        assert (
            h_pt.attributes["url.template"]
            == "/download/storage/v1/b/{bucket}/o/{object}"
        )

    # 2. Download single_shot_download=True (multi-slice, delayed gzip first=b"", empty, uninstrumented), empty stream, and stream=None
    large_oneshot = b"x" * 9000
    delayed_dl_resp = _media_response(b"", status_code=200, streaming=True)
    delayed_dl_resp.raw.read = mock.Mock(side_effect=[b"", b"delayed-gzip-dl"])
    session.request.side_effect = [
        _media_response(large_oneshot, status_code=200, streaming=True),
        delayed_dl_resp,
        _media_response(b"", status_code=200, streaming=True),
        _media_response(chunks=[], status_code=200, streaming=True),
        _media_response(b"nostream", status_code=200, streaming=False),
    ]
    dl_single_buf = io.BytesIO()
    dl_single = Download(media_url, stream=dl_single_buf, single_shot_download=True)
    dl_single.consume(session)
    assert dl_single_buf.getvalue() == large_oneshot
    dl_delayed_buf = io.BytesIO()
    Download(
        media_url, stream=dl_delayed_buf, single_shot_download=True, checksum=None
    ).consume(session)
    assert dl_delayed_buf.getvalue() == b"delayed-gzip-dl"
    Download(media_url, stream=io.BytesIO(), single_shot_download=True).consume(session)
    dl_empty = Download(media_url, stream=io.BytesIO(), single_shot_download=False)
    dl_empty.consume(session)
    dl_nostream = Download(media_url, stream=None)
    dl_nostream.consume(session)

    plain_transport = mock.MagicMock(spec=["request"])
    plain_transport.request.side_effect = [
        _media_response(b"plain-dl", status_code=200, streaming=True),
        _media_response(b"plain-raw", status_code=200, streaming=True),
    ]
    plain_dl_buf = io.BytesIO()
    Download(media_url, stream=plain_dl_buf, single_shot_download=True).consume(
        plain_transport
    )
    assert plain_dl_buf.getvalue() == b"plain-dl"
    plain_raw_buf = io.BytesIO()
    RawDownload(media_url, stream=plain_raw_buf, single_shot_download=True).consume(
        plain_transport
    )
    assert plain_raw_buf.getvalue() == b"plain-raw"

    # 3. RawDownload: single_shot_download=True (multi-slice, delayed first=b"", & empty), multi-chunk, empty stream, and stream=None
    delayed_raw_resp = _media_response(b"", status_code=200, streaming=True)
    delayed_raw_resp.raw.read = mock.Mock(side_effect=[b"", b"delayed-raw-body"])
    session.request.side_effect = [
        _media_response(large_oneshot, status_code=200, streaming=True),
        delayed_raw_resp,
        _media_response(b"", status_code=200, streaming=True),
        _media_response(chunks=[b"raw-", b"multi"], status_code=200, streaming=True),
        _media_response(chunks=[], status_code=200, streaming=True),
        _media_response(chunks=[b"raw-nostream"], status_code=200, streaming=True),
    ]
    raw_single_buf = io.BytesIO()
    RawDownload(media_url, stream=raw_single_buf, single_shot_download=True).consume(
        session
    )
    assert raw_single_buf.getvalue() == large_oneshot
    raw_delayed_buf = io.BytesIO()
    RawDownload(
        media_url, stream=raw_delayed_buf, single_shot_download=True, checksum=None
    ).consume(session)
    assert raw_delayed_buf.getvalue() == b"delayed-raw-body"
    RawDownload(media_url, stream=io.BytesIO(), single_shot_download=True).consume(
        session
    )
    RawDownload(media_url, stream=io.BytesIO(), single_shot_download=False).consume(
        session
    )
    RawDownload(media_url, stream=io.BytesIO(), single_shot_download=False).consume(
        session
    )
    RawDownload(media_url, stream=None).consume(session)

    # 4. ChunkedDownload & RawChunkedDownload (streaming TTFB, error response cleanup, and 0-byte 416)
    err_cd_active = _media_response(b"err", status_code=500, streaming=True)
    err_cd_active.close = mock.MagicMock(wraps=err_cd_active.close)
    err_cd_plain = _media_response(b"err", status_code=500, streaming=False)
    err_cd_plain.close = mock.MagicMock(wraps=err_cd_plain.close)

    session.request.side_effect = [
        _media_response(
            chunks=[b"ab", b"cd"],
            status_code=http.client.PARTIAL_CONTENT,
            headers={"content-range": "bytes 0-3/4", "content-length": "4"},
            streaming=True,
        ),
        err_cd_active,
        _media_response(
            chunks=[b"ab", b"cd"],
            status_code=http.client.PARTIAL_CONTENT,
            headers={"content-range": "bytes 0-3/4", "content-length": "4"},
            streaming=True,
        ),
        _media_response(
            b"",
            status_code=http.client.REQUESTED_RANGE_NOT_SATISFIABLE,
            headers={"content-range": "bytes */0"},
            streaming=True,
        ),
    ]
    cd_buf = io.BytesIO()
    cd = ChunkedDownload(media_url, chunk_size=4, stream=cd_buf)
    cd.consume_next_chunk(session)
    assert cd.finished
    assert cd_buf.getvalue() == b"abcd"

    cd_fail_active = ChunkedDownload(
        media_url, chunk_size=4, stream=io.BytesIO(), retry=None
    )
    with pytest.raises(InvalidResponse):
        cd_fail_active.consume_next_chunk(session)
    err_cd_active.close.assert_called_once()

    plain_transport.request.side_effect = [err_cd_plain]
    cd_fail_plain = ChunkedDownload(
        media_url, chunk_size=4, stream=io.BytesIO(), retry=None
    )
    with pytest.raises(InvalidResponse):
        cd_fail_plain.consume_next_chunk(plain_transport)
    err_cd_plain.close.assert_not_called()

    rcd = RawChunkedDownload(media_url, chunk_size=4, stream=io.BytesIO())
    rcd.consume_next_chunk(session)
    assert rcd.finished

    bucket = client.bucket("b1")
    zero_blob = bucket.blob("empty-obj", chunk_size=262144)
    zero_buf = io.BytesIO()
    zero_blob.download_to_file(zero_buf)
    assert zero_buf.getvalue() == b""

    pts_after = _collect_metrics(reader)
    dl_ops = [
        p
        for p in pts_after["gcp.storage.client.operations"]
        if p.attributes["gcp.client.method"] == "storage.Blob.download_to_file"
    ]
    assert sum(p.value for p in dl_ops) == 2
    assert all(p.attributes["error.type"] == "OK" for p in dl_ops)
    body_pts = pts_after["gcp.storage.client.response.body.size"]
    assert any(p.sum == 0 for p in body_pts)


def test_all_media_upload_classes_and_xml_mpu(metrics_env, tmp_path):
    client, session, reader = metrics_env
    upload_url = "https://storage.googleapis.com/upload/storage/v1/b/b1/o?uploadType=media&name=o1"
    mp_url = (
        "https://storage.googleapis.com/upload/storage/v1/b/b1/o?uploadType=multipart"
    )
    res_url = (
        "https://storage.googleapis.com/upload/storage/v1/b/b1/o?uploadType=resumable"
    )
    session_uri = "https://storage.googleapis.com/upload/storage/v1/b/b1/o?uploadType=resumable&upload_id=abc"
    xml_url = "https://storage.googleapis.com/b1/o1"

    # 1. SimpleUpload & MultipartUpload
    session.request.side_effect = [
        _json_response({"name": "o1", "size": "3"}),
        _json_response({"name": "o1", "size": "5"}),
    ]
    su = SimpleUpload(upload_url)
    su.transmit(session, b"abc", "text/plain")
    mu = MultipartUpload(mp_url)
    mu.transmit(session, b"hello", {"name": "o1"}, "text/plain")

    # 2. ResumableUpload: initiate + transmit_next_chunk + recover
    chunk_size = 256 * 1024
    ru_bytes = b"x" * chunk_size + b"y" * 10
    stream = io.BytesIO(ru_bytes)
    ru = ResumableUpload(res_url, chunk_size)
    session.request.side_effect = [
        _media_response(
            b"",
            status_code=http.client.OK,
            headers={"location": session_uri},
        ),
        _media_response(
            b"",
            status_code=http.client.PERMANENT_REDIRECT,
            headers={"range": f"bytes=0-{chunk_size - 1}"},
        ),
        _media_response(
            b"",
            status_code=http.client.PERMANENT_REDIRECT,
            headers={"range": f"bytes=0-{chunk_size - 1}"},
        ),
        _json_response(
            {
                "name": "o1",
                "size": str(chunk_size + 10),
                "crc32c": _crc32c_b64(ru_bytes),
            }
        ),
    ]
    ru.initiate(session, stream, {"name": "o1"}, "application/octet-stream")
    ru.transmit_next_chunk(session)
    # Simulate _invalid=True and recover()
    ru._invalid = True
    ru.recover(session)
    assert not ru.invalid
    ru.transmit_next_chunk(session)
    assert ru.finished

    # 3. XMLMPUContainer (initiate, finalize, cancel) & XMLMPUPart (upload)
    sample_file = tmp_path / "mpu.bin"
    sample_file.write_bytes(b"0123456789")
    xml_ns = 'xmlns="http://s3.amazonaws.com/doc/2006-03-01/"'
    session.request.side_effect = [
        _media_response(
            f"<InitiateMultipartUploadResult {xml_ns}><UploadId>u-123</UploadId></InitiateMultipartUploadResult>".encode(
                "utf-8"
            ),
            status_code=200,
        ),
        _media_response(
            b"",
            status_code=200,
            headers={
                "ETag": '"etag-1"',
                "x-goog-hash": f"crc32c={_crc32c_b64(b'0123456789')}",
            },
        ),
        _media_response(
            f'<CompleteMultipartUploadResult {xml_ns}><ETag>"final"</ETag></CompleteMultipartUploadResult>'.encode(
                "utf-8"
            ),
            status_code=200,
        ),
        _media_response(b"", status_code=204),
    ]
    container = XMLMPUContainer(xml_url, str(sample_file))
    container.initiate(session, content_type="application/octet-stream")
    assert container.upload_id == "u-123"
    part = XMLMPUPart(
        xml_url,
        "u-123",
        str(sample_file),
        start=0,
        end=10,
        part_number=1,
        checksum="crc32c",
    )
    part.upload(session)
    container.register_part(1, part.etag)
    container.finalize(session)
    container.cancel(session)

    pts = _collect_metrics(reader)
    templates = {
        p.attributes["url.template"] for p in pts["http.client.request.duration"]
    }
    assert "/upload/storage/v1/b/{bucket}/o" in templates
    assert "/{bucket}/{object}" in templates
    assert sum(p.value for p in pts["gcp.storage.client.attempts"]) == 10


def test_blob_media_methods_body_size_and_corruption_cleanup(metrics_env, tmp_path):
    client, session, reader = metrics_env
    bucket = client.bucket("b1")
    blob = bucket.blob("o1")
    payload = b"storage-payload"
    crc_hdr = f"crc32c={_crc32c_b64(payload)}"

    # 1. download_to_file (with ConditionalRetryPolicy), download_as_bytes, download_as_string, download_to_filename
    dl_file = tmp_path / "downloaded.bin"
    blob._properties["updated"] = "2026-01-02T03:04:05.000Z"
    session.request.side_effect = [
        _media_response(
            payload,
            status_code=200,
            headers={"x-goog-generation": "7", "x-goog-hash": crc_hdr},
            streaming=True,
        ),
        _media_response(
            payload,
            status_code=200,
            headers={"x-goog-generation": "7", "x-goog-hash": crc_hdr},
            streaming=True,
        ),
        _media_response(
            payload,
            status_code=200,
            headers={"x-goog-generation": "7", "x-goog-hash": crc_hdr},
            streaming=True,
        ),
        _media_response(
            payload,
            status_code=200,
            headers={"x-goog-generation": "7", "x-goog-hash": crc_hdr},
            streaming=True,
        ),
    ]
    blob.download_to_file(
        io.BytesIO(),
        if_generation_match=7,
        retry=DEFAULT_RETRY_IF_GENERATION_SPECIFIED,
    )
    assert blob.download_as_bytes() == payload
    with pytest.warns(PendingDeprecationWarning):
        assert blob.download_as_string() == payload
    blob.download_to_filename(str(dl_file))
    assert dl_file.read_bytes() == payload
    assert isinstance(blob.updated, datetime.datetime)

    # 2. download_to_filename NotFound & DataCorruption remove file and record NOT_FOUND / CHECKSUM_MISMATCH
    missing_dest = tmp_path / "missing.bin"
    corrupt_dest = tmp_path / "corrupt.bin"
    session.request.side_effect = [
        _json_response({"error": {"message": "not found"}}, status_code=404),
        _media_response(
            b"tampered",
            status_code=200,
            headers={"x-goog-generation": "7", "x-goog-hash": crc_hdr},
            streaming=True,
        ),
    ]
    with pytest.raises(NotFound):
        blob.download_to_filename(str(missing_dest), retry=None)
    assert not missing_dest.exists()

    with pytest.raises(DataCorruption):
        blob.download_to_filename(str(corrupt_dest), retry=None)
    assert not corrupt_dest.exists()

    # 3. Multipart upload_from_string, upload_from_filename, and failed upload_from_file
    up_file = tmp_path / "upload.txt"
    up_file.write_bytes(b"from-disk")
    session.request.side_effect = [
        _json_response({"name": "o1", "size": "9"}),
        _json_response({"name": "o1", "size": "9"}),
        _json_response({"error": {"message": "forbidden"}}, status_code=403),
    ]
    blob.upload_from_string(b"123456789")
    blob.upload_from_filename(str(up_file))
    with pytest.raises(Forbidden):
        blob.upload_from_file(io.BytesIO(b"denied"), size=6, retry=None)

    # 4. Multi-chunk ResumableUpload success + DataCorruption suppressing self.delete()
    res_blob = bucket.blob("resumable-obj", chunk_size=256 * 1024)
    res_data = b"a" * (256 * 1024) + b"b" * 100
    session_uri = "https://storage.googleapis.com/upload/storage/v1/b/b1/o?uploadType=resumable&upload_id=r1"
    session.request.side_effect = [
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _media_response(
            b"",
            status_code=http.client.PERMANENT_REDIRECT,
            headers={"range": f"bytes=0-{256 * 1024 - 1}"},
        ),
        _json_response(
            {
                "name": "resumable-obj",
                "size": str(len(res_data)),
                "crc32c": _crc32c_b64(res_data),
            }
        ),
    ]
    res_blob.upload_from_file(io.BytesIO(res_data))

    # Resumable DataCorruption triggers self.delete() which MUST be suppressed!
    session.request.side_effect = [
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _json_response(None, status_code=204),  # suppressed self.delete()
    ]
    with mock.patch.object(
        ResumableUpload,
        "transmit_next_chunk",
        side_effect=DataCorruption(mock.Mock(), "hash mismatch"),
    ):
        with pytest.raises(DataCorruption):
            res_blob.upload_from_file(io.BytesIO(b"corrupt"), retry=None)

    # 5. Defensive branches in _do_download / _do_multipart_upload / _do_resumable_upload
    #    when recorder is None or _bytes_downloaded / bytes_uploaded is bool
    disabled_session = mock.MagicMock()
    disabled_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=disabled_session,
        enable_metrics=False,
    )
    disabled_client._bucket_metadata_cache = None
    d_blob = disabled_client.bucket("b1").blob("o1")
    disabled_session.request.side_effect = [
        _media_response(b"ok", status_code=200, streaming=True),
        _json_response({"name": "o1", "size": "2"}),
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _json_response({"name": "o1", "size": "2", "crc32c": _crc32c_b64(b"ok")}),
    ]
    d_blob.download_to_file(io.BytesIO())
    d_blob.upload_from_string(b"ok")
    d_res_blob = disabled_client.bucket("b1").blob("o2", chunk_size=256 * 1024)
    d_res_blob.upload_from_file(io.BytesIO(b"ok"))
    disabled_client.close()

    with mock.patch.object(
        Download,
        "consume",
        autospec=True,
        side_effect=lambda self_dl, *a, **kw: (
            setattr(self_dl, "_bytes_downloaded", True) or _media_response(b"")
        ),
    ):
        blob._do_download(
            session,
            io.BytesIO(),
            "https://storage.googleapis.com/download/storage/v1/b/b1/o/o1?alt=media",
            {},
        )
    mock_up = mock.MagicMock()
    mock_up.finished = False
    mock_up.resumable_url = session_uri

    def _finish_bool(*a, **kw):
        mock_up.finished = True
        mock_up.bytes_uploaded = True
        return _json_response({"name": "o1"})

    mock_up.transmit_next_chunk.side_effect = _finish_bool
    with mock.patch.object(
        res_blob,
        "_initiate_resumable_upload",
        return_value=(mock_up, session),
    ):
        res_blob.upload_from_file(io.BytesIO(b"x"))

    with _helpers._suppress_body_size():
        session.request.side_effect = [
            _json_response({"name": "o1", "size": "3"}),
            _media_response(b"", status_code=200, headers={"location": session_uri}),
            _json_response({"name": "o1", "size": "3", "crc32c": _crc32c_b64(b"sup")}),
        ]
        blob.upload_from_string(b"sup")
        res_blob.upload_from_file(io.BytesIO(b"sup"))

    pts = _collect_metrics(reader)
    ops = pts["gcp.storage.client.operations"]
    assert not any(p.attributes["gcp.storage.operation"] == "DeleteObject" for p in ops)
    op_err_pairs = {
        (p.attributes["gcp.storage.operation"], p.attributes["error.type"]) for p in ops
    }
    assert ("ReadObject", "NOT_FOUND") in op_err_pairs
    assert ("ReadObject", "CHECKSUM_MISMATCH") in op_err_pairs
    assert ("WriteObject", "CHECKSUM_MISMATCH") in op_err_pairs
    resp_sizes = [p.sum for p in pts["gcp.storage.client.response.body.size"]]
    assert resp_sizes.count(len(payload)) == 4
    req_sizes = [p.sum for p in pts["gcp.storage.client.request.body.size"]]
    assert len(res_data) in req_sizes
    assert 9 in req_sizes


def test_blob_open_and_fileio_stream_lifetime_metrics(metrics_env):
    client, session, reader = metrics_env
    bucket = client.bucket("b1")

    # 1. Blob.open validation errors before stream construction
    b_open = bucket.blob("open-validate")
    invalid_open_calls = [
        (
            {"mode": "rb", "encoding": "utf-8"},
            ValueError,
            "ReadObject",
            "CLIENT_VALIDATION_ERROR",
        ),
        (
            {"mode": "rb", "ignore_flush": True},
            ValueError,
            "ReadObject",
            "CLIENT_VALIDATION_ERROR",
        ),
        (
            {"mode": "wb", "encoding": "utf-8"},
            ValueError,
            "WriteObject",
            "CLIENT_VALIDATION_ERROR",
        ),
        (
            {"mode": "rt", "ignore_flush": True},
            ValueError,
            "ReadObject",
            "CLIENT_VALIDATION_ERROR",
        ),
        (
            {"mode": "wt", "ignore_flush": False},
            ValueError,
            "WriteObject",
            "CLIENT_VALIDATION_ERROR",
        ),
        ({"mode": "rw"}, NotImplementedError, "ReadObject", "UNKNOWN"),
        ({"mode": "wx"}, NotImplementedError, "WriteObject", "UNKNOWN"),
        ({"mode": "ab"}, NotImplementedError, "UNKNOWN", "UNKNOWN"),
    ]
    for kwargs, exc_cls, expected_op, expected_err in invalid_open_calls:
        with pytest.raises(exc_cls):
            b_open.open(**kwargs)
    pts_val = _collect_metrics(reader)
    assert sum(p.value for p in pts_val["gcp.storage.client.operations"]) == len(
        invalid_open_calls
    )
    seen_pairs = [
        (p.attributes["gcp.storage.operation"], p.attributes["error.type"])
        for p in pts_val["gcp.storage.client.operations"]
    ]
    for _, _, expected_op, expected_err in invalid_open_calls:
        assert (expected_op, expected_err) in seen_pairs

    # 2. Blob.open TextIOWrapper construction failure cleans up raw_reader / raw_writer
    with pytest.raises(ValueError):
        b_open.open("rt", newline="invalid-newline")
    with pytest.raises(ValueError):
        b_open.open("wt", newline="invalid-newline")

    # 3. Blob.open("rb"), ("rt"), ("wb"), ("wt") attribute stream lifetime to storage.Blob.open
    #    and record exact caller-consumed / caller-written bytes (not prefetched bytes!)
    read_blob = bucket.blob("stream-read")
    session.request.side_effect = [
        # Blob.open("rb", chunk_size=8): caller reads only 3 bytes, then closes!
        _media_response(
            b"01234567",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"x-goog-generation": "1", "content-range": "bytes 0-7/16"},
            streaming=True,
        ),
        # Blob.open("rt", chunk_size=8): reads all "hello" + 416 EOF
        _media_response(
            b"hello",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"x-goog-generation": "1", "content-range": "bytes 0-4/5"},
            streaming=True,
        ),
        _json_response(
            {"error": {"message": "range not satisfiable"}}, status_code=416
        ),
    ]
    with read_blob.open("rb", chunk_size=8) as r_bin:
        assert r_bin.read1(3) == b"012"
    r_bin.close()  # Idempotent second close emits nothing

    with read_blob.open("rt", chunk_size=8, encoding="utf-8") as r_txt:
        assert r_txt.read() == "hello"

    write_blob = bucket.blob("stream-write")
    session_uri = "https://storage.googleapis.com/upload/storage/v1/b/b1/o?uploadType=resumable&upload_id=w1"
    chunk_sz = 256 * 1024
    wb_payload = b"x" * chunk_sz + b"12345"
    session.request.side_effect = [
        # Blob.open("wb"): multi-chunk write (chunk 1 uploaded during write(), tail during close())
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _media_response(
            b"",
            status_code=http.client.PERMANENT_REDIRECT,
            headers={"range": f"bytes=0-{chunk_sz - 1}"},
        ),
        _json_response(
            {
                "name": "stream-write",
                "size": str(chunk_sz + 5),
                "crc32c": _crc32c_b64(wb_payload),
            }
        ),
        # Blob.open("wt"): small text write uploaded during close()
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _json_response(
            {
                "name": "stream-write",
                "size": "4",
                "crc32c": _crc32c_b64(b"text"),
            }
        ),
    ]
    with write_blob.open("wb", chunk_size=chunk_sz) as w_bin:
        w_bin.write(b"x" * chunk_sz + b"12345")
    w_bin.close()  # Idempotent second close

    with write_blob.open("wt", encoding="utf-8") as w_txt:
        w_txt.write("text")

    pts_streams = _collect_metrics(reader)
    resp_pts = [
        p
        for p in pts_streams["gcp.storage.client.response.body.size"]
        if p.attributes["gcp.client.method"] == "storage.Blob.open"
    ]
    # Sum of 3 bytes (from rb partial read) + 5 bytes (from rt full read) = 8 bytes!
    assert sum(p.sum for p in resp_pts) == 8
    assert sum(p.count for p in resp_pts) == 2

    req_pts = [
        p
        for p in pts_streams["gcp.storage.client.request.body.size"]
        if p.attributes["gcp.client.method"] == "storage.Blob.open"
    ]
    assert sum(p.sum for p in req_pts) == (chunk_sz + 5) + 4
    assert sum(p.count for p in req_pts) == 2


def test_direct_blob_reader_and_writer_edge_cases_and_errors(metrics_env):
    client, session, reader = metrics_env
    bucket = client.bucket("b1")
    blob = bucket.blob("direct-fileio")

    # 1. Suppressed / disabled BlobReader & BlobWriter construction (with valid kwargs)
    with _helpers._suppress_internal_metrics():
        sup_r = fileio.BlobReader(blob, raw_download=True)
        sup_r.close()
        sup_w = fileio.BlobWriter(blob, content_type="text/plain")
        sup_w.terminate()

    # 2. Invalid constructor arguments on direct BlobReader & BlobWriter
    with pytest.raises(ValueError):
        fileio.BlobReader(blob, unsupported_kwarg=123)
    with pytest.raises(ValueError):
        fileio.BlobWriter(blob, unsupported_kwarg=123)
    with pytest.raises(ValueError):
        fileio.BlobWriter(blob, chunk_size=100)  # Not a multiple of 256 KiB

    # 3. BlobReader seek(whence=2) triggering blob.reload() (success & failure) + invalid whence
    seek_blob = bucket.blob("seek-blob")
    session.request.side_effect = [
        _json_response({"name": "seek-blob", "size": "10", "generation": "1"}),
    ]
    sr = fileio.BlobReader(seek_blob, chunk_size=4)
    assert sr.seek(-2, 2) == 8
    with pytest.raises(ValueError):
        sr.seek(0, 99)
    sr.close()

    seek_fail_blob = bucket.blob("seek-fail")
    session.request.side_effect = [
        _json_response({"error": {"message": "missing"}}, status_code=404),
    ]
    sr_fail = fileio.BlobReader(seek_fail_blob, retry=None)
    with pytest.raises(NotFound):
        sr_fail.seek(0, 2)
    sr_fail.close()

    # 4. BlobReader mid-stream read error (with 0 bytes read vs >0 bytes read)
    err_blob = bucket.blob("read-err")
    session.request.side_effect = [
        _json_response({"error": {"message": "missing"}}, status_code=404),
        _media_response(
            b"abcd",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"x-goog-generation": "1", "content-range": "bytes 0-3/8"},
            streaming=True,
        ),
        _json_response({"error": {"message": "gone"}}, status_code=404),
    ]
    r_zero = fileio.BlobReader(err_blob, chunk_size=4, retry=None)
    with pytest.raises(NotFound):
        r_zero.read(4)
    r_zero.close()

    r_partial = fileio.BlobReader(err_blob, chunk_size=4, retry=None)
    assert r_partial.read(4) == b"abcd"
    with pytest.raises(NotFound):
        r_partial.read(4)
    r_partial.close()

    # 5. BlobWriter:
    #    - terminate() before initiate -> CANCELLED
    #    - terminate() after initiate -> suppresses transport.delete(), records CANCELLED
    #    - error during write() inside context manager -> __exit__ calls terminate(), records error
    #    - error during close() -> records error, no body size
    session_uri = "https://storage.googleapis.com/upload/storage/v1/b/b1/o?uploadType=resumable&upload_id=term1"
    chunk_sz = 256 * 1024

    w_cancel_early = fileio.BlobWriter(blob, chunk_size=chunk_sz)
    w_cancel_early.terminate()

    session.request.side_effect = [
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _media_response(
            b"",
            status_code=http.client.PERMANENT_REDIRECT,
            headers={"range": f"bytes=0-{chunk_sz - 1}"},
        ),
    ]
    session.delete.return_value = _json_response(None, status_code=499)
    w_cancel_active = fileio.BlobWriter(blob, chunk_size=chunk_sz)
    w_cancel_active.write(b"a" * chunk_sz)
    w_cancel_active.terminate()
    session.delete.assert_called_once()

    session.request.side_effect = [
        _json_response({"error": {"message": "denied"}}, status_code=403),
    ]
    with pytest.raises(InvalidResponse):
        with fileio.BlobWriter(blob, chunk_size=chunk_sz, retry=None) as w_err:
            w_err.write(b"a" * chunk_sz)

    session.request.side_effect = [
        _json_response({"error": {"message": "unavailable"}}, status_code=503),
    ]
    w_close_err = fileio.BlobWriter(blob, chunk_size=chunk_sz, retry=None)
    w_close_err.write(b"small")
    with pytest.raises(InvalidResponse):
        w_close_err.close()

    pts = _collect_metrics(reader)
    reader_ops = [
        p
        for p in pts["gcp.storage.client.operations"]
        if p.attributes["gcp.client.method"] == "storage.fileio.BlobReader"
    ]
    writer_ops = [
        p
        for p in pts["gcp.storage.client.operations"]
        if p.attributes["gcp.client.method"] == "storage.fileio.BlobWriter"
    ]
    assert sum(p.value for p in reader_ops) == 5
    assert sum(p.value for p in writer_ops) == 6
    cancelled_pts = [p for p in writer_ops if p.attributes["error.type"] == "CANCELLED"]
    assert sum(p.value for p in cancelled_pts) == 2
    # seek() reload must NOT have emitted any GetObject logical operation
    assert not any(
        p.attributes["gcp.storage.operation"] == "GetObject"
        for p in pts["gcp.storage.client.operations"]
    )


def test_transfer_manager_many_operations_thread_and_process(metrics_env, tmp_path):
    client, session, reader = metrics_env
    bucket = client.bucket("tm-bucket")

    f1 = tmp_path / "u1.txt"
    f1.write_bytes(b"file-1")
    f2 = tmp_path / "u2.txt"
    f2.write_bytes(b"file-2")

    # 1. upload_many (THREAD) with filename (multipart) + BytesIO (resumable)
    tm_res_uri = "https://storage.googleapis.com/upload/storage/v1/b/tm-bucket/o?uploadType=resumable&upload_id=tm1"

    def _tm_upload_transport(method, url, **kw):
        if method == "POST" and "uploadType=resumable" in url:
            return _media_response(
                b"", status_code=200, headers={"location": tm_res_uri}
            )
        if method == "PUT":
            return _json_response(
                {"name": "b2", "size": "5", "crc32c": _crc32c_b64(b"mem-2")}
            )
        return _json_response({"name": "b1", "size": "6"})

    session.request.side_effect = _tm_upload_transport
    res_up = transfer_manager.upload_many(
        [(str(f1), bucket.blob("b1")), (io.BytesIO(b"mem-2"), bucket.blob("b2"))],
        worker_type=transfer_manager.THREAD,
        max_workers=2,
        raise_exception=True,
    )
    assert res_up == [None, None]

    # 2. upload_many_from_filenames (THREAD) attributes gcp.client.method properly
    session.request.side_effect = lambda method, url, **kw: _json_response(
        {"name": "uploaded", "size": "6"}
    )
    transfer_manager.upload_many_from_filenames(
        bucket,
        ["u1.txt", "u2.txt"],
        source_directory=str(tmp_path),
        worker_type=transfer_manager.THREAD,
        max_workers=2,
        raise_exception=True,
    )

    # 3. download_many (THREAD) with filename, skipped existing file, and BytesIO
    existing_dest = tmp_path / "already_exists.txt"
    existing_dest.write_bytes(b"keep")
    new_dest = tmp_path / "d1.txt"
    payload = b"dl-bytes"
    crc_hdr = f"crc32c={_crc32c_b64(payload)}"
    session.request.side_effect = lambda method, url, **kw: _media_response(
        payload,
        status_code=200,
        headers={"x-goog-generation": "1", "x-goog-hash": crc_hdr},
        streaming=True,
    )
    mem_out = io.BytesIO()
    transfer_manager.download_many(
        [
            (bucket.blob("skip-me"), str(existing_dest)),
            (bucket.blob("d1"), str(new_dest)),
            (bucket.blob("d2"), mem_out),
        ],
        skip_if_exists=True,
        worker_type=transfer_manager.THREAD,
        max_workers=2,
        raise_exception=True,
    )
    assert new_dest.read_bytes() == payload
    assert mem_out.getvalue() == payload

    # 4. download_many_to_path (THREAD) attributes gcp.client.method properly
    dl_dir = tmp_path / "dl_dir"
    dl_dir.mkdir()
    session.request.side_effect = [
        _media_response(
            payload,
            status_code=200,
            headers={"x-goog-generation": "1", "x-goog-hash": crc_hdr},
            streaming=True,
        ),
    ]
    transfer_manager.download_many_to_path(
        bucket,
        ["p1.txt"],
        destination_directory=str(dl_dir),
        worker_type=transfer_manager.THREAD,
        max_workers=1,
        raise_exception=True,
    )
    assert (dl_dir / "p1.txt").read_bytes() == payload

    # 5. PROCESS worker_type pickling branches (using ThreadPoolExecutor stand-in for deterministic mock transport)
    with pytest.raises(ValueError):
        transfer_manager.upload_many(
            [(io.BytesIO(b"bad"), bucket.blob("bad"))],
            worker_type=transfer_manager.PROCESS,
        )
    with pytest.raises(ValueError):
        transfer_manager.download_many(
            [(bucket.blob("bad"), io.BytesIO())],
            worker_type=transfer_manager.PROCESS,
        )

    proc_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        enable_metrics=False,
    )
    proc_client._bucket_metadata_cache = None
    proc_bucket = proc_client.bucket("proc-b")
    proc_dest = tmp_path / "proc_dl.txt"
    with mock.patch(
        "google.cloud.storage.transfer_manager._get_pool_class_and_requirements",
        return_value=(concurrent.futures.ThreadPoolExecutor, True),
    ):
        with mock.patch.object(
            transfer_manager.Blob, "_handle_filename_and_upload", return_value=None
        ):
            transfer_manager.upload_many(
                [(str(f1), proc_bucket.blob("pb1"))],
                worker_type=transfer_manager.PROCESS,
                max_workers=1,
                raise_exception=True,
            )
        with mock.patch.object(
            transfer_manager.Blob, "_handle_filename_and_download", return_value=None
        ):
            transfer_manager.download_many(
                [(proc_bucket.blob("pb1"), str(proc_dest))],
                worker_type=transfer_manager.PROCESS,
                max_workers=1,
                raise_exception=True,
            )
    proc_client.close()

    pts = _collect_metrics(reader)
    by_method = {}
    for p in pts["gcp.storage.client.operations"]:
        key = (
            p.attributes["gcp.client.method"],
            p.attributes["gcp.storage.operation"],
        )
        by_method[key] = by_method.get(key, 0) + p.value

    assert by_method == {
        ("storage.transfer_manager.upload_many", "WriteObject"): 2,
        ("storage.transfer_manager.upload_many_from_filenames", "WriteObject"): 2,
        ("storage.transfer_manager.download_many", "ReadObject"): 2,
        ("storage.transfer_manager.download_many_to_path", "ReadObject"): 1,
    }


def test_transfer_manager_concurrent_chunked_operations(metrics_env, tmp_path):
    client, session, reader = metrics_env
    bucket = client.bucket("chunked-bucket")

    # 1. download_chunks_concurrently validation errors -> CLIENT_VALIDATION_ERROR
    v_blob = bucket.blob("val-blob")
    with pytest.raises(ValueError):
        transfer_manager.download_chunks_concurrently(
            v_blob, str(tmp_path / "v1"), download_kwargs={"start": 0}
        )
    with pytest.raises(ValueError):
        transfer_manager.download_chunks_concurrently(
            v_blob, str(tmp_path / "v2"), download_kwargs={"checksum": "md5"}
        )

    # 2. download_chunks_concurrently (THREAD): reload + 2 shards -> 1 ReadObject, 1 body size, 3 HTTP attempts
    full_data = b"0123456789"
    full_crc = _crc32c_b64(full_data)
    d_blob = bucket.blob("sharded-dl")

    def _sharded_get(method, url, **kwargs):
        if "/storage/v1/b/" in url and "/download/" not in url:
            return _json_response(
                {
                    "name": "sharded-dl",
                    "size": "10",
                    "generation": "42",
                    "crc32c": full_crc,
                }
            )
        rng = (kwargs.get("headers") or {}).get("range", "")
        if rng == "bytes=0-5":
            return _media_response(
                b"012345",
                status_code=http.client.PARTIAL_CONTENT,
                headers={"content-range": "bytes 0-5/10", "x-goog-generation": "42"},
                streaming=True,
            )
        return _media_response(
            b"6789",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"content-range": "bytes 6-9/10", "x-goog-generation": "42"},
            streaming=True,
        )

    session.request.side_effect = _sharded_get
    dl_target = tmp_path / "sharded_out.bin"
    transfer_manager.download_chunks_concurrently(
        d_blob,
        str(dl_target),
        chunk_size=6,
        worker_type=transfer_manager.THREAD,
        max_workers=2,
        crc32c_checksum=True,
    )
    assert dl_target.read_bytes() == full_data

    # 3. download_chunks_concurrently CRC32C mismatch -> CHECKSUM_MISMATCH, no body size recorded
    bad_blob = bucket.blob("bad-crc")
    bad_blob._properties.update(
        {"size": 4, "generation": "9", "crc32c": _crc32c_b64(b"zzzz")}
    )
    session.request.side_effect = [
        _media_response(
            b"abcd",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"content-range": "bytes 0-3/4", "x-goog-generation": "9"},
            streaming=True,
        )
    ]
    with pytest.raises(DataCorruption):
        transfer_manager.download_chunks_concurrently(
            bad_blob,
            str(tmp_path / "bad_crc.bin"),
            chunk_size=4,
            worker_type=transfer_manager.THREAD,
            max_workers=1,
            crc32c_checksum=True,
        )

    # 4. upload_chunks_concurrently (THREAD): initiate + 2 parts + finalize -> 1 WriteObject, 1 body size, 4 attempts
    up_src = tmp_path / "sharded_up.bin"
    up_src.write_bytes(b"abcdefghij")
    u_blob = (
        bucket.bucket.blob("u")
        if hasattr(bucket, "bucket")
        else bucket.blob("sharded-up")
    )
    u_blob._bucket = bucket.__class__(client, "chunked-bucket", user_project="up-proj")
    u_blob.kms_key_name = "projects/p/locations/l/keyRings/r/cryptoKeys/k"

    xml_ns = 'xmlns="http://s3.amazonaws.com/doc/2006-03-01/"'

    def _mpu_transport(method, url, **kwargs):
        if method == "POST" and "uploads" in url:
            return _media_response(
                f"<InitiateMultipartUploadResult {xml_ns}><UploadId>mpu-1</UploadId></InitiateMultipartUploadResult>".encode(
                    "utf-8"
                ),
                status_code=200,
            )
        if method == "PUT":
            part_bytes = kwargs.get("data", b"")
            return _media_response(
                b"",
                status_code=200,
                headers={
                    "ETag": '"part-etag"',
                    "x-goog-hash": f"crc32c={_crc32c_b64(part_bytes)}",
                },
            )
        return _media_response(
            f'<CompleteMultipartUploadResult {xml_ns}><ETag>"done"</ETag></CompleteMultipartUploadResult>'.encode(
                "utf-8"
            ),
            status_code=200,
        )

    session.request.side_effect = _mpu_transport
    transfer_manager.upload_chunks_concurrently(
        str(up_src),
        u_blob,
        chunk_size=6,
        worker_type=transfer_manager.THREAD,
        max_workers=2,
    )

    # 5. upload_chunks_concurrently part failure triggers suppressed container.cancel()
    def _mpu_fail_transport(method, url, **kwargs):
        if method == "POST" and "uploads" in url:
            return _media_response(
                f"<InitiateMultipartUploadResult {xml_ns}><UploadId>mpu-fail</UploadId></InitiateMultipartUploadResult>".encode(
                    "utf-8"
                ),
                status_code=200,
            )
        if method == "PUT":
            return _json_response({"error": {"message": "503"}}, status_code=503)
        # DELETE abort call
        return _media_response(b"", status_code=204)

    session.request.side_effect = _mpu_fail_transport
    with pytest.raises(InvalidResponse):
        transfer_manager.upload_chunks_concurrently(
            str(up_src),
            bucket.blob("sharded-up-fail"),
            chunk_size=10,
            worker_type=transfer_manager.THREAD,
            max_workers=1,
            retry=None,
        )

    # 6. PROCESS pickling & suppressed / disabled metrics branches for chunked helpers
    with _helpers._suppress_body_size():
        session.request.side_effect = _mpu_transport
        transfer_manager.upload_chunks_concurrently(
            str(up_src),
            bucket.blob("suppressed-body-up"),
            chunk_size=10,
            worker_type=transfer_manager.THREAD,
            max_workers=1,
        )
        zero_sharded = bucket.blob("zero-sharded")
        zero_sharded._properties.update({"size": 4, "generation": "1"})
        session.request.side_effect = [
            _media_response(
                b"0123",
                status_code=http.client.PARTIAL_CONTENT,
                headers={"content-range": "bytes 0-3/4", "x-goog-generation": "1"},
                streaming=True,
            )
        ]
        transfer_manager.download_chunks_concurrently(
            zero_sharded,
            str(tmp_path / "sup_dl.bin"),
            chunk_size=4,
            worker_type=transfer_manager.THREAD,
            max_workers=1,
            crc32c_checksum=False,
        )

    proc_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        enable_metrics=False,
    )
    proc_client._bucket_metadata_cache = None
    p_blob = proc_client.bucket("pb").blob("po")
    p_blob._properties.update({"size": 4, "generation": "1"})
    with mock.patch(
        "google.cloud.storage.transfer_manager._get_pool_class_and_requirements",
        return_value=(concurrent.futures.ThreadPoolExecutor, True),
    ):
        with mock.patch.object(
            transfer_manager.Blob, "_prep_and_do_download", return_value=None
        ):
            transfer_manager.download_chunks_concurrently(
                p_blob,
                str(tmp_path / "proc_sharded.bin"),
                chunk_size=4,
                worker_type=transfer_manager.PROCESS,
                max_workers=1,
                crc32c_checksum=False,
            )
        with mock.patch.object(XMLMPUContainer, "initiate"):
            with mock.patch.object(XMLMPUContainer, "finalize"):
                with mock.patch.object(XMLMPUPart, "upload"):
                    transfer_manager.upload_chunks_concurrently(
                        str(up_src),
                        p_blob,
                        chunk_size=10,
                        worker_type=transfer_manager.PROCESS,
                        max_workers=1,
                    )
    proc_client.close()

    pts = _collect_metrics(reader)
    dl_chunk_ops = [
        p
        for p in pts["gcp.storage.client.operations"]
        if p.attributes["gcp.client.method"]
        == "storage.transfer_manager.download_chunks_concurrently"
    ]
    # 2 validation errors + 1 success + 1 CRC mismatch + 1 suppressed-body success = 5 logical ops
    assert sum(p.value for p in dl_chunk_ops) == 5
    assert any(p.attributes["error.type"] == "CHECKSUM_MISMATCH" for p in dl_chunk_ops)

    up_chunk_ops = [
        p
        for p in pts["gcp.storage.client.operations"]
        if p.attributes["gcp.client.method"]
        == "storage.transfer_manager.upload_chunks_concurrently"
    ]
    # 1 success + 1 part failure + 1 suppressed-body success = 3 logical ops
    assert sum(p.value for p in up_chunk_ops) == 3

    # Verify container.cancel DELETE request was completely suppressed from HTTP attempts!
    assert not any(
        p.attributes.get("http.request.method") == "DELETE"
        for p in pts["http.client.request.duration"]
    )
    # Verify exact single body size recording for sharded download (10) and sharded upload (10)
    resp_body = pts["gcp.storage.client.response.body.size"]
    assert sum(p.count for p in resp_body) == 1
    assert resp_body[0].sum == 10
    req_body = pts["gcp.storage.client.request.body.size"]
    assert sum(p.count for p in req_body) == 1
    assert req_body[0].sum == 10


def test_text_io_wrapper_gc_safety_and_error_recovery(metrics_env):
    client, session, reader = metrics_env
    bucket = client.bucket("b1")
    session_uri = "https://storage.googleapis.com/upload/storage/v1/b/b1/o?uploadType=resumable&upload_id=txt1"

    # 1. Disabled client preserves exact stdlib io.TextIOWrapper; enabled uses _MetricsTextIOWrapper
    disabled_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=mock.MagicMock(),
        enable_metrics=False,
    )
    disabled_client._bucket_metadata_cache = None
    d_blob = disabled_client.bucket("b1").blob("plain-txt")
    t_read = d_blob.open("rt")
    t_write = d_blob.open("wt")
    assert type(t_read) is io.TextIOWrapper
    assert type(t_write) is io.TextIOWrapper
    t_read.close()
    t_write.buffer.terminate()
    disabled_client.close()

    # 2. _MetricsTextIOWrapper: readline, seek(0), __next__ (StopIteration & UnicodeDecodeError),
    #    read UnicodeDecodeError, seek/truncate UnsupportedOperation, and detached buffer safety
    txt_blob = bucket.blob("txt-read")
    txt_blob._properties["size"] = 12
    session.request.side_effect = [
        _media_response(
            b"line1\nline2\n",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"x-goog-generation": "1", "content-range": "bytes 0-11/12"},
            streaming=True,
        ),
        _json_response({"error": {"message": "eof"}}, status_code=416),
        _media_response(
            b"\xff\xfe",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"x-goog-generation": "1", "content-range": "bytes 0-1/2"},
            streaming=True,
        ),
        _media_response(
            b"ok\n\xff\xfe",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"x-goog-generation": "1", "content-range": "bytes 0-4/5"},
            streaming=True,
        ),
    ]
    with txt_blob.open("rt", chunk_size=16, encoding="utf-8") as f_ok:
        assert type(f_ok) is fileio._MetricsTextIOWrapper
        assert f_ok.seek(0) == 0
        assert f_ok.readline() == "line1\n"
        assert list(f_ok) == ["line2\n"]

    with pytest.raises(UnicodeDecodeError):
        with txt_blob.open("rt", chunk_size=16, encoding="utf-8") as f_bad_read:
            f_bad_read.read()

    with pytest.raises(UnicodeDecodeError):
        with txt_blob.open("rt", chunk_size=16, encoding="utf-8") as f_bad_iter:
            list(f_bad_iter)

    with pytest.raises(io.UnsupportedOperation):
        with txt_blob.open("rt", chunk_size=16, encoding="utf-8") as f_bad_seek:
            f_bad_seek.seek(1, io.SEEK_CUR)

    with pytest.raises(io.UnsupportedOperation):
        with txt_blob.open("rt", chunk_size=16, encoding="utf-8") as f_bad_trunc:
            f_bad_trunc.truncate()

    f_detached = txt_blob.open("rt", chunk_size=16, encoding="utf-8")
    raw_detached = f_detached.detach()
    with pytest.raises(ValueError, match="detached"):
        f_detached.read()
    with pytest.raises(ValueError, match="detached"):
        next(f_detached)
    del f_detached
    gc.collect()
    raw_detached.close()

    # 3. _MetricsTextIOWrapper write, writelines, UnicodeEncodeError abort, context-exit abort,
    #    closed exit, and BlobWriter.close() primary error preservation (R2-#3)
    chunk_sz = 256 * 1024
    w_txt_blob = bucket.blob("txt-write")
    session.request.side_effect = [
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _json_response(
            {"name": "txt-write", "size": "6", "crc32c": _crc32c_b64(b"a\nb\nc\n")}
        ),
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _json_response(
            {"name": "txt-write", "size": "2", "crc32c": _crc32c_b64(b"hi")}
        ),
    ]
    with w_txt_blob.open("wt", encoding="ascii") as fw_ok:
        fw_ok.writelines(["a\n", "b\n"])
        fw_ok.write("c\n")

    session.request.reset_mock()
    session.request.side_effect = None
    with pytest.raises(UnicodeEncodeError):
        with w_txt_blob.open("wt", encoding="ascii") as fw_enc_err:
            fw_enc_err.write("\u2603")
    assert session.request.call_count == 0
    assert fw_enc_err.closed

    with pytest.raises(RuntimeError, match="caller-boom"):
        with w_txt_blob.open("wt", encoding="utf-8") as fw_abort:
            fw_abort.write("buffered-data-never-flushed")
            raise RuntimeError("caller-boom")
    assert session.request.call_count == 0
    assert fw_abort.closed

    session.request.side_effect = [
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _json_response(
            {"name": "txt-write", "size": "2", "crc32c": _crc32c_b64(b"hi")}
        ),
    ]
    with pytest.raises(RuntimeError, match="after-explicit-close"):
        with w_txt_blob.open("wt", encoding="utf-8") as fw_already_closed:
            fw_already_closed.write("hi")
            fw_already_closed.close()
            raise RuntimeError("after-explicit-close")

    # Buffered flush during TextIOWrapper.close() fails with 403 InvalidResponse, then
    # BlobWriter.close() hits secondary ValueError("Upload is in an invalid state."):
    # must preserve PERMISSION_DENIED rather than overwriting with CLIENT_VALIDATION_ERROR!
    session.request.side_effect = [
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _json_response({"error": {"message": "forbidden"}}, status_code=403),
    ]
    fw_flush_403 = w_txt_blob.open(
        "wt", encoding="ascii", chunk_size=chunk_sz, retry=None
    )
    fw_flush_403.buffer.write(b"a" * (chunk_sz - 2))
    fw_flush_403.write("bc")
    with pytest.raises(ValueError, match="invalid state"):
        fw_flush_403.close()

    # Caught UnicodeEncodeError followed by real HTTP 503 during close() must record UNAVAILABLE!
    session.request.side_effect = [
        _json_response({"error": {"message": "unavailable"}}, status_code=503),
    ]
    fw_close_503 = w_txt_blob.open(
        "wt", encoding="ascii", chunk_size=chunk_sz, retry=None
    )
    fw_close_503.write("ok")
    with pytest.raises(UnicodeEncodeError):
        fw_close_503.write("\u2603")
    with pytest.raises(InvalidResponse):
        fw_close_503.close()

    # 4. GC safety (__del__) on unclosed BlobReader, BlobWriter, uninitialized BlobReader, and _MetricsTextIOWrapper
    pts_before_gc = _collect_metrics(reader)
    ops_before_gc = sum(p.value for p in pts_before_gc["gcp.storage.client.operations"])
    session.request.reset_mock()
    session.request.side_effect = AssertionError("GC must never trigger network I/O")

    unclosed_r = fileio.BlobReader(bucket.blob("gc-r"))
    unclosed_w = fileio.BlobWriter(bucket.blob("gc-w"))
    unclosed_w.write(b"unflushed")
    uninit_r = fileio.BlobReader.__new__(fileio.BlobReader)
    unclosed_tw = bucket.blob("gc-tw").open("wt")
    unclosed_tw.write("unflushed-text")
    del unclosed_r, unclosed_w, uninit_r, unclosed_tw
    gc.collect()

    assert session.request.call_count == 0
    pts_after_gc = _collect_metrics(reader)
    ops_after_gc = sum(p.value for p in pts_after_gc["gcp.storage.client.operations"])
    assert ops_after_gc == ops_before_gc

    # 5. BlobWriter.terminate() finalizes CANCELLED metric and closes buffer even if transport.delete raises
    session.request.side_effect = [
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _media_response(
            b"",
            status_code=http.client.PERMANENT_REDIRECT,
            headers={"range": f"bytes=0-{chunk_sz - 1}"},
        ),
    ]
    session.delete.side_effect = requests.ConnectionError("abort transport down")
    w_term_err = fileio.BlobWriter(bucket.blob("term-err"), chunk_size=chunk_sz)
    w_term_err.write(b"x" * chunk_sz)
    with pytest.raises(requests.ConnectionError, match="abort transport down"):
        w_term_err.terminate()
    assert w_term_err.closed
    session.delete.side_effect = None

    # 6. Transient error recovery on BlobReader (caught seek + read error -> OK) and BlobWriter (caught write error -> OK)
    rec_r_blob = bucket.blob("recover-read")
    rec_r_blob._properties["size"] = 4
    session.request.side_effect = [
        _json_response({"error": {"message": "transient"}}, status_code=404),
        _media_response(
            b"good",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"x-goog-generation": "1", "content-range": "bytes 0-3/4"},
            streaming=True,
        ),
    ]
    rec_r = fileio.BlobReader(rec_r_blob, chunk_size=4, retry=None)
    with pytest.raises(ValueError):
        rec_r.seek(0, 99)
    with pytest.raises(NotFound):
        rec_r.read(4)
    assert rec_r.read(4) == b"good"
    rec_r.close()

    rec_w_blob = bucket.blob("recover-write")
    w_data = b"a" * chunk_sz + b"b" * chunk_sz
    session.request.side_effect = [
        _json_response({"error": {"message": "transient"}}, status_code=503),
        _media_response(b"", status_code=200, headers={"location": session_uri}),
        _media_response(
            b"",
            status_code=http.client.PERMANENT_REDIRECT,
            headers={"range": f"bytes=0-{chunk_sz - 1}"},
        ),
        _media_response(
            b"",
            status_code=http.client.PERMANENT_REDIRECT,
            headers={"range": f"bytes=0-{2 * chunk_sz - 1}"},
        ),
        _json_response(
            {
                "name": "recover-write",
                "size": str(2 * chunk_sz),
                "crc32c": _crc32c_b64(w_data),
            }
        ),
    ]
    rec_w = fileio.BlobWriter(rec_w_blob, chunk_size=chunk_sz, retry=None)
    with pytest.raises(InvalidResponse):
        rec_w.write(b"a" * chunk_sz)
    rec_w.write(b"b" * chunk_sz)
    rec_w.close()

    pts_final = _collect_metrics(reader)
    r_ok = [
        p
        for p in pts_final["gcp.storage.client.operations"]
        if p.attributes["gcp.client.method"] == "storage.fileio.BlobReader"
        and p.attributes["error.type"] == "OK"
    ]
    assert sum(p.value for p in r_ok) == 1
    w_ops = [
        p
        for p in pts_final["gcp.storage.client.operations"]
        if p.attributes["gcp.client.method"] == "storage.fileio.BlobWriter"
    ]
    assert {(p.attributes["error.type"], p.value) for p in w_ops} == {
        ("CANCELLED", 1),
        ("OK", 1),
    }
    open_ops = [
        p
        for p in pts_final["gcp.storage.client.operations"]
        if p.attributes["gcp.client.method"] == "storage.Blob.open"
    ]
    open_by_pair = {}
    for p in open_ops:
        k = (p.attributes["gcp.storage.operation"], p.attributes["error.type"])
        open_by_pair[k] = open_by_pair.get(k, 0) + p.value
    assert open_by_pair == {
        ("ReadObject", "OK"): 2,
        ("ReadObject", "CLIENT_VALIDATION_ERROR"): 2,
        ("ReadObject", "CONNECTION_ERROR"): 2,
        ("WriteObject", "OK"): 2,
        ("WriteObject", "CLIENT_VALIDATION_ERROR"): 1,
        ("WriteObject", "CANCELLED"): 1,
        ("WriteObject", "PERMISSION_DENIED"): 1,
        ("WriteObject", "UNAVAILABLE"): 1,
    }


def test_round1_transfer_manager_and_primary_exception_fixes(
    metrics_env, tmp_path, monkeypatch
):
    client, session, reader = metrics_env
    bucket = client.bucket("r1-bucket")
    session_uri = "https://storage.googleapis.com/upload/storage/v1/b/r1-bucket/o?uploadType=resumable&upload_id=r1"
    xml_ns = 'xmlns="http://s3.amazonaws.com/doc/2006-03-01/"'

    # 1. _record_primary_exception edge cases & nested _start_storage_operation exception (R2-#2):
    #    - outside op is a safe no-op
    #    - nested cleanup chaining (c2.__context__ = c1) preserves first primary exception
    #    - caught cleanup followed by unrelated exception does NOT leak stale pin
    #    - caught cleanup followed by a second independent cleanup updates pin
    _helpers._record_primary_exception(
        RuntimeError("outside-op"), RuntimeError("outside-cleanup")
    )
    c1 = RuntimeError("cleanup-1")
    c2 = RuntimeError("cleanup-2")
    c2.__context__ = c1
    with pytest.raises(RuntimeError, match="cleanup-2"):
        with _helpers._start_storage_operation(client, "outer.chained", "WriteObject"):
            _helpers._record_primary_exception(ValueError("first-pin"), c1)
            _helpers._record_primary_exception(KeyError("second-ignored"), c2)
            with pytest.raises(RuntimeError, match="nested-boom"):
                with _helpers._start_storage_operation(
                    client, "inner.method", "DeleteObject"
                ):
                    raise RuntimeError("nested-boom")
            raise c2

    with pytest.raises(ValueError, match="unrelated-after-caught"):
        with _helpers._start_storage_operation(client, "outer.caught", "WriteObject"):
            _helpers._record_primary_exception(
                DataCorruption(mock.Mock(), "stale"), RuntimeError("caught-cleanup")
            )
            raise ValueError("unrelated-after-caught")

    c_second = RuntimeError("independent-cleanup")
    with pytest.raises(RuntimeError, match="independent-cleanup"):
        with _helpers._start_storage_operation(client, "outer.repinned", "WriteObject"):
            _helpers._record_primary_exception(
                ValueError("caught-pin"), RuntimeError("caught-cleanup")
            )
            _helpers._record_primary_exception(KeyError("fresh-pin"), c_second)
            raise c_second

    # 2. Blob._do_resumable_upload DataCorruption where cleanup self.delete() raises a multi-hop
    #    chained exception (Forbidden -> ConnectionError -> DataCorruption):
    #    Forbidden propagates with ALL intermediate __context__ links intact, while WriteObject
    #    records CHECKSUM_MISMATCH!
    res_blob = bucket.blob("corrupt-cleanup-err", chunk_size=256 * 1024)
    session.request.side_effect = [
        _media_response(b"", status_code=200, headers={"location": session_uri}),
    ]
    corrupt_exc = DataCorruption(mock.Mock(), "bad crc")
    mid_conn_exc = requests.ConnectionError("delete retry transport failure")
    top_cleanup_exc = Forbidden("delete denied after retry")

    def _chained_delete(*args, **kwargs):
        try:
            raise mid_conn_exc
        except requests.ConnectionError:
            raise top_cleanup_exc

    with (
        mock.patch.object(
            ResumableUpload,
            "transmit_next_chunk",
            side_effect=corrupt_exc,
        ),
        mock.patch.object(res_blob, "delete", side_effect=_chained_delete),
    ):
        with pytest.raises(Forbidden) as exc_info:
            res_blob.upload_from_file(io.BytesIO(b"bad"), retry=None)
    assert exc_info.value is top_cleanup_exc
    assert exc_info.value.__context__ is mid_conn_exc
    assert exc_info.value.__context__.__context__ is corrupt_exc

    # 3. upload_chunks_concurrently where part upload raises 403 InvalidResponse AND container.cancel raises ConnectionError:
    #    ConnectionError propagates to caller, but WriteObject records PERMISSION_DENIED!
    up_src = tmp_path / "mpu_cleanup.bin"
    up_src.write_bytes(b"0123456789")
    session.request.side_effect = [
        _media_response(
            f"<InitiateMultipartUploadResult {xml_ns}><UploadId>u-clean</UploadId></InitiateMultipartUploadResult>".encode(
                "utf-8"
            ),
            status_code=200,
        ),
        _json_response({"error": {"message": "part forbidden"}}, status_code=403),
        requests.ConnectionError("cancel network down"),
    ]
    with pytest.raises(requests.ConnectionError, match="cancel network down"):
        transfer_manager.upload_chunks_concurrently(
            str(up_src),
            bucket.blob("mpu-cleanup-err"),
            chunk_size=10,
            worker_type=transfer_manager.THREAD,
            max_workers=1,
            retry=None,
        )

    # 4. download_chunks_concurrently honors download_kwargs["client"] (including blob.reload(client=...))
    disabled_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=mock.MagicMock(),
        enable_metrics=False,
    )
    disabled_client._bucket_metadata_cache = None
    foreign_blob = disabled_client.bucket("r1-bucket").blob("foreign-sharded")
    full_bytes = b"abcdefgh"
    session.request.side_effect = [
        _json_response(
            {
                "name": "foreign-sharded",
                "size": "8",
                "generation": "5",
                "crc32c": _crc32c_b64(full_bytes),
            }
        ),
        _media_response(
            b"abcd",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"content-range": "bytes 0-3/8", "x-goog-generation": "5"},
            streaming=True,
        ),
        _media_response(
            b"efgh",
            status_code=http.client.PARTIAL_CONTENT,
            headers={"content-range": "bytes 4-7/8", "x-goog-generation": "5"},
            streaming=True,
        ),
    ]
    foreign_out = tmp_path / "foreign_out.bin"
    transfer_manager.download_chunks_concurrently(
        foreign_blob,
        str(foreign_out),
        chunk_size=4,
        download_kwargs={"client": client},
        worker_type=transfer_manager.THREAD,
        max_workers=1,
        crc32c_checksum=True,
    )
    assert foreign_out.read_bytes() == full_bytes
    disabled_client.close()

    # 5. upload_many_from_filenames & download_many_to_path with needs_pickling=True preserve gcp.client.method,
    #    and _suppress_internal_metrics() propagates across needs_pickling=True for all 4 transfer_manager helpers!
    src_dir = tmp_path / "proc_src"
    src_dir.mkdir()
    (src_dir / "f1.txt").write_bytes(b"hello")
    dst_dir = tmp_path / "proc_dst"
    dst_dir.mkdir()

    with monkeypatch.context() as mp_cache:
        mp_cache.setattr(transfer_manager, "_cached_clients", {id(client): client})
        with mock.patch(
            "google.cloud.storage.transfer_manager._get_pool_class_and_requirements",
            return_value=(concurrent.futures.ThreadPoolExecutor, True),
        ):
            session.request.side_effect = [
                _json_response({"name": "f1.txt", "size": "5"}),
                _media_response(
                    b"hello",
                    status_code=200,
                    headers={
                        "x-goog-generation": "1",
                        "x-goog-hash": f"crc32c={_crc32c_b64(b'hello')}",
                    },
                    streaming=True,
                ),
            ]
            transfer_manager.upload_many_from_filenames(
                bucket,
                ["f1.txt"],
                source_directory=str(src_dir),
                worker_type=transfer_manager.PROCESS,
                max_workers=1,
                raise_exception=True,
            )
            transfer_manager.download_many_to_path(
                bucket,
                ["f1.txt"],
                destination_directory=str(dst_dir),
                worker_type=transfer_manager.PROCESS,
                max_workers=1,
                raise_exception=True,
            )
            assert (dst_dir / "f1.txt").read_bytes() == b"hello"

            pts_pre_sup = _collect_metrics(reader)
            attempts_pre_sup = sum(
                p.value for p in pts_pre_sup["gcp.storage.client.attempts"]
            )
            ops_pre_sup = sum(
                p.value for p in pts_pre_sup["gcp.storage.client.operations"]
            )

            sup_blob = bucket.blob("sup-sharded")
            sup_blob._properties.update({"size": 4, "generation": "1"})
            session.request.side_effect = [
                _json_response({"name": "f1.txt", "size": "5"}),
                _media_response(
                    b"hello",
                    status_code=200,
                    headers={
                        "x-goog-generation": "1",
                        "x-goog-hash": f"crc32c={_crc32c_b64(b'hello')}",
                    },
                    streaming=True,
                ),
                _media_response(
                    b"0123",
                    status_code=http.client.PARTIAL_CONTENT,
                    headers={"content-range": "bytes 0-3/4", "x-goog-generation": "1"},
                    streaming=True,
                ),
                _media_response(
                    f"<InitiateMultipartUploadResult {xml_ns}><UploadId>u-sup</UploadId></InitiateMultipartUploadResult>".encode(
                        "utf-8"
                    ),
                    status_code=200,
                ),
                _media_response(
                    b"",
                    status_code=200,
                    headers={
                        "ETag": '"e1"',
                        "x-goog-hash": f"crc32c={_crc32c_b64(b'0123456789')}",
                    },
                ),
                _media_response(
                    f'<CompleteMultipartUploadResult {xml_ns}><ETag>"done"</ETag></CompleteMultipartUploadResult>'.encode(
                        "utf-8"
                    ),
                    status_code=200,
                ),
            ]
            with _helpers._suppress_internal_metrics():
                transfer_manager.upload_many(
                    [(str(src_dir / "f1.txt"), bucket.blob("sup-u"))],
                    worker_type=transfer_manager.PROCESS,
                    max_workers=1,
                    raise_exception=True,
                )
                transfer_manager.download_many(
                    [(bucket.blob("sup-d"), str(tmp_path / "sup_d.txt"))],
                    worker_type=transfer_manager.PROCESS,
                    max_workers=1,
                    raise_exception=True,
                )
                transfer_manager.download_chunks_concurrently(
                    sup_blob,
                    str(tmp_path / "sup_chunk_d.bin"),
                    chunk_size=4,
                    worker_type=transfer_manager.PROCESS,
                    max_workers=1,
                    crc32c_checksum=False,
                )
                transfer_manager.upload_chunks_concurrently(
                    str(up_src),
                    bucket.blob("sup-chunk-u"),
                    chunk_size=10,
                    worker_type=transfer_manager.PROCESS,
                    max_workers=1,
                )

            pts_post_sup = _collect_metrics(reader)
            assert (
                sum(p.value for p in pts_post_sup["gcp.storage.client.attempts"])
                == attempts_pre_sup
            )
            assert (
                sum(p.value for p in pts_post_sup["gcp.storage.client.operations"])
                == ops_pre_sup
            )

    # 6. Isolated _LazyClient & _cleanup_cached_clients branches (R2-#4 & R2-#5), plus real subprocess smoke test
    with monkeypatch.context() as mp:
        fake_atexit = mock.MagicMock()
        fake_finalize = mock.MagicMock()
        mp.setattr(transfer_manager, "_cached_clients", {})
        mp.setattr(transfer_manager, "_cleanup_registered_pid", None)
        mp.setattr(transfer_manager.atexit, "register", fake_atexit)
        mp.setattr(transfer_manager.multiprocessing.util, "Finalize", fake_finalize)

        base_pos = ("proj", _make_credentials(), mock.MagicMock(), None, None)
        c5 = transfer_manager._LazyClient("id-5", *base_pos, {}, True, False)
        assert transfer_manager._LazyClient("id-5", *base_pos) is c5
        transfer_manager._LazyClient("id-5only", *base_pos, enable_metrics=False)
        transfer_manager._LazyClient(
            "id-6", *base_pos, {"X-Test": "1"}, enable_metrics=False
        )
        transfer_manager._LazyClient("id-7", *base_pos, {}, False)
        transfer_manager._LazyClient("id-8", *base_pos, {}, False, False)
        fake_atexit.assert_called_once_with(transfer_manager._cleanup_cached_clients)
        fake_finalize.assert_called_once_with(
            None, transfer_manager._cleanup_cached_clients, exitpriority=10
        )

        # Active metrics client triggers force_flush once; second call is idempotent empty-cache no-op!
        flush_provider = mock.Mock(spec=["force_flush"])
        with mock.patch.object(
            _opentelemetry_metrics.metrics,
            "get_meter_provider",
            return_value=flush_provider,
        ):
            transfer_manager._cleanup_cached_clients()
            transfer_manager._cleanup_cached_clients()
        flush_provider.force_flush.assert_called_once()
        assert transfer_manager._cached_clients == {}

        # Disabled clients close cleanly (even when one close() raises) WITHOUT touching MeterProvider!
        bad_close_cl = mock.Mock(
            metrics_enabled=False,
            debug_metrics_enabled=False,
            close=mock.Mock(side_effect=RuntimeError("close boom")),
        )
        ok_close_cl = mock.Mock(metrics_enabled=False, debug_metrics_enabled=False)
        transfer_manager._cached_clients.update({"b1": bad_close_cl, "b2": ok_close_cl})
        with mock.patch.object(
            _opentelemetry_metrics.metrics,
            "get_meter_provider",
            side_effect=AssertionError("must not flush when metrics disabled"),
        ):
            transfer_manager._cleanup_cached_clients()
        bad_close_cl.close.assert_called_once()
        ok_close_cl.close.assert_called_once()

        # force_flush exception is swallowed cleanly; provider without force_flush; metrics=None
        err_flush_provider = mock.Mock(
            spec=["force_flush"],
            force_flush=mock.Mock(side_effect=RuntimeError("flush boom")),
        )
        transfer_manager._cached_clients["dbg"] = mock.Mock(
            metrics_enabled=False, debug_metrics_enabled=True
        )
        with mock.patch.object(
            _opentelemetry_metrics.metrics,
            "get_meter_provider",
            return_value=err_flush_provider,
        ):
            transfer_manager._cleanup_cached_clients()
        err_flush_provider.force_flush.assert_called_once()

        transfer_manager._cached_clients["act-no-flush"] = mock.Mock(
            metrics_enabled=True, debug_metrics_enabled=False
        )
        with mock.patch.object(
            _opentelemetry_metrics.metrics,
            "get_meter_provider",
            return_value=object(),
        ):
            transfer_manager._cleanup_cached_clients()

        transfer_manager._cached_clients["act-no-otel"] = mock.Mock(
            metrics_enabled=True, debug_metrics_enabled=False
        )
        mp.setattr(_opentelemetry_metrics, "metrics", None)
        transfer_manager._cleanup_cached_clients()

    real_proc_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        client_options={"api_endpoint": "http://127.0.0.1:1"},
        enable_metrics=True,
    )
    real_proc_client._bucket_metadata_cache = None
    real_results = transfer_manager.upload_many(
        [(str(src_dir / "f1.txt"), real_proc_client.bucket("b").blob("o"))],
        upload_kwargs={"retry": None, "timeout": 0.2},
        worker_type=transfer_manager.PROCESS,
        max_workers=1,
        raise_exception=False,
    )
    assert len(real_results) == 1
    assert isinstance(real_results[0], Exception)
    real_proc_client.close()

    pts = _collect_metrics(reader)
    by_method_err = {
        (
            p.attributes["gcp.client.method"],
            p.attributes["gcp.storage.operation"],
            p.attributes["error.type"],
        ): p.value
        for p in pts["gcp.storage.client.operations"]
    }
    assert (
        "outer.chained",
        "WriteObject",
        "CLIENT_VALIDATION_ERROR",
    ) in by_method_err
    assert (
        "outer.caught",
        "WriteObject",
        "CLIENT_VALIDATION_ERROR",
    ) in by_method_err
    assert (
        "outer.repinned",
        "WriteObject",
        "UNKNOWN",
    ) in by_method_err
    assert (
        "storage.Blob.upload_from_file",
        "WriteObject",
        "CHECKSUM_MISMATCH",
    ) in by_method_err
    assert (
        "storage.transfer_manager.upload_chunks_concurrently",
        "WriteObject",
        "PERMISSION_DENIED",
    ) in by_method_err
    assert (
        "storage.transfer_manager.download_chunks_concurrently",
        "ReadObject",
        "OK",
    ) in by_method_err
    assert (
        "storage.transfer_manager.upload_many_from_filenames",
        "WriteObject",
        "OK",
    ) in by_method_err
    assert (
        "storage.transfer_manager.download_many_to_path",
        "ReadObject",
        "OK",
    ) in by_method_err
