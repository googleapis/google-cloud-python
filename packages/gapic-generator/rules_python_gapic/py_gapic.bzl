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

load("@com_google_api_codegen//rules_gapic:gapic.bzl", "proto_custom_library")

def py_gapic_library(name, srcs, **kwargs):
    #    srcjar_target_name = "%s_srcjar" % name
    srcjar_target_name = name
    srcjar_output_suffix = ".srcjar"

    proto_custom_library(
        name = srcjar_target_name,
        deps = srcs,
        plugin = Label("@gapic_generator_python//:gapic_plugin"),
        plugin_args = [],
        plugin_file_args = {},
        output_type = "python_gapic",
        output_suffix = srcjar_output_suffix,
        **kwargs
    )
