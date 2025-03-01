#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
#
import argparse
import os
import libcst as cst
import pathlib
import sys
from typing import (Any, Callable, Dict, List, Sequence, Tuple)


def partition(
    predicate: Callable[[Any], bool],
    iterator: Sequence[Any]
) -> Tuple[List[Any], List[Any]]:
    """A stable, out-of-place partition."""
    results = ([], [])

    for i in iterator:
        results[int(predicate(i))].append(i)

    # Returns trueList, falseList
    return results[1], results[0]


class containerCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'cancel_operation': ('project_id', 'zone', 'operation_id', 'name', ),
        'check_autopilot_compatibility': ('name', ),
        'complete_ip_rotation': ('project_id', 'zone', 'cluster_id', 'name', ),
        'complete_node_pool_upgrade': ('name', ),
        'create_cluster': ('project_id', 'zone', 'cluster', 'parent', ),
        'create_node_pool': ('project_id', 'zone', 'cluster_id', 'node_pool', 'parent', ),
        'delete_cluster': ('project_id', 'zone', 'cluster_id', 'name', ),
        'delete_node_pool': ('project_id', 'zone', 'cluster_id', 'node_pool_id', 'name', ),
        'get_cluster': ('project_id', 'zone', 'cluster_id', 'name', ),
        'get_json_web_keys': ('parent', ),
        'get_node_pool': ('project_id', 'zone', 'cluster_id', 'node_pool_id', 'name', ),
        'get_operation': ('project_id', 'zone', 'operation_id', 'name', ),
        'get_server_config': ('project_id', 'zone', 'name', ),
        'list_clusters': ('project_id', 'zone', 'parent', ),
        'list_locations': ('parent', ),
        'list_node_pools': ('project_id', 'zone', 'cluster_id', 'parent', ),
        'list_operations': ('project_id', 'zone', 'parent', ),
        'list_usable_subnetworks': ('parent', 'filter', 'page_size', 'page_token', ),
        'rollback_node_pool_upgrade': ('project_id', 'zone', 'cluster_id', 'node_pool_id', 'name', 'respect_pdb', ),
        'set_addons_config': ('project_id', 'zone', 'cluster_id', 'addons_config', 'name', ),
        'set_labels': ('project_id', 'zone', 'cluster_id', 'resource_labels', 'label_fingerprint', 'name', ),
        'set_legacy_abac': ('project_id', 'zone', 'cluster_id', 'enabled', 'name', ),
        'set_locations': ('project_id', 'zone', 'cluster_id', 'locations', 'name', ),
        'set_logging_service': ('project_id', 'zone', 'cluster_id', 'logging_service', 'name', ),
        'set_maintenance_policy': ('project_id', 'zone', 'cluster_id', 'maintenance_policy', 'name', ),
        'set_master_auth': ('project_id', 'zone', 'cluster_id', 'action', 'update', 'name', ),
        'set_monitoring_service': ('project_id', 'zone', 'cluster_id', 'monitoring_service', 'name', ),
        'set_network_policy': ('project_id', 'zone', 'cluster_id', 'network_policy', 'name', ),
        'set_node_pool_autoscaling': ('project_id', 'zone', 'cluster_id', 'node_pool_id', 'autoscaling', 'name', ),
        'set_node_pool_management': ('project_id', 'zone', 'cluster_id', 'node_pool_id', 'management', 'name', ),
        'set_node_pool_size': ('project_id', 'zone', 'cluster_id', 'node_pool_id', 'node_count', 'name', ),
        'start_ip_rotation': ('project_id', 'zone', 'cluster_id', 'name', 'rotate_credentials', ),
        'update_cluster': ('project_id', 'zone', 'cluster_id', 'update', 'name', ),
        'update_master': ('project_id', 'zone', 'cluster_id', 'master_version', 'name', ),
        'update_node_pool': ('project_id', 'zone', 'cluster_id', 'node_pool_id', 'node_version', 'image_type', 'locations', 'workload_metadata_config', 'name', 'upgrade_settings', 'tags', 'taints', 'labels', 'linux_node_config', 'kubelet_config', 'node_network_config', 'gcfs_config', 'confidential_nodes', 'gvnic', 'etag', 'fast_socket', 'logging_config', 'resource_labels', 'windows_node_config', 'accelerators', 'machine_type', 'disk_type', 'disk_size_gb', 'resource_manager_tags', 'containerd_config', 'queued_provisioning', ),
    }

    def leave_Call(self, original: cst.Call, updated: cst.Call) -> cst.CSTNode:
        try:
            key = original.func.attr.value
            kword_params = self.METHOD_TO_PARAMS[key]
        except (AttributeError, KeyError):
            # Either not a method from the API or too convoluted to be sure.
            return updated

        # If the existing code is valid, keyword args come after positional args.
        # Therefore, all positional args must map to the first parameters.
        args, kwargs = partition(lambda a: not bool(a.keyword), updated.args)
        if any(k.keyword.value == "request" for k in kwargs):
            # We've already fixed this file, don't fix it again.
            return updated

        kwargs, ctrl_kwargs = partition(
            lambda a: a.keyword.value not in self.CTRL_PARAMS,
            kwargs
        )

        args, ctrl_args = args[:len(kword_params)], args[len(kword_params):]
        ctrl_kwargs.extend(cst.Arg(value=a.value, keyword=cst.Name(value=ctrl))
                           for a, ctrl in zip(ctrl_args, self.CTRL_PARAMS))

        request_arg = cst.Arg(
            value=cst.Dict([
                cst.DictElement(
                    cst.SimpleString("'{}'".format(name)),
cst.Element(value=arg.value)
                )
                # Note: the args + kwargs looks silly, but keep in mind that
                # the control parameters had to be stripped out, and that
                # those could have been passed positionally or by keyword.
                for name, arg in zip(kword_params, args + kwargs)]),
            keyword=cst.Name("request")
        )

        return updated.with_changes(
            args=[request_arg] + ctrl_kwargs
        )


