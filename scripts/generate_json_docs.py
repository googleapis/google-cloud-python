# Copyright 2016 Google Inc. All rights reserved.
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

import argparse
import cgi
import doctest
import inspect
import json
import os
import shutil
import types

import pdoc
from parinx.parser import parse_docstring
from parinx.errors import MethodParsingException
import six

from verify_included_modules import get_public_modules


_DOCSTRING_TEST_PARSER = doctest.DocTestParser()


class Module(object):

    def __init__(self, module_id, name, description=None,
                 examples=None, methods=None, source=None):
        self.module_id = module_id
        self.name = name
        self.description = description
        self.examples = examples or []
        self.methods = methods
        self.source = source

    @classmethod
    def from_module_name(cls, name, base_path):
        module = pdoc.Module(pdoc.import_module(name), allsubmodules=True)
        methods = module.functions() + module.variables()
        examples = []

        if '__init__' in name:
            snippets = get_snippet_examples(name.split('.')[1],
                                            os.path.join(base_path, 'docs'))
            examples.extend(snippets)

        source_path = clean_source_path(module)

        return cls(module_id=name,
                   name=name.split('.')[-1].title(),
                   description=module.docstring,
                   examples=examples or [],
                   methods=[Method.from_pdoc(m) for m in methods],
                   source=source_path)

    def to_dict(self):
        return {'id': self.module_id,
                'name': self.name,
                'description': format_sphinx_doc(self.description),
                'examples': self.examples,
                'methods': [m.to_dict() for m in self.methods],
                'source': self.source}


class Klass(object):
    def __init__(self, module_id, name, refname=None, description=None,
                 examples=None, methods=None, source=None):
        self.module_id = module_id
        self.name = name
        self.refname = refname
        self.description = description
        self.examples = examples or []
        self.methods = methods
        self.source = source

    @classmethod
    def from_class_name(cls, module, kls):
        methods = kls.methods()

        examples = []
        source_path = clean_source_path(module)

        return cls(module_id=kls.name,
                   name=kls.name.split('.')[-1].title(),
                   refname=module.refname,
                   description=module.docstring,
                   examples=examples,
                   methods=[Method.from_pdoc(m) for m in methods],
                   source=source_path)

    def to_dict(self):
        return {'id': '%s.%s' % (self.refname, self.name.lower()),
                'name': self.name,
                'description': format_sphinx_doc(self.description),
                'examples': self.examples,
                'methods': [m.to_dict() for m in self.methods],
                'source': self.source}


class Method(object):

    def __init__(self, method_id, name, is_class, examples=None, params=None,
                 exceptions=None, returns=None, source=None):
        self.method_id = method_id
        self.name = name
        self.examples = examples or []
        self.params = params or []
        self.exceptions = exceptions or []
        self.returns = returns or []
        self.source = source or ''

        if is_class:
            self.type = 'constructor'
        else:
            self.type = 'instance'

    def add_param(self, param):
        self.params.append(param)

    def add_example(self, example):
        self.examples.append({'code': example})

    def add_source_line(self, source_line):
        self.source = source_line

    def set_returns(self, return_types):
        self.returns = [{'types': [return_types]}]

    def to_dict(self):
        return {'id': self.method_id,
                'name': self.name,
                'examples': self.examples,
                'source': self.source,
                'params': [p.to_dict() for p in self.params],
                'exceptions': self.exceptions,
                'returns': self.returns,
                'type': self.type}

    @classmethod
    def from_pdoc(cls, element):
        is_class = isinstance(element, pdoc.Class)
        method = cls(element.refname, element.name, is_class)
        components = element.refname.split('.')

        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)

        # Get method line number.
        method.add_source_line(get_source_line_number(mod))

        # Get method Examples.
        examples = get_examples_from_docstring(element.docstring)
        if examples:
            method.add_example(examples)

        if element.docstring:
            if not isinstance(element, pdoc.Class) and element.cls:
                klass = element.cls.cls
            elif element.cls:
                klass = element.cls
            else:
                klass = None

            # Hack for old-style classes
            if not str(klass).startswith('<'):
                klass = '<class \'%s\'>' % (klass,)

            try:
                method_info = parse_docstring(element.docstring, klass)
            except (MethodParsingException, IndexError):
                return method

            for name, data in method_info['arguments'].items():
                param = Param.from_docstring_section(name, data)
                method.add_param(param)

            if method_info.get('return'):
                if len(method_info['return']['type_name']) > 0:
                    type_name = method_info.get('return').get('type_name')

                    type_type = 'instance'
                    if any(x.isupper() for x in type_name):
                        type_type = 'constructor'

                    type_markup = build_link_from_type(type_name, type_type)

                    method.set_returns(type_markup)

        return method


