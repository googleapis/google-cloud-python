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

"""Unit tests for OpenTelemetry standard metrics across HTTP JSON & Veneer."""

import functools
import http.client
import io
import json
from unittest import mock

import pytest
import requests
from google.api_core import iam, retry
from google.auth import credentials as auth_credentials
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace import TracerProvider

from google.cloud.storage import _helpers, _opentelemetry_metrics
from google.cloud.storage._bucket_metadata_cache import BucketMetadataCache
from google.cloud.storage.acl import ACL, BucketACL, DefaultObjectACL, ObjectACL
from google.cloud.storage.blob import Blob
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.client import Client
from google.cloud.storage.hmac_key import HMACKeyMetadata
from google.cloud.storage.notification import BucketNotification


def _make_credentials():
    return auth_credentials.AnonymousCredentials()


def _json_response(payload=None, status_code=http.client.OK, headers=None):
    response = requests.Response()
    response.status_code = status_code
    response.headers.update({"Content-Type": "application/json"})
    if headers:
        response.headers.update(headers)
    if payload is not None:
        response._content = (
            payload
            if isinstance(payload, bytes)
            else json.dumps(payload).encode("utf-8")
        )
    else:
        response._content = b""
    response.request = requests.Request(
        "GET", "https://storage.googleapis.com/storage/v1/b"
    ).prepare()
    return response


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
    # Disable async daemon cache fetches from consuming session.request.side_effect
    client._bucket_metadata_cache = None
    yield client, session, reader
    client.close()


def test_client_metrics_disabled_by_default_and_fast_paths(monkeypatch):
    monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", False)
    session = mock.MagicMock()
    session.request.return_value = _json_response({"items": []})
    client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=session,
        enable_metrics=True,
    )
    assert client._metrics_recorder.enabled is False
    iterator = client.list_buckets()
    assert isinstance(iterator.api_request, functools.partial)
    assert list(iterator) == []
    resp = client._connection._make_request("GET", "/b")
    assert resp.status_code == http.client.OK
    client.close()


def test_client_custom_endpoint_and_owned_shutdown(monkeypatch):
    session = mock.MagicMock()
    session.request.return_value = _json_response({"email_address": "sa@example.com"})
    reader = InMemoryMetricReader()
    provider = MeterProvider(metric_readers=[reader])
    client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=session,
        client_options={"api_endpoint": "https://custom.storage.example.com:8443"},
        enable_metrics=True,
        meter_provider=provider,
    )
    assert client.get_service_account_email() == "sa@example.com"
    pts = _collect_metrics(reader)
    op_pt = pts["gcp.storage.client.operations"][0]
    dur_pt = pts["gcp.client.request.duration"][0]
    assert op_pt.attributes["server.address"] == "custom.storage.example.com"
    assert dur_pt.attributes["server.address"] == "custom.storage.example.com"
    assert op_pt.attributes["rpc.system.name"] == "http"

    att_pt = pts["gcp.storage.client.attempts"][0]
    http_dur_pt = pts["http.client.request.duration"][0]
    assert att_pt.attributes["server.address"] == "custom.storage.example.com"
    assert http_dur_pt.attributes["server.address"] == "custom.storage.example.com"
    assert att_pt.attributes["network.path"] == "cloudpath"

    with client:
        pass

    with mock.patch.object(client._metrics_recorder, "shutdown") as mock_shutdown:
        client.close()
    mock_shutdown.assert_called_once()

    # Immutable _http and missing _metrics_recorder on close() are safe no-ops
    ro_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=object(),
        enable_metrics=True,
    )
    assert ro_client._http is ro_client._http_internal
    assert ro_client.metrics_enabled is True
    assert ro_client.debug_metrics_enabled is False
    ro_client._metrics_recorder.shutdown()
    ro_client._metrics_recorder = None
    assert ro_client.metrics_enabled is False
    assert ro_client.debug_metrics_enabled is False
    assert ro_client._http is ro_client._http_internal
    ro_client.close()

    # Lazy _http session creation attaches _gcs_metrics_recorder on first access
    lazy_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=None,
        enable_metrics=True,
        meter_provider=provider,
    )
    lazy_client._bucket_metadata_cache = None
    lazy_session = mock.MagicMock()
    with mock.patch(
        "google.cloud.client.ClientWithProject._http",
        new_callable=mock.PropertyMock,
        return_value=lazy_session,
    ):
        assert lazy_client._http is lazy_session
        assert lazy_session._gcs_metrics_recorder is lazy_client._metrics_recorder
    lazy_client.close()


