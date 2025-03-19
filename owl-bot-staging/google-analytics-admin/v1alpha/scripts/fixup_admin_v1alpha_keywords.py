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


class adminCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'acknowledge_user_data_collection': ('property', 'acknowledgement', ),
        'approve_display_video360_advertiser_link_proposal': ('name', ),
        'archive_audience': ('name', ),
        'archive_custom_dimension': ('name', ),
        'archive_custom_metric': ('name', ),
        'batch_create_access_bindings': ('parent', 'requests', ),
        'batch_delete_access_bindings': ('parent', 'requests', ),
        'batch_get_access_bindings': ('parent', 'names', ),
        'batch_update_access_bindings': ('parent', 'requests', ),
        'cancel_display_video360_advertiser_link_proposal': ('name', ),
        'create_access_binding': ('parent', 'access_binding', ),
        'create_ad_sense_link': ('parent', 'adsense_link', ),
        'create_audience': ('parent', 'audience', ),
        'create_big_query_link': ('parent', 'bigquery_link', ),
        'create_calculated_metric': ('parent', 'calculated_metric_id', 'calculated_metric', ),
        'create_channel_group': ('parent', 'channel_group', ),
        'create_connected_site_tag': ('connected_site_tag', 'property', ),
        'create_conversion_event': ('conversion_event', 'parent', ),
        'create_custom_dimension': ('parent', 'custom_dimension', ),
        'create_custom_metric': ('parent', 'custom_metric', ),
        'create_data_stream': ('parent', 'data_stream', ),
        'create_display_video360_advertiser_link': ('parent', 'display_video_360_advertiser_link', ),
        'create_display_video360_advertiser_link_proposal': ('parent', 'display_video_360_advertiser_link_proposal', ),
        'create_event_create_rule': ('parent', 'event_create_rule', ),
        'create_event_edit_rule': ('parent', 'event_edit_rule', ),
        'create_expanded_data_set': ('parent', 'expanded_data_set', ),
        'create_firebase_link': ('parent', 'firebase_link', ),
        'create_google_ads_link': ('parent', 'google_ads_link', ),
        'create_key_event': ('key_event', 'parent', ),
        'create_measurement_protocol_secret': ('parent', 'measurement_protocol_secret', ),
        'create_property': ('property', ),
        'create_rollup_property': ('rollup_property', 'source_properties', ),
        'create_rollup_property_source_link': ('parent', 'rollup_property_source_link', ),
        'create_search_ads360_link': ('parent', 'search_ads_360_link', ),
        'create_sk_ad_network_conversion_value_schema': ('parent', 'skadnetwork_conversion_value_schema', ),
        'create_subproperty_event_filter': ('parent', 'subproperty_event_filter', ),
        'delete_access_binding': ('name', ),
        'delete_account': ('name', ),
        'delete_ad_sense_link': ('name', ),
        'delete_big_query_link': ('name', ),
        'delete_calculated_metric': ('name', ),
        'delete_channel_group': ('name', ),
        'delete_connected_site_tag': ('property', 'tag_id', ),
        'delete_conversion_event': ('name', ),
        'delete_data_stream': ('name', ),
        'delete_display_video360_advertiser_link': ('name', ),
        'delete_display_video360_advertiser_link_proposal': ('name', ),
        'delete_event_create_rule': ('name', ),
        'delete_event_edit_rule': ('name', ),
        'delete_expanded_data_set': ('name', ),
        'delete_firebase_link': ('name', ),
        'delete_google_ads_link': ('name', ),
        'delete_key_event': ('name', ),
        'delete_measurement_protocol_secret': ('name', ),
        'delete_property': ('name', ),
        'delete_rollup_property_source_link': ('name', ),
        'delete_search_ads360_link': ('name', ),
        'delete_sk_ad_network_conversion_value_schema': ('name', ),
        'delete_subproperty_event_filter': ('name', ),
        'fetch_automated_ga4_configuration_opt_out': ('property', ),
        'fetch_connected_ga4_property': ('property', ),
        'get_access_binding': ('name', ),
        'get_account': ('name', ),
        'get_ad_sense_link': ('name', ),
        'get_attribution_settings': ('name', ),
        'get_audience': ('name', ),
        'get_big_query_link': ('name', ),
        'get_calculated_metric': ('name', ),
        'get_channel_group': ('name', ),
        'get_conversion_event': ('name', ),
        'get_custom_dimension': ('name', ),
        'get_custom_metric': ('name', ),
        'get_data_redaction_settings': ('name', ),
        'get_data_retention_settings': ('name', ),
        'get_data_sharing_settings': ('name', ),
        'get_data_stream': ('name', ),
        'get_display_video360_advertiser_link': ('name', ),
        'get_display_video360_advertiser_link_proposal': ('name', ),
        'get_enhanced_measurement_settings': ('name', ),
        'get_event_create_rule': ('name', ),
        'get_event_edit_rule': ('name', ),
        'get_expanded_data_set': ('name', ),
        'get_global_site_tag': ('name', ),
        'get_google_signals_settings': ('name', ),
        'get_key_event': ('name', ),
        'get_measurement_protocol_secret': ('name', ),
        'get_property': ('name', ),
        'get_rollup_property_source_link': ('name', ),
        'get_search_ads360_link': ('name', ),
        'get_sk_ad_network_conversion_value_schema': ('name', ),
        'get_subproperty_event_filter': ('name', ),
        'list_access_bindings': ('parent', 'page_size', 'page_token', ),
        'list_accounts': ('page_size', 'page_token', 'show_deleted', ),
        'list_account_summaries': ('page_size', 'page_token', ),
        'list_ad_sense_links': ('parent', 'page_size', 'page_token', ),
        'list_audiences': ('parent', 'page_size', 'page_token', ),
        'list_big_query_links': ('parent', 'page_size', 'page_token', ),
        'list_calculated_metrics': ('parent', 'page_size', 'page_token', ),
        'list_channel_groups': ('parent', 'page_size', 'page_token', ),
        'list_connected_site_tags': ('property', ),
        'list_conversion_events': ('parent', 'page_size', 'page_token', ),
        'list_custom_dimensions': ('parent', 'page_size', 'page_token', ),
        'list_custom_metrics': ('parent', 'page_size', 'page_token', ),
        'list_data_streams': ('parent', 'page_size', 'page_token', ),
        'list_display_video360_advertiser_link_proposals': ('parent', 'page_size', 'page_token', ),
        'list_display_video360_advertiser_links': ('parent', 'page_size', 'page_token', ),
        'list_event_create_rules': ('parent', 'page_size', 'page_token', ),
        'list_event_edit_rules': ('parent', 'page_size', 'page_token', ),
        'list_expanded_data_sets': ('parent', 'page_size', 'page_token', ),
        'list_firebase_links': ('parent', 'page_size', 'page_token', ),
        'list_google_ads_links': ('parent', 'page_size', 'page_token', ),
        'list_key_events': ('parent', 'page_size', 'page_token', ),
        'list_measurement_protocol_secrets': ('parent', 'page_size', 'page_token', ),
        'list_properties': ('filter', 'page_size', 'page_token', 'show_deleted', ),
        'list_rollup_property_source_links': ('parent', 'page_size', 'page_token', ),
        'list_search_ads360_links': ('parent', 'page_size', 'page_token', ),
        'list_sk_ad_network_conversion_value_schemas': ('parent', 'page_size', 'page_token', ),
        'list_subproperty_event_filters': ('parent', 'page_size', 'page_token', ),
        'provision_account_ticket': ('account', 'redirect_uri', ),
        'provision_subproperty': ('subproperty', 'subproperty_event_filter', ),
        'reorder_event_edit_rules': ('parent', 'event_edit_rules', ),
        'run_access_report': ('entity', 'dimensions', 'metrics', 'date_ranges', 'dimension_filter', 'metric_filter', 'offset', 'limit', 'time_zone', 'order_bys', 'return_entity_quota', 'include_all_users', 'expand_groups', ),
        'search_change_history_events': ('account', 'property', 'resource_type', 'action', 'actor_email', 'earliest_change_time', 'latest_change_time', 'page_size', 'page_token', ),
        'set_automated_ga4_configuration_opt_out': ('property', 'opt_out', ),
        'update_access_binding': ('access_binding', ),
        'update_account': ('account', 'update_mask', ),
        'update_attribution_settings': ('attribution_settings', 'update_mask', ),
        'update_audience': ('audience', 'update_mask', ),
        'update_big_query_link': ('bigquery_link', 'update_mask', ),
        'update_calculated_metric': ('calculated_metric', 'update_mask', ),
        'update_channel_group': ('channel_group', 'update_mask', ),
        'update_conversion_event': ('conversion_event', 'update_mask', ),
        'update_custom_dimension': ('update_mask', 'custom_dimension', ),
        'update_custom_metric': ('update_mask', 'custom_metric', ),
        'update_data_redaction_settings': ('data_redaction_settings', 'update_mask', ),
        'update_data_retention_settings': ('data_retention_settings', 'update_mask', ),
        'update_data_stream': ('update_mask', 'data_stream', ),
        'update_display_video360_advertiser_link': ('update_mask', 'display_video_360_advertiser_link', ),
        'update_enhanced_measurement_settings': ('enhanced_measurement_settings', 'update_mask', ),
        'update_event_create_rule': ('event_create_rule', 'update_mask', ),
        'update_event_edit_rule': ('event_edit_rule', 'update_mask', ),
        'update_expanded_data_set': ('expanded_data_set', 'update_mask', ),
        'update_google_ads_link': ('update_mask', 'google_ads_link', ),
        'update_google_signals_settings': ('google_signals_settings', 'update_mask', ),
        'update_key_event': ('key_event', 'update_mask', ),
        'update_measurement_protocol_secret': ('measurement_protocol_secret', 'update_mask', ),
        'update_property': ('property', 'update_mask', ),
        'update_search_ads360_link': ('update_mask', 'search_ads_360_link', ),
        'update_sk_ad_network_conversion_value_schema': ('skadnetwork_conversion_value_schema', 'update_mask', ),
        'update_subproperty_event_filter': ('subproperty_event_filter', 'update_mask', ),
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
    transformer=adminCallTransformer(),
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
        description="""Fix up source that uses the admin client library.

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
