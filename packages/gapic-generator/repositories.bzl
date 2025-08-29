load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

_PANDOC_BUILD_FILE = """
filegroup(
    name = "pandoc",
    srcs = ["bin/pandoc"],
    visibility = ["//visibility:public"],
)"""

def gapic_generator_python():

    _protobuf_version = "3.21.12"
    _protobuf_sha256 = "930c2c3b5ecc6c9c12615cf5ad93f1cd6e12d0aba862b572e076259970ac3a53"
    _protobuf_version_in_link = "v{}".format(_protobuf_version)
    _maybe(
        http_archive,
        name = "com_google_protobuf",
        sha256 = _protobuf_sha256,
        url = "https://github.com/protocolbuffers/protobuf/archive/refs/tags/{}.tar.gz".format(_protobuf_version_in_link),
        strip_prefix = "protobuf-{}".format(_protobuf_version),
    )

    _maybe(
        http_archive,
        name = "bazel_skylib",
        strip_prefix = "bazel-skylib-2169ae1c374aab4a09aa90e65efe1a3aad4e279b",
        urls = ["https://github.com/bazelbuild/bazel-skylib/archive/2169ae1c374aab4a09aa90e65efe1a3aad4e279b.tar.gz"],
    )

    _grpc_version = "1.47.0"
    _grpc_sha256 = "edf25f4db6c841853b7a29d61b0980b516dc31a1b6cdc399bcf24c1446a4a249"
    _maybe(
        http_archive,
        name = "com_github_grpc_grpc",
        sha256 = _grpc_sha256,
        strip_prefix = "grpc-{}".format(_grpc_version),
        url = "https://github.com/grpc/grpc/archive/v{}.zip".format(_grpc_version),
    )

    _maybe(
        http_archive,
        name = "pandoc_linux_arm_64",
        build_file_content = _PANDOC_BUILD_FILE,
        strip_prefix = "pandoc-3.7.0.2",
        url = "https://github.com/jgm/pandoc/releases/download/3.7.0.2/pandoc-3.7.0.2-linux-arm64.tar.gz",
    )

    _maybe(
        http_archive,
        name = "pandoc_linux_x86_64",
        build_file_content = _PANDOC_BUILD_FILE,
        strip_prefix = "pandoc-3.7.0.2",
        url = "https://github.com/jgm/pandoc/releases/download/3.7.0.2/pandoc-3.7.0.2-linux-amd64.tar.gz",
    )

    _maybe(
        http_archive,
        name = "pandoc_macOS_arm_64",
        build_file_content = _PANDOC_BUILD_FILE,
        strip_prefix = "pandoc-3.7.0.2",
        url = "https://github.com/jgm/pandoc/releases/download/3.7.0.2/pandoc-3.7.0.2-arm64-macOS.zip",
    )

    _maybe(
        http_archive,
        name = "pandoc_macOS_x86_64",
        build_file_content = _PANDOC_BUILD_FILE,
        strip_prefix = "pandoc-3.7.0.2",
        url = "https://github.com/jgm/pandoc/releases/download/3.7.0.2/pandoc-3.7.0.2-x86_64-macOS.zip",
    )

    _maybe(
        http_archive,
        name = "pandoc_windows_x86_64",
        build_file_content = _PANDOC_BUILD_FILE,
        strip_prefix = "pandoc-3.7.0.2",
        url = "https://github.com/jgm/pandoc/releases/download/3.7.0.2/pandoc-3.7.0.2-windows-x86_64.zip",
    )

    _rules_gapic_version = "0.5.4"
    _maybe(
        http_archive,
        name = "rules_gapic",
        strip_prefix = "rules_gapic-%s" % _rules_gapic_version,
        urls = ["https://github.com/googleapis/rules_gapic/archive/v%s.tar.gz" % _rules_gapic_version],
    )
    _commit_sha = "fae3e6e091418d6343902debaf545cfc8f32c3ff"
    _maybe(
        http_archive,
        name = "com_google_googleapis",
        strip_prefix = "googleapis-{}".format(_commit_sha),
        urls = ["https://github.com/googleapis/googleapis/archive/{}.zip".format(_commit_sha)],
    )

def gapic_generator_register_toolchains():
    native.register_toolchains(
        "@gapic_generator_python//:pandoc_toolchain_linux_arm_64",
        "@gapic_generator_python//:pandoc_toolchain_linux_x86_64",
        "@gapic_generator_python//:pandoc_toolchain_macOS_arm_64",
        "@gapic_generator_python//:pandoc_toolchain_macOS_x86_64",
        "@gapic_generator_python//:pandoc_toolchain_windows_x86_64",
    )

def _maybe(repo_rule, name, strip_repo_prefix = "", **kwargs):
    if not name.startswith(strip_repo_prefix):
        return
    repo_name = name[len(strip_repo_prefix):]
    if repo_name in native.existing_rules():
        return
    repo_rule(name = repo_name, **kwargs)