def test_helpers_context_managers_and_mixin_fallbacks():
    class _BrokenClientObj:
        _client = "fallback-client"

        @property
        def client(self):
            raise RuntimeError("unbound")

    broken = _BrokenClientObj()
    assert _helpers._resolve_operation_client(broken, client="explicit") == "explicit"
    assert _helpers._resolve_operation_client(broken) == "fallback-client"

    with _helpers._suppress_body_size():
        assert _helpers._SUPPRESS_BODY_SIZE.get() is True
    assert _helpers._SUPPRESS_BODY_SIZE.get() is False

    with _helpers._list_metrics_context("outer.method", "ListObjects"):
        with _helpers._list_metrics_context("inner.method", "ListBuckets"):
            assert _helpers._LIST_METRICS_CONTEXT.get() == (
                "outer.method",
                "ListObjects",
            )
    assert _helpers._LIST_METRICS_CONTEXT.get() is None

    with _helpers._client_method_override("outer.override"):
        with _helpers._client_method_override("inner.override"):
            assert _helpers._CLIENT_METHOD_OVERRIDE.get() == "outer.override"
    assert _helpers._CLIENT_METHOD_OVERRIDE.get() is None

    # Custom _PropertyMixin without _METRICS_CLASS_NAME executes uninstrumented branch
    class _CustomResource(_helpers._PropertyMixin):
        path = "/custom/1"
        user_project = None

        def __init__(self, client):
            super().__init__(name="c1")
            self._client = client

        @property
        def client(self):
            return self._client

    mock_client = mock.MagicMock()
    mock_client._get_resource.return_value = {"k": "v"}
    mock_client._patch_resource.return_value = {"k": "v2"}
    mock_client._put_resource.return_value = {"k": "v3"}
    res = _CustomResource(mock_client)
    res.reload()
    res.patch()
    res.update()
    assert res._properties == {"k": "v3"}


def test_http_connection_direct_make_request_and_edge_branches(metrics_env):
    client, session, reader = metrics_env
    conn = client._connection

    # 1. Suppressed internal metrics bypasses recording
    session.request.return_value = _json_response({"ok": True})
    with _helpers._suppress_internal_metrics():
        with _helpers._start_storage_operation(
            client, "storage.Client.get_bucket", "GetBucket"
        ) as st:
            assert st is None
        conn._make_request("GET", "https://storage.googleapis.com/storage/v1/b/b1")
        conn.api_request(method="GET", path="/b/b1")
    assert _collect_metrics(reader) == {}

    # 2. Direct _make_request network exception -> CONNECTION_ERROR, no TTFB, no status_code
    session.request.side_effect = requests.ConnectionError("reset by peer")
    with _helpers._start_storage_operation(client, "storage.Batch.finish", "Batch"):
        with pytest.raises(requests.ConnectionError):
            conn._make_request(
                "POST", "https://storage.googleapis.com/batch/storage/v1"
            )
    pts = _collect_metrics(reader)
    assert "gcp.storage.client.ttfb" not in pts
    att = pts["gcp.storage.client.attempts"][-1]
    assert att.attributes["error.type"] == "CONNECTION_ERROR"
    assert "http.response.status_code" not in att.attributes

    # 3. Direct _make_request non-2xx with normal response AND broken response object
    session.request.side_effect = None
    session.request.return_value = _json_response(
        {"error": {"message": "unavailable"}}, status_code=503
    )
    resp_503 = conn._make_request(
        "POST", "https://storage.googleapis.com/batch/storage/v1"
    )
    assert resp_503.status_code == 503

    broken_resp = mock.Mock()
    broken_resp.status_code = 500
    session.request.return_value = broken_resp
    conn._make_request("POST", "https://storage.googleapis.com/batch/storage/v1")

    bool_sc_resp = mock.Mock()
    bool_sc_resp.status_code = True
    session.request.return_value = bool_sc_resp
    conn._make_request("POST", "https://storage.googleapis.com/batch/storage/v1")

    pts2 = _collect_metrics(reader)
    statuses = [
        p.attributes.get("http.response.status_code")
        for p in pts2["http.client.request.duration"]
    ]
    assert 503 in statuses
    assert 500 in statuses
    assert statuses[-1] is None
    assert sum(p.count for p in pts2["gcp.storage.client.ttfb"]) == 2

    # 4. api_request fallback branches when base_call bypasses _make_request or url is empty
    with mock.patch("google.cloud._http.JSONConnection.api_request", return_value={}):
        conn.api_request("GET", "/b/my-bucket")
    weird_resp = _json_response({"ok": True})
    weird_resp.status_code = True  # bool is excluded from int status_code
    with mock.patch.object(
        _helpers._opentelemetry_metrics,
        "normalize_url_template",
        wraps=_opentelemetry_metrics.normalize_url_template,
    ):
        session.request.return_value = _json_response({"ok": True})
        with mock.patch(
            "google.cloud._http.JSONConnection._make_request",
            return_value=weird_resp,
        ):
            with mock.patch(
                "google.cloud._http.JSONConnection.api_request",
                side_effect=lambda *a, **kw: (conn._make_request("GET", "") and {}),
            ):
                conn.api_request(method="GET", path="/b/my-bucket")

        with mock.patch(
            "google.cloud._http.JSONConnection._make_request",
            return_value=weird_resp,
        ):
            with mock.patch(
                "google.cloud._http.JSONConnection.api_request",
                side_effect=lambda *a, **kw: (
                    conn._make_request("GET", "")
                    and (_ for _ in ()).throw(RuntimeError("boom"))
                ),
            ):
                with pytest.raises(RuntimeError):
                    conn.api_request(method="GET", path="/b/my-bucket")


