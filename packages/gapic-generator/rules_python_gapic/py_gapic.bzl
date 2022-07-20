# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

load("@rules_gapic//:gapic.bzl", "proto_custom_library", "unzipped_srcjar")
load("@rules_python//python:defs.bzl", "py_library")
load("@gapic_generator_python_pip_deps//:requirements.bzl", "requirement")

def _gapic_test_file_impl(ctx):
    generated_test_file = ctx.actions.declare_file(ctx.label.name)

    ctx.actions.expand_template(
        template = ctx.attr.template.files.to_list()[0],
        output = generated_test_file,
        substitutions = {},
    )

    return [DefaultInfo(files = depset(direct = [generated_test_file]))]

gapic_test_file = rule(
    _gapic_test_file_impl,
    attrs = {
        "template": attr.label(allow_files = True),
    },
)

def py_gapic_library(
        name,
        srcs,
        grpc_service_config = None,
        plugin_args = None,
        opt_args = None,
        metadata = True,
        service_yaml = None,
        deps = [],
        **kwargs):
    srcjar_target_name = "%s_srcjar" % name
    srcjar_output_suffix = ".srcjar"

    plugin_args = plugin_args or []
    opt_args = opt_args or []

    if metadata:
        plugin_args.append("metadata")

    file_args = {}
    if grpc_service_config:
        file_args[grpc_service_config] = "retry-config"
    if service_yaml:
        file_args[service_yaml] = "service-yaml"

    proto_custom_library(
        name = srcjar_target_name,
        deps = srcs,
        plugin = Label("@gapic_generator_python//:gapic_plugin"),
        plugin_args = plugin_args,
        plugin_file_args = file_args,
        opt_args = opt_args,
        output_type = "python_gapic",
        output_suffix = srcjar_output_suffix,
        **kwargs
    )

    main_file = "%s" % srcjar_target_name + srcjar_output_suffix
    main_dir = "%s.py" % srcjar_target_name

    unzipped_srcjar(
        name = main_dir,
        srcjar = ":%s" % main_file,
    )

    actual_deps = deps + [
        "@com_github_grpc_grpc//src/python/grpcio/grpc:grpcio",
        requirement("protobuf"),
        requirement("proto-plus"),
        requirement("google-api-core"),
        requirement("googleapis-common-protos"),
        requirement("pytest-asyncio"),
    ]

    py_library(
        name = name,
        srcs = [":%s" % main_dir],
        deps = actual_deps,
    )

    test_file_target_name = "%s_test.py" % name

    gapic_test_file(
        name = test_file_target_name,
        template = Label("//rules_python_gapic:test.py"),
    )

    test_runner_file_target_name = "%s_pytest.py" % name

    gapic_test_file(
        name = test_runner_file_target_name,
        template = Label("//rules_python_gapic:pytest.py"),
    )
