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


class translateCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'adaptive_mt_translate': ('parent', 'dataset', 'content', 'reference_sentence_config', 'glossary_config', ),
        'batch_translate_document': ('parent', 'source_language_code', 'target_language_codes', 'input_configs', 'output_config', 'models', 'glossaries', 'format_conversions', 'customized_attribution', 'enable_shadow_removal_native_pdf', 'enable_rotation_correction', ),
        'batch_translate_text': ('parent', 'source_language_code', 'target_language_codes', 'input_configs', 'output_config', 'models', 'glossaries', 'labels', ),
        'create_adaptive_mt_dataset': ('parent', 'adaptive_mt_dataset', ),
        'create_dataset': ('parent', 'dataset', ),
        'create_glossary': ('parent', 'glossary', ),
        'create_glossary_entry': ('parent', 'glossary_entry', ),
        'create_model': ('parent', 'model', ),
        'delete_adaptive_mt_dataset': ('name', ),
        'delete_adaptive_mt_file': ('name', ),
        'delete_dataset': ('name', ),
        'delete_glossary': ('name', ),
        'delete_glossary_entry': ('name', ),
        'delete_model': ('name', ),
        'detect_language': ('parent', 'model', 'content', 'mime_type', 'labels', ),
        'export_data': ('dataset', 'output_config', ),
        'get_adaptive_mt_dataset': ('name', ),
        'get_adaptive_mt_file': ('name', ),
        'get_dataset': ('name', ),
        'get_glossary': ('name', ),
        'get_glossary_entry': ('name', ),
        'get_model': ('name', ),
        'get_supported_languages': ('parent', 'display_language_code', 'model', ),
        'import_adaptive_mt_file': ('parent', 'file_input_source', 'gcs_input_source', ),
        'import_data': ('dataset', 'input_config', ),
        'list_adaptive_mt_datasets': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_adaptive_mt_files': ('parent', 'page_size', 'page_token', ),
        'list_adaptive_mt_sentences': ('parent', 'page_size', 'page_token', ),
        'list_datasets': ('parent', 'page_size', 'page_token', ),
        'list_examples': ('parent', 'filter', 'page_size', 'page_token', ),
        'list_glossaries': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_glossary_entries': ('parent', 'page_size', 'page_token', ),
        'list_models': ('parent', 'filter', 'page_size', 'page_token', ),
        'romanize_text': ('parent', 'contents', 'source_language_code', ),
        'translate_document': ('parent', 'target_language_code', 'document_input_config', 'source_language_code', 'document_output_config', 'model', 'glossary_config', 'labels', 'customized_attribution', 'is_translate_native_pdf_only', 'enable_shadow_removal_native_pdf', 'enable_rotation_correction', ),
        'translate_text': ('contents', 'target_language_code', 'parent', 'mime_type', 'source_language_code', 'model', 'glossary_config', 'transliteration_config', 'labels', ),
        'update_glossary': ('glossary', 'update_mask', ),
        'update_glossary_entry': ('glossary_entry', ),
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
    transformer=translateCallTransformer(),
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
        description="""Fix up source that uses the translate client library.

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