def fix_files(
    in_dir: pathlib.Path,
    out_dir: pathlib.Path,
    *,
    transformer=containerCallTransformer(),
):
    """Duplicate the input dir to the output dir, fixing file method calls.

    Preconditions:
    * in_dir is a real directory
    * out_dir is a real, empty directory
    """
    pyfile_gen = (
        pathlib.Path(os.path.join(root, f))
        for root, _, files in os.walk(in_dir)
        for f in files if os.path.splitext(f)[1] == ".py"
    )

    for fpath in pyfile_gen:
        with open(fpath, 'r') as f:
            src = f.read()

        # Parse the code and insert method call fixes.
        tree = cst.parse_module(src)
        updated = tree.visit(transformer)

        # Create the path and directory structure for the new file.
        updated_path = out_dir.joinpath(fpath.relative_to(in_dir))
        updated_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate the updated source file at the corresponding path.
        with open(updated_path, 'w') as f:
            f.write(updated.code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Fix up source that uses the container client library.

The existing sources are NOT overwritten but are copied to output_dir with changes made.

Note: This tool operates at a best-effort level at converting positional
      parameters in client method calls to keyword based parameters.
      Cases where it WILL FAIL include
      A) * or ** expansion in a method call.
      B) Calls via function or method alias (includes free function calls)
      C) Indirect or dispatched calls (e.g. the method is looked up dynamically)

      These all constitute false negatives. The tool will also detect false
      positives when an API method shares a name with another method.
""")
    parser.add_argument(
        '-d',
        '--input-directory',
        required=True,
        dest='input_dir',
        help='the input directory to walk for python files to fix up',
    )
    parser.add_argument(
        '-o',
        '--output-directory',
        required=True,
        dest='output_dir',
        help='the directory to output files fixed via un-flattening',
    )
    args = parser.parse_args()
    input_dir = pathlib.Path(args.input_dir)
    output_dir = pathlib.Path(args.output_dir)
    if not input_dir.is_dir():
        print(
            f"input directory '{input_dir}' does not exist or is not a directory",
            file=sys.stderr,
        )
        sys.exit(-1)

    if not output_dir.is_dir():
        print(
            f"output directory '{output_dir}' does not exist or is not a directory",
            file=sys.stderr,
        )
        sys.exit(-1)

    if os.listdir(output_dir):
        print(
            f"output directory '{output_dir}' is not empty",
            file=sys.stderr,
        )
        sys.exit(-1)

    fix_files(input_dir, output_dir)
