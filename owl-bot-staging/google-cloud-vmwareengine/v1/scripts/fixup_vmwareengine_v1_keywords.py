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


class vmwareengineCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'create_cluster': ('parent', 'cluster_id', 'cluster', 'request_id', 'validate_only', ),
        'create_external_access_rule': ('parent', 'external_access_rule', 'external_access_rule_id', 'request_id', ),
        'create_external_address': ('parent', 'external_address', 'external_address_id', 'request_id', ),
        'create_hcx_activation_key': ('parent', 'hcx_activation_key', 'hcx_activation_key_id', 'request_id', ),
        'create_logging_server': ('parent', 'logging_server', 'logging_server_id', 'request_id', ),
        'create_management_dns_zone_binding': ('parent', 'management_dns_zone_binding', 'management_dns_zone_binding_id', 'request_id', ),
        'create_network_peering': ('parent', 'network_peering_id', 'network_peering', 'request_id', ),
        'create_network_policy': ('parent', 'network_policy_id', 'network_policy', 'request_id', ),
        'create_private_cloud': ('parent', 'private_cloud_id', 'private_cloud', 'request_id', 'validate_only', ),
        'create_private_connection': ('parent', 'private_connection_id', 'private_connection', 'request_id', ),
        'create_vmware_engine_network': ('parent', 'vmware_engine_network_id', 'vmware_engine_network', 'request_id', ),
        'delete_cluster': ('name', 'request_id', ),
        'delete_external_access_rule': ('name', 'request_id', ),
        'delete_external_address': ('name', 'request_id', ),
        'delete_logging_server': ('name', 'request_id', ),
        'delete_management_dns_zone_binding': ('name', 'request_id', ),
        'delete_network_peering': ('name', 'request_id', ),
        'delete_network_policy': ('name', 'request_id', ),
        'delete_private_cloud': ('name', 'request_id', 'force', 'delay_hours', ),
        'delete_private_connection': ('name', 'request_id', ),
        'delete_vmware_engine_network': ('name', 'request_id', 'etag', ),
        'fetch_network_policy_external_addresses': ('network_policy', 'page_size', 'page_token', ),
        'get_cluster': ('name', ),
        'get_dns_bind_permission': ('name', ),
        'get_dns_forwarding': ('name', ),
        'get_external_access_rule': ('name', ),
        'get_external_address': ('name', ),
        'get_hcx_activation_key': ('name', ),
        'get_logging_server': ('name', ),
        'get_management_dns_zone_binding': ('name', ),
        'get_network_peering': ('name', ),
        'get_network_policy': ('name', ),
        'get_node': ('name', ),
        'get_node_type': ('name', ),
        'get_private_cloud': ('name', ),
        'get_private_connection': ('name', ),
        'get_subnet': ('name', ),
        'get_vmware_engine_network': ('name', ),
        'grant_dns_bind_permission': ('name', 'principal', 'request_id', ),
        'list_clusters': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_external_access_rules': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_external_addresses': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_hcx_activation_keys': ('parent', 'page_size', 'page_token', ),
        'list_logging_servers': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_management_dns_zone_bindings': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_network_peerings': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_network_policies': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_nodes': ('parent', 'page_size', 'page_token', ),
        'list_node_types': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_peering_routes': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_private_clouds': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_private_connection_peering_routes': ('parent', 'page_size', 'page_token', ),
        'list_private_connections': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_subnets': ('parent', 'page_size', 'page_token', ),
        'list_vmware_engine_networks': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'repair_management_dns_zone_binding': ('name', 'request_id', ),
        'reset_nsx_credentials': ('private_cloud', 'request_id', ),
        'reset_vcenter_credentials': ('private_cloud', 'request_id', 'username', ),
        'revoke_dns_bind_permission': ('name', 'principal', 'request_id', ),
        'show_nsx_credentials': ('private_cloud', ),
        'show_vcenter_credentials': ('private_cloud', 'username', ),
        'undelete_private_cloud': ('name', 'request_id', ),
        'update_cluster': ('update_mask', 'cluster', 'request_id', 'validate_only', ),
        'update_dns_forwarding': ('dns_forwarding', 'update_mask', 'request_id', ),
        'update_external_access_rule': ('update_mask', 'external_access_rule', 'request_id', ),
        'update_external_address': ('update_mask', 'external_address', 'request_id', ),
        'update_logging_server': ('update_mask', 'logging_server', 'request_id', ),
        'update_management_dns_zone_binding': ('update_mask', 'management_dns_zone_binding', 'request_id', ),
        'update_network_peering': ('network_peering', 'update_mask', 'request_id', ),
        'update_network_policy': ('network_policy', 'update_mask', 'request_id', ),
        'update_private_cloud': ('private_cloud', 'update_mask', 'request_id', ),
        'update_private_connection': ('private_connection', 'update_mask', 'request_id', ),
        'update_subnet': ('update_mask', 'subnet', ),
        'update_vmware_engine_network': ('vmware_engine_network', 'update_mask', 'request_id', ),
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
    transformer=vmwareengineCallTransformer(),
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
        description="""Fix up source that uses the vmwareengine client library.

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