def test_retries_errors_ttfb_and_checksum_classification(metrics_env):
    client, session, reader = metrics_env
    session.request.side_effect = [
        _json_response({"error": {"message": "503-1"}}, status_code=503),
        requests.ConnectionError("transient reset"),
        _json_response({"id": "my-bucket", "name": "my-bucket"}, status_code=200),
    ]
    fast_retry = retry.Retry(initial=0.001, maximum=0.002, deadline=5.0)
    bucket = client.get_bucket("my-bucket", retry=fast_retry)
    assert bucket.name == "my-bucket"

    pts = _collect_metrics(reader)
    assert len(pts["gcp.storage.client.operations"]) == 1
    op = pts["gcp.storage.client.operations"][0]
    dur = pts["gcp.client.request.duration"][0]
    assert op.attributes["gcp.storage.operation"] == "GetBucket"
    assert op.attributes["gcp.client.method"] == "storage.Client.get_bucket"
    assert op.attributes["error.type"] == "OK"
    assert dur.attributes["rpc.method"] == "google.storage.v2.Storage/GetBucket"
    assert dur.attributes["error.type"] == "OK"

    attempts = pts["gcp.storage.client.attempts"]
    assert sum(p.value for p in attempts) == 3
    err_types = {p.attributes.get("error.type", "OK") for p in attempts}
    assert err_types == {"UNAVAILABLE", "CONNECTION_ERROR", "OK"}

    retries_pts = pts["gcp.storage.client.retries"]
    assert sum(p.value for p in retries_pts) == 2
    retry_errs = {p.attributes["error.type"] for p in retries_pts}
    assert retry_errs == {"UNAVAILABLE", "CONNECTION_ERROR"}

    errors_pts = pts["gcp.storage.client.errors"]
    assert sum(p.value for p in errors_pts) == 2

    # TTFB recorded only for the 503 response and the 200 response (NOT ConnectionError)
    ttfb_pts = pts["gcp.storage.client.ttfb"]
    assert sum(p.count for p in ttfb_pts) == 2

    # Terminal HTTP 400 BadRequest maps to INVALID_ARGUMENT
    session.request.side_effect = [
        _json_response(
            {"error": {"message": "Invalid bucket configuration"}},
            status_code=400,
        )
    ]
    b = client.bucket("my-bucket")
    with pytest.raises(Exception):
        b.patch(retry=None)
    pts_after = _collect_metrics(reader)
    patch_ops = [
        p
        for p in pts_after["gcp.storage.client.operations"]
        if p.attributes["gcp.client.method"] == "storage.Bucket.patch"
    ]
    assert len(patch_ops) == 1
    assert patch_ops[0].attributes["error.type"] == "INVALID_ARGUMENT"


def test_existence_and_lookup_404_semantics(metrics_env):
    client, session, reader = metrics_env
    session.request.side_effect = [
        _json_response({"error": {"message": "not found"}}, status_code=404),
        _json_response({"error": {"message": "not found"}}, status_code=404),
        _json_response({"error": {"message": "not found"}}, status_code=404),
        _json_response({"error": {"message": "not found"}}, status_code=404),
        _json_response({"error": {"message": "not found"}}, status_code=404),
        _json_response({"error": {"message": "not found"}}, status_code=404),
    ]

    assert client.lookup_bucket("missing-b") is None
    bucket = client.bucket("missing-b")
    assert bucket.exists() is False
    assert bucket.get_blob("missing-obj") is None
    blob = bucket.blob("missing-obj")
    assert blob.exists() is False
    hmac_meta = HMACKeyMetadata(client, access_id="GOOG123")
    assert hmac_meta.exists() is False
    notif = BucketNotification(bucket, notification_id="n1")
    assert notif.exists() is False

    pts = _collect_metrics(reader)
    ops = pts["gcp.storage.client.operations"]
    assert sum(p.value for p in ops) == 6
    for op in ops:
        assert op.attributes["error.type"] == "OK"
    for dur in pts["gcp.client.request.duration"]:
        assert dur.attributes["error.type"] == "OK"

    attempts = pts["gcp.storage.client.attempts"]
    assert sum(p.value for p in attempts) == 6
    for att in attempts:
        assert att.attributes["error.type"] == "NOT_FOUND"
    for http_dur in pts["http.client.request.duration"]:
        assert http_dur.attributes["http.response.status_code"] == 404


