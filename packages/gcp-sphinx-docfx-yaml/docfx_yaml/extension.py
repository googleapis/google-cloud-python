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
from functools import partial
from itertools import zip_longest

try:
    from subprocess import getoutput
except ImportError:
    from commands import getoutput

from yaml import safe_dump as dump

from sphinx.util.console import darkgreen, bold
from sphinx.util import ensuredir
from sphinx.errors import ExtensionError
from sphinx.util.nodes import make_refnode

from .utils import transform_node, transform_string
from .settings import API_ROOT
from .monkeypatch import patch_docfields
from .directives import RemarksDirective, TodoDirective
from .nodes import remarks


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
REF_PATTERN = ':(py:)?(func|class|meth|mod|ref):`~?[a-zA-Z_\.<> ]*?`'


def build_init(app):
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
    elif _type in [METHOD, ATTRIBUTE]:
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
        'name': datam['name'],
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


def _resolve_reference_in_module_summary(lines):
    new_lines = []
    for line in lines:
        matched_objs = list(re.finditer(REF_PATTERN, line))
        new_line = line
        for matched_obj in matched_objs:
            start = matched_obj.start()
            end = matched_obj.end()
            matched_str = line[start:end]
            if '<' in matched_str and '>' in matched_str:
                # match string like ':func:`***<***>`'
                index = matched_str.index('<')
                ref_name = matched_str[index+1:-2]
            else:
                # match string like ':func:`~***`' or ':func:`***`'
                index = matched_str.index('~') if '~' in matched_str else matched_str.index('`')
                ref_name = matched_str[index+1:-1]
            new_line = new_line.replace(matched_str, '<xref:{}>'.format(ref_name))
        new_lines.append(new_line)
    return new_lines


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
    short_name = name.split('.')[-1]
    args = []
    try:
        if _type in [METHOD, FUNCTION]:
            argspec = inspect.getfullargspec(obj) # noqa
            for arg in argspec.args:
                args.append({'id': arg})
            if argspec.defaults:
                for count, default in enumerate(argspec.defaults):
                    cut_count = len(argspec.defaults)
                    # Only add defaultValue when str(default) doesn't contain object address string(object at 0x)
                    # inspect.getargspec method will return wrong defaults which contain object address for some default values, like sys.stdout
                    # Match the defaults with the count
                    if 'object at 0x' not in str(default):
                        args[len(args) - cut_count + count]['defaultValue'] = str(default)
    except Exception as e:
        print("Can't get argspec for {}: {}. Exception: {}".format(type(obj), name, e))

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

        # append relative path defined in conf.py (in case of "binding python" project)
        try:
            source_prefix  # does source_prefix exist in the current namespace
            path = source_prefix + path
        except NameError:
            pass

    except (TypeError, OSError):
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

    # Only add summary to parts of the code that we don't get it from the monkeypatch
    if _type == MODULE:
        lines = _resolve_reference_in_module_summary(lines)
        summary = app.docfx_transform_string('\n'.join(_refact_example_in_module_summary(lines)))
        if summary:
            datam['summary'] = summary.strip(" \n\r\r")

    if args or sig:
        datam['syntax'] = {}
        if args:
            datam['syntax']['parameters'] = args
        if sig:
            datam['syntax']['content'] = sig
    if cls:
        datam[CLASS] = cls
    if _type in [CLASS, MODULE]:
        datam['children'] = []
        datam['references'] = []

    if _type in [FUNCTION, METHOD]:
        datam['name'] = app.env.docfx_signature_funcs_methods.get(name, datam['name'])

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
    # Use exception as class

    if _type == EXCEPTION:
        _type = CLASS

    cls, module = _get_cls_module(_type, name)
    if not module:
        print('Unknown Type: %s' % _type)
        return None

    datam = _create_datam(app, cls, module, name, _type, obj, lines)

    if _type == MODULE:
        if module not in app.env.docfx_yaml_modules:
            app.env.docfx_yaml_modules[module] = [datam]
        else:
            app.env.docfx_yaml_modules[module].append(datam)

    if _type == CLASS:
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