class Param(object):

    def __init__(self, name, description=None, param_types=None, optional=None,
                 nullable=None):
        self.name = name
        self.description = description
        self.param_types = param_types or []
        self.optional = optional
        self.nullable = nullable

    def to_dict(self):
        return {'name': self.name,
                'description': process_words(self.description),
                'types': build_link_from_list_of_types(self.param_types),
                'optional': self.optional,
                'nullable': self.nullable}

    @classmethod
    def from_docstring_section(cls, name, data):
        param_types = build_link_from_type(data['type_name'])
        return cls(name=name, description=data['description'],
                   param_types=[param_types])


def clean_type_name(type_name):
    if type_name.lower().startswith('list of'):
        type_name = (type_name.replace('list of', '')
                     .replace('List of', ''))
    type_name = (type_name.replace('`', '').replace('class', '')
                 .replace(':', ''))
    return type_name


def build_link_from_list_of_types(type_names, object_type=None):
    processed_types = []
    for type_link in type_names:
        type_link = clean_type_name(type_link)
        processed_types.append(build_link_from_type(type_link, object_type))
    return processed_types


def build_link_from_type(type_name, object_type=None):
    type_name = clean_type_name(type_name)

    if not type_name.startswith('gcloud'):
        return type_name
    doc_path = type_name

    doc_path = '/'.join(doc_path.split('.')).lower()

    type_markup = '<a data-custom-type="%s"' % doc_path
    if object_type == 'instance':
        type_markup += ' data-method="%s"' % type_name
    type_markup += '>%s</a>' % (type_name,)

    return type_markup


def build_source(module, method):
    if isinstance(module, (types.ModuleType, types.ClassType,
                           types.MethodType, types.FunctionType,
                           types.TracebackType, types.FrameType,
                           types.CodeType, types.TypeType)):

        _, line = inspect.getsourcelines(module)
        source_path = clean_source_path(module)

        if line:
            source_path = source_path + '#L' + str(line)

        method.add_source_line(source_path)

        # Sketchy get examples from method docstring.
        examples = []
        for example in examples:
            method.add_example(example)


def build_toc_entry(title, toc_type):
    return {
        'title': title,
        'type': toc_type
    }


def build_type(type_id, title, contents):
    return {
        'id': type_id,
        'title': title,
        'contents': contents
    }


def clean_source_path(module):
    if isinstance(module, six.string_types):
        source_id = module
    elif hasattr(module, 'refname'):
        source_id = module.refname
    else:
        source_id = inspect.getmodule(module).__name__
    return '%s.py' % (source_id.replace('.', '/'),)


def get_examples_from_docstring(doc_str):
    """Parse doctest style code examples from a docstring."""
    examples = _DOCSTRING_TEST_PARSER.get_examples(doc_str)
    example_str = ''
    for example in examples:
        example_str += '%s' % (example.source,)
        example_str += '%s' % (example.want,)

    return cgi.escape(example_str)


def get_source_line_number(module):
    if isinstance(module, (types.ModuleType, types.ClassType,
                           types.MethodType, types.FunctionType,
                           types.TracebackType, types.FrameType,
                           types.CodeType, types.TypeType)):

        _, line = inspect.getsourcelines(module)
        source_path = clean_source_path(module)

        if line:
            source_path = source_path + '#L' + str(line)
        return source_path


def process_code_blocks(doc):
    blocks = []
    index = 0

    for line in doc.splitlines(True):
        if len(blocks) - 1 < index:
            blocks.append('')

        if line.strip():
            blocks[index] += line
        else:
            index += 1

    formatted_blocks = []
    for block in blocks:
        is_code = False
        if block.splitlines()[0].startswith('  '):
            is_code = True

        if is_code:
            block = {'code': '<pre><code>%s</code></pre>' % (block,)}

        formatted_blocks.append(block)
    return formatted_blocks


def format_sphinx_doc(doc):
    doc = process_code_blocks(doc)
    example_lines = ""
    for line in doc:
        if isinstance(line, dict):
            line = line['code']
        else:
            line = process_words(line)
        example_lines = '%s\n%s' % (example_lines, line)
    return example_lines


