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

import re
from docutils.io import StringOutput
from docutils.utils import new_document
from docutils import nodes
from inspect import signature
from collections import namedtuple

from .writer import MarkdownWriter as Writer


def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.

    # From Django
    """
    value = re.sub('[^\w\s-]', '', value).strip()
    return re.sub('[-\s]+', '-', value)


def transform_string(app, string):
    ret = []
    for para in string.split('\n\n'):
        tmp = nodes.paragraph(para, para)
        ret.append(transform_node(app, tmp))
    return '\n\n'.join(ret)


def transform_node(app, node):
    destination = StringOutput(encoding='utf-8')
    doc = new_document(b'<partial node>')
    doc.append(node)

    # Resolve refs
    doc['docname'] = 'inmemory'
    app.env.resolve_references(doctree=doc, fromdocname='inmemory', builder=app.builder)

    writer = Writer(app.builder)
    writer.write(doc, destination)
    return destination.destination.decode('utf-8')