def test_lazy_pagination_iterators_and_precedence(metrics_env):
    client, session, reader = metrics_env

    # Constructing iterators emits 0 metrics
    b_iter = client.bucket("my-bucket").list_blobs()
    c_iter = client.list_blobs("my-bucket")
    buckets_iter = client.list_buckets()
    hmac_iter = client.list_hmac_keys()
    notif_iter = client.bucket("my-bucket").list_notifications()
    assert _collect_metrics(reader) == {}

    # Iterating 2 pages on Bucket.list_blobs emits 2 ListObjects operations
    # attributed to storage.Bucket.list_blobs (outermost wins over Client.list_blobs)
    session.request.side_effect = [
        _json_response({"items": [{"name": "o1"}], "nextPageToken": "tok2"}),
        _json_response({"items": [{"name": "o2"}]}),
        _json_response({"items": [{"name": "o3"}]}),
        _json_response({"items": [{"name": "b1"}]}),
        _json_response({"items": [{"accessId": "k1"}]}),
        _json_response(
            {
                "items": [
                    {
                        "id": "n1",
                        "topic": "//pubsub.googleapis.com/projects/my-proj/topics/my-topic",
                    }
                ]
            }
        ),
    ]
    assert [b.name for b in b_iter] == ["o1", "o2"]
    assert [b.name for b in c_iter] == ["o3"]
    assert [b.name for b in buckets_iter] == ["b1"]
    assert [k.access_id for k in hmac_iter] == ["k1"]
    assert [n.notification_id for n in notif_iter] == ["n1"]

    pts = _collect_metrics(reader)
    by_method = {}
    for p in pts["gcp.storage.client.operations"]:
        key = (
            p.attributes["gcp.client.method"],
            p.attributes["gcp.storage.operation"],
        )
        by_method[key] = by_method.get(key, 0) + p.value

    assert by_method == {
        ("storage.Bucket.list_blobs", "ListObjects"): 2,
        ("storage.Client.list_blobs", "ListObjects"): 1,
        ("storage.Client.list_buckets", "ListBuckets"): 1,
        ("storage.Client.list_hmac_keys", "ListHMACKeys"): 1,
        ("storage.Bucket.list_notifications", "ListNotifications"): 1,
    }