def process_words(line):
    processed_line = ''
    for word in line.split():
        end_sentence = False
        if word.endswith('.'):
            end_sentence = True
            word = word[:-1]

        if word.startswith('``') and word.endswith('``'):
            word = word.replace('``', '')
            word = '<code>%s</code>' % (word,)

        if word.startswith('**') and word.endswith('**'):
            word = word.replace('**', '')
            word = '<b>%s</b>' % (word,)

        if word.startswith(':class:'):
            word = word.replace(':class:', '').replace('`', '')
            word = build_link_from_type(word)

        if word.startswith(':mod:'):
            word = word.replace(':mod:', '').replace('`', '')
            word = build_link_from_type(word)

        if word.startswith(':meth:'):
            word = word.replace(':meth:', '').replace('`', '')
            word = build_link_from_type(word)

        if word.startswith(':func:'):
            word = word.replace(':func:', '').replace('`', '')
            word = build_link_from_type(word)

        word = word.replace('`', '')

        if word.startswith('https://') or word.startswith('http://'):
            word = '<a href="%s">%s</a>' % (word, word)

        if end_sentence:
            word += '.'

        processed_line += ' %s' % (word,)

    processed_line = processed_line.replace('::', '')

    return processed_line


def write_docs_file(path, contents):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            raise
    with open(path, 'w') as output_file:
        output_file.write(contents)


def generate_doc_types_json(modules, types_file_path):
    doc_types_list = [{
        'id': 'gcloud',
        'contents': 'index.json',
        'title': 'gcloud'
    }]

    for module_name in modules:
        if module_name == 'gcloud.__init__':
            continue

        module_title = module_name.replace('.__init__', '').split('.')
        module_contents = (module_name.replace('.', '/')
                           .replace('__init__', 'index'))

        if len(module_name.split('.')) > 2:
            module_id = module_name.replace('.', '/')
        else:
            module_id = (module_name.replace('.', '/'))

        module_contents += '.json'

        doc_type_object = build_type(module_id.replace('/__init__', ''),
                                     module_title, module_contents)

        doc_types_list.append(doc_type_object)

        pdoc_module = pdoc.Module(pdoc.import_module(module_name),
                                  allsubmodules=True)
        for c in pdoc_module.classes():
            generate_doc_types_classes_json(c, doc_types_list)

    write_docs_file(types_file_path,
                    json.dumps(doc_types_list))


def generate_doc_types_classes_json(klass, doc_types_list):

    module_contents = (klass.refname.replace('.', '/')
                       .replace('__init__', 'index'))
    module_contents += '.json'

    doc_type_object = build_type(klass.refname.lower().replace('.', '/'),
                                 klass.refname.split('.'),
                                 module_contents.lower())

    doc_types_list.append(doc_type_object)


def generate_module_docs(modules, docs_path, real_base_path, toc):
    for module_name in modules:
        module = Module.from_module_name(module_name, real_base_path)
        pdoc_module = pdoc.Module(pdoc.import_module(module_name),
                                  allsubmodules=True)
        for c in pdoc_module.classes():
            generate_class_docs(pdoc_module, c, docs_path, toc)

        module_path = (module_name.replace('.', '/')
                       .replace('__init__', 'index'))
        module_docs_path = os.path.join(docs_path, module_path) + '.json'

        if pdoc_module.functions():
            toc_key = module_name.replace('gcloud.', '').split('.')[0]
            toc_entry = build_toc_entry(module.name, module_path)
            toc['services'][toc_key].append(toc_entry)

        write_docs_file(module_docs_path,
                        json.dumps(module.to_dict(),
                                   indent=2, sort_keys=True))


def generate_class_docs(module, klass, base_path, toc):
    kls = Klass.from_class_name(module, klass)

    module_path = (module.refname.replace('.', '/')
                   .replace('__init__', 'index'))
    module_docs_path = os.path.join(base_path, module_path,
                                    klass.name.lower()) + '.json'
    toc_key = module.name.replace('gcloud.', '').split('.')[0]

    toc_entry = build_toc_entry(klass.name,
                                os.path.join(module_path,
                                             klass.name.lower()))

    toc['services'][toc_key].append(toc_entry)

    write_docs_file(module_docs_path,
                    json.dumps(kls.to_dict(),
                               indent=2, sort_keys=True))


