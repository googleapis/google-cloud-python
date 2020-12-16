workspace(name = "gapic_generator_python")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "bazel_skylib",
    urls = ["https://github.com/bazelbuild/bazel-skylib/releases/download/0.9.0/bazel_skylib-0.9.0.tar.gz"],
)

http_archive(
    name = "rules_python",
    strip_prefix = "rules_python-0.1.0,
    url = "https://github.com/bazelbuild/rules_python/archive/0.1.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

load("@rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

#
# Import gapic-generator-python specific dependencies
#
load("//:repositories.bzl",
    "gapic_generator_python",
    "gapic_generator_register_toolchains"
)

gapic_generator_python()

gapic_generator_register_toolchains()

load("@gapic_generator_python_pip_deps//:requirements.bzl", "pip_install")

pip_install()

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

load("@upb//bazel:repository_defs.bzl", "bazel_version_repository")

bazel_version_repository(
    name = "bazel_version",
)

load("@build_bazel_rules_apple//apple:repositories.bzl", "apple_rules_dependencies")

apple_rules_dependencies()

load("@build_bazel_apple_support//lib:repositories.bzl", "apple_support_dependencies")

apple_support_dependencies()
