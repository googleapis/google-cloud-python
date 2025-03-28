#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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


class netappCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'create_active_directory': ('parent', 'active_directory', 'active_directory_id', ),
        'create_backup': ('parent', 'backup_id', 'backup', ),
        'create_backup_policy': ('parent', 'backup_policy', 'backup_policy_id', ),
        'create_backup_vault': ('parent', 'backup_vault_id', 'backup_vault', ),
        'create_kms_config': ('parent', 'kms_config_id', 'kms_config', ),
        'create_quota_rule': ('parent', 'quota_rule', 'quota_rule_id', ),
        'create_replication': ('parent', 'replication', 'replication_id', ),
        'create_snapshot': ('parent', 'snapshot', 'snapshot_id', ),
        'create_storage_pool': ('parent', 'storage_pool_id', 'storage_pool', ),
        'create_volume': ('parent', 'volume_id', 'volume', ),
        'delete_active_directory': ('name', ),
        'delete_backup': ('name', ),
        'delete_backup_policy': ('name', ),
        'delete_backup_vault': ('name', ),
        'delete_kms_config': ('name', ),
        'delete_quota_rule': ('name', ),
        'delete_replication': ('name', ),
        'delete_snapshot': ('name', ),
        'delete_storage_pool': ('name', ),
        'delete_volume': ('name', 'force', ),
        'encrypt_volumes': ('name', ),
        'establish_peering': ('name', 'peer_cluster_name', 'peer_svm_name', 'peer_volume_name', 'peer_ip_addresses', ),
        'get_active_directory': ('name', ),
        'get_backup': ('name', ),
        'get_backup_policy': ('name', ),
        'get_backup_vault': ('name', ),
        'get_kms_config': ('name', ),
        'get_quota_rule': ('name', ),
        'get_replication': ('name', ),
        'get_snapshot': ('name', ),
        'get_storage_pool': ('name', ),
        'get_volume': ('name', ),
        'list_active_directories': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_backup_policies': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_backups': ('parent', 'page_size', 'page_token', 'order_by', 'filter', ),
        'list_backup_vaults': ('parent', 'page_size', 'page_token', 'order_by', 'filter', ),
        'list_kms_configs': ('parent', 'page_size', 'page_token', 'order_by', 'filter', ),
        'list_quota_rules': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_replications': ('parent', 'page_size', 'page_token', 'order_by', 'filter', ),
        'list_snapshots': ('parent', 'page_size', 'page_token', 'order_by', 'filter', ),
        'list_storage_pools': ('parent', 'page_size', 'page_token', 'order_by', 'filter', ),
        'list_volumes': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'resume_replication': ('name', ),
        'reverse_replication_direction': ('name', ),
        'revert_volume': ('name', 'snapshot_id', ),
        'stop_replication': ('name', 'force', ),
        'switch_active_replica_zone': ('name', ),
        'sync_replication': ('name', ),
        'update_active_directory': ('update_mask', 'active_directory', ),
        'update_backup': ('update_mask', 'backup', ),
        'update_backup_policy': ('update_mask', 'backup_policy', ),
        'update_backup_vault': ('update_mask', 'backup_vault', ),
        'update_kms_config': ('update_mask', 'kms_config', ),
        'update_quota_rule': ('quota_rule', 'update_mask', ),
        'update_replication': ('update_mask', 'replication', ),
        'update_snapshot': ('update_mask', 'snapshot', ),
        'update_storage_pool': ('update_mask', 'storage_pool', ),
        'update_volume': ('update_mask', 'volume', ),
        'validate_directory_service': ('name', 'directory_service_type', ),
        'verify_kms_config': ('name', ),
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
    transformer=netappCallTransformer(),
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
        description="""Fix up source that uses the netapp client library.

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
