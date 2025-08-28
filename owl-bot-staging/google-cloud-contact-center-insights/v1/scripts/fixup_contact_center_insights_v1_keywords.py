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


class contact_center_insightsCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'bulk_analyze_conversations': ('parent', 'filter', 'analysis_percentage', 'annotator_selector', ),
        'bulk_delete_conversations': ('parent', 'filter', 'max_delete_count', 'force', ),
        'bulk_download_feedback_labels': ('parent', 'gcs_destination', 'filter', 'max_download_count', 'feedback_label_type', 'conversation_filter', 'template_qa_scorecard_id', ),
        'bulk_upload_feedback_labels': ('parent', 'gcs_source', 'validate_only', ),
        'calculate_issue_model_stats': ('issue_model', ),
        'calculate_stats': ('location', 'filter', ),
        'create_analysis': ('parent', 'analysis', ),
        'create_analysis_rule': ('parent', 'analysis_rule', ),
        'create_conversation': ('parent', 'conversation', 'conversation_id', ),
        'create_feedback_label': ('parent', 'feedback_label', 'feedback_label_id', ),
        'create_issue_model': ('parent', 'issue_model', ),
        'create_phrase_matcher': ('parent', 'phrase_matcher', ),
        'create_qa_question': ('parent', 'qa_question', 'qa_question_id', ),
        'create_qa_scorecard': ('parent', 'qa_scorecard', 'qa_scorecard_id', ),
        'create_qa_scorecard_revision': ('parent', 'qa_scorecard_revision', 'qa_scorecard_revision_id', ),
        'create_view': ('parent', 'view', ),
        'delete_analysis': ('name', ),
        'delete_analysis_rule': ('name', ),
        'delete_conversation': ('name', 'force', ),
        'delete_feedback_label': ('name', ),
        'delete_issue': ('name', ),
        'delete_issue_model': ('name', ),
        'delete_phrase_matcher': ('name', ),
        'delete_qa_question': ('name', ),
        'delete_qa_scorecard': ('name', 'force', ),
        'delete_qa_scorecard_revision': ('name', 'force', ),
        'delete_view': ('name', ),
        'deploy_issue_model': ('name', ),
        'deploy_qa_scorecard_revision': ('name', ),
        'export_insights_data': ('parent', 'big_query_destination', 'filter', 'kms_key', 'write_disposition', ),
        'export_issue_model': ('name', 'gcs_destination', ),
        'get_analysis': ('name', ),
        'get_analysis_rule': ('name', ),
        'get_conversation': ('name', 'view', ),
        'get_encryption_spec': ('name', ),
        'get_feedback_label': ('name', ),
        'get_issue': ('name', ),
        'get_issue_model': ('name', ),
        'get_phrase_matcher': ('name', ),
        'get_qa_question': ('name', ),
        'get_qa_scorecard': ('name', ),
        'get_qa_scorecard_revision': ('name', ),
        'get_settings': ('name', ),
        'get_view': ('name', ),
        'import_issue_model': ('parent', 'gcs_source', 'create_new_model', ),
        'ingest_conversations': ('parent', 'gcs_source', 'transcript_object_config', 'conversation_config', 'redaction_config', 'speech_config', 'sample_size', ),
        'initialize_encryption_spec': ('encryption_spec', ),
        'list_all_feedback_labels': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_analyses': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_analysis_rules': ('parent', 'page_size', 'page_token', ),
        'list_conversations': ('parent', 'page_size', 'page_token', 'filter', 'order_by', 'view', ),
        'list_feedback_labels': ('parent', 'filter', 'page_size', 'page_token', ),
        'list_issue_models': ('parent', ),
        'list_issues': ('parent', ),
        'list_phrase_matchers': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_qa_questions': ('parent', 'page_size', 'page_token', ),
        'list_qa_scorecard_revisions': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_qa_scorecards': ('parent', 'page_size', 'page_token', ),
        'list_views': ('parent', 'page_size', 'page_token', ),
        'query_metrics': ('location', 'filter', 'time_granularity', 'dimensions', 'measure_mask', ),
        'tune_qa_scorecard_revision': ('parent', 'filter', 'validate_only', ),
        'undeploy_issue_model': ('name', ),
        'undeploy_qa_scorecard_revision': ('name', ),
        'update_analysis_rule': ('analysis_rule', 'update_mask', ),
        'update_conversation': ('conversation', 'update_mask', ),
        'update_feedback_label': ('feedback_label', 'update_mask', ),
        'update_issue': ('issue', 'update_mask', ),
        'update_issue_model': ('issue_model', 'update_mask', ),
        'update_phrase_matcher': ('phrase_matcher', 'update_mask', ),
        'update_qa_question': ('qa_question', 'update_mask', ),
        'update_qa_scorecard': ('qa_scorecard', 'update_mask', ),
        'update_settings': ('settings', 'update_mask', ),
        'update_view': ('view', 'update_mask', ),
        'upload_conversation': ('parent', 'conversation', 'conversation_id', 'redaction_config', 'speech_config', ),
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
    transformer=contact_center_insightsCallTransformer(),
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
        description="""Fix up source that uses the contact_center_insights client library.

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
