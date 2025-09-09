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
        "language_proto": {
            "name": "language_proto",
            "srcs": ["language_service.proto"],
            "deps": [
                "//google/api:annotations_proto",
                "//google/api:client_proto",
                "//google/api:field_behavior_proto",
            ],
        },
        "language_proto_with_info": {
            "name": "language_proto_with_info",
            "deps": [":language_proto", "//google/cloud:common_resources_proto"],
        },
        "language_java_proto": {
            "name": "language_java_proto",
            "deps": [":language_proto"],
        },
        "language_java_grpc": {
            "name": "language_java_grpc",
            "srcs": [":language_proto"],
            "deps": [":language_java_proto"],
        },
        "language_java_gapic": {
            "name": "language_java_gapic",
            "srcs": [":language_proto_with_info"],
            "gapic_yaml": None,
            "grpc_service_config": "language_grpc_service_config.json",
            "rest_numeric_enums": True,
            "service_yaml": "language_v1.yaml",
            "test_deps": [":language_java_grpc"],
            "transport": "grpc+rest",
            "deps": [":language_java_proto", "//google/api:api_java_proto"],
        },
        "language_java_gapic_test_suite": {
            "name": "language_java_gapic_test_suite",
            "test_classes": [
                "com.google.cloud.language.v1.LanguageServiceClientHttpJsonTest",
                "com.google.cloud.language.v1.LanguageServiceClientTest",
            ],
            "runtime_deps": [":language_java_gapic_test"],
        },
        "google-cloud-language-v1-java": {
            "name": "google-cloud-language-v1-java",
            "include_samples": True,
            "transport": "grpc+rest",
            "deps": [
                ":language_java_gapic",
                ":language_java_grpc",
                ":language_java_proto",
                ":language_proto",
            ],
        },
        "language_go_proto": {
            "name": "language_go_proto",
            "compilers": ["@io_bazel_rules_go//proto:go_grpc"],
            "importpath": "cloud.google.com/go/language/apiv1/languagepb",
            "protos": [":language_proto"],
            "deps": ["//google/api:annotations_go_proto"],
        },
        "language_go_gapic": {
            "name": "language_go_gapic",
            "srcs": [":language_proto_with_info"],
            "grpc_service_config": "language_grpc_service_config.json",
            "importpath": "cloud.google.com/go/language/apiv1;language",
            "metadata": True,
            "release_level": "ga",
            "rest_numeric_enums": True,
            "service_yaml": "language_v1.yaml",
            "transport": "grpc+rest",
            "deps": [":language_go_proto"],
        },
        "gapi-cloud-language-v1-go": {
            "name": "gapi-cloud-language-v1-go",
            "deps": [
                ":language_go_gapic",
                ":language_go_gapic_srcjar-metadata.srcjar",
                ":language_go_gapic_srcjar-snippets.srcjar",
                ":language_go_gapic_srcjar-test.srcjar",
                ":language_go_proto",
            ],
        },
        "language_py_gapic": {
            "name": "language_py_gapic",
            "srcs": [":language_proto"],
            "grpc_service_config": "language_grpc_service_config.json",
            "rest_numeric_enums": True,
            "service_yaml": "language_v1.yaml",
            "transport": "grpc+rest",
            "deps": [],
        },
        "language_py_gapic_test": {
            "name": "language_py_gapic_test",
            "srcs": ["language_py_gapic_pytest.py", "language_py_gapic_test.py"],
            "legacy_create_init": False,
            "deps": [":language_py_gapic"],
        },
        "language-v1-py": {"name": "language-v1-py", "deps": [":language_py_gapic"]},
        "language_php_proto": {
            "name": "language_php_proto",
            "deps": [":language_proto"],
        },
        "language_php_gapic": {
            "name": "language_php_gapic",
            "srcs": [":language_proto_with_info"],
            "grpc_service_config": "language_grpc_service_config.json",
            "migration_mode": "NEW_SURFACE_ONLY",
            "rest_numeric_enums": True,
            "service_yaml": "language_v1.yaml",
            "transport": "grpc+rest",
            "deps": [":language_php_proto"],
        },
        "google-cloud-language-v1-php": {
            "name": "google-cloud-language-v1-php",
            "deps": [":language_php_gapic", ":language_php_proto"],
        },
        "language_nodejs_gapic": {
            "name": "language_nodejs_gapic",
            "package_name": "@google-cloud/language",
            "src": ":language_proto_with_info",
            "extra_protoc_parameters": ["metadata"],
            "grpc_service_config": "language_grpc_service_config.json",
            "package": "google.cloud.language.v1",
            "rest_numeric_enums": True,
            "service_yaml": "language_v1.yaml",
            "transport": "grpc+rest",
            "deps": [],
        },
        "language-v1-nodejs": {
            "name": "language-v1-nodejs",
            "deps": [":language_nodejs_gapic", ":language_proto"],
        },
        "language_ruby_proto": {
            "name": "language_ruby_proto",
            "deps": [":language_proto"],
        },
        "language_ruby_grpc": {
            "name": "language_ruby_grpc",
            "srcs": [":language_proto"],
            "deps": [":language_ruby_proto"],
        },
        "language_ruby_gapic": {
            "name": "language_ruby_gapic",
            "srcs": [":language_proto_with_info"],
            "extra_protoc_parameters": [
                "ruby-cloud-api-id=language.googleapis.com",
                "ruby-cloud-api-shortname=language",
                "ruby-cloud-env-prefix=LANGUAGE",
                "ruby-cloud-gem-name=google-cloud-language-v1",
                "ruby-cloud-product-url=https://cloud.google.com/natural-language",
            ],
            "grpc_service_config": "language_grpc_service_config.json",
            "rest_numeric_enums": True,
            "ruby_cloud_description": "Provides natural language understanding technologies, such as sentiment analysis, entity recognition, entity sentiment analysis, and other text annotations.",
            "ruby_cloud_title": "Natural Language V1",
            "service_yaml": "language_v1.yaml",
            "transport": "grpc+rest",
            "deps": [":language_ruby_grpc", ":language_ruby_proto"],
        },
        "google-cloud-language-v1-ruby": {
            "name": "google-cloud-language-v1-ruby",
            "deps": [
                ":language_ruby_gapic",
                ":language_ruby_grpc",
                ":language_ruby_proto",
            ],
        },
        "language_csharp_proto": {
            "name": "language_csharp_proto",
            "deps": [":language_proto"],
        },
        "language_csharp_grpc": {
            "name": "language_csharp_grpc",
            "srcs": [":language_proto"],
            "deps": [":language_csharp_proto"],
        },
        "language_csharp_gapic": {
            "name": "language_csharp_gapic",
            "srcs": [":language_proto_with_info"],
            "common_resources_config": "@gax_dotnet//:Google.Api.Gax/ResourceNames/CommonResourcesConfig.json",
            "grpc_service_config": "language_grpc_service_config.json",
            "rest_numeric_enums": True,
            "service_yaml": "language_v1.yaml",
            "transport": "grpc+rest",
            "deps": [":language_csharp_grpc", ":language_csharp_proto"],
        },
        "google-cloud-language-v1-csharp": {
            "name": "google-cloud-language-v1-csharp",
            "deps": [
                ":language_csharp_gapic",
                ":language_csharp_grpc",
                ":language_csharp_proto",
            ],
        },
        "language_cc_proto": {"name": "language_cc_proto", "deps": [":language_proto"]},
        "language_cc_grpc": {
            "name": "language_cc_grpc",
            "srcs": [":language_proto"],
            "grpc_only": True,
            "deps": [":language_cc_proto"],
        },
    }
    result = None
    with open(BUILD_BAZEL_PATH, "r") as f:
        content = f.read()
        result = parse_googleapis_content.parse_content(content)

    assert result == expected_result
