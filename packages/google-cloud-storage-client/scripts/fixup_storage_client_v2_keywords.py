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


class storage_clientCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'bidi_write_object': ('write_offset', 'upload_id', 'write_object_spec', 'checksummed_data', 'object_checksums', 'state_lookup', 'flush', 'finish_write', 'common_object_request_params', ),
        'cancel_resumable_write': ('upload_id', ),
        'compose_object': ('destination', 'source_objects', 'destination_predefined_acl', 'if_generation_match', 'if_metageneration_match', 'kms_key', 'common_object_request_params', 'object_checksums', ),
        'create_bucket': ('parent', 'bucket_id', 'bucket', 'predefined_acl', 'predefined_default_object_acl', ),
        'create_hmac_key': ('project', 'service_account_email', ),
        'create_notification_config': ('parent', 'notification_config', ),
        'delete_bucket': ('name', 'if_metageneration_match', 'if_metageneration_not_match', ),
        'delete_hmac_key': ('access_id', 'project', ),
        'delete_notification_config': ('name', ),
        'delete_object': ('bucket', 'object_', 'generation', 'if_generation_match', 'if_generation_not_match', 'if_metageneration_match', 'if_metageneration_not_match', 'common_object_request_params', ),
        'get_bucket': ('name', 'if_metageneration_match', 'if_metageneration_not_match', 'read_mask', ),
        'get_hmac_key': ('access_id', 'project', ),
        'get_iam_policy': ('resource', 'options', ),
        'get_notification_config': ('name', ),
        'get_object': ('bucket', 'object_', 'generation', 'soft_deleted', 'if_generation_match', 'if_generation_not_match', 'if_metageneration_match', 'if_metageneration_not_match', 'common_object_request_params', 'read_mask', ),
        'get_service_account': ('project', ),
        'list_buckets': ('parent', 'page_size', 'page_token', 'prefix', 'read_mask', ),
        'list_hmac_keys': ('project', 'page_size', 'page_token', 'service_account_email', 'show_deleted_keys', ),
        'list_notification_configs': ('parent', 'page_size', 'page_token', ),
        'list_objects': ('parent', 'page_size', 'page_token', 'delimiter', 'include_trailing_delimiter', 'prefix', 'versions', 'read_mask', 'lexicographic_start', 'lexicographic_end', 'soft_deleted', 'include_folders_as_prefixes', 'match_glob', ),
        'lock_bucket_retention_policy': ('bucket', 'if_metageneration_match', ),
        'query_write_status': ('upload_id', 'common_object_request_params', ),
        'read_object': ('bucket', 'object_', 'generation', 'read_offset', 'read_limit', 'if_generation_match', 'if_generation_not_match', 'if_metageneration_match', 'if_metageneration_not_match', 'common_object_request_params', 'read_mask', ),
        'restore_object': ('bucket', 'object_', 'generation', 'if_generation_match', 'if_generation_not_match', 'if_metageneration_match', 'if_metageneration_not_match', 'copy_source_acl', 'common_object_request_params', ),
        'rewrite_object': ('destination_name', 'destination_bucket', 'source_bucket', 'source_object', 'destination_kms_key', 'destination', 'source_generation', 'rewrite_token', 'destination_predefined_acl', 'if_generation_match', 'if_generation_not_match', 'if_metageneration_match', 'if_metageneration_not_match', 'if_source_generation_match', 'if_source_generation_not_match', 'if_source_metageneration_match', 'if_source_metageneration_not_match', 'max_bytes_rewritten_per_call', 'copy_source_encryption_algorithm', 'copy_source_encryption_key_bytes', 'copy_source_encryption_key_sha256_bytes', 'common_object_request_params', 'object_checksums', ),
        'set_iam_policy': ('resource', 'policy', 'update_mask', ),
        'start_resumable_write': ('write_object_spec', 'common_object_request_params', 'object_checksums', ),
        'test_iam_permissions': ('resource', 'permissions', ),
        'update_bucket': ('bucket', 'update_mask', 'if_metageneration_match', 'if_metageneration_not_match', 'predefined_acl', 'predefined_default_object_acl', ),
        'update_hmac_key': ('hmac_key', 'update_mask', ),
        'update_object': ('object_', 'update_mask', 'if_generation_match', 'if_generation_not_match', 'if_metageneration_match', 'if_metageneration_not_match', 'predefined_acl', 'common_object_request_params', ),
        'write_object': ('write_offset', 'upload_id', 'write_object_spec', 'checksummed_data', 'object_checksums', 'finish_write', 'common_object_request_params', ),
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
    transformer=storage_clientCallTransformer(),
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
        description="""Fix up source that uses the storage_client client library.

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
