load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@rules_python//python:pip.bzl", "pip_import")

def gapic_generator_python():
    _maybe(
        pip_import,
        name = "gapic_generator_python_pip_deps",
        python_interpreter = "python3",
        requirements = "@gapic_generator_python//:requirements.txt",
    )

    _protobuf_version = "3.11.2"
    _protobuf_version_in_link = "v%s" % _protobuf_version
    _maybe(
        http_archive,
        name = "com_google_protobuf",
        urls = ["https://github.com/protocolbuffers/protobuf/archive/%s.zip" % _protobuf_version_in_link],
        strip_prefix = "protobuf-%s" % _protobuf_version,
    )

    _maybe(
        http_archive,
        name = "bazel_skylib",
        strip_prefix = "bazel-skylib-2169ae1c374aab4a09aa90e65efe1a3aad4e279b",
        urls = ["https://github.com/bazelbuild/bazel-skylib/archive/2169ae1c374aab4a09aa90e65efe1a3aad4e279b.tar.gz"],
    )

    _maybe(
        http_archive,
        name = "com_google_api_codegen",
        strip_prefix = "gapic-generator-b32c73219d617f90de70bfa6ff0ea0b0dd638dfe",
        urls = ["https://github.com/googleapis/gapic-generator/archive/b32c73219d617f90de70bfa6ff0ea0b0dd638dfe.zip"],
    )

def _maybe(repo_rule, name, strip_repo_prefix = "", **kwargs):
    if not name.startswith(strip_repo_prefix):
        return
    repo_name = name[len(strip_repo_prefix):]
    if repo_name in native.existing_rules():
        return
    repo_rule(name = repo_name, **kwargs)
