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


class channelCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'activate_entitlement': ('name', 'request_id', ),
        'cancel_entitlement': ('name', 'request_id', ),
        'change_offer': ('name', 'offer', 'parameters', 'purchase_order_id', 'request_id', ),
        'change_parameters': ('name', 'parameters', 'request_id', 'purchase_order_id', ),
        'change_renewal_settings': ('name', 'renewal_settings', 'request_id', ),
        'check_cloud_identity_accounts_exist': ('parent', 'domain', ),
        'create_channel_partner_link': ('parent', 'channel_partner_link', ),
        'create_channel_partner_repricing_config': ('parent', 'channel_partner_repricing_config', ),
        'create_customer': ('parent', 'customer', ),
        'create_customer_repricing_config': ('parent', 'customer_repricing_config', ),
        'create_entitlement': ('parent', 'entitlement', 'request_id', ),
        'delete_channel_partner_repricing_config': ('name', ),
        'delete_customer': ('name', ),
        'delete_customer_repricing_config': ('name', ),
        'fetch_report_results': ('report_job', 'page_size', 'page_token', 'partition_keys', ),
        'get_channel_partner_link': ('name', 'view', ),
        'get_channel_partner_repricing_config': ('name', ),
        'get_customer': ('name', ),
        'get_customer_repricing_config': ('name', ),
        'get_entitlement': ('name', ),
        'import_customer': ('domain', 'cloud_identity_id', 'parent', 'overwrite_if_exists', 'auth_token', 'channel_partner_id', 'customer', ),
        'list_channel_partner_links': ('parent', 'page_size', 'page_token', 'view', ),
        'list_channel_partner_repricing_configs': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_customer_repricing_configs': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_customers': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_entitlement_changes': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_entitlements': ('parent', 'page_size', 'page_token', ),
        'list_offers': ('parent', 'page_size', 'page_token', 'filter', 'language_code', 'show_future_offers', ),
        'list_products': ('account', 'page_size', 'page_token', 'language_code', ),
        'list_purchasable_offers': ('customer', 'create_entitlement_purchase', 'change_offer_purchase', 'page_size', 'page_token', 'language_code', ),
        'list_purchasable_skus': ('customer', 'create_entitlement_purchase', 'change_offer_purchase', 'page_size', 'page_token', 'language_code', ),
        'list_reports': ('parent', 'page_size', 'page_token', 'language_code', ),
        'list_sku_group_billable_skus': ('parent', 'page_size', 'page_token', ),
        'list_sku_groups': ('parent', 'page_size', 'page_token', ),
        'list_skus': ('parent', 'account', 'page_size', 'page_token', 'language_code', ),
        'list_subscribers': ('account', 'page_size', 'page_token', ),
        'list_transferable_offers': ('parent', 'sku', 'cloud_identity_id', 'customer_name', 'page_size', 'page_token', 'language_code', ),
        'list_transferable_skus': ('parent', 'cloud_identity_id', 'customer_name', 'page_size', 'page_token', 'auth_token', 'language_code', ),
        'lookup_offer': ('entitlement', ),
        'provision_cloud_identity': ('customer', 'cloud_identity_info', 'user', 'validate_only', ),
        'register_subscriber': ('account', 'service_account', ),
        'run_report_job': ('name', 'date_range', 'filter', 'language_code', ),
        'start_paid_service': ('name', 'request_id', ),
        'suspend_entitlement': ('name', 'request_id', ),
        'transfer_entitlements': ('parent', 'entitlements', 'auth_token', 'request_id', ),
        'transfer_entitlements_to_google': ('parent', 'entitlements', 'request_id', ),
        'unregister_subscriber': ('account', 'service_account', ),
        'update_channel_partner_link': ('name', 'channel_partner_link', 'update_mask', ),
        'update_channel_partner_repricing_config': ('channel_partner_repricing_config', ),
        'update_customer': ('customer', 'update_mask', ),
        'update_customer_repricing_config': ('customer_repricing_config', ),
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
    transformer=channelCallTransformer(),
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
        description="""Fix up source that uses the channel client library.

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
