# Copyright 2025 Google LLC
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

import datetime
from unittest import mock

import bigframes.bigquery.obj as obj
import bigframes.operations as ops
import bigframes.series


def create_mock_series():
    result = mock.create_autospec(bigframes.series.Series, instance=True)
    result.copy.return_value = result
    return result


def test_fetch_metadata_op_structure():
    op = ops.obj_fetch_metadata_op
    assert op.name == "obj_fetch_metadata"


def test_get_access_url_op_structure():
    op = ops.ObjGetAccessUrl(mode="r")
    assert op.name == "obj_get_access_url"
    assert op.mode == "r"
    assert op.duration is None


def test_get_access_url_with_duration_op_structure():
    op = ops.ObjGetAccessUrl(mode="rw", duration=3600000000)
    assert op.name == "obj_get_access_url"
    assert op.mode == "rw"
    assert op.duration == 3600000000


def test_make_ref_op_structure():
    op = ops.obj_make_ref_op
    assert op.name == "obj_make_ref"


def test_make_ref_json_op_structure():
    op = ops.obj_make_ref_json_op
    assert op.name == "obj_make_ref_json"


def test_fetch_metadata_calls_apply_unary_op():
    series = create_mock_series()

    obj.fetch_metadata(series)

    series._apply_unary_op.assert_called_once()
    args, _ = series._apply_unary_op.call_args
    assert args[0] == ops.obj_fetch_metadata_op


def test_get_access_url_calls_apply_unary_op_without_duration():
    series = create_mock_series()

    obj.get_access_url(series, mode="r")

    series._apply_unary_op.assert_called_once()
    args, _ = series._apply_unary_op.call_args
    assert isinstance(args[0], ops.ObjGetAccessUrl)
    assert args[0].mode == "r"
    assert args[0].duration is None


def test_get_access_url_calls_apply_unary_op_with_duration():
    series = create_mock_series()
    duration = datetime.timedelta(hours=1)

    obj.get_access_url(series, mode="rw", duration=duration)

    series._apply_unary_op.assert_called_once()
    args, _ = series._apply_unary_op.call_args
    assert isinstance(args[0], ops.ObjGetAccessUrl)
    assert args[0].mode == "rw"
    # 1 hour = 3600 seconds = 3600 * 1000 * 1000 microseconds
    assert args[0].duration == 3600000000


def test_make_ref_calls_apply_binary_op_with_authorizer():
    uri = create_mock_series()
    auth = create_mock_series()

    obj.make_ref(uri, authorizer=auth)

    uri._apply_binary_op.assert_called_once()
    args, _ = uri._apply_binary_op.call_args
    assert args[0] == auth
    assert args[1] == ops.obj_make_ref_op


def test_make_ref_calls_apply_binary_op_with_authorizer_string():
    uri = create_mock_series()
    auth = "us.bigframes-test-connection"

    obj.make_ref(uri, authorizer=auth)

    uri._apply_binary_op.assert_called_once()
    args, _ = uri._apply_binary_op.call_args
    assert args[0] == auth
    assert args[1] == ops.obj_make_ref_op


def test_make_ref_calls_apply_unary_op_without_authorizer():
    json_val = create_mock_series()

    obj.make_ref(json_val)

    json_val._apply_unary_op.assert_called_once()
    args, _ = json_val._apply_unary_op.call_args
    assert args[0] == ops.obj_make_ref_json_op