def test_all_client_bucket_blob_acl_hmac_notification_methods(metrics_env):
    client, session, reader = metrics_env

    # Client methods
    session.request.side_effect = [
        _json_response({"name": "created-b"}),  # create_bucket
        _json_response({"name": "restored-b"}),  # restore_bucket
        _json_response(
            {"secret": "sec", "metadata": {"accessId": "GOOG1"}}
        ),  # create_hmac_key
        _json_response({"accessId": "GOOG1", "state": "ACTIVE"}),  # get_hmac_key_meta
    ]
    assert client.create_bucket("created-b").name == "created-b"
    assert client.restore_bucket("restored-b", generation=123).name == "restored-b"
    meta, secret = client.create_hmac_key("sa@test.iam.gserviceaccount.com")
    assert secret == "sec"
    assert meta.access_id == "GOOG1"
    assert client.get_hmac_key_metadata("GOOG1").state == "ACTIVE"

    # Client.download_blob_to_file (mocking _prep_and_do_download to test JSON Veneer wrapper)
    bucket = client.bucket("my-bucket")
    blob = bucket.blob("my-obj")
    with mock.patch.object(Blob, "_prep_and_do_download"):
        client.download_blob_to_file(blob, io.BytesIO())

    # Bucket methods
    iam_payload = {
        "version": 1,
        "etag": "CAE=",
        "bindings": [{"role": "roles/storage.objectViewer", "members": ["allUsers"]}],
    }
    session.request.side_effect = [
        _json_response({"name": "my-bucket"}),  # bucket.create
        _json_response({"name": "my-bucket"}),  # bucket.reload
        _json_response({"name": "my-bucket"}),  # bucket.update
        _json_response({"name": "my-bucket"}),  # bucket.patch
        _json_response(
            {
                "id": "n1",
                "topic": "//pubsub.googleapis.com/projects/my-proj/topics/my-topic",
            }
        ),  # bucket.get_notification
        _json_response(None, status_code=204),  # bucket.delete_blob
        _json_response({"resource": {"name": "copied"}}),  # bucket.copy_blob
        _json_response({"name": "moved"}),  # bucket.move_blob
        _json_response({"name": "restored"}),  # bucket.restore_blob
        _json_response(iam_payload),  # bucket.get_iam_policy
        _json_response(iam_payload),  # bucket.set_iam_policy
        _json_response({"permissions": ["storage.objects.get"]}),  # test_iam
        _json_response({"name": "my-bucket", "metageneration": "2"}),  # lock_retention
        _json_response(None, status_code=204),  # bucket.delete
    ]
    bucket.create()
    bucket.reload()
    bucket.update()
    bucket.patch()
    assert bucket.get_notification("n1").notification_id == "n1"
    bucket.delete_blob("old-obj")
    bucket.copy_blob(blob, bucket, new_name="copied")
    bucket.move_blob(blob, new_name="moved")
    bucket.restore_blob("restored", generation=1)
    pol = bucket.get_iam_policy()
    bucket.set_iam_policy(pol)
    assert bucket.test_iam_permissions(["storage.objects.get"]) == [
        "storage.objects.get"
    ]
    bucket._properties["metageneration"] = 1
    bucket._properties["retentionPolicy"] = {"retentionPeriod": 100}
    bucket.lock_retention_policy()
    bucket.delete()

    # Subclass of Bucket & Blob preserves canonical class name in gcp.client.method
    class _UserBucket(Bucket):
        pass

    class _UserBlob(Blob):
        pass

    session.request.side_effect = [
        _json_response({"name": "sub-b"}),
        _json_response({"name": "sub-o"}),
    ]
    ub = _UserBucket(client, "sub-b")
    ub.reload()
    uo = _UserBlob("sub-o", ub)
    uo.reload()

    # Multi-RPC Bucket methods: delete(force=True), delete_blobs(on_error=...),
    # rename_blob, make_public(recursive=True, future=True), make_private(recursive=True, future=True)
    session.request.side_effect = [
        _json_response({"items": [{"name": "o1"}]}),  # delete(force=True) list_blobs
        _json_response(None, status_code=204),  # delete(force=True) delete o1
        _json_response(None, status_code=204),  # delete(force=True) delete bucket
        _json_response(
            {"error": {"message": "404"}}, status_code=404
        ),  # delete_blobs 1
        _json_response(None, status_code=204),  # delete_blobs 2
        _json_response({"resource": {"name": "renamed"}}),  # rename_blob copy
        _json_response(None, status_code=204),  # rename_blob delete
        _json_response({"items": []}),  # make_public reload bucket acl
        _json_response({"acl": []}),  # make_public patch bucket acl
        _json_response({"items": []}),  # make_public reload default acl
        _json_response({"defaultObjectAcl": []}),  # make_public patch default acl
        _json_response({"items": [{"name": "o1", "acl": []}]}),  # make_public list
        _json_response({"acl": []}),  # make_public blob o1 patch
        _json_response({"acl": []}),  # make_private patch bucket acl (already loaded)
        _json_response({"defaultObjectAcl": []}),  # make_private patch default acl
        _json_response({"items": [{"name": "o1", "acl": []}]}),  # make_private list
        _json_response({"acl": []}),  # make_private blob o1 patch
    ]
    bucket.delete(force=True)
    errors = []
    bucket.delete_blobs(["missing", "present"], on_error=errors.append)
    assert len(errors) == 1
    bucket.rename_blob(blob, new_name="renamed")
    bucket.make_public(recursive=True, future=True)
    bucket.make_private(recursive=True, future=True)

    # Blob methods (JSON + mocked media helpers for Veneer coverage)
    session.request.side_effect = [
        _json_response({"name": "my-obj"}),  # blob.update
        _json_response({"name": "my-obj"}),  # blob.patch
        _json_response(iam_payload),  # blob.get_iam_policy
        _json_response(iam_payload),  # blob.set_iam_policy
        _json_response({"permissions": ["storage.objects.get"]}),  # blob.test_iam
        _json_response({"items": []}),  # blob.make_public reload acl
        _json_response({"acl": []}),  # blob.make_public save acl
        _json_response({"acl": []}),  # blob.make_private save acl (loaded)
        _json_response({"name": "my-obj"}),  # blob.compose
        _json_response(
            {
                "done": False,
                "rewriteToken": "tok1",
                "totalBytesRewritten": "10",
                "objectSize": "20",
            }
        ),  # blob.rewrite step 1
        _json_response(
            {
                "done": False,
                "rewriteToken": "tok2",
                "totalBytesRewritten": "10",
                "objectSize": "20",
            }
        ),  # blob.update_storage_class step 1
        _json_response(
            {
                "done": True,
                "totalBytesRewritten": "20",
                "objectSize": "20",
                "resource": {"name": "my-obj", "storageClass": "NEARLINE"},
            }
        ),  # blob.update_storage_class step 2
        _json_response(None, status_code=204),  # blob.delete
    ]
    blob.update()
    blob.patch()
    b_pol = iam.Policy()
    assert blob.get_iam_policy().version == 1
    blob.set_iam_policy(b_pol)
    assert blob.test_iam_permissions(["storage.objects.get"]) == ["storage.objects.get"]
    blob.make_public()
    blob.make_private()
    src1 = bucket.blob("s1")
    src2 = bucket.blob("s2")
    blob.compose([src1, src2])
    token, _, _ = blob.rewrite(src1)
    assert token == "tok1"
    blob._encryption_key = b"0" * 32
    blob.update_storage_class("NEARLINE")
    blob._encryption_key = None
    blob.delete()

    with mock.patch.object(Blob, "_prep_and_do_download", return_value=None):
        blob.download_to_file(io.BytesIO())
        with mock.patch("builtins.open", mock.mock_open()):
            blob.download_to_filename("/tmp/fake-download-unused")
    with mock.patch.object(
        Blob,
        "_prep_and_do_download",
        side_effect=lambda buf, **kw: buf.write(b"hello"),
    ):
        assert blob.download_as_bytes() == b"hello"
        with pytest.warns(PendingDeprecationWarning):
            assert blob.download_as_string() == b"hello"
        assert blob.download_as_text() == "hello"

    with mock.patch.object(Blob, "_do_upload", return_value={"name": "my-obj"}):
        blob.upload_from_file(io.BytesIO(b"abc"))
        blob.upload_from_string("abc")
        with mock.patch("builtins.open", mock.mock_open(read_data=b"abc")):
            with mock.patch("os.path.getsize", return_value=3):
                blob.upload_from_filename("/tmp/fake-upload-unused")

    with mock.patch.object(
        Blob,
        "_initiate_resumable_upload",
        return_value=(mock.Mock(resumable_url="https://u"), None),
    ):
        assert blob.create_resumable_upload_session() == "https://u"

    # ACL, DefaultObjectACL, ObjectACL
    for acl_obj in (BucketACL(bucket), DefaultObjectACL(bucket), ObjectACL(blob)):
        # save() when loaded=False is a local no-op -> 0 metrics
        acl_obj.loaded = False
        acl_obj.save()
        session.request.side_effect = [
            _json_response({"items": [{"entity": "allUsers", "role": "READER"}]}),
            _json_response({}),
            _json_response({}),
            _json_response({}),
        ]
        acl_obj.reload()
        acl_obj.save()
        acl_obj.save_predefined("publicRead")
        acl_obj.clear()
        assert isinstance(acl_obj, ACL)

    # HMACKeyMetadata
    hmac_meta = HMACKeyMetadata(client, access_id="GOOG999")
    hmac_meta.state = "INACTIVE"
    session.request.side_effect = [
        _json_response({"accessId": "GOOG999", "state": "ACTIVE"}),
        _json_response({"accessId": "GOOG999", "state": "ACTIVE"}),
        _json_response({"accessId": "GOOG999", "state": "INACTIVE"}),
        _json_response(None, status_code=204),
    ]
    assert hmac_meta.exists() is True
    hmac_meta.reload()
    hmac_meta.state = "INACTIVE"
    hmac_meta.update()
    hmac_meta.delete()

    # BucketNotification (including client validation error when notification_id is None)
    notif_missing_id = BucketNotification(bucket)
    for fn in (
        notif_missing_id.exists,
        notif_missing_id.reload,
        notif_missing_id.delete,
    ):
        with pytest.raises(ValueError):
            fn()

    notif = BucketNotification(bucket, topic_name="my-topic", topic_project="my-proj")
    session.request.side_effect = [
        _json_response(
            {
                "id": "notif-1",
                "topic": "//pubsub.googleapis.com/projects/my-proj/topics/my-topic",
            }
        ),
        _json_response({"id": "notif-1"}),
        _json_response(
            {
                "id": "notif-1",
                "topic": "//pubsub.googleapis.com/projects/my-proj/topics/my-topic",
            }
        ),
        _json_response(None, status_code=204),
    ]
    notif.create()
    assert notif.exists() is True
    notif.reload()
    notif.delete()

    pts = _collect_metrics(reader)
    methods_seen = {
        p.attributes["gcp.client.method"] for p in pts["gcp.storage.client.operations"]
    }
    expected_subset = {
        "storage.Client.create_bucket",
        "storage.Client.restore_bucket",
        "storage.Client.create_hmac_key",
        "storage.Client.get_hmac_key_metadata",
        "storage.Client.download_blob_to_file",
        "storage.Bucket.create",
        "storage.Bucket.reload",
        "storage.Bucket.update",
        "storage.Bucket.patch",
        "storage.Bucket.get_notification",
        "storage.Bucket.delete_blob",
        "storage.Bucket.delete_blobs",
        "storage.Bucket.copy_blob",
        "storage.Bucket.rename_blob",
        "storage.Bucket.move_blob",
        "storage.Bucket.restore_blob",
        "storage.Bucket.get_iam_policy",
        "storage.Bucket.set_iam_policy",
        "storage.Bucket.test_iam_permissions",
        "storage.Bucket.make_public",
        "storage.Bucket.make_private",
        "storage.Bucket.lock_retention_policy",
        "storage.Bucket.delete",
        "storage.Blob.reload",
        "storage.Blob.update",
        "storage.Blob.patch",
        "storage.Blob.delete",
        "storage.Blob.get_iam_policy",
        "storage.Blob.set_iam_policy",
        "storage.Blob.test_iam_permissions",
        "storage.Blob.make_public",
        "storage.Blob.make_private",
        "storage.Blob.compose",
        "storage.Blob.rewrite",
        "storage.Blob.update_storage_class",
        "storage.Blob.download_to_file",
        "storage.Blob.download_to_filename",
        "storage.Blob.download_as_bytes",
        "storage.Blob.download_as_string",
        "storage.Blob.download_as_text",
        "storage.Blob.upload_from_file",
        "storage.Blob.upload_from_filename",
        "storage.Blob.upload_from_string",
        "storage.Blob.create_resumable_upload_session",
        "storage.BucketACL.reload",
        "storage.BucketACL.save",
        "storage.BucketACL.save_predefined",
        "storage.BucketACL.clear",
        "storage.DefaultObjectACL.reload",
        "storage.DefaultObjectACL.save",
        "storage.DefaultObjectACL.save_predefined",
        "storage.DefaultObjectACL.clear",
        "storage.ObjectACL.reload",
        "storage.ObjectACL.save",
        "storage.ObjectACL.save_predefined",
        "storage.ObjectACL.clear",
        "storage.HMACKeyMetadata.exists",
        "storage.HMACKeyMetadata.reload",
        "storage.HMACKeyMetadata.update",
        "storage.HMACKeyMetadata.delete",
        "storage.BucketNotification.create",
        "storage.BucketNotification.exists",
        "storage.BucketNotification.reload",
        "storage.BucketNotification.delete",
    }
    assert expected_subset.issubset(methods_seen)
    assert not any("_UserBucket" in m or "_UserBlob" in m for m in methods_seen)
    # delete_blobs 404 swallowed by on_error must NOT cause a false retry on the next blob
    assert "gcp.storage.client.retries" not in pts


