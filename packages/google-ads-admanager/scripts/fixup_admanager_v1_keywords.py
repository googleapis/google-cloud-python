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


class admanagerCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'batch_activate_ad_units': ('parent', 'names', ),
        'batch_activate_custom_fields': ('parent', 'names', ),
        'batch_activate_custom_targeting_keys': ('parent', 'names', ),
        'batch_activate_placements': ('parent', 'names', ),
        'batch_activate_teams': ('parent', 'names', ),
        'batch_allow_ad_review_center_ads': ('parent', 'names', ),
        'batch_archive_ad_units': ('parent', 'names', ),
        'batch_archive_placements': ('parent', 'names', ),
        'batch_block_ad_review_center_ads': ('parent', 'names', ),
        'batch_create_ad_units': ('parent', 'requests', ),
        'batch_create_contacts': ('parent', 'requests', ),
        'batch_create_custom_fields': ('parent', 'requests', ),
        'batch_create_custom_targeting_keys': ('parent', 'requests', ),
        'batch_create_entity_signals_mappings': ('parent', 'requests', ),
        'batch_create_placements': ('parent', 'requests', ),
        'batch_create_sites': ('parent', 'requests', ),
        'batch_create_teams': ('parent', 'requests', ),
        'batch_deactivate_ad_units': ('parent', 'names', ),
        'batch_deactivate_custom_fields': ('parent', 'names', ),
        'batch_deactivate_custom_targeting_keys': ('parent', 'names', ),
        'batch_deactivate_placements': ('parent', 'names', ),
        'batch_deactivate_sites': ('parent', 'names', ),
        'batch_deactivate_teams': ('parent', 'names', ),
        'batch_submit_sites_for_approval': ('parent', 'names', ),
        'batch_update_ad_units': ('parent', 'requests', ),
        'batch_update_contacts': ('parent', 'requests', ),
        'batch_update_custom_fields': ('parent', 'requests', ),
        'batch_update_custom_targeting_keys': ('parent', 'requests', ),
        'batch_update_entity_signals_mappings': ('parent', 'requests', ),
        'batch_update_placements': ('parent', 'requests', ),
        'batch_update_sites': ('parent', 'requests', ),
        'batch_update_teams': ('parent', 'requests', ),
        'create_ad_break': ('parent', 'ad_break', ),
        'create_ad_unit': ('parent', 'ad_unit', ),
        'create_contact': ('parent', 'contact', ),
        'create_custom_field': ('parent', 'custom_field', ),
        'create_custom_targeting_key': ('parent', 'custom_targeting_key', ),
        'create_entity_signals_mapping': ('parent', 'entity_signals_mapping', ),
        'create_placement': ('parent', 'placement', ),
        'create_private_auction': ('parent', 'private_auction', ),
        'create_private_auction_deal': ('parent', 'private_auction_deal', ),
        'create_report': ('parent', 'report', ),
        'create_site': ('parent', 'site', ),
        'create_team': ('parent', 'team', ),
        'delete_ad_break': ('name', ),
        'fetch_report_result_rows': ('name', 'page_size', 'page_token', ),
        'get_ad_break': ('name', ),
        'get_ad_unit': ('name', ),
        'get_application': ('name', ),
        'get_audience_segment': ('name', ),
        'get_bandwidth_group': ('name', ),
        'get_browser': ('name', ),
        'get_browser_language': ('name', ),
        'get_cms_metadata_key': ('name', ),
        'get_cms_metadata_value': ('name', ),
        'get_company': ('name', ),
        'get_contact': ('name', ),
        'get_content': ('name', ),
        'get_content_bundle': ('name', ),
        'get_content_label': ('name', ),
        'get_creative_template': ('name', ),
        'get_custom_field': ('name', ),
        'get_custom_targeting_key': ('name', ),
        'get_custom_targeting_value': ('name', ),
        'get_device_capability': ('name', ),
        'get_device_category': ('name', ),
        'get_device_manufacturer': ('name', ),
        'get_entity_signals_mapping': ('name', ),
        'get_geo_target': ('name', ),
        'get_line_item': ('name', ),
        'get_mobile_carrier': ('name', ),
        'get_mobile_device': ('name', ),
        'get_mobile_device_submodel': ('name', ),
        'get_network': ('name', ),
        'get_operating_system': ('name', ),
        'get_operating_system_version': ('name', ),
        'get_order': ('name', ),
        'get_placement': ('name', ),
        'get_private_auction': ('name', ),
        'get_private_auction_deal': ('name', ),
        'get_programmatic_buyer': ('name', ),
        'get_report': ('name', ),
        'get_role': ('name', ),
        'get_site': ('name', ),
        'get_taxonomy_category': ('name', ),
        'get_team': ('name', ),
        'get_user': ('name', ),
        'list_ad_breaks': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_ad_units': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_ad_unit_sizes': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_applications': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_audience_segments': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_bandwidth_groups': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_browser_languages': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_browsers': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_cms_metadata_keys': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_cms_metadata_values': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_companies': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_contacts': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_content': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_content_bundles': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_content_labels': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_creative_templates': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_custom_fields': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_custom_targeting_keys': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_custom_targeting_values': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_device_capabilities': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_device_categories': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_device_manufacturers': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_entity_signals_mappings': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_geo_targets': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_line_items': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_mobile_carriers': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_mobile_devices': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_mobile_device_submodels': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_networks': ('page_size', 'page_token', 'skip', ),
        'list_operating_systems': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_operating_system_versions': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_orders': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_placements': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_private_auction_deals': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_private_auctions': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_programmatic_buyers': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_reports': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_roles': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_sites': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_taxonomy_categories': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'list_teams': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'skip', ),
        'run_report': ('name', ),
        'search_ad_review_center_ads': ('parent', 'page_size', 'page_token', 'status', 'ad_review_center_ad_id', 'date_time_range', 'search_text', 'buyer_account_id', ),
        'update_ad_break': ('ad_break', 'update_mask', ),
        'update_ad_unit': ('ad_unit', 'update_mask', ),
        'update_contact': ('contact', 'update_mask', ),
        'update_custom_field': ('custom_field', 'update_mask', ),
        'update_custom_targeting_key': ('custom_targeting_key', 'update_mask', ),
        'update_entity_signals_mapping': ('entity_signals_mapping', 'update_mask', ),
        'update_placement': ('placement', 'update_mask', ),
        'update_private_auction': ('private_auction', 'update_mask', ),
        'update_private_auction_deal': ('private_auction_deal', 'update_mask', ),
        'update_report': ('report', 'update_mask', ),
        'update_site': ('site', 'update_mask', ),
        'update_team': ('team', 'update_mask', ),
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
    transformer=admanagerCallTransformer(),
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
        description="""Fix up source that uses the admanager client library.

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
