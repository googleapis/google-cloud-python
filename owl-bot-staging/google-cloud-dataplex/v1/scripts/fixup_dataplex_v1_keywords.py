#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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


class dataplexCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'cancel_job': ('name', ),
        'create_asset': ('parent', 'asset_id', 'asset', 'validate_only', ),
        'create_content': ('parent', 'content', 'validate_only', ),
        'create_data_scan': ('parent', 'data_scan', 'data_scan_id', 'validate_only', ),
        'create_entity': ('parent', 'entity', 'validate_only', ),
        'create_environment': ('parent', 'environment_id', 'environment', 'validate_only', ),
        'create_lake': ('parent', 'lake_id', 'lake', 'validate_only', ),
        'create_partition': ('parent', 'partition', 'validate_only', ),
        'create_task': ('parent', 'task_id', 'task', 'validate_only', ),
        'create_zone': ('parent', 'zone_id', 'zone', 'validate_only', ),
        'delete_asset': ('name', ),
        'delete_content': ('name', ),
        'delete_data_scan': ('name', ),
        'delete_entity': ('name', 'etag', ),
        'delete_environment': ('name', ),
        'delete_lake': ('name', ),
        'delete_partition': ('name', 'etag', ),
        'delete_task': ('name', ),
        'delete_zone': ('name', ),
        'get_asset': ('name', ),
        'get_content': ('name', 'view', ),
        'get_data_scan': ('name', 'view', ),
        'get_data_scan_job': ('name', 'view', ),
        'get_entity': ('name', 'view', ),
        'get_environment': ('name', ),
        'get_iam_policy': ('resource', 'options', ),
        'get_job': ('name', ),
        'get_lake': ('name', ),
        'get_partition': ('name', ),
        'get_task': ('name', ),
        'get_zone': ('name', ),
        'list_asset_actions': ('parent', 'page_size', 'page_token', ),
        'list_assets': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_content': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_data_scan_jobs': ('parent', 'page_size', 'page_token', ),
        'list_data_scans': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_entities': ('parent', 'view', 'page_size', 'page_token', 'filter', ),
        'list_environments': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_jobs': ('parent', 'page_size', 'page_token', ),
        'list_lake_actions': ('parent', 'page_size', 'page_token', ),
        'list_lakes': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_partitions': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_sessions': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_tasks': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_zone_actions': ('parent', 'page_size', 'page_token', ),
        'list_zones': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'run_data_scan': ('name', ),
        'run_task': ('name', ),
        'set_iam_policy': ('resource', 'policy', 'update_mask', ),
        'test_iam_permissions': ('resource', 'permissions', ),
        'update_asset': ('update_mask', 'asset', 'validate_only', ),
        'update_content': ('update_mask', 'content', 'validate_only', ),
        'update_data_scan': ('data_scan', 'update_mask', 'validate_only', ),
        'update_entity': ('entity', 'validate_only', ),
        'update_environment': ('update_mask', 'environment', 'validate_only', ),
        'update_lake': ('update_mask', 'lake', 'validate_only', ),
        'update_task': ('update_mask', 'task', 'validate_only', ),
        'update_zone': ('update_mask', 'zone', 'validate_only', ),
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
    transformer=dataplexCallTransformer(),
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
        description="""Fix up source that uses the dataplex client library.

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
