import starlark as sl
import json
import logging
import sys

logger = logging.getLogger(__name__)


def parse_content(content: str) -> dict:
    glb = sl.Globals.standard()
    mod = sl.Module()
    packages = {}

    def bazel_target(**args):
        if args["name"] is not None:
            packages[args["name"]] = args
        else:
            logger.warning("bazel target without a name", args)

    def noop_bazel_rule(**args):
        pass

    def fake_glob(paths=[], **args):
        return []

    def load(name):
        # print(f"in load: {name}")
        mod = sl.Module()
        if name == "@rules_proto//proto:defs.bzl":
            mod.add_callable("proto_library", bazel_target)
        elif name == "@com_google_googleapis_imports//:imports.bzl":
            # print("adding callables")
            mod.add_callable("py_gapic_assembly_pkg", bazel_target)
            mod.add_callable("py_gapic_library", bazel_target)
            mod.add_callable("py_test", bazel_target)
            mod.add_callable("py_proto_library", bazel_target)
            mod.add_callable("py_grpc_library", bazel_target)
            mod.add_callable("py_import", bazel_target)

            mod.add_callable("proto_library_with_info", bazel_target)
            mod.add_callable("java_gapic_assembly_gradle_pkg", bazel_target)
            mod.add_callable("java_gapic_library", bazel_target)
            mod.add_callable("java_gapic_test", bazel_target)
            mod.add_callable("java_grpc_library", bazel_target)
            mod.add_callable("java_proto_library", bazel_target)
            mod.add_callable("go_gapic_assembly_pkg", bazel_target)
            mod.add_callable("go_gapic_library", bazel_target)
            mod.add_callable("go_proto_library", bazel_target)
            mod.add_callable("go_grpc_library", bazel_target)
            mod.add_callable("php_gapic_assembly_pkg", bazel_target)
            mod.add_callable("php_gapic_library", bazel_target)
            mod.add_callable("php_grpc_library", bazel_target)
            mod.add_callable("php_proto_library", bazel_target)
            mod.add_callable("nodejs_gapic_assembly_pkg", bazel_target)
            mod.add_callable("nodejs_gapic_library", bazel_target)
            mod.add_callable("ruby_ads_gapic_library", bazel_target)
            mod.add_callable("ruby_cloud_gapic_library", bazel_target)
            mod.add_callable("ruby_gapic_assembly_pkg", bazel_target)
            mod.add_callable("ruby_grpc_library", bazel_target)
            mod.add_callable("ruby_proto_library", bazel_target)
            mod.add_callable("csharp_gapic_assembly_pkg", bazel_target)
            mod.add_callable("csharp_gapic_library", bazel_target)
            mod.add_callable("csharp_grpc_library", bazel_target)
            mod.add_callable("csharp_proto_library", bazel_target)
            mod.add_callable("cc_grpc_library", bazel_target)
            mod.add_callable("cc_gapic_library", bazel_target)
            mod.add_callable("cc_proto_library", bazel_target)
            mod.add_callable("moved_proto_library", bazel_target)
            mod.add_callable("proto_library", bazel_target)
            mod.add_callable("upb_c_proto_library", bazel_target)
        elif name == ":failure_test.bzl":
            mod.add_callable(
                "php_proto_library_fails_with_message_test", noop_bazel_rule
            )
        elif name == "//google/maps:postprocessing.bzl":
            mod.add_callable("maps_assembly_pkg", bazel_target)
        elif (
            name
            == "@com_google_disco_to_proto3_converter//rules_gapic:disco_to_proto.bzl"
        ):
            mod.add_callable("gapic_yaml_from_disco", noop_bazel_rule)
            mod.add_callable("grpc_service_config_from_disco", noop_bazel_rule)
            mod.add_callable("proto_from_disco", noop_bazel_rule)
        else:
            raise f"Missing file: {name}"

        return mod.freeze()

    mod.add_callable("package", noop_bazel_rule)
    mod.add_callable("alias", noop_bazel_rule)
    mod.add_callable("exports_files", fake_glob)
    mod.add_callable("py_test", noop_bazel_rule)
    mod.add_callable("glob", fake_glob)
    mod.add_callable("sh_binary", noop_bazel_rule)
    mod.add_callable("proto_library", noop_bazel_rule)
    mod.add_callable("java_proto_library", noop_bazel_rule)
    mod.add_callable("genrule", noop_bazel_rule)

    ast = sl.parse("BUILD.bazel", content)

    sl.eval(mod, ast, glb, sl.FileLoader(load))

    return packages

