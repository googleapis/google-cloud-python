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

import starlark as sl


_PY_CALLABLES = (
    "py_gapic_assembly_pkg",
    "py_gapic_library",
    "py_test",
    "py_proto_library",
    "py_grpc_library",
    "py_import",
)

_JAVA_CALLABLES = (
    "java_gapic_assembly_gradle_pkg",
    "java_gapic_library",
    "java_gapic_test",
    "java_grpc_library",
    "java_proto_library",
)

_GO_CALLABLES = (
    "go_gapic_assembly_pkg",
    "go_gapic_library",
    "go_proto_library",
    "go_grpc_library",
)

_PHP_CALLABLES = (
    "php_gapic_assembly_pkg",
    "php_gapic_library",
    "php_grpc_library",
    "php_proto_library",
)

_NODEJS_CALLABLES = ("nodejs_gapic_assembly_pkg", "nodejs_gapic_library")

_RUBY_CALLABLES = (
    "ruby_ads_gapic_library",
    "ruby_cloud_gapic_library",
    "ruby_gapic_assembly_pkg",
    "ruby_grpc_library",
    "ruby_proto_library",
)

_CSHARP_CALLABLES = (
    "csharp_gapic_assembly_pkg",
    "csharp_gapic_library",
    "csharp_grpc_library",
    "csharp_proto_library",
)

_CC_CALLABLES = ("cc_grpc_library", "cc_gapic_library", "cc_proto_library")

_MISC_CALLABLES = (
    "moved_proto_library",
    "proto_library",
    "proto_library_with_info",
    "upb_c_proto_library",
)

_CALLABLE_MAP = {
    "@rules_proto//proto:defs.bzl": ("proto_library",),
    "@com_google_googleapis_imports//:imports.bzl": (
        _PY_CALLABLES
        + _JAVA_CALLABLES
        + _GO_CALLABLES
        + _PHP_CALLABLES
        + _NODEJS_CALLABLES
        + _RUBY_CALLABLES
        + _CSHARP_CALLABLES
        + _CC_CALLABLES
        + _MISC_CALLABLES
    ),
}

_NOOP_CALLABLES = (
    "package",
    "alias",
    "sh_binary",
    "java_proto_library",
    "genrule",
    "gapic_yaml_from_disco",
    "grpc_service_config_from_disco",
    "proto_from_disco",
)

_GLOB_CALLABLES = (
    "exports_files",
    "glob",
)


def parse_content(content: str) -> dict:
    """Parses content from BUILD.bazel and returns a dictionary
    containing bazel rules and arguments.

    Args:
        content(str): contents of a BUILD.bazel.

    Returns: Dictionary containing bazel rules and arguments.

    """
    glb = sl.Globals.standard()
    mod = sl.Module()
    packages = {}

    def bazel_target(**args):
        if args["name"] is not None:
            packages[args["name"]] = args

    def noop_bazel_rule(**args):
        pass

    def fake_glob(paths=[], **args):
        return []

    mod.add_callable("package", noop_bazel_rule)
    mod.add_callable("proto_library", noop_bazel_rule)
    mod.add_callable("py_test", noop_bazel_rule)

    for glob_callable in _GLOB_CALLABLES:
        mod.add_callable(glob_callable, fake_glob)

    def load(name):
        mod = sl.Module()

        for noop_callable in _NOOP_CALLABLES:
            mod.add_callable(noop_callable, noop_bazel_rule)

        for callable_name in _CALLABLE_MAP.get(name, []):
            mod.add_callable(callable_name, bazel_target)
        return mod.freeze()

    ast = sl.parse("BUILD.bazel", content)

    sl.eval(mod, ast, glb, sl.FileLoader(load))

    return packages