def get_snippet_examples(module, json_docs_dir):
    snippets_file_path = os.path.join(json_docs_dir,
                                      module + '_snippets.py')
    usage_rst_path = os.path.join(json_docs_dir, module + '-usage.rst')

    snippet_labels = {}

    if os.path.isfile(usage_rst_path):
        with open(usage_rst_path, 'r') as snippet_labels_file:
            usage_rst = snippet_labels_file.read().splitlines()
            line_index = 0

            include_string = '.. literalinclude:: %s_snippets.py'
            for line in usage_rst:
                if line.startswith(include_string % module):
                    label_key = (usage_rst[line_index + 1]
                                 .replace('   :start-after: [START ', '')
                                 .replace(']', ''))
                    snippet_labels[label_key] = usage_rst[line_index - 2]
                line_index += 1

    snippets = []

    if os.path.isfile(snippets_file_path):
        with open(snippets_file_path, 'r') as snippets_file:
            snippets_string = snippets_file.read()
            label = None
            snippet = ''
            for line in snippets_string.splitlines(True):
                if line.strip().startswith('# [END'):
                    example = {
                        'caption': snippet_labels.get(label),
                        'code': snippet
                    }
                    snippets.append(example)

                    # Reset for next snippet
                    snippet = ''
                    label = None

                if label:
                    snippet += line

                if line.strip().startswith('# [START'):
                    label = (line.replace('# [START', '').replace(']', '')
                             .strip())
                    snippet = '# %s\n' % label
    return snippets


def package_files(generated_json_dir, docs_build_dir, static_json_dir,
                  tag='master'):
    """Copy app and JSON files into a convenient place to deploy from.

    Structure needs to be...
    root
        - src/
            - images/
            - app.js
            - app.css
            - vendor.js
            - vendor.css
        - json/
            - master/
                - toc.json
                - types.json
                - index.json
                - overview.html
            - home.html
        - index.html
        - manifest.json
    """
    package_path = os.path.join(docs_build_dir, 'json_build')
    shutil.rmtree(package_path, ignore_errors=True)

    shutil.copytree(static_json_dir, package_path)
    shutil.copytree(os.path.join(generated_json_dir, 'gcloud'),
                    os.path.join(package_path, 'json', tag, 'gcloud'))
    shutil.copyfile(os.path.join(generated_json_dir, 'types.json'),
                    os.path.join(package_path, 'json', tag, 'types.json'))


def main():
    parser = argparse.ArgumentParser(description='Document Python modules.')
    parser.add_argument('--tag', help='The version of the documentation.',
                        default='master')
    parser.add_argument('--basepath', help='Path to the library.',
                        default=os.path.join(os.path.dirname(__file__), '..'))
    parser.add_argument('--show-toc', help='Prints partial table of contents',
                        default=False)
    args = parser.parse_args()

    toc = {
        'services': {
            '__init__': [],
            'gcloud': [],
            'bigquery': [],
            'bigtable': [],
            'client': [],
            'connection': [],
            'credentials': [],
            'datastore': [],
            'dns': [],
            'environment_vars': [],
            'error_reporting': [],
            'exceptions': [],
            'iterator': [],
            'language': [],
            'logging': [],
            'monitoring': [],
            'operation': [],
            'pubsub': [],
            'resource_manager': [],
            'storage': [],
            'streaming': [],
            'translate': [],
            'vision': [],
        }
    }

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    BASE_JSON_DOCS_DIR = os.path.join(BASE_DIR, 'docs', 'json')

    DOCS_BUILD_DIR = os.path.join(BASE_DIR, 'docs', '_build')
    JSON_DOCS_DIR = os.path.join(DOCS_BUILD_DIR, 'json', args.tag)
    LIB_DIR = os.path.abspath(args.basepath)

    library_dir = os.path.join(LIB_DIR, 'gcloud')
    public_mods = get_public_modules(library_dir, base_package='gcloud')

    generate_module_docs(public_mods, JSON_DOCS_DIR, BASE_DIR, toc)
    generate_doc_types_json(public_mods,
                            os.path.join(JSON_DOCS_DIR, 'types.json'))
    package_files(JSON_DOCS_DIR, DOCS_BUILD_DIR, BASE_JSON_DOCS_DIR)
    if args.show_toc:
        print json.dumps(toc, indent=4)

if __name__ == '__main__':
    main()
