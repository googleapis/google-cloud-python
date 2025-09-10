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


import parse_googleapis_content
from pathlib import Path

GENERATOR_DIR = Path(__file__).resolve().parent
BUILD_BAZEL_PATH = f"{GENERATOR_DIR}/test-resources/librarian/BUILD.bazel"


def test_parse_build_bazel():
    expected_result = {
        "language_proto": {"name": "language_proto"},
        "language_py_gapic": {
            "deps": [],
            "grpc_service_config": "language_grpc_service_config.json",
            "name": "language_py_gapic",
            "rest_numeric_enums": True,
            "service_yaml": "language_v1.yaml",
            "srcs": [":language_proto"],
            "transport": "grpc+rest",
        },
    }
    with open(BUILD_BAZEL_PATH, "r") as f:
        content = f.read()
        result = parse_googleapis_content.parse_content(content)

    assert result == expected_result
