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


class discoveryengineCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'advanced_complete_query': ('completion_config', 'query', 'query_model', 'user_pseudo_id', 'user_info', 'include_tail_suggestions', 'boost_spec', 'suggestion_types', ),
        'answer_query': ('serving_config', 'query', 'session', 'safety_spec', 'related_questions_spec', 'grounding_spec', 'answer_generation_spec', 'search_spec', 'query_understanding_spec', 'asynchronous_mode', 'user_pseudo_id', 'user_labels', ),
        'batch_create_target_sites': ('parent', 'requests', ),
        'batch_get_documents_metadata': ('parent', 'matcher', ),
        'batch_verify_target_sites': ('parent', ),
        'check_grounding': ('grounding_config', 'answer_candidate', 'facts', 'grounding_spec', 'user_labels', ),
        'collect_user_event': ('parent', 'user_event', 'uri', 'ets', ),
        'complete_query': ('data_store', 'query', 'query_model', 'user_pseudo_id', 'include_tail_suggestions', ),
        'converse_conversation': ('name', 'query', 'serving_config', 'conversation', 'safe_search', 'user_labels', 'summary_spec', 'filter', 'boost_spec', ),
        'create_control': ('parent', 'control', 'control_id', ),
        'create_conversation': ('parent', 'conversation', ),
        'create_data_store': ('parent', 'data_store', 'data_store_id', 'create_advanced_site_search', 'skip_default_schema_creation', ),
        'create_document': ('parent', 'document', 'document_id', ),
        'create_engine': ('parent', 'engine', 'engine_id', ),
        'create_evaluation': ('parent', 'evaluation', ),
        'create_sample_query': ('parent', 'sample_query', 'sample_query_id', ),
        'create_sample_query_set': ('parent', 'sample_query_set', 'sample_query_set_id', ),
        'create_schema': ('parent', 'schema', 'schema_id', ),
        'create_session': ('parent', 'session', ),
        'create_sitemap': ('parent', 'sitemap', ),
        'create_target_site': ('parent', 'target_site', ),
        'delete_control': ('name', ),
        'delete_conversation': ('name', ),
        'delete_data_store': ('name', ),
        'delete_document': ('name', ),
        'delete_engine': ('name', ),
        'delete_sample_query': ('name', ),
        'delete_sample_query_set': ('name', ),
        'delete_schema': ('name', ),
        'delete_session': ('name', ),
        'delete_sitemap': ('name', ),
        'delete_target_site': ('name', ),
        'disable_advanced_site_search': ('site_search_engine', ),
        'enable_advanced_site_search': ('site_search_engine', ),
        'fetch_domain_verification_status': ('site_search_engine', 'page_size', 'page_token', ),
        'fetch_sitemaps': ('parent', 'matcher', ),
        'generate_grounded_content': ('location', 'system_instruction', 'contents', 'generation_spec', 'grounding_spec', 'user_labels', ),
        'get_answer': ('name', ),
        'get_control': ('name', ),
        'get_conversation': ('name', ),
        'get_data_store': ('name', ),
        'get_document': ('name', ),
        'get_engine': ('name', ),
        'get_evaluation': ('name', ),
        'get_sample_query': ('name', ),
        'get_sample_query_set': ('name', ),
        'get_schema': ('name', ),
        'get_serving_config': ('name', ),
        'get_session': ('name', ),
        'get_site_search_engine': ('name', ),
        'get_target_site': ('name', ),
        'import_completion_suggestions': ('parent', 'inline_source', 'gcs_source', 'bigquery_source', 'error_config', ),
        'import_documents': ('parent', 'inline_source', 'gcs_source', 'bigquery_source', 'fhir_store_source', 'spanner_source', 'cloud_sql_source', 'firestore_source', 'alloy_db_source', 'bigtable_source', 'error_config', 'reconciliation_mode', 'update_mask', 'auto_generate_ids', 'id_field', ),
        'import_sample_queries': ('parent', 'inline_source', 'gcs_source', 'bigquery_source', 'error_config', ),
        'import_suggestion_deny_list_entries': ('parent', 'inline_source', 'gcs_source', ),
        'import_user_events': ('parent', 'inline_source', 'gcs_source', 'bigquery_source', 'error_config', ),
        'list_controls': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_conversations': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_custom_models': ('data_store', ),
        'list_data_stores': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_documents': ('parent', 'page_size', 'page_token', ),
        'list_engines': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_evaluation_results': ('evaluation', 'page_size', 'page_token', ),
        'list_evaluations': ('parent', 'page_size', 'page_token', ),
        'list_sample_queries': ('parent', 'page_size', 'page_token', ),
        'list_sample_query_sets': ('parent', 'page_size', 'page_token', ),
        'list_schemas': ('parent', 'page_size', 'page_token', ),
        'list_serving_configs': ('parent', 'page_size', 'page_token', ),
        'list_sessions': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_target_sites': ('parent', 'page_size', 'page_token', ),
        'pause_engine': ('name', ),
        'provision_project': ('name', 'accept_data_use_terms', 'data_use_terms_version', ),
        'purge_completion_suggestions': ('parent', ),
        'purge_documents': ('parent', 'filter', 'gcs_source', 'inline_source', 'error_config', 'force', ),
        'purge_suggestion_deny_list_entries': ('parent', ),
        'purge_user_events': ('parent', 'filter', 'force', ),
        'rank': ('ranking_config', 'records', 'model', 'top_n', 'query', 'ignore_record_details_in_response', 'user_labels', ),
        'recommend': ('serving_config', 'user_event', 'page_size', 'filter', 'validate_only', 'params', 'user_labels', ),
        'recrawl_uris': ('site_search_engine', 'uris', 'site_credential', ),
        'resume_engine': ('name', ),
        'search': ('serving_config', 'branch', 'query', 'image_query', 'page_size', 'page_token', 'offset', 'one_box_page_size', 'data_store_specs', 'filter', 'canonical_filter', 'order_by', 'user_info', 'language_code', 'region_code', 'facet_specs', 'boost_spec', 'params', 'query_expansion_spec', 'spell_correction_spec', 'user_pseudo_id', 'content_search_spec', 'embedding_spec', 'ranking_expression', 'safe_search', 'user_labels', 'natural_language_query_understanding_spec', 'search_as_you_type_spec', 'session', 'session_spec', 'relevance_threshold', 'personalization_spec', ),
        'search_lite': ('serving_config', 'branch', 'query', 'image_query', 'page_size', 'page_token', 'offset', 'one_box_page_size', 'data_store_specs', 'filter', 'canonical_filter', 'order_by', 'user_info', 'language_code', 'region_code', 'facet_specs', 'boost_spec', 'params', 'query_expansion_spec', 'spell_correction_spec', 'user_pseudo_id', 'content_search_spec', 'embedding_spec', 'ranking_expression', 'safe_search', 'user_labels', 'natural_language_query_understanding_spec', 'search_as_you_type_spec', 'session', 'session_spec', 'relevance_threshold', 'personalization_spec', ),
        'stream_generate_grounded_content': ('location', 'system_instruction', 'contents', 'generation_spec', 'grounding_spec', 'user_labels', ),
        'train_custom_model': ('data_store', 'gcs_training_input', 'model_type', 'error_config', 'model_id', ),
        'tune_engine': ('name', ),
        'update_control': ('control', 'update_mask', ),
        'update_conversation': ('conversation', 'update_mask', ),
        'update_data_store': ('data_store', 'update_mask', ),
        'update_document': ('document', 'allow_missing', 'update_mask', ),
        'update_engine': ('engine', 'update_mask', ),
        'update_sample_query': ('sample_query', 'update_mask', ),
        'update_sample_query_set': ('sample_query_set', 'update_mask', ),
        'update_schema': ('schema', 'allow_missing', ),
        'update_serving_config': ('serving_config', 'update_mask', ),
        'update_session': ('session', 'update_mask', ),
        'update_target_site': ('target_site', ),
        'write_user_event': ('parent', 'user_event', 'write_async', ),
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
    transformer=discoveryengineCallTransformer(),
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
        description="""Fix up source that uses the discoveryengine client library.

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