def test_batch_deferral_and_subresponse_semantics(metrics_env):
    client, session, reader = metrics_env
    bucket = client.bucket("my-bucket")

    # Empty batch finish -> CLIENT_VALIDATION_ERROR
    empty_batch = client.batch()
    with pytest.raises(ValueError):
        empty_batch.finish()
    pts_empty = _collect_metrics(reader)
    assert (
        pts_empty["gcp.storage.client.operations"][0].attributes["error.type"]
        == "CLIENT_VALIDATION_ERROR"
    )

    multipart_ok_and_500 = (
        b"--batch_boundary\r\n"
        b"Content-Type: application/http\r\n"
        b"Content-ID: <response-1>\r\n\r\n"
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json\r\n\r\n"
        b'{"name": "o1"}\r\n'
        b"--batch_boundary\r\n"
        b"Content-Type: application/http\r\n"
        b"Content-ID: <response-2>\r\n\r\n"
        b"HTTP/1.1 403 Forbidden\r\n"
        b"Content-Type: application/json\r\n\r\n"
        b'{"error": {"message": "denied"}}\r\n'
        b"--batch_boundary--\r\n"
    )

    # 1. raise_exception=False: queuing emits 0 metrics; finish emits Batch OK
    session.request.return_value = _json_response(
        multipart_ok_and_500,
        status_code=200,
        headers={"Content-Type": "multipart/mixed; boundary=batch_boundary"},
    )
    with client.batch(raise_exception=False):
        bucket.blob("o1").patch()
        bucket.blob("o2").delete()
        # No new operations recorded while queuing inside with client.batch()
        pts_during = _collect_metrics(reader)
        assert len(pts_during["gcp.storage.client.operations"]) == 1

    pts_after_no_raise = _collect_metrics(reader)
    assert len(pts_after_no_raise["gcp.storage.client.operations"]) == 2

    # 2. raise_exception=True: subresponse 403 fails Batch with PERMISSION_DENIED
    session.request.return_value = _json_response(
        multipart_ok_and_500,
        status_code=200,
        headers={"Content-Type": "multipart/mixed; boundary=batch_boundary"},
    )
    with pytest.raises(Exception):
        with client.batch(raise_exception=True):
            bucket.blob("o1").patch()
            bucket.blob("o2").delete()

    pts_final = _collect_metrics(reader)
    batch_ops = pts_final["gcp.storage.client.operations"]
    err_map = [p.attributes.get("error.type", "OK") for p in batch_ops]
    assert "CLIENT_VALIDATION_ERROR" in err_map
    assert "OK" in err_map
    assert "PERMISSION_DENIED" in err_map

    http_att = pts_final["http.client.request.duration"][0]
    assert http_att.attributes["url.template"] == "/batch/storage/v1"
    assert http_att.attributes["http.request.method"] == "POST"