def process_signature(app, _type, name, obj, options, signature, return_annotation):
    if signature:
        short_name = name.split('.')[-1]
        signature = short_name + signature
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
    # Find the class which the datam belongs to
    for obj in insert_class:
        if obj['type'] != CLASS:
            continue
        # Add methods & attributes to class
        if _type in [METHOD, ATTRIBUTE] and \
                obj[CLASS] == datam[CLASS]:
            obj['children'].append(datam['uid'])
            obj['references'].append(_create_reference(datam, parent=obj['uid']))
            insert_class.append(datam)


def insert_children_on_function(app, _type, datam):
    """
    Insert children of a specific class
    """
    if FUNCTION not in datam:
        return

    insert_functions = app.env.docfx_yaml_functions[datam[FUNCTION]]
    insert_functions.append(datam)


def build_finished(app, exception):
    """
    Output YAML on the file system.
    """

    # Used to get rid of the uidname field for cleaner toc file.
    def sanitize_uidname_field(toc_yaml):
        for module in toc_yaml:
            if 'items' in module:
                sanitize_uidname_field(module['items'])
            module.pop('uidname')

    # Parses the package name and returns package name and module name.
    def find_package_name(package_name):
        for name in package_name:
            if name != "google" and name != "cloud":
                return [name, package_name[-1]]

    # Used to disambiguate names that have same entries.
    def disambiguate_toc_name(toc_yaml):
        names = {}
        for module in toc_yaml:
            names[module['name']] = 1 if module['name'] not in names else 2
            if 'items' in module:
                disambiguate_toc_name(module['items'])

        for module in toc_yaml:
            if names[module['name']] > 1:
                module['name'] = ".".join(find_package_name(module['uidname'].split(".")))

    def find_node_in_toc_tree(toc_yaml, to_add_node):
        for module in toc_yaml:
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
                obj['type'] = 'package'
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

    toc_yaml = []
    # Used to record filenames dumped to avoid confliction
    # caused by Windows case insensitive file system
    file_name_set = set()

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
                    obj['namewithoutparameters'] = obj['source']['id']

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

            # Output file
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
           
            # Parse the name of the object.
            # Some types will need additional parsing to de-duplicate their names and contain
            # a portion of their parent name for better disambiguation. This is done in 
            # disambiguate_toc_name
            
            node_name = obj.get('class').split(".")[-1] if obj.get('class') else obj['name']

            # Build nested TOC
            if uid.count('.') >= 1:
                parent_level = '.'.join(uid.split('.')[:-1])
                found_node = find_node_in_toc_tree(toc_yaml, parent_level)

                if found_node:
                    found_node.pop('uid', 'No uid found')
                    found_node.setdefault(
                      'items', 
                      [{'name': 'Overview', 'uidname': parent_level, 'uid': parent_level}]
                    ).append({
                      'name': node_name,
                      'uidname': uid, 
                      'uid': uid
                    })
                else:
                    toc_yaml.append({
                      'name': node_name, 
                      'uidname': uid, 
                      'uid': uid
                    })

            else:
                toc_yaml.append({
                  'name': node_name, 
                  'uidname': uid, 
                  'uid': uid
                })

    if len(toc_yaml) == 0:
        raise RuntimeError("No documentation for this module.")

    # Perform additional disambiguation of the name
    disambiguate_toc_name(toc_yaml)

    # Keeping uidname field carrys over onto the toc.yaml files, we need to
    # be keep using them but don't need them in the actual file
    toc_yaml_with_uid = copy.deepcopy(toc_yaml)

    sanitize_uidname_field(toc_yaml)

    toc_file = os.path.join(normalized_outdir, 'toc.yml')
    with open(toc_file, 'w') as writable:
        writable.write(
            dump(
                [{
                    'name': app.config.project,
                    'items': [{'name': 'Overview', 'uid': 'project-' + app.config.project}] + toc_yaml
                }],
                default_flow_style=False,
            )
        )

    index_file = os.path.join(normalized_outdir, 'index.yml')
    index_children = []
    index_references = []
    for item in toc_yaml_with_uid:
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
                    'summary': '',
                    'children': index_children
                }],
                'references': index_references
            },
            index_file_obj,
            default_flow_style=False
        )


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
