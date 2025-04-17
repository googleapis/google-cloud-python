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


class visionaiCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'acquire_lease': ('series', 'owner', 'term', 'lease_type', ),
        'add_application_stream_input': ('name', 'application_stream_inputs', 'request_id', ),
        'add_collection_item': ('item', ),
        'analyze_asset': ('name', ),
        'analyze_corpus': ('name', ),
        'batch_run_process': ('parent', 'requests', 'options', 'batch_id', ),
        'clip_asset': ('name', 'temporal_partition', ),
        'create_analysis': ('parent', 'analysis_id', 'analysis', 'request_id', ),
        'create_annotation': ('parent', 'annotation', 'annotation_id', ),
        'create_application': ('parent', 'application_id', 'application', 'request_id', ),
        'create_application_instances': ('name', 'application_instances', 'request_id', ),
        'create_asset': ('parent', 'asset', 'asset_id', ),
        'create_cluster': ('parent', 'cluster_id', 'cluster', 'request_id', ),
        'create_collection': ('parent', 'collection', 'collection_id', ),
        'create_corpus': ('parent', 'corpus', ),
        'create_data_schema': ('parent', 'data_schema', ),
        'create_draft': ('parent', 'draft_id', 'draft', 'request_id', ),
        'create_event': ('parent', 'event_id', 'event', 'request_id', ),
        'create_index': ('parent', 'index', 'index_id', ),
        'create_index_endpoint': ('parent', 'index_endpoint', 'index_endpoint_id', ),
        'create_operator': ('parent', 'operator_id', 'operator', 'request_id', ),
        'create_process': ('parent', 'process_id', 'process', 'request_id', ),
        'create_processor': ('parent', 'processor_id', 'processor', 'request_id', ),
        'create_search_config': ('parent', 'search_config', 'search_config_id', ),
        'create_search_hypernym': ('parent', 'search_hypernym', 'search_hypernym_id', ),
        'create_series': ('parent', 'series_id', 'series', 'request_id', ),
        'create_stream': ('parent', 'stream_id', 'stream', 'request_id', ),
        'delete_analysis': ('name', 'request_id', ),
        'delete_annotation': ('name', ),
        'delete_application': ('name', 'request_id', 'force', ),
        'delete_application_instances': ('name', 'instance_ids', 'request_id', ),
        'delete_asset': ('name', ),
        'delete_cluster': ('name', 'request_id', ),
        'delete_collection': ('name', ),
        'delete_corpus': ('name', ),
        'delete_data_schema': ('name', ),
        'delete_draft': ('name', 'request_id', ),
        'delete_event': ('name', 'request_id', ),
        'delete_index': ('name', ),
        'delete_index_endpoint': ('name', ),
        'delete_operator': ('name', 'request_id', ),
        'delete_process': ('name', 'request_id', ),
        'delete_processor': ('name', 'request_id', ),
        'delete_search_config': ('name', ),
        'delete_search_hypernym': ('name', ),
        'delete_series': ('name', 'request_id', ),
        'delete_stream': ('name', 'request_id', ),
        'deploy_application': ('name', 'validate_only', 'request_id', 'enable_monitoring', ),
        'deploy_index': ('index_endpoint', 'deployed_index', ),
        'generate_hls_uri': ('name', 'temporal_partitions', 'live_view_enabled', ),
        'generate_retrieval_url': ('name', ),
        'generate_stream_hls_token': ('stream', ),
        'get_analysis': ('name', ),
        'get_annotation': ('name', ),
        'get_application': ('name', ),
        'get_asset': ('name', ),
        'get_cluster': ('name', ),
        'get_collection': ('name', ),
        'get_corpus': ('name', ),
        'get_data_schema': ('name', ),
        'get_draft': ('name', ),
        'get_event': ('name', ),
        'get_index': ('name', ),
        'get_index_endpoint': ('name', ),
        'get_instance': ('name', ),
        'get_operator': ('name', ),
        'get_process': ('name', ),
        'get_processor': ('name', ),
        'get_search_config': ('name', ),
        'get_search_hypernym': ('name', ),
        'get_series': ('name', ),
        'get_stream': ('name', ),
        'get_stream_thumbnail': ('stream', 'gcs_object_name', 'event', 'request_id', ),
        'health_check': ('cluster', ),
        'import_assets': ('parent', 'assets_gcs_uri', ),
        'index_asset': ('name', 'index', ),
        'ingest_asset': ('config', 'time_indexed_data', ),
        'list_analyses': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_annotations': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_applications': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_assets': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_clusters': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_collections': ('parent', 'page_size', 'page_token', ),
        'list_corpora': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_data_schemas': ('parent', 'page_size', 'page_token', ),
        'list_drafts': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_events': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_index_endpoints': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_indexes': ('parent', 'page_size', 'page_token', ),
        'list_instances': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_operators': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_prebuilt_processors': ('parent', ),
        'list_processes': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_processors': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_public_operators': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_search_configs': ('parent', 'page_size', 'page_token', ),
        'list_search_hypernyms': ('parent', 'page_size', 'page_token', ),
        'list_series': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_streams': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'materialize_channel': ('parent', 'channel_id', 'channel', 'request_id', ),
        'receive_events': ('setup_request', 'commit_request', ),
        'receive_packets': ('setup_request', 'commit_request', ),
        'release_lease': ('id', 'series', 'owner', ),
        'remove_application_stream_input': ('name', 'target_stream_inputs', 'request_id', ),
        'remove_collection_item': ('item', ),
        'remove_index_asset': ('name', 'index', ),
        'renew_lease': ('id', 'series', 'owner', 'term', ),
        'resolve_operator_info': ('parent', 'queries', ),
        'search_assets': ('corpus', 'schema_key_sorting_strategy', 'page_size', 'page_token', 'content_time_ranges', 'criteria', 'facet_selections', 'result_annotation_keys', 'search_query', ),
        'search_index_endpoint': ('index_endpoint', 'image_query', 'text_query', 'criteria', 'exclusion_criteria', 'page_size', 'page_token', ),
        'send_packets': ('packet', 'metadata', ),
        'undeploy_application': ('name', 'request_id', ),
        'undeploy_index': ('index_endpoint', ),
        'update_analysis': ('update_mask', 'analysis', 'request_id', ),
        'update_annotation': ('annotation', 'update_mask', ),
        'update_application': ('application', 'update_mask', 'request_id', ),
        'update_application_instances': ('name', 'application_instances', 'request_id', 'allow_missing', ),
        'update_application_stream_input': ('name', 'application_stream_inputs', 'request_id', 'allow_missing', ),
        'update_asset': ('asset', 'update_mask', ),
        'update_cluster': ('update_mask', 'cluster', 'request_id', ),
        'update_collection': ('collection', 'update_mask', ),
        'update_corpus': ('corpus', 'update_mask', ),
        'update_data_schema': ('data_schema', 'update_mask', ),
        'update_draft': ('draft', 'update_mask', 'request_id', 'allow_missing', ),
        'update_event': ('update_mask', 'event', 'request_id', ),
        'update_index': ('index', 'update_mask', ),
        'update_index_endpoint': ('index_endpoint', 'update_mask', ),
        'update_operator': ('update_mask', 'operator', 'request_id', ),
        'update_process': ('update_mask', 'process', 'request_id', ),
        'update_processor': ('processor', 'update_mask', 'request_id', ),
        'update_search_config': ('search_config', 'update_mask', ),
        'update_search_hypernym': ('search_hypernym', 'update_mask', ),
        'update_series': ('update_mask', 'series', 'request_id', ),
        'update_stream': ('update_mask', 'stream', 'request_id', ),
        'upload_asset': ('name', 'asset_source', ),
        'view_collection_items': ('collection', 'page_size', 'page_token', ),
        'view_indexed_assets': ('index', 'page_size', 'page_token', 'filter', ),
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
    transformer=visionaiCallTransformer(),
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
        description="""Fix up source that uses the visionai client library.

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
