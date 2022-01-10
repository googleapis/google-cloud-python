workspace(name = "gapic_generator_python")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

_bazel_skylib_version = "0.9.0"

_bazel_skylib_sha256 = "1dde365491125a3db70731e25658dfdd3bc5dbdfd11b840b3e987ecf043c7ca0"

http_archive(
    name = "bazel_skylib",
    sha256 = _bazel_skylib_sha256,
    url = "https://github.com/bazelbuild/bazel-skylib/releases/download/{0}/bazel_skylib-{0}.tar.gz".format(_bazel_skylib_version),
)

_rules_python_version = "0.5.0"

_rules_python_sha256 = "a2fd4c2a8bcf897b718e5643040b03d9528ac6179f6990774b7c19b2dc6cd96b"

http_archive(
    name = "rules_python",
    sha256 = _rules_python_sha256,
    strip_prefix = "rules_python-{}".format(_rules_python_version),
    url = "https://github.com/bazelbuild/rules_python/archive/{}.tar.gz".format(_rules_python_version),
)

#
# Import gapic-generator-python specific dependencies
#
load(
    "//:repositories.bzl",
    "gapic_generator_python",
    "gapic_generator_register_toolchains",
)

gapic_generator_python()

gapic_generator_register_toolchains()

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

#
# Import grpc as a native bazel dependency. This avoids duplication and also
# speeds up loading phase a lot (otherwise python_rules will be building grpcio
# from sources in a single-core speed, which takes around 5 minutes on a regular
# workstation)
#
load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", "grpc_deps")

grpc_deps()

load("@com_github_grpc_grpc//bazel:grpc_extra_deps.bzl", "grpc_extra_deps")

grpc_extra_deps()

load("@build_bazel_rules_apple//apple:repositories.bzl", "apple_rules_dependencies")

apple_rules_dependencies()

load("@build_bazel_apple_support//lib:repositories.bzl", "apple_support_dependencies")

apple_support_dependencies()

load("@com_google_googleapis//:repository_rules.bzl", "switched_rules_by_language")

switched_rules_by_language(
    name = "com_google_googleapis_imports",
    gapic = True,
    grpc = True,
)
