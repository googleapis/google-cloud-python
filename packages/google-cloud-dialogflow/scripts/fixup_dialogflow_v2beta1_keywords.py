#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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


class dialogflowCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
          'analyze_content': ('participant', 'text_input', 'event_input', 'reply_audio_config', 'query_params', 'message_send_time', 'request_id', ),
          'batch_create_entities': ('parent', 'entities', 'language_code', ),
          'batch_create_messages': ('parent', 'requests', ),
          'batch_delete_entities': ('parent', 'entity_values', 'language_code', ),
          'batch_delete_entity_types': ('parent', 'entity_type_names', ),
          'batch_delete_intents': ('parent', 'intents', ),
          'batch_update_entities': ('parent', 'entities', 'language_code', 'update_mask', ),
          'batch_update_entity_types': ('parent', 'entity_type_batch_uri', 'entity_type_batch_inline', 'language_code', 'update_mask', ),
          'batch_update_intents': ('parent', 'intent_batch_uri', 'intent_batch_inline', 'language_code', 'update_mask', 'intent_view', ),
          'compile_suggestion': ('parent', 'latest_message', 'context_size', ),
          'complete_conversation': ('name', ),
          'create_context': ('parent', 'context', ),
          'create_conversation': ('parent', 'conversation', 'conversation_id', ),
          'create_conversation_profile': ('parent', 'conversation_profile', ),
          'create_document': ('parent', 'document', 'import_gcs_custom_metadata', ),
          'create_entity_type': ('parent', 'entity_type', 'language_code', ),
          'create_environment': ('parent', 'environment', 'environment_id', ),
          'create_intent': ('parent', 'intent', 'language_code', 'intent_view', ),
          'create_knowledge_base': ('parent', 'knowledge_base', ),
          'create_participant': ('parent', 'participant', ),
          'create_session_entity_type': ('parent', 'session_entity_type', ),
          'create_version': ('parent', 'version', ),
          'delete_agent': ('parent', ),
          'delete_all_contexts': ('parent', ),
          'delete_context': ('name', ),
          'delete_conversation_profile': ('name', ),
          'delete_document': ('name', ),
          'delete_entity_type': ('name', ),
          'delete_environment': ('name', ),
          'delete_intent': ('name', ),
          'delete_knowledge_base': ('name', 'force', ),
          'delete_session_entity_type': ('name', ),
          'delete_version': ('name', ),
          'detect_intent': ('session', 'query_input', 'query_params', 'output_audio_config', 'output_audio_config_mask', 'input_audio', ),
          'export_agent': ('parent', 'agent_uri', ),
          'get_agent': ('parent', ),
          'get_answer_record': ('name', ),
          'get_context': ('name', ),
          'get_conversation': ('name', ),
          'get_conversation_profile': ('name', ),
          'get_document': ('name', ),
          'get_entity_type': ('name', 'language_code', ),
          'get_environment': ('name', ),
          'get_environment_history': ('parent', 'page_size', 'page_token', ),
          'get_fulfillment': ('name', ),
          'get_intent': ('name', 'language_code', 'intent_view', ),
          'get_knowledge_base': ('name', ),
          'get_participant': ('name', ),
          'get_session_entity_type': ('name', ),
          'get_validation_result': ('parent', 'language_code', ),
          'get_version': ('name', ),
          'import_agent': ('parent', 'agent_uri', 'agent_content', ),
          'import_documents': ('parent', 'document_template', 'gcs_source', 'import_gcs_custom_metadata', ),
          'list_answer_records': ('parent', 'page_size', 'page_token', ),
          'list_contexts': ('parent', 'page_size', 'page_token', ),
          'list_conversation_profiles': ('parent', 'page_size', 'page_token', ),
          'list_conversations': ('parent', 'page_size', 'page_token', 'filter', ),
          'list_documents': ('parent', 'page_size', 'page_token', 'filter', ),
          'list_entity_types': ('parent', 'language_code', 'page_size', 'page_token', ),
          'list_environments': ('parent', 'page_size', 'page_token', ),
          'list_intents': ('parent', 'language_code', 'intent_view', 'page_size', 'page_token', ),
          'list_knowledge_bases': ('parent', 'page_size', 'page_token', 'filter', ),
          'list_messages': ('parent', 'filter', 'page_size', 'page_token', ),
          'list_participants': ('parent', 'page_size', 'page_token', ),
          'list_session_entity_types': ('parent', 'page_size', 'page_token', ),
          'list_suggestions': ('parent', 'page_size', 'page_token', 'filter', ),
          'list_versions': ('parent', 'page_size', 'page_token', ),
          'reload_document': ('name', 'gcs_source', 'import_gcs_custom_metadata', ),
          'restore_agent': ('parent', 'agent_uri', 'agent_content', ),
          'search_agents': ('parent', 'page_size', 'page_token', ),
          'set_agent': ('agent', 'update_mask', ),
          'streaming_detect_intent': ('session', 'query_input', 'query_params', 'single_utterance', 'output_audio_config', 'output_audio_config_mask', 'input_audio', ),
          'suggest_articles': ('parent', 'latest_message', 'context_size', ),
          'suggest_faq_answers': ('parent', 'latest_message', 'context_size', ),
          'suggest_smart_replies': ('parent', 'current_text_input', 'latest_message', 'context_size', ),
          'train_agent': ('parent', ),
          'update_answer_record': ('answer_record', 'update_mask', ),
          'update_context': ('context', 'update_mask', ),
          'update_conversation_profile': ('conversation_profile', 'update_mask', ),
          'update_document': ('document', 'update_mask', ),
          'update_entity_type': ('entity_type', 'language_code', 'update_mask', ),
          'update_environment': ('environment', 'update_mask', 'allow_load_to_draft_and_discard_changes', ),
          'update_fulfillment': ('fulfillment', 'update_mask', ),
          'update_intent': ('intent', 'language_code', 'update_mask', 'intent_view', ),
          'update_knowledge_base': ('knowledge_base', 'update_mask', ),
          'update_participant': ('participant', 'update_mask', ),
          'update_session_entity_type': ('session_entity_type', 'update_mask', ),
          'update_version': ('version', 'update_mask', ),
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
            lambda a: not a.keyword.value in self.CTRL_PARAMS,
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
    transformer=dialogflowCallTransformer(),
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
        description="""Fix up source that uses the dialogflow client library.

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
