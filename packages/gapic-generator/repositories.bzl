load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@rules_python//python:pip.bzl", "pip_install")

_PANDOC_BUILD_FILE = """
filegroup(
    name = "pandoc",
    srcs = ["bin/pandoc"],
    visibility = ["//visibility:public"],
)"""

def gapic_generator_python():
    _maybe(
        pip_install,
        name = "gapic_generator_python_pip_deps",
        requirements = "@gapic_generator_python//:requirements.txt",
    )

    _protobuf_version = "3.19.2"
    _protobuf_sha256 = "9ceef0daf7e8be16cd99ac759271eb08021b53b1c7b6edd399953a76390234cd"
    _protobuf_version_in_link = "v{}".format(_protobuf_version)
    _maybe(
        http_archive,
        name = "com_google_protobuf",
        sha256 = _protobuf_sha256,
        url = "https://github.com/protocolbuffers/protobuf/archive/refs/tags/{}.zip".format(_protobuf_version_in_link),
        strip_prefix = "protobuf-{}".format(_protobuf_version),
    )

    _maybe(
        http_archive,
        name = "bazel_skylib",
        strip_prefix = "bazel-skylib-2169ae1c374aab4a09aa90e65efe1a3aad4e279b",
        urls = ["https://github.com/bazelbuild/bazel-skylib/archive/2169ae1c374aab4a09aa90e65efe1a3aad4e279b.tar.gz"],
    )

    _grpc_version = "1.43.0"
    _grpc_sha256 = "9647220c699cea4dafa92ec0917c25c7812be51a18143af047e20f3fb05adddc"
    _maybe(
        http_archive,
        name = "com_github_grpc_grpc",
        sha256 = _grpc_sha256,
        strip_prefix = "grpc-{}".format(_grpc_version),
        url = "https://github.com/grpc/grpc/archive/v{}.tar.gz".format(_grpc_version),
    )

    _maybe(
        http_archive,
        name = "pandoc_linux",
        build_file_content = _PANDOC_BUILD_FILE,
        strip_prefix = "pandoc-2.2.1",
        url = "https://github.com/jgm/pandoc/releases/download/2.2.1/pandoc-2.2.1-linux.tar.gz",
    )

    _maybe(
        http_archive,
        name = "pandoc_macOS",
        build_file_content = _PANDOC_BUILD_FILE,
        strip_prefix = "pandoc-2.2.1",
        url = "https://github.com/jgm/pandoc/releases/download/2.2.1/pandoc-2.2.1-macOS.zip",
    )

    _rules_gapic_version = "0.5.4"
    _maybe(
        http_archive,
        name = "rules_gapic",
        strip_prefix = "rules_gapic-%s" % _rules_gapic_version,
        urls = ["https://github.com/googleapis/rules_gapic/archive/v%s.tar.gz" % _rules_gapic_version],
    )

    _maybe(
        http_archive,
        name = "com_google_googleapis",
        strip_prefix = "googleapis-ffc531383747ebb702dad3db237ef5fdea796363",
        urls = ["https://github.com/googleapis/googleapis/archive/ffc531383747ebb702dad3db237ef5fdea796363.zip"],
    )

def gapic_generator_register_toolchains():
    native.register_toolchains(
        "@gapic_generator_python//:pandoc_toolchain_linux",
        "@gapic_generator_python//:pandoc_toolchain_macOS",
    )

def _maybe(repo_rule, name, strip_repo_prefix = "", **kwargs):
    if not name.startswith(strip_repo_prefix):
        return
    repo_name = name[len(strip_repo_prefix):]
    if repo_name in native.existing_rules():
        return
    repo_rule(name = repo_name, **kwargs)
