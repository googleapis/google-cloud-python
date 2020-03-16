workspace(name = "gapic_generator_python")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

#
# Import rules_python
#
http_archive(
    name = "rules_python",
    strip_prefix = "rules_python-748aa53d7701e71101dfd15d800e100f6ff8e5d1",
    url = "https://github.com/bazelbuild/rules_python/archive/748aa53d7701e71101dfd15d800e100f6ff8e5d1.zip",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

load("@rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

#
# Import gapic-generator-python specific dependencies
#
load("//:repositories.bzl", "gapic_generator_python")

gapic_generator_python()

load("@gapic_generator_python_pip_deps//:requirements.bzl", "pip_install")

pip_install()

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()
