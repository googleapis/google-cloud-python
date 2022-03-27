#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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


class dialogflowcxCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'batch_delete_test_cases': ('parent', 'names', ),
        'batch_run_test_cases': ('parent', 'test_cases', 'environment', ),
        'calculate_coverage': ('agent', 'type_', ),
        'compare_versions': ('base_version', 'target_version', 'language_code', ),
        'create_agent': ('parent', 'agent', ),
        'create_entity_type': ('parent', 'entity_type', 'language_code', ),
        'create_environment': ('parent', 'environment', ),
        'create_experiment': ('parent', 'experiment', ),
        'create_flow': ('parent', 'flow', 'language_code', ),
        'create_intent': ('parent', 'intent', 'language_code', ),
        'create_page': ('parent', 'page', 'language_code', ),
        'create_security_settings': ('parent', 'security_settings', ),
        'create_session_entity_type': ('parent', 'session_entity_type', ),
        'create_test_case': ('parent', 'test_case', ),
        'create_transition_route_group': ('parent', 'transition_route_group', 'language_code', ),
        'create_version': ('parent', 'version', ),
        'create_webhook': ('parent', 'webhook', ),
        'delete_agent': ('name', ),
        'delete_entity_type': ('name', 'force', ),
        'delete_environment': ('name', ),
        'delete_experiment': ('name', ),
        'delete_flow': ('name', 'force', ),
        'delete_intent': ('name', ),
        'delete_page': ('name', 'force', ),
        'delete_security_settings': ('name', ),
        'delete_session_entity_type': ('name', ),
        'delete_transition_route_group': ('name', 'force', ),
        'delete_version': ('name', ),
        'delete_webhook': ('name', 'force', ),
        'deploy_flow': ('environment', 'flow_version', ),
        'detect_intent': ('session', 'query_input', 'query_params', 'output_audio_config', ),
        'export_agent': ('name', 'agent_uri', 'data_format', 'environment', ),
        'export_flow': ('name', 'flow_uri', 'include_referenced_flows', ),
        'export_test_cases': ('parent', 'gcs_uri', 'data_format', 'filter', ),
        'fulfill_intent': ('match_intent_request', 'match', 'output_audio_config', ),
        'get_agent': ('name', ),
        'get_agent_validation_result': ('name', 'language_code', ),
        'get_changelog': ('name', ),
        'get_deployment': ('name', ),
        'get_entity_type': ('name', 'language_code', ),
        'get_environment': ('name', ),
        'get_experiment': ('name', ),
        'get_flow': ('name', 'language_code', ),
        'get_flow_validation_result': ('name', 'language_code', ),
        'get_intent': ('name', 'language_code', ),
        'get_page': ('name', 'language_code', ),
        'get_security_settings': ('name', ),
        'get_session_entity_type': ('name', ),
        'get_test_case': ('name', ),
        'get_test_case_result': ('name', ),
        'get_transition_route_group': ('name', 'language_code', ),
        'get_version': ('name', ),
        'get_webhook': ('name', ),
        'import_flow': ('parent', 'flow_uri', 'flow_content', 'import_option', ),
        'import_test_cases': ('parent', 'gcs_uri', 'content', ),
        'list_agents': ('parent', 'page_size', 'page_token', ),
        'list_changelogs': ('parent', 'filter', 'page_size', 'page_token', ),
        'list_continuous_test_results': ('parent', 'page_size', 'page_token', ),
        'list_deployments': ('parent', 'page_size', 'page_token', ),
        'list_entity_types': ('parent', 'language_code', 'page_size', 'page_token', ),
        'list_environments': ('parent', 'page_size', 'page_token', ),
        'list_experiments': ('parent', 'page_size', 'page_token', ),
        'list_flows': ('parent', 'page_size', 'page_token', 'language_code', ),
        'list_intents': ('parent', 'language_code', 'intent_view', 'page_size', 'page_token', ),
        'list_pages': ('parent', 'language_code', 'page_size', 'page_token', ),
        'list_security_settings': ('parent', 'page_size', 'page_token', ),
        'list_session_entity_types': ('parent', 'page_size', 'page_token', ),
        'list_test_case_results': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_test_cases': ('parent', 'page_size', 'page_token', 'view', ),
        'list_transition_route_groups': ('parent', 'page_size', 'page_token', 'language_code', ),
        'list_versions': ('parent', 'page_size', 'page_token', ),
        'list_webhooks': ('parent', 'page_size', 'page_token', ),
        'load_version': ('name', 'allow_override_agent_resources', ),
        'lookup_environment_history': ('name', 'page_size', 'page_token', ),
        'match_intent': ('session', 'query_input', 'query_params', ),
        'restore_agent': ('name', 'agent_uri', 'agent_content', 'restore_option', ),
        'run_continuous_test': ('environment', ),
        'run_test_case': ('name', 'environment', ),
        'start_experiment': ('name', ),
        'stop_experiment': ('name', ),
        'streaming_detect_intent': ('query_input', 'session', 'query_params', 'output_audio_config', 'enable_partial_response', ),
        'train_flow': ('name', ),
        'update_agent': ('agent', 'update_mask', ),
        'update_entity_type': ('entity_type', 'language_code', 'update_mask', ),
        'update_environment': ('environment', 'update_mask', ),
        'update_experiment': ('experiment', 'update_mask', ),
        'update_flow': ('flow', 'update_mask', 'language_code', ),
        'update_intent': ('intent', 'language_code', 'update_mask', ),
        'update_page': ('page', 'language_code', 'update_mask', ),
        'update_security_settings': ('security_settings', 'update_mask', ),
        'update_session_entity_type': ('session_entity_type', 'update_mask', ),
        'update_test_case': ('test_case', 'update_mask', ),
        'update_transition_route_group': ('transition_route_group', 'update_mask', 'language_code', ),
        'update_version': ('version', 'update_mask', ),
        'update_webhook': ('webhook', 'update_mask', ),
        'validate_agent': ('name', 'language_code', ),
        'validate_flow': ('name', 'language_code', ),
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
    transformer=dialogflowcxCallTransformer(),
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
        description="""Fix up source that uses the dialogflowcx client library.

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