def test_bucket_metadata_cache_background_suppression(metrics_env):
    client, session, reader = metrics_env
    cache = BucketMetadataCache(client)

    session.request.side_effect = [
        _json_response({"id": "b1", "name": "b1", "location": "US"}),
        _json_response({"error": {"message": "404"}}, status_code=404),
    ]
    cache._fetch_background("b1")
    cache._verify_existence_background("b1")

    assert _collect_metrics(reader) == {}


def test_trace_exemplar_correlation_on_http_json_metrics(metrics_env):
    client, session, reader = metrics_env
    session.request.return_value = _json_response({"name": "my-bucket"})

    tracer_provider = TracerProvider()
    tracer = tracer_provider.get_tracer("test-tracer")
    with tracer.start_as_current_span("parent-span") as span:
        expected_trace_id = span.get_span_context().trace_id
        expected_span_id = span.get_span_context().span_id
        client.get_bucket("my-bucket")

    pts = _collect_metrics(reader)
    op_exemplars = pts["gcp.client.request.duration"][0].exemplars
    http_exemplars = pts["http.client.request.duration"][0].exemplars
    assert len(op_exemplars) >= 1
    assert len(http_exemplars) >= 1
    assert op_exemplars[0].trace_id == expected_trace_id
    assert op_exemplars[0].span_id != 0
    assert http_exemplars[0].trace_id == expected_trace_id
    assert http_exemplars[0].span_id != 0
    # When SDK tracing spans are disabled, exemplar span_id matches the caller's span
    assert expected_span_id != 0


