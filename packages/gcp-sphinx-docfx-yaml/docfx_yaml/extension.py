# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""
Sphinx DocFX YAML Top-level Extension.

This extension allows you to automagically generate DocFX YAML from your Python AutoAPI docs.
"""
import os
import inspect
import re
import copy
import shutil
import black
import logging

from pathlib import Path
from functools import partial
from itertools import zip_longest
from typing import Dict, Iterable, List, Optional
from black import InvalidInput

try:
    from subprocess import getoutput
except ImportError:
    from commands import getoutput

from yaml import safe_dump as dump

from sphinx.util.console import darkgreen, bold
from sphinx.util import ensuredir
from sphinx.errors import ExtensionError
from sphinx.util.nodes import make_refnode
from sphinxcontrib.napoleon.docstring import GoogleDocstring
from sphinxcontrib.napoleon import Config, _process_docstring

from .utils import transform_node, transform_string
from .settings import API_ROOT
from .monkeypatch import patch_docfields
from .directives import RemarksDirective, TodoDirective
from .nodes import remarks

import subprocess
import ast
from docuploader import shell

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


try:
    from conf import *
except ImportError:
    print(Bcolors.FAIL + 'can not import conf.py! '
    'you should have a conf.py in working project folder' + Bcolors.ENDC)

METHOD = 'method'
FUNCTION = 'function'
MODULE = 'module'
CLASS = 'class'
EXCEPTION = 'exception'
ATTRIBUTE = 'attribute'
REFMETHOD = 'meth'
REFFUNCTION = 'func'
INITPY = '__init__.py'
# Regex expression for checking references of pattern like ":class:`~package_v1.module`"
REF_PATTERN = ':(py:)?(func|class|meth|mod|ref|attr|exc):`~?[a-zA-Z0-9_\.<> ]*(\(\))?`'
# Regex expression for checking references of pattern like "~package_v1.subpackage.module"
REF_PATTERN_LAST = '~([a-zA-Z0-9_<>]*\.)*[a-zA-Z0-9_<>]*(\(\))?'
# Regex expression for checking references of pattern like
# "[module][google.cloud.cloudkms_v1.module]"
REF_PATTERN_BRACKETS = '\[[a-zA-Z0-9\_\<\>\-\. ]+\]\[[a-zA-Z0-9\_\<\>\-\. ]+\]'

REF_PATTERNS = [
    REF_PATTERN,
    REF_PATTERN_LAST,
    REF_PATTERN_BRACKETS,
]

PROPERTY = 'property'
CODEBLOCK = "code-block"
CODE = "code"
PACKAGE = "package"

# Disable blib2to3 output that clutters debugging log.
logging.getLogger("blib2to3").setLevel(logging.ERROR)

# Run sphinx-build with Markdown builder in the plugin.
def run_sphinx_markdown():
    cwd = os.getcwd()
    # Skip running sphinx-build for Markdown for some unit tests.
    # Not required other than to output DocFX YAML.
    if "docs" in cwd:
        return

    return shell.run(
        [
            "sphinx-build",
            "-M",
            "markdown",
            "docs/",
            "docs/_build",
        ],
        hide_output=False
    )


def build_init(app):
    print("Running sphinx-build with Markdown first...")
    run_sphinx_markdown()
    print("Completed running sphinx-build with Markdown files.")

    """
    Set up environment data
    """
    if not app.config.docfx_yaml_output:
        raise ExtensionError('You must configure an docfx_yaml_output setting')

    # This stores YAML object for modules
    app.env.docfx_yaml_modules = {}
    # This stores YAML object for classes
    app.env.docfx_yaml_classes = {}
    # This stores YAML object for functions
    app.env.docfx_yaml_functions = {}
    # This store the data extracted from the info fields
    app.env.docfx_info_field_data = {}
    # This stores signature for functions and methods
    app.env.docfx_signature_funcs_methods = {}
    # This store the uid-type mapping info
    app.env.docfx_info_uid_types = {}
    # This stores uidnames of docstrings already parsed
    app.env.docfx_uid_names = {}
    # This stores file path for class when inspect cannot retrieve file path
    app.env.docfx_class_paths = {}
    # This stores the name and href of the markdown pages.
    app.env.markdown_pages = []

    app.env.docfx_xrefs = {}

    remote = getoutput('git remote -v')

    try:
        app.env.docfx_remote = remote.split('\t')[1].split(' ')[0]
    except Exception:
        app.env.docfx_remote = None
    try:
        app.env.docfx_branch = getoutput('git rev-parse --abbrev-ref HEAD').strip()
    except Exception:
        app.env.docfx_branch = None

    try:
        app.env.docfx_root = getoutput('git rev-parse --show-toplevel').strip()
    except Exception:
        app.env.docfx_root = None

    patch_docfields(app)

    app.docfx_transform_node = partial(transform_node, app)
    app.docfx_transform_string = partial(transform_string, app)


def _get_cls_module(_type, name):
    """
    Get the class and module name for an object

    .. _sending:

    Foo

    """

    cls = None
    if _type in [FUNCTION, EXCEPTION]:
        module = '.'.join(name.split('.')[:-1])
    elif _type in [METHOD, ATTRIBUTE, PROPERTY]:
        cls = '.'.join(name.split('.')[:-1])
        module = '.'.join(name.split('.')[:-2])
    elif _type in [CLASS]:
        cls = name
        module = '.'.join(name.split('.')[:-1])
    elif _type in [MODULE]:
        module = name
    else:
        return (None, None)
    return (cls, module)


def _create_reference(datam, parent, is_external=False):
    return {
        'uid': datam['uid'],
        'parent': parent,
        'isExternal': is_external,
        'name': datam['source']['id'],
        'fullName': datam['fullName'],
    }


def _refact_example_in_module_summary(lines):
    new_lines = []
    block_lines = []
    example_block_flag = False
    for line in lines:
        if line.startswith('.. admonition:: Example'):
            example_block_flag = True
            line = '### Example\n\n'
            new_lines.append(line)
        elif example_block_flag and len(line) != 0 and not line.startswith('   '):
            example_block_flag = False
            new_lines.append(''.join(block_lines))
            new_lines.append(line)
            block_lines[:] = []
        elif example_block_flag:
            if line == '   ':  # origianl line is blank line ('\n').
                line = '\n'  # after outer ['\n'.join] operation,
                             # this '\n' will be appended to previous line then. BINGO!
            elif line.startswith('   '):
                # will be indented by 4 spaces according to yml block syntax.
                # https://learnxinyminutes.com/docs/yaml/
                line = ' ' + line + '\n'
            block_lines.append(line)

        else:
            new_lines.append(line)
    return new_lines


def _resolve_reference_in_module_summary(pattern, lines):
    new_lines, xrefs = [], []
    for line in lines:
        matched_objs = list(re.finditer(pattern, line))
        new_line = line
        for matched_obj in matched_objs:
            start = matched_obj.start()
            end = matched_obj.end()
            matched_str = line[start:end]
            # TODO: separate this portion into a function per pattern.
            if pattern == REF_PATTERN:
                if '<' in matched_str and '>' in matched_str:
                    # match string like ':func:`***<***>`'
                    index = matched_str.index('<')
                    ref_name = matched_str[index+1:-2]
                else:
                    # match string like ':func:`~***`' or ':func:`***`'
                    index = matched_str.index('~') if '~' in matched_str else matched_str.index('`')
                    ref_name = matched_str[index+1:-1]

                index = ref_name.rfind('.') + 1
                # Find the last component of the target. "~Queue.get" only returns <xref:get>
                ref_name = ref_name[index:]

            elif pattern == REF_PATTERN_LAST:
                index = matched_str.rfind('.') + 1
                if index == 0:
                    # If there is no dot, push index to not include tilde
                    index = 1
                ref_name = matched_str[index:]

            elif pattern == REF_PATTERN_BRACKETS:
                lbracket = matched_str.find('[')+1
                rbracket = matched_str.find(']')
                ref_name = matched_str[lbracket:rbracket]

            else:
                raise ValueError(f'Encountered wrong ref pattern: \n{pattern}')

            # Find the uid to add for xref
            index = matched_str.find("google.cloud")
            if index > -1:
                xref = matched_str[index:]
                while not xref[-1].isalnum():
                    xref = xref[:-1]
                xrefs.append(xref)

            # Check to see if we should create an xref for it.
            if 'google.cloud' in matched_str:
                new_line = new_line.replace(matched_str, '<xref uid=\"{}\">{}</xref>'.format(xref, ref_name))
            # If it not a Cloud library, don't create xref for it.
            else:
                # Carefully extract the original uid
                if pattern == REF_PATTERN:
                    index = matched_str.index('~') if '~' in matched_str else matched_str.index('`')
                    ref_name = matched_str[index+1:-1]
                else:
                    ref_name = matched_str[1:]
                new_line = new_line.replace(matched_str, '`{}`'.format(ref_name))

        new_lines.append(new_line)
    return new_lines, xrefs


def enumerate_extract_signature(doc, max_args=20):
    el = "((?P<p%d>[*a-zA-Z_]+) *(?P<a%d>: *[a-zA-Z_.]+)? *(?P<d%d>= *[^ ]+?)?)"
    els = [el % (i, i, i) for i in range(0, max_args)]
    par = els[0] + "?" + "".join(["( *, *" + e + ")?" for e in els[1:]])
    exp = "(?P<name>[a-zA-Z_]+) *[(] *(?P<sig>{0}) *[)]".format(par)
    reg = re.compile(exp)
    for func in reg.finditer(doc.replace("\n", " ")):
        yield func


def enumerate_cleaned_signature(doc, max_args=20):
    for sig in enumerate_extract_signature(doc, max_args=max_args):
        dic = sig.groupdict()
        name = sig["name"]
        args = []
        for i in range(0, max_args):
            p = dic.get('p%d' % i, None)
            if p is None:
                break
            d = dic.get('d%d' % i, None)
            if d is None:
                args.append(p)
            else:
                args.append("%s%s" % (p, d))
        yield "{0}({1})".format(name, ", ".join(args))


def _extract_signature(obj_sig):
    try:    
        signature = inspect.signature(obj_sig)
        parameters = signature.parameters
    except TypeError as e:
        mes = "[docfx] unable to get signature of '{0}' - {1}.".format(
            object_name, str(e).replace("\n", "\\n"))
        signature = None
        parameters = None
    except ValueError as e:
        # Backup plan, no __text_signature__, this happen
        # when a function was created with pybind11.
        doc = obj_sig.__doc__
        sigs = set(enumerate_cleaned_signature(doc))
        if len(sigs) == 0:
            mes = "[docfx] unable to get signature of '{0}' - {1}.".format(
                object_name, str(e).replace("\n", "\\n"))
            signature = None
            parameters = None
        elif len(sigs) > 1:
            mes = "[docfx] too many signatures for '{0}' - {1} - {2}.".format(
                object_name, str(e).replace("\n", "\\n"), " *** ".join(sigs))
            signature = None
            parameters = None
        else:
            try:
                signature = inspect._signature_fromstr(
                    inspect.Signature, obj_sig, list(sigs)[0])
                parameters = signature.parameters
            except TypeError as e:
                mes = "[docfx] unable to get signature of '{0}' - {1}.".format(
                    object_name, str(e).replace("\n", "\\n"))
                signature = None
                parameters = None    
    return signature, parameters


# Given a line containing restructured keyword, returns which keyword it is.
def extract_keyword(line):
    # Must be in the form of:
    #   .. keyword::
    # where it begind with 2 dot prefix, followed by a space, then the keyword
    # followed by 2 collon suffix.
    try:
        return line[ 3 : line.index("::") ]
    except ValueError:
        # TODO: handle reST template.
        if line[3] != "_":
            raise ValueError(f"Wrong formatting enoucntered for \n{line}")
        return line


def indent_code_left(lines, tab_space):
    """Indents code lines left by tab_space.

    Args:
        lines: String lines of code.
        tab_space: Number of spaces to indent to left by.

    Returns:
        String lines of left-indented code.
    """
    parts = lines.split("\n")
    parts = [part[tab_space:] for part in parts]
    return "\n".join(parts)


def _parse_docstring_summary(summary):
    summary_parts = []
    attributes = []
    attribute_type_token = ":type:"
    keyword = name = description = var_type = ""

    # We need to separate in chunks, which is defined by 3 newline breaks.
    # Otherwise when parsing for code and blocks of stuff, we will not be able
    # to have the entire context when just splitting by single newlines.
    # We should fix this from the library side for consistent docstring style,
    # rather than monkey-patching it in the plugin.
    for part in summary.split("\n\n\n"):
        # Don't process empty string
        if part == "":
            continue

        # Continue adding parts for code-block.
        if keyword and keyword in [CODE, CODEBLOCK]:
            # If we reach the end of keyword, close up the code block.
            if not part.startswith(" "*tab_space) or part.startswith(".."):
                if code_snippet:
                    parts = [indent_code_left(part, tab_space) for part in code_snippet]
                    summary_parts.append("\n\n".join(parts))
                summary_parts.append("```\n")
                keyword = ""

            else:
                if tab_space == -1:
                    parts = [split_part for split_part in part.split("\n") if split_part]
                    tab_space = len(parts[0]) - len(parts[0].lstrip(" "))
                    if tab_space == 0:
                        raise ValueError(f"Code in the code block should be indented. Please check the docstring: \n{summary}")
                if not part.startswith(" "*tab_space):
                    # No longer looking at code-block, reset keyword.
                    if code_snippet:
                        parts = [indent_code_left(part, tab_space) for part in code_snippet]
                        summary_parts.append("\n\n".join(parts))
                    keyword = ""
                    summary_parts.append("```\n")
                code_snippet.append(part)
                continue

        # Attributes come in 3 parts, parse the latter two here.
        elif keyword and keyword == ATTRIBUTE:
            # Second part, extract the description.
            if not found_name:
                description = part.strip()
                found_name = True
                continue
            # Third part, extract the attribute type then add the completed one
            # set to a list to be returned. Close up as needed.
            else:
                if attribute_type_token in part:
                    var_type = part.split(":type:")[1].strip()
                keyword = ""
                if name and description and var_type:
                    attributes.append({
                        "id": name,
                        "description": description,
                        "var_type": var_type
                    })

                else:
                    print(f"Could not process the attribute. Please check the docstring: \n{summary}")

                continue

        # Parse keywords if found.
        # lstrip is added to parse code blocks that are not formatted well.
        if part.lstrip('\n').startswith('..'):
            try:
                keyword = extract_keyword(part.lstrip('\n'))
            except ValueError:
                raise ValueError(f"Please check the docstring: \n{summary}")
            # Works for both code-block and code
            if keyword and keyword in [CODE, CODEBLOCK]:
                # Retrieve the language found in the format of
                #   .. code-block:: lang
                # {lang} is optional however.
                language = part.split("::")[1].strip()
                summary_parts.append(f"```{language}")

                code_snippet = []
                tab_space = -1

            # Extract the name for attribute first.
            elif keyword and keyword == ATTRIBUTE:
                found_name = False
                name = part.split("::")[1].strip()

            # Reserve for additional parts
            # elif keyword == keyword:
            else:
                summary_parts.append(part + "\n")

        else:
            summary_parts.append(part + "\n")

    # Close up from the keyword if needed.
    if keyword and keyword in [CODE, CODEBLOCK]:
        # Check if it's already closed.
        if code_snippet:
            parts = [indent_code_left(part, tab_space) for part in code_snippet]
            summary_parts.append("\n\n".join(parts))
        if summary_parts[-1] != "```\n":
            summary_parts.append("```\n")

    # Requires 2 newline chars to properly show on cloud site.
    return "\n".join(summary_parts), attributes


# Given documentation docstring, parse them into summary_info.
def _extract_docstring_info(summary_info, summary, name):
    top_summary = ""
    # Return clean summary if returning early.
    parsed_text = summary

    # Initialize known types needing further processing.
    var_types = {
        ':rtype:': 'returns',
        ':returns:': 'returns',
        ':type': 'variables',
        ':param': 'variables',
        ':raises': 'exceptions',
        ':raises:': 'exceptions'
    }
    
    initial_index = -1
    front_tag = '<xref'
    end_tag = '/xref>'
    end_len = len(end_tag)
        
    # Prevent GoogleDocstring crashing on custom types and parse all xrefs to normal
    if front_tag in parsed_text:
        type_pairs = []
        # Constant length for end of xref tag
        initial_index = max(0, parsed_text.find(front_tag))

        summary_part = parsed_text[initial_index:]
       
        # Remove all occurrences of "<xref uid="uid">text</xref>"
        while front_tag in summary_part:

            # Expecting format of "<xref uid="uid">text</xref>"
            if front_tag in summary_part:
                # Retrieve the index for starting position of xref tag
                initial_index += summary_part.find(front_tag)

                # Find the index of the end of xref tag, relative to the start of xref tag
                end_tag_index = initial_index + parsed_text[initial_index:].find(end_tag) + end_len

                # Retrieve the entire xref tag
                original_type = parsed_text[initial_index:end_tag_index]
                initial_index += len(original_type)
                original_type = " ".join(filter(None, re.split(r'\n|  |\|\s|\t', original_type)))

                # Extract text from "<xref uid="uid">text</xref>"
                index = original_type.find(">")
                safe_type = 'xref_' + original_type[index+1:index+(original_type[index:].find("<"))]
            else:
                raise ValueError("Encountered unexpected type in Exception docstring.")

            type_pairs.append([original_type, safe_type])
            summary_part = parsed_text[initial_index:]

        # Replace all the found occurrences
        for pairs in type_pairs:
            original_type, safe_type = pairs[0], pairs[1]
            parsed_text = parsed_text.replace(original_type, safe_type)
        
    # Clean the string by cleaning newlines and backlashes, then split by white space.
    config = Config(napoleon_use_param=True, napoleon_use_rtype=True)
    # Convert Google style to reStructuredText
    parsed_text = str(GoogleDocstring(parsed_text, config))
    
    # Trim the top summary but maintain its formatting.
    indexes = []
    for types in var_types:
        # Ensure that we look for exactly the string we want.
        # Adding the extra space for non-colon ending types
        # helps determine if we simply ran into desired occurrence
        # or if we ran into a similar looking syntax but shouldn't
        # parse upon it.
        types += ' ' if types[-1] != ':' else ''
        if types in parsed_text:
            index = parsed_text.find(types)
            if index > -1:
                # For now, skip on parsing custom fields like attribute
                if types == ':type ' and 'attribute::' in parsed_text:
                    continue
                indexes.append(index)

    # If we found types needing further processing, locate its index,
    # if we found empty array for indexes, stop processing further.
    index = min(indexes) if indexes else 0

    # Store the top summary separately. Ensure that the docstring is not empty.
    if index == 0 and not indexes:
        return summary

    top_summary = parsed_text[:index]
    parsed_text = parsed_text[index:]

    # Revert back to original type
    if initial_index > -1:
        for pairs in type_pairs:
            original_type, safe_type = pairs[0], pairs[1]
            parsed_text = parsed_text.replace(safe_type, original_type)

    # Clean up whitespace and other characters
    parsed_text = " ".join(filter(None, re.split(r'\|\s', parsed_text))).split()

    cur_type = ''
    words = []
    arg_name = ''
    index = 0
    # Used to track return type and description
    r_type, r_descr = '', ''

    # Using counter iteration to easily extract names rather than
    # coming up with more complicated stopping logic for each tags.
    while index <= len(parsed_text):
        word = parsed_text[index] if index < len(parsed_text) else ""
        # Check if we encountered specific words.
        if word in var_types or index == len(parsed_text):               
            # Finish processing previous section.
            if cur_type:
                if cur_type == ':type':
                    summary_info[var_types[cur_type]][arg_name]['var_type'] = " ".join(words)
                elif cur_type == ':param':
                    summary_info[var_types[cur_type]][arg_name]['description'] = " ".join(words)
                elif ":raises" in cur_type:
                    summary_info[var_types[cur_type]].append({
                        'var_type': arg_name,
                        'description': " ".join(words)
                    })
                else:
                    if cur_type == ':rtype:':
                        r_type = " ".join(words)
                    else:
                        r_descr = " ".join(words)
                    if r_type and r_descr:
                        summary_info[var_types[cur_type]].append({
                            'var_type': r_type,
                            'description': r_descr
                        })
                        r_type, r_descr = '', ''

            else:

                # If after we processed the top summary and get in this state,
                # likely we encountered a type that's not covered above or the docstring
                # was formatted badly. This will likely break docfx job later on, should not
                # process further.
                if word not in var_types:
                    raise ValueError(f"Encountered wrong formatting, please check docstring for {name}")
   
            # Reached end of string, break after finishing processing
            if index == len(parsed_text):
                break
    
            # Start processing for new section
            cur_type = word
            if cur_type in [':type', ':param', ':raises', ':raises:']:
                index += 1
                # Exception that's not xref should be treated same as other names
                if ':raises' not in cur_type or 'xref' not in parsed_text[index]:
                    arg_name = parsed_text[index][:-1]
                # xrefs are treated by taking its second half and combining the two
                elif ':raises' in cur_type and 'xref' in parsed_text[index]:
                    arg_name = f'{parsed_text[index]} {parsed_text[index+1][:-1]}'
                    index += 1

                try:
                    # Initialize empty dictionary if it doesn't exist already
                    if arg_name not in summary_info[var_types[cur_type]] and ':raises' not in cur_type:
                        summary_info[var_types[cur_type]][arg_name] = {}
                except KeyError:
                    raise KeyError(f"Encountered wrong formatting, please check docstring for {name}")

            # Empty target string
            words = []
        else:
            words.append(word)
    
        index += 1

    return top_summary


# Returns appropriate product name to display for given full name of entry.
def extract_product_name(name):
    if 'google.cloud' in name:
        product_name = '.'.join(name.split('.')[2:])
    elif 'google' in name:
        product_name = '.'.join(name.split('.')[1:])
    else:
        # Use the short name for other formats.
        product_name = name.split('.')[-1]

    return product_name


def _create_datam(app, cls, module, name, _type, obj, lines=None):
    """
    Build the data structure for an autodoc class
    """

    def _update_friendly_package_name(path):
        package_name_index = path.find(os.sep)
        package_name = path[:package_name_index]
        if len(package_name) > 0:
            try:
                for name in namespace_package_dict:
                    if re.match(name, package_name) is not None:
                        package_name = namespace_package_dict[name]
                        path = os.path.join(package_name, path[package_name_index + 1:])
                        return path

            except NameError:
                pass

        return path

    if lines is None:
        lines = []
    short_name = name.split(".")[-1]
    args = []
    # Check how many arguments are present in the function.
    arg_count = 0
    try:
        if _type in [METHOD, FUNCTION, CLASS]:
            argspec = inspect.getfullargspec(obj) # noqa
            type_map = {}
            if argspec.annotations:
                for annotation in argspec.annotations:
                    if annotation == "return":
                        continue
                    # Extract names for simple types.
                    try:
                        type_map[annotation] = (argspec.annotations[annotation]).__name__
                    # Try to extract names for more complicated types.
                    except AttributeError:
                        vartype = argspec.annotations[annotation]
                        try:
                            type_map[annotation] = str(vartype._name)
                            if vartype.__args__:
                                type_map[annotation] += str(vartype.__args__)[:-2] + ")"
                        except AttributeError:
                            print(f"Could not parse argument information for {annotation}.")
                            continue

            # Add up the number of arguments. `argspec.args` contains a list of
            # all the arguments from the function.
            arg_count += len(argspec.args)
            for arg in argspec.args:
                arg_map = {}
                # Ignore adding in entry for "self"
                if arg != 'cls':
                    arg_map['id'] = arg
                    if arg in type_map:
                        arg_map['var_type'] = type_map[arg]
                        args.append(arg_map)

            if argspec.varargs:
                args.append({'id': argspec.varargs})
            if argspec.varkw:
                args.append({'id': argspec.varkw})

            if argspec.defaults:
                # Attempt to add default values to arguments.
                try:
                    for count, default in enumerate(argspec.defaults):
                        # Find the first index which default arguments start at.
                        # Every argument after this offset_count all have default values.
                        offset_count = len(argspec.defaults)
                        # Find the index of the current default value argument
                        index = len(args) + count - offset_count

                        # Only add defaultValue when str(default) doesn't contain object address string(object at 0x)
                        # inspect.getargspec method will return wrong defaults which contain object address for some default values, like sys.stdout
                        if 'object at 0x' not in str(default):
                            args[index]['defaultValue'] = str(default)
                # If we cannot find the argument, it is missing a type and was taken out intentionally.
                except IndexError:
                    pass
            try:
                if len(lines) == 0:
                    lines = inspect.getdoc(obj)
                    lines = lines.split("\n") if lines else []
            except TypeError as e:
                print("couldn't getdoc from method, function: {}".format(e))
        elif _type in [PROPERTY]:
            lines = inspect.getdoc(obj)
            lines = lines.split("\n") if lines else []
    except TypeError as e:
        print("Can't get argspec for {}: {}. {}".format(type(obj), name, e))

    if name in app.env.docfx_signature_funcs_methods:
        sig = app.env.docfx_signature_funcs_methods[name]
    else:
        sig = None

    try:
        full_path = inspect.getsourcefile(obj)

        if full_path is None: # Meet a .pyd file
            raise TypeError()
        # Sub git repo path
        path = full_path.replace(app.env.docfx_root, '')
        # Support global file imports, if it's installed already
        import_path = os.path.dirname(inspect.getfile(os))
        path = path.replace(os.path.join(import_path, 'site-packages'), '')
        path = path.replace(import_path, '')

        # Make relative
        path = path.replace(os.sep, '', 1)
        start_line = inspect.getsourcelines(obj)[1]

        path = _update_friendly_package_name(path)

        # Get folder name from conf.py
        path = os.path.join(app.config.folder, path)
        app.env.docfx_class_paths[cls] = path

        # append relative path defined in conf.py (in case of "binding python" project)
        try:
            source_prefix  # does source_prefix exist in the current namespace
            path = source_prefix + path
            app.env.docfx_class_paths[cls] = path
        except NameError:
            pass

    except (TypeError, OSError):
        # TODO: remove this once there is full handler for property
        if _type in [PROPERTY]:
            print("Skip inspecting for property: {}".format(name))
        else:
            print("Can't inspect type {}: {}".format(type(obj), name))
        path = None
        start_line = None

    datam = {
        'module': module,
        'uid': name,
        'type': _type,
        'name': short_name,
        'fullName': name,
        'source': {
            'remote': {
                'path': path,
                'branch': app.env.docfx_branch,
                'repo': app.env.docfx_remote,
            },
            'id': short_name,
            'path': path,
            'startLine': start_line,
        },
        'langs': ['python'],
    }

    summary_info = {
        'variables': {},  # Stores mapping of variables and its description & types
        'returns': [],    # Stores the return info
        'exceptions': []  # Stores the exception info
    }

    # Add extracted summary
    if lines != []:
        for ref_pattern in REF_PATTERNS:
            lines, xrefs = _resolve_reference_in_module_summary(ref_pattern, lines)
            for xref in xrefs:
                if xref not in app.env.docfx_xrefs:
                    app.env.docfx_xrefs[xref] = ''

        summary = app.docfx_transform_string('\n'.join(_refact_example_in_module_summary(lines)))

        # Extract summary info into respective sections.
        if summary:
            top_summary = _extract_docstring_info(summary_info, summary, name)
            try:
                datam['summary'], datam['attributes'] = _parse_docstring_summary(top_summary)
            except ValueError:
                debug_line = []
                if path:
                    debug_line.append(f"In file {path}\n")
                debug_line.append(f"For module {module}, type {_type}:\n")
                debug_line.append(f"Failed to parse docstring on {name}.")
                raise ValueError("".join(debug_line))


    # If there is no summary, add a short snippet.
    else:
        product_name = extract_product_name(name)
        datam['summary'] = f"API documentation for `{product_name}` {_type}."

    if args or sig or summary_info:
        datam['syntax'] = {}

    # If there are well-formatted arguments or a lot of arguments we should look
    # into, loop through what we got from the docstring.
    if args or arg_count > 0:
        variables = summary_info['variables']
        arg_id = []
        incomplete_args = []
        for arg in args:
            arg_id.append(arg['id'])

            if arg['id'] in variables:
                # Retrieve argument info from extracted map of variable info
                arg_var = variables[arg['id']]
                arg['var_type'] = arg_var.get('var_type')
                arg['description'] = arg_var.get('description')

            # Only add arguments with type and description.
            if not (arg.get('var_type') and arg.get('description')):
                incomplete_args.append(arg)

        # Remove any arguments with missing type or description from the YAML.
        for incomplete_arg in incomplete_args:
            args.remove(incomplete_arg)

        # Add any variables we might have missed from extraction.
        for variable in variables:
            if variable not in arg_id:
                # Only include arguments with type and description.
                if variables[variable].get('var_type') and variables[variable].get('description'):
                    new_arg = {
                        "id": variable,
                        "var_type": variables[variable].get('var_type'),
                        "description": variables[variable].get('description')
                    }
                    args.append(new_arg)

        datam['syntax']['parameters'] = args

    if sig:
        datam['syntax']['content'] = sig

    if summary_info['returns']:
        datam['syntax']['returns'] = summary_info['returns']

    if summary_info['exceptions']:
        datam['syntax']['exceptions'] = summary_info['exceptions']

    if cls:
        datam[CLASS] = cls
    if _type in [CLASS, MODULE]:
        datam['children'] = []
        datam['references'] = []

    return datam


def _fullname(obj):
    """
    Get the fullname from a Python object
    """
    return obj.__module__ + "." + obj.__name__


def process_docstring(app, _type, name, obj, options, lines):
    """
    This function takes the docstring and indexes it into memory.
    """

    cls = ""
    module = ""

    # Check if we already processed this docstring.
    if name in app.env.docfx_uid_names:
        if _type != CLASS:
            return
        else:
            # If we run into the same docstring twice for a class it's a
            # constructor. Change the constructor type from CLASS to METHOD.
            cls, module = _get_cls_module(_type, name)
            _type = METHOD

    # Register current docstring to a set.
    app.env.docfx_uid_names[name] = ''

    # Use exception as class
    if _type == EXCEPTION:
        _type = CLASS

    if not cls and not module:
        cls, module = _get_cls_module(_type, name)

    if not module and _type != PROPERTY:
        print('Unknown Type: %s' % _type)
        return None

    datam = _create_datam(app, cls, module, name, _type, obj, lines)

    if _type == MODULE:
        if module not in app.env.docfx_yaml_modules:
            app.env.docfx_yaml_modules[module] = [datam]
        else:
            app.env.docfx_yaml_modules[module].append(datam)

    if _type == CLASS or _type == PROPERTY:
        if cls not in app.env.docfx_yaml_classes:
            app.env.docfx_yaml_classes[cls] = [datam]
        else:
            app.env.docfx_yaml_classes[cls].append(datam)

    if _type == FUNCTION and app.config.autodoc_functions:
        if datam['uid'] is None:
            raise ValueError("Issue with {0} (name={1})".format(datam, name))
        if cls is None:
            cls = name
        if cls is None:
            raise ValueError("cls is None for name='{1}' {0}".format(datam, name))
        if cls not in app.env.docfx_yaml_functions:
            app.env.docfx_yaml_functions[cls] = [datam]
        else:
            app.env.docfx_yaml_functions[cls].append(datam)

    insert_inheritance(app, _type, obj, datam)
    insert_children_on_module(app, _type, datam)
    insert_children_on_class(app, _type, datam)
    insert_children_on_function(app, _type, datam)

    app.env.docfx_info_uid_types[datam['uid']] = _type


# Uses black.format_str() to reformat code as if running black/linter
# for better presnetation.
def format_code(code):
    # Signature code comes in raw text without formatting, to run black it
    # requires the code to look like actual function declaration in code.
    # Returns the original formatted code without the added bits.
    return black.format_str("def " + code + ": pass", mode=black.FileMode())[4:-11]


def process_signature(app, _type, name, obj, options, signature, return_annotation):
    if signature:
        short_name = name.split('.')[-1]
        signature = short_name + signature
        try:
            signature = format_code(signature)
        except InvalidInput as e:
            print(f"Could not format the given code: \n{e})")
        app.env.docfx_signature_funcs_methods[name] = signature


def insert_inheritance(app, _type, obj, datam):

    def collect_inheritance(base, to_add):
        for new_base in base.__bases__:
            new_add = {'type': _fullname(new_base)}
            collect_inheritance(new_base, new_add)
            if 'inheritance' not in to_add:
                to_add['inheritance'] = []
            to_add['inheritance'].append(new_add)

    if hasattr(obj, '__bases__'):
        if 'inheritance' not in datam:
            datam['inheritance'] = []
        for base in obj.__bases__:
            to_add = {'type': _fullname(base)}
            collect_inheritance(base, to_add)
            datam['inheritance'].append(to_add)


def insert_children_on_module(app, _type, datam):
    """
    Insert children of a specific module
    """

    if MODULE not in datam or datam[MODULE] not in app.env.docfx_yaml_modules:
        return

    insert_module = app.env.docfx_yaml_modules[datam[MODULE]]
    # Find the module which the datam belongs to
    for obj in insert_module:
        # Add standardlone function to global class
        if _type in [FUNCTION] and \
                obj['type'] == MODULE and \
                obj[MODULE] == datam[MODULE]:
            obj['children'].append(datam['uid'])

            # If it is a function, add this to its module. No need for class and module since this is
            # done before calling this function.
            insert_module.append(datam)
            obj['references'].append(_create_reference(datam, parent=obj['uid']))
            break
        # Add classes & exceptions to module
        if _type in [CLASS, EXCEPTION] and \
                obj['type'] == MODULE and \
                obj[MODULE] == datam[MODULE]:
            obj['children'].append(datam['uid'])
            obj['references'].append(_create_reference(datam, parent=obj['uid']))
            break

    if _type in [MODULE]: # Make sure datam is a module.
        # Add this module(datam) to parent module node
        if datam[MODULE].count('.') >= 1:
            parent_module_name = '.'.join(datam[MODULE].split('.')[:-1])

            if parent_module_name not in app.env.docfx_yaml_modules:
                return

            insert_module = app.env.docfx_yaml_modules[parent_module_name]

            for obj in insert_module:
                if obj['type'] == MODULE and obj[MODULE] == parent_module_name:
                    obj['children'].append(datam['uid'])
                    obj['references'].append(_create_reference(datam, parent=obj['uid']))
                    break

        # Add datam's children modules to it. Based on Python's passing by reference.
        # If passing by reference would be changed in python's future release.
        # Time complex: O(N^2)
        for module, module_contents in app.env.docfx_yaml_modules.items():
            if module != datam['uid'] and \
                    module[:module.rfind('.')] == datam['uid']: # Current module is submodule/subpackage of datam
                for obj in module_contents: # Traverse module's contents to find the module itself.
                    if obj['type'] == MODULE and obj['uid'] == module:
                        datam['children'].append(module)
                        datam['references'].append(_create_reference(obj, parent=module))
                        break


def insert_children_on_class(app, _type, datam):
    """
    Insert children of a specific class
    """
    if CLASS not in datam:
        return

    insert_class = app.env.docfx_yaml_classes[datam[CLASS]]
    # Find the parent class using the module for subclasses of a class.
    parent_class = app.env.docfx_yaml_classes.get(datam[MODULE])

    # Find the class which the datam belongs to
    for obj in insert_class:
        if obj['type'] != CLASS:
            continue
        # Add subclass & methods & attributes & properties to class
        if _type in [METHOD, ATTRIBUTE, PROPERTY, CLASS] and \
          (obj[CLASS] == datam[CLASS] and obj != datam):
            obj['children'].append(datam['uid'])
            obj['references'].append(_create_reference(datam, parent=obj['uid']))
            insert_class.append(datam)

    # If there is a parent class, determine if current class is a subclass.
    if not parent_class:
        return
    for obj in parent_class:
        if obj['type'] != CLASS:
            continue
        if _type == CLASS and obj['class'] == datam['module']:
            # No need to add datam to the parent class.
            obj['children'].append(datam['uid'])
            obj['references'].append(_create_reference(datam, parent=obj['uid']))


def insert_children_on_function(app, _type, datam):
    """
    Insert children of a specific class
    """
    if FUNCTION not in datam:
        return

    insert_functions = app.env.docfx_yaml_functions[datam[FUNCTION]]
    insert_functions.append(datam)

# Parses the package name and returns unique identifer and name.
def find_unique_name(package_name, entries):
    for name in package_name:
        # Only find unique identifiers beside "google" and "cloud"
        # For example, if given
        #   "google.cloud.spanner.v1.params_v1.types"
        #   "google.cloud.spanner.v1.instance_v1.types"
        # it will return "instace_v1" or "params_v1" and "types".
        # Also ensure that if name == package_name[-1], we only return one of
        # the duplicate and not both.
        if name != "google" and name != "cloud" and entries[name] == 1 and name != package_name[-1]:
            return [name, package_name[-1]]

    # If there is no way to disambiguate or we found duplicates, return the identifier name.
    return [package_name[-1]]

# Used to disambiguate names that have same entries.
# Returns a dictionary of names that are disambiguated in the form of:
# {uidname: disambiguated_name}
def disambiguate_toc_name(pkg_toc_yaml):
    name_entries = {}
    disambiguated_names = {}

    for module in pkg_toc_yaml:
        module_name = module['name']
        if module_name not in name_entries:
            name_entries[module_name] = {}

        # Split the name and mark all duplicates.
        # There will be at least 1 unique identifer for each name.
        for part in module['uidname'].split("."):
            if part not in name_entries[module_name]:
                name_entries[module_name][part] = 1
            else:
                name_entries[module_name][part] += 1

        # Some entries don't contain `name` in `uidname`, add these into the map as well.
        if module_name not in name_entries[module_name]:
            name_entries[module_name][module_name] = 1

        if 'items' in module:
            # Update the dictionary of dismabiguated names
            disambiguated_names.update(disambiguate_toc_name(module['items']))

    for module in pkg_toc_yaml:
        module_name = module['name']
        # Check if there are multiple entires of module['name'], disambiguate if needed.
        if name_entries[module_name][module_name] > 1:
            module['name'] = ".".join(find_unique_name(module['uidname'].split("."), name_entries[module_name]))
            disambiguated_names[module['uidname']] = module['name']

    return disambiguated_names


# Combines pkg_toc_yaml entries with similar version headers.
def group_by_package(pkg_toc_yaml):
    new_pkg_toc_yaml = []
    package_groups = {}
    for module in pkg_toc_yaml:
        package_group = find_package_group(module['uidname'])
        if package_group not in package_groups:
            package_name = pretty_package_name(package_group)
            package_groups[package_group] = {
                "name": package_name,
                "uidname": package_group,
                "items": []
            }
        package_groups[package_group]['items'].append(module)

    for package_group in package_groups:
        new_pkg_toc_yaml.append(package_groups[package_group])

    return new_pkg_toc_yaml


# Given the full uid, return the package group including its prefix.
def find_package_group(uid):
    return ".".join(uid.split(".")[:3])


# Given the package group, make its name presentable.
def pretty_package_name(package_group):
    name = ""

    # Retrieve only the package name
    split_name = package_group.split(".")[-1]
    # Capitalize the first letter of each package name part
    capitalized_name = [part.capitalize() for part in split_name.split("_")]
    return " ".join(capitalized_name)


# Check is the current lines conform to markdown header format.
def parse_markdown_header(header_line, prev_line):
    # Markdown h1 prefix should have only 1 of '#' character followed by exactly one space.
    h1_header_prefix = "# "
    if h1_header_prefix in header_line and header_line.count("#") == 1:
        # Check for proper h1 header formatting, ensure there's more than just
        # the hashtag character, and exactly only one space after the hashtag.
        if not header_line[header_line.index(h1_header_prefix)+2].isspace() and \
            len(header_line) > 2:

            return header_line[header_line.index(h1_header_prefix):].strip("#").strip()

    elif "=" in header_line:
        # Check if we're inspecting an empty or undefined lines.
        if not prev_line:
            return ""

        # Check if the current line only has equal sign divider.
        if header_line.count("=") == len(header_line.strip()):
            # Update header to the previous line.
            return prev_line.strip()

    return ""


def extract_header_from_markdown(mdfile: Iterable[str]) -> str:
    """For a given markdown file, extract its header line.

    Args:
        mdfile: iterator to the markdown file.

    Returns:
        A string for header or empty string if header is not found.
    """
    prev_line = ""

    for header_line in mdfile:

        # Ignore licenses and other non-headers prior to the header.
        header = parse_markdown_header(header_line, prev_line)
        # If we've found the header, return the header.
        if header != "":
            return header

        prev_line = header_line

    return ""


# For a given markdown file, adds syntax highlighting to code blocks.
def highlight_md_codeblocks(mdfile):
    fence = '```'
    fence_with_python = '```python'
    new_lines = []

    with open(mdfile) as mdfile_iterator:
        file_content = mdfile_iterator.read()
        # If there is an odd number of code block annotations, do not syntax
        # highlight.
        if file_content.count(fence) % 2 != 0:
            print(f'{mdfile_iterator.name} contains wrong format of code blocks. Skipping syntax highlighting.')
            return
        # Retrieve code block positions to replace
        codeblocks = [[m.start(), m.end()] for m in re.finditer(
                                                      fence,
                                                      file_content)]

        # This is equivalent to grabbing every odd index item.
        codeblocks = codeblocks[::2]
        # Used to store code blocks that come without language indicators.
        blocks_without_indicators = []

        # Check if the fence comes without a language indicator. If so, include
        # this to a list to render.
        for start, end in codeblocks:
            if file_content[end] == '\n':
                blocks_without_indicators.append([start, end])

        # Stitch content that does not need to be parsed, and replace with
        # `fence_with_python` for parsed portions.
        prev_start = prev_end = 0
        for start, end in blocks_without_indicators:
            new_lines.append(file_content[prev_end:start])
            new_lines.append(fence_with_python)
            prev_start, prev_end = start, end

        # Include rest of the content.
        new_lines.append(file_content[prev_end:])

    # Overwrite with newly parsed content.
    with open(mdfile, 'w') as mdfile_iterator:
        new_content = ''.join(new_lines)
        mdfile_iterator.write(new_content)


def prepend_markdown_header(filename: str, mdfile: Iterable[str]):
    """Prepends the filename as a Markdown header.

    Args:
        filename: the name of the markdown file to prepend.
        mdfile: iterator to the markdown file that is both readable
          and writable.
    """
    file_content = f'# {filename}\n\n' + mdfile.read()
    # Reset file position to the beginning to write
    mdfile.seek(0)
    mdfile.write(file_content)


# Given generated markdown files, incorporate them into the docfx_yaml output.
# The markdown file metadata will be added to top level of the TOC.
def find_markdown_pages(app, outdir):
    # Use this to ignore markdown files that are unnecessary.
    files_to_ignore = [
        "index.md",     # merge index.md and README.md and index.yaml later.
                        # See https://github.com/googleapis/sphinx-docfx-yaml/issues/105.

        "reference.md", # Reference docs overlap with Overview. Will try and incorporate this in later.
                        # See https://github.com/googleapis/sphinx-docfx-yaml/issues/106.

        "readme.md",    # README does not seem to work in cloud site
                        # See https://github.com/googleapis/sphinx-docfx-yaml/issues/107.
    ]

    markdown_dir = Path(app.builder.outdir).parent / "markdown"
    if not markdown_dir.exists():
        print("There's no markdown file to move.")
        return

    # For each file, if it is a markdown file move to the top level pages.
    for mdfile in markdown_dir.iterdir():
        if mdfile.is_file() and mdfile.name.lower() not in files_to_ignore:
            mdfile_name = ""
            highlight_md_codeblocks(markdown_dir / mdfile.name)

            # Extract the header name for TOC.
            with open(mdfile) as mdfile_iterator:
                name = extract_header_from_markdown(mdfile_iterator)

            if not name:
                with open(mdfile, 'r+') as mdfile_iterator:
                    mdfile_name = mdfile_iterator.name.split("/")[-1].split(".")[0].capitalize()

                    print(f"Could not find a title for {mdfile_iterator.name}. Using {mdfile_name} as the title instead.")
                    name = mdfile_name

                    prepend_markdown_header(name, mdfile_iterator)

            shutil.copy(mdfile, f"{outdir}/{mdfile.name.lower()}")

            # Add the file to the TOC later.
            app.env.markdown_pages.append({
                'name': name,
                'href': mdfile.name.lower(),
            })

def find_uid_to_convert(
    current_word: str,
    words: List[str],
    index: int,
    known_uids: List[str],
    current_object_name: str,
    processed_words: List[str],
    hard_coded_references: Dict[str, str] = None
) -> Optional[str]:
    """Given `current_word`, returns the `uid` to convert to cross reference if found.

    Args:
        current_word: current word being looked at
        words: list of words used to check and compare content before and after `current_word`
        index: index position of `current_word` within words
        known_uids: list of uid references to look for
        current_object_name: the name of the current Python object being processed
        processed_words: list of words containing words that's been processed so far
        hard_coded_references: Optional list containing a list of hard coded reference

    Returns:
        None if current word does not contain any reference `uid`, or the `uid`
          that should be converted.
    """
    for uid in known_uids:
        # Do not convert references to itself or containing partial
        # references. This could result in `storage.types.ReadSession` being
        # prematurely converted to
        # `<xref uid="storage.types">storage.types</xref>ReadSession`
        # instead of
        # `<xref uid="storage.types.ReadSession">storage.types.ReadSession</xref>`
        if uid in current_object_name:
            continue

        if uid in current_word:
            # If the cross reference has been processed already, "<xref" or
            # "<a" will appear as the previous word.
            # For hard coded references, we use "<a href" style.
            if "<xref" not in words[index-1] and "<a" not in words[index-1]:
                # Check to see if the reference has been converted already.
                if not (processed_words and ( \
                    f"<xref uid=\"{uid}" in processed_words[-1] or \
                    (hard_coded_references and f"<a href=\"{hard_coded_references.get(uid)}" in processed_words[-1]))):
                  return uid

    return None


def convert_cross_references(content: str, current_object_name: str, known_uids: List[str]) -> str:
    """Finds and replaces references that should be a cross reference in given content.

    This should not convert any references that contain `current_object_name`,
    i.e. if we're processing docstring for `google.cloud.spanner.v1.services`,
    references to `google.cloud.spanner.v1.services` should not be convereted
    to references.

    Args:
        content: body of content to parse and look for references in
        current_object_name: the name of the current Python object being processed
        known_uids: list of uid references to look for

    Returns:
        content that has been modified with proper cross references if found.
    """
    words = content.split(" ")

    # Contains a list of words that is not a valid reference or converted
    # references.
    processed_words = []

    # TODO(https://github.com/googleapis/sphinx-docfx-yaml/issues/208):
    # remove this in the future.
    iam_policy_link = "http://github.com/googleapis/python-grpc-google-iam-v1/blob/8e73b45993f030f521c0169b380d0fbafe66630b/google/iam/v1/iam_policy_pb2_grpc.py"
    hard_coded_references = {
        "google.iam.v1.iam_policy_pb2.SetIamPolicyRequest": iam_policy_link + "#L103-L109",
        "google.iam.v1.iam_policy_pb2.GetIamPolicyRequest": iam_policy_link + "#L111-L118",
        "google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest": iam_policy_link + "#L120-L131",
        "google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse": iam_policy_link + "#L120-L131"
    }
    known_uids.extend(hard_coded_references.keys())

    for index, word in enumerate(words):
        uid = find_uid_to_convert(
            word, words, index, known_uids, current_object_name, processed_words, hard_coded_references
        )

        if uid:
            cross_reference = f"<a href=\"{hard_coded_references[uid]}\">{uid}</a>" \
                if uid in hard_coded_references else \
                f"<xref uid=\"{uid}\">{uid}</xref>"

            processed_words.append(word.replace(uid, cross_reference))
            print(f"Converted {uid} into cross reference in: \n{content}")

        else:
            # If cross reference has not been found, add current unchanged content.
            processed_words.append(word)

    return " ".join(processed_words)


# Used to look for cross references in the obj's data where applicable.
# For now, we inspect summary, syntax and attributes.
def search_cross_references(obj, current_object_name: str, known_uids: List[str]):
    if obj.get("summary"):
        obj["summary"] = convert_cross_references(obj["summary"], current_object_name, known_uids)

    if obj.get("syntax"):
        if obj["syntax"].get("parameters"):
            for param in obj["syntax"]["parameters"]:
                if param.get("description"):
                    param["description"] = convert_cross_references(
                        param["description"],
                        current_object_name,
                        known_uids
                    )

                if param.get("id"):
                    param["id"] = convert_cross_references(
                        param["id"],
                        current_object_name,
                        known_uids
                    )

                if param.get("var_type"):
                    param["var_type"] = convert_cross_references(
                        param["var_type"],
                        current_object_name,
                        known_uids
                    )

        if obj["syntax"].get("exceptions"):
            for exception in obj["syntax"]["exceptions"]:
                if exception.get("description"):
                    exception["description"] = convert_cross_references(
                        exception["description"],
                        current_object_name,
                        known_uids
                    )

                if exception.get("var_type"):
                    exception["var_type"] = convert_cross_references(
                        exception["var_type"],
                        current_object_name,
                        known_uids
                    )

        if obj["syntax"].get("returns"):
            for ret in obj["syntax"]["returns"]:
                if ret.get("description"):
                    ret["description"] = convert_cross_references(
                        ret["description"],
                        current_object_name,
                        known_uids
                    )

                if ret.get("var_type"):
                    ret["var_type"] = convert_cross_references(
                        ret["var_type"],
                        current_object_name,
                        known_uids
                    )


    if obj.get("attributes"):
        for attribute in obj["attributes"]:
            if attribute.get("description"):
                attribute["description"] = convert_cross_references(
                    attribute["description"],
                    current_object_name,
                    known_uids
                )

            if attribute.get("id"):
                attribute["id"] = convert_cross_references(
                    attribute["id"],
                    current_object_name,
                    known_uids
                )

            if attribute.get("var_type"):
                attribute["var_type"] = convert_cross_references(
                    attribute["var_type"],
                    current_object_name,
                    known_uids
                )


def build_finished(app, exception):
    """
    Output YAML on the file system.
    """

    # Used to get rid of the uidname field for cleaner toc file.
    def sanitize_uidname_field(pkg_toc_yaml):
        for module in pkg_toc_yaml:
            if 'items' in module:
                sanitize_uidname_field(module['items'])
            module.pop('uidname')

    def find_node_in_toc_tree(pkg_toc_yaml, to_add_node):
        for module in pkg_toc_yaml:
            if module['uidname'] == to_add_node:
                return module

            if 'items' in module:
                items = module['items']
                found_module = find_node_in_toc_tree(items, to_add_node)
                if found_module != None:
                    return found_module
        return None

    def convert_module_to_package_if_needed(obj):
        if 'source' in obj and 'path' in obj['source'] and obj['source']['path']:
            if obj['source']['path'].endswith(INITPY):
                obj['type'] = 'subPackage'
                product_name = extract_product_name(obj['fullName'])
                obj['summary'] = f"API documentation for `{product_name}` package."
                return

        for child_uid in obj['children']:
            if child_uid in app.env.docfx_info_uid_types:
                child_uid_type = app.env.docfx_info_uid_types[child_uid]

                if child_uid_type == MODULE:
                    obj['type'] = 'package'
                    return


    normalized_outdir = os.path.normpath(os.path.join(
        app.builder.outdir,  # Output Directory for Builder
        API_ROOT,
    ))
    ensuredir(normalized_outdir)

    # Add markdown pages to the configured output directory.
    find_markdown_pages(app, normalized_outdir)

    pkg_toc_yaml = []
    # Used to record filenames dumped to avoid confliction
    # caused by Windows case insensitive file system
    file_name_set = set()

    # Used to disambiguate entry names
    yaml_map = {}

    # Order matters here, we need modules before lower level classes,
    # so that we can make sure to inject the TOC properly
    for data_set in (app.env.docfx_yaml_modules,
                     app.env.docfx_yaml_classes, 
                     app.env.docfx_yaml_functions):  # noqa

        for uid, yaml_data in iter(sorted(data_set.items())):
            if not uid:
                # Skip objects without a module
                continue

            references = []

            # Merge module data with class data
            for obj in yaml_data:
                arg_params = obj.get('syntax', {}).get('parameters', [])
                if(len(arg_params) > 0 and 'id' in arg_params[0] and arg_params[0]['id'] == 'self'):
                    # Support having `self` as an arg param, but not documented
                    arg_params = arg_params[1:]
                    obj['syntax']['parameters'] = arg_params
                if obj['uid'] in app.env.docfx_info_field_data and \
                    obj['type'] == app.env.docfx_info_field_data[obj['uid']]['type']:
                    # Avoid entities with same uid and diff type.
                    del(app.env.docfx_info_field_data[obj['uid']]['type']) # Delete `type` temporarily
                    if 'syntax' not in obj:
                        obj['syntax'] = {}
                    merged_params = []
                    if 'parameters' in app.env.docfx_info_field_data[obj['uid']]:
                        doc_params = app.env.docfx_info_field_data[obj['uid']].get('parameters', [])
                        if arg_params and doc_params:
                            if len(arg_params) - len(doc_params) > 0:
                                app.warn(
                                    "Documented params don't match size of params:"
                                    " {}".format(obj['uid']))
                            # Zip 2 param lists until the long one is exhausted
                            for args, docs in zip_longest(arg_params, doc_params, fillvalue={}):
                                if len(args) == 0:
                                    merged_params.append(docs)
                                else:
                                    args.update(docs)
                                    merged_params.append(args)
                    obj['syntax'].update(app.env.docfx_info_field_data[obj['uid']])
                    if merged_params:
                        obj['syntax']['parameters'] = merged_params

                    if 'parameters' in obj['syntax'] and obj['type'] == 'method':	
                        for args in obj['syntax']['parameters']:
                            if 'isRequired' not in args and 'defaultValue' not in args:
                                args['isRequired'] = True

                    # Raise up summary
                    if 'summary' in obj['syntax'] and obj['syntax']['summary']:
                        obj['summary'] = obj['syntax'].pop('summary').strip(" \n\r\r")

                    # Raise up remarks
                    if 'remarks' in obj['syntax'] and obj['syntax']['remarks']:
                        obj['remarks'] = obj['syntax'].pop('remarks')

                    # Raise up seealso
                    if 'seealso' in obj['syntax'] and obj['syntax']['seealso']:
                        obj['seealsoContent'] = obj['syntax'].pop('seealso')

                    # Raise up example
                    if 'example' in obj['syntax'] and obj['syntax']['example']:
                        obj.setdefault('example', []).append(obj['syntax'].pop('example'))

                    # Raise up exceptions
                    if 'exceptions' in obj['syntax'] and obj['syntax']['exceptions']:
                        obj['exceptions'] = obj['syntax'].pop('exceptions')

                    # Raise up references
                    if 'references' in obj['syntax'] and obj['syntax']['references']:
                        obj.setdefault('references', []).extend(obj['syntax'].pop('references'))

                    # add content of temp list 'added_attribute' to children and yaml_data
                    if 'added_attribute' in obj['syntax'] and obj['syntax']['added_attribute']:
                        added_attribute = obj['syntax'].pop('added_attribute')
                        for attrData in added_attribute:
                            existed_Data = next((n for n in yaml_data if n['uid'] == attrData['uid']), None)
                            if existed_Data:
                                # Update data for already existed one which has attribute comment in source file
                                existed_Data.update(attrData)
                            else:
                                obj.get('children', []).append(attrData['uid'])
                                yaml_data.append(attrData)
                                if 'class' in attrData:
                                    # Get parent for attrData of Non enum class
                                    parent = attrData['class']
                                else:
                                    # Get parent for attrData of enum class
                                    parent = attrData['parent']
                                obj['references'].append(_create_reference(attrData, parent))
                    app.env.docfx_info_field_data[obj['uid']]['type'] = obj['type'] # Revert `type` for other objects to use

                if 'references' in obj:
                    # Ensure that references have no duplicate ref
                    ref_uids = [r['uid'] for r in references]
                    for ref_obj in obj['references']:
                        if ref_obj['uid'] not in ref_uids:
                            references.append(ref_obj)
                    obj.pop('references')

                if obj['type'] == 'module':
                    convert_module_to_package_if_needed(obj)

                if obj['type'] == 'method':
                    # Update the name to use shorter name to show
                    obj['name'] = obj['source']['id']

                # To distinguish distribution package and import package
                if obj.get('type', '') == 'package' and obj.get('kind', '') != 'distribution':
                    obj['kind'] = 'import'

                try:
                    if remove_inheritance_for_notfound_class:
                        if 'inheritance' in obj:
                            python_sdk_name = obj['uid'].split('.')[0]
                            obj['inheritance'] = [n for n in obj['inheritance'] if not n['type'].startswith(python_sdk_name) or
                                                  n['type'] in app.env.docfx_info_uid_types]
                            if not obj['inheritance']:
                                obj.pop('inheritance')

                except NameError:
                    pass

                if 'source' in obj and (not obj['source']['remote']['repo'] or \
                    obj['source']['remote']['repo'] == 'https://apidrop.visualstudio.com/Content%20CI/_git/ReferenceAutomation'):
                        del(obj['source'])


                # Extract any missing cross references where applicable.
                # Potential targets are instances of full uid shown, or
                # if we find a short form of the uid of one of current
                # package's items. For example:
                # cross reference candidates:
                #   google.cloud.bigquery_storage_v1.types.storage.SplitReadStreamResponse
                #   SplitReadStreamResponse
                # non-candidates:
                #   (not from the same library)
                #   google.cloud.aiplatform.AutoMLForecastingTrainingJob

                current_object_name = obj["fullName"]
                known_uids = sorted(app.env.docfx_uid_names.keys(), reverse=True)
                # Currently we only need to look in summary, syntax and
                # attributes for cross references.
                search_cross_references(obj, current_object_name, known_uids)

            yaml_map[uid] = [yaml_data, references]

            # Parse the name of the object.
            # Some types will need additional parsing to de-duplicate their names and contain
            # a portion of their parent name for better disambiguation. This is done in
            # disambiguate_toc_name

            node_name = uid.split(".")[-1]

            # Build nested TOC
            if uid.count('.') >= 1:
                parent_level = '.'.join(uid.split('.')[:-1])
                found_node = find_node_in_toc_tree(pkg_toc_yaml, parent_level)

                if found_node:
                    found_node.setdefault(
                      'items',
                      [{'name': 'Overview', 'uidname': parent_level, 'uid': parent_level}]
                    ).append({
                      'name': node_name,
                      'uidname': uid,
                      'uid': uid
                    })
                else:
                    pkg_toc_yaml.append({
                      'name': node_name,
                      'uidname': uid,
                      'uid': uid
                    })

            else:
                pkg_toc_yaml.append({
                  'name': node_name,
                  'uidname': uid,
                  'uid': uid
                })

    # Exit if there are no generated YAML pages or Markdown pages.
    if len(pkg_toc_yaml) == 0 and len(app.env.markdown_pages) == 0:
        raise RuntimeError("No documentation for this module.")

    pkg_toc_yaml = group_by_package(pkg_toc_yaml)

    # Perform additional disambiguation of the name
    disambiguated_names = disambiguate_toc_name(pkg_toc_yaml)

    # Keeping uidname field carrys over onto the toc.yaml files, we need to
    # be keep using them but don't need them in the actual file
    pkg_toc_yaml_with_uid = copy.deepcopy(pkg_toc_yaml)

    sanitize_uidname_field(pkg_toc_yaml)

    toc_file = os.path.join(normalized_outdir, 'toc.yml')
    with open(toc_file, 'w') as writable:
        writable.write(
            dump(
                [{
                    'name': app.config.project,
                    'items': [{'name': 'Overview', 'uid': 'project-' + app.config.project}] + app.env.markdown_pages + pkg_toc_yaml
                }],
                default_flow_style=False,
            )
        )

    # Output files
    for uid, data in iter(yaml_map.items()):

        for yaml_item in data:
            for obj in yaml_item:
                # If the entry was disambiguated, update here:
                obj_full_name = obj['fullName']
                if disambiguated_names.get(obj_full_name):
                    obj['name'] = disambiguated_names[obj_full_name]
                    if obj['type'] == 'subPackage':
                        obj['summary'] = "API documentation for `{}` package.".format(obj['name'])

        # data is formatted as [yaml_data, references]
        yaml_data, references = data

        if uid.lower() in file_name_set:
            filename = uid + "(%s)" % app.env.docfx_info_uid_types[uid]
        else:
            filename = uid

        out_file = os.path.join(normalized_outdir, '%s.yml' % filename)
        ensuredir(os.path.dirname(out_file))
        if app.verbosity >= 1:
            app.info(bold('[docfx_yaml] ') + darkgreen('Outputting %s' % filename))

        with open(out_file, 'w') as out_file_obj:
            out_file_obj.write('### YamlMime:UniversalReference\n')
            try:
                dump(
                    {
                        'items': yaml_data,
                        'references': references,
                        'api_name': [],  # Hack around docfx YAML
                    },
                    out_file_obj,
                    default_flow_style=False
                )
            except Exception as e:
                raise ValueError("Unable to dump object\n{0}".format(yaml_data)) from e

        file_name_set.add(filename)

    index_file = os.path.join(normalized_outdir, 'index.yml')
    index_children = []
    index_references = []
    for package in pkg_toc_yaml_with_uid:
        for item in package.get("items"):
            index_children.append(item.get('uidname', ''))
            index_references.append({
                'uid': item.get('uidname', ''),
                'name': item.get('name', ''),
                'fullname': item.get('uidname', ''),
                'isExternal': False
            })
    with open(index_file, 'w') as index_file_obj:
        index_file_obj.write('### YamlMime:UniversalReference\n')
        dump(
            {
                'items': [{
                    'uid': 'project-' + app.config.project,
                    'name': app.config.project,
                    'fullName': app.config.project,
                    'langs': ['python'],
                    'type': 'package',
                    'kind': 'distribution',
                    'summary': 'Reference API documentation for `{}`.'.format(app.config.project),
                    'children': index_children
                }],
                'references': index_references
            },
            index_file_obj,
            default_flow_style=False
        )

    '''
    # TODO: handle xref for other products.
    xref_file = os.path.join(normalized_outdir, 'xrefs.yml')
    with open(xref_file, 'w') as xref_file_obj:
        for xref in app.env.docfx_xrefs:
            xref_file_obj.write(f'{xref}\n')
    '''

def missing_reference(app, env, node, contnode):
    reftarget = ''
    refdoc = ''
    reftype = ''
    module = ''
    if 'refdomain' in node.attributes and node.attributes['refdomain'] == 'py':
        reftarget = node['reftarget']
        reftype = node['reftype']
        if 'refdoc' in node:
            refdoc = node['refdoc']
        if 'py:module' in node:
            module = node['py:module']

        #Refactor reftarget to fullname if it is a short name
        if reftype in [CLASS, REFFUNCTION, REFMETHOD] and module and '.' not in reftarget:
            if reftype in [CLASS, REFFUNCTION]:
                fields = (module, reftarget)
            else:
                fields = (module, node['py:class'], reftarget)
            reftarget = '.'.join(field for field in fields if field is not None)

        return make_refnode(app.builder, refdoc, reftarget, '', contnode)


def setup(app):
    """
    Plugin init for our Sphinx extension.

    Args:
        app (Application): The Sphinx application instance

    """

    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-process-docstring', _process_docstring)

    app.add_node(remarks, html = (remarks.visit_remarks, remarks.depart_remarks))
    app.add_directive('remarks', RemarksDirective)
    app.add_directive('todo', TodoDirective)

    app.connect('builder-inited', build_init)
    app.connect('autodoc-process-docstring', process_docstring)
    app.connect('autodoc-process-signature', process_signature)
    app.connect('build-finished', build_finished)
    app.connect('missing-reference', missing_reference)
    app.add_config_value('docfx_yaml_output', API_ROOT, 'html')
    app.add_config_value('folder', '', 'html')
    app.add_config_value('autodoc_functions', False, 'env')