def test_lazy_acl_methods_batch_non_batchable_ops_and_update_storage_class_client(
    metrics_env,
):
    client, session, reader = metrics_env
    bucket = client.bucket("my-bucket")

    # 1. Lazy ACL methods attribute reload to the user-invoked method when unloaded,
    #    and emit 0 metrics once loaded=True.
    acl_Payload = {"items": [{"entity": "user-a@example.com", "role": "READER"}]}
    lazy_cases = [
        ("__iter__", lambda acl: list(acl)),
        (
            "entity_from_dict",
            lambda acl: acl.entity_from_dict(
                {"entity": "user-b@example.com", "role": "READER"}
            ),
        ),
        ("has_entity", lambda acl: acl.has_entity("user-a@example.com")),
        ("get_entity", lambda acl: acl.get_entity("user-a@example.com")),
        (
            "add_entity",
            lambda acl: acl.add_entity(acl.user("c@example.com")),
        ),
        ("entity", lambda acl: acl.entity("user", "a@example.com")),
        ("user", lambda acl: acl.user("a@example.com")),
        ("group", lambda acl: acl.group("g@example.com")),
        ("domain", lambda acl: acl.domain("example.com")),
        ("all", lambda acl: acl.all()),
        ("all_authenticated", lambda acl: acl.all_authenticated()),
        ("get_entities", lambda acl: acl.get_entities()),
    ]
    for method_name, fn in lazy_cases:
        session.request.return_value = _json_response(acl_Payload)
        acl = BucketACL(bucket)
        # Note: for add_entity, construct _ACLEntity directly so add_entity itself is outermost
        if method_name == "add_entity":
            from google.cloud.storage.acl import _ACLEntity

            ent = _ACLEntity("user", "c@example.com")
            acl.add_entity(ent)
            acl.add_entity(ent)  # loaded=True fast path
        else:
            fn(acl)
            fn(acl)  # loaded=True fast path -> 0 additional metrics

    pts_acl = _collect_metrics(reader)
    acl_ops = pts_acl["gcp.storage.client.operations"]
    assert len(acl_ops) == len(lazy_cases)
    assert {p.attributes["gcp.client.method"] for p in acl_ops} == {
        f"storage.BucketACL.{name}" for name, _ in lazy_cases
    }
    assert all(
        p.attributes["gcp.storage.operation"] == "ListBucketACLs" for p in acl_ops
    )

    # 2. Non-batchable operations inside with client.batch() still record logical operations
    session.request.return_value = _json_response(
        b"--b\r\nContent-Type: application/http\r\nContent-ID: <response-1>\r\n\r\n"
        b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"name": "o1"}\r\n--b--\r\n',
        status_code=200,
        headers={"Content-Type": "multipart/mixed; boundary=b"},
    )
    blob = bucket.blob("media-in-batch")
    with (
        mock.patch.object(blob, "_do_download"),
        mock.patch.object(blob, "_do_upload", return_value={"name": "media-in-batch"}),
        mock.patch(
            "google.cloud.storage.blob.ResumableUpload.initiate",
            return_value=_json_response(
                {}, headers={"location": "https://upload.example/1"}
            ),
        ),
    ):
        with client.batch():
            bucket.blob("o1").patch()  # Batchable JSON -> deferred to Batch.finish
            blob.download_as_bytes()
            blob.upload_from_string(b"abc")
            blob.create_resumable_upload_session()

    pts_batch = _collect_metrics(reader)
    batch_methods = {
        p.attributes["gcp.client.method"]
        for p in pts_batch["gcp.storage.client.operations"]
    }
    assert {
        "storage.Batch.finish",
        "storage.Blob.download_as_bytes",
        "storage.Blob.upload_from_string",
        "storage.Blob.create_resumable_upload_session",
    }.issubset(batch_methods)
    assert "storage.Blob.patch" not in batch_methods

    # 3. Blob.update_storage_class(..., client=other_client) routes both logical and HTTP metrics to other_client
    uninstrumented_session = mock.MagicMock()
    uninstrumented_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=uninstrumented_session,
        enable_metrics=False,
    )
    uninstrumented_client._bucket_metadata_cache = None
    other_reader = InMemoryMetricReader()
    other_provider = MeterProvider(metric_readers=[other_reader])
    other_session = mock.MagicMock()
    other_session.request.side_effect = [
        _json_response(
            {
                "done": False,
                "rewriteToken": "tok-1",
                "totalBytesRewritten": "5",
                "objectSize": "10",
            }
        ),
        _json_response(
            {
                "done": True,
                "totalBytesRewritten": "10",
                "objectSize": "10",
                "resource": {"name": "obj", "storageClass": "NEARLINE"},
            }
        ),
    ]
    other_client = Client(
        project="test-project",
        credentials=_make_credentials(),
        _http=other_session,
        enable_metrics=True,
        meter_provider=other_provider,
    )
    other_client._bucket_metadata_cache = None
    ublob = uninstrumented_client.bucket("my-bucket").blob("obj")
    ublob.update_storage_class("NEARLINE", client=other_client)

    assert uninstrumented_session.request.call_count == 0
    assert other_session.request.call_count == 2
    other_pts = _collect_metrics(other_reader)
    assert len(other_pts["gcp.storage.client.operations"]) == 1
    assert (
        other_pts["gcp.storage.client.operations"][0].attributes["gcp.client.method"]
        == "storage.Blob.update_storage_class"
    )
    assert sum(p.value for p in other_pts["gcp.storage.client.attempts"]) == 2
    uninstrumented_client.close()
    other_client.close()
