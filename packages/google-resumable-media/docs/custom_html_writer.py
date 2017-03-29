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

"""Custom HTML builder.

This is used to verify that snippets do not get stale.

See http://www.sphinx-doc.org/en/stable/extdev/tutorial.html to learn
how to write a custom Sphinx extension.
"""

from sphinx import errors
from sphinx.writers import html


_LITERAL_ERR_TEMPLATE = """\
All literal blocks must either be used for doctest or explicitly
declared as a language other than Python. Current node:

{}

has combination of language ({!r}) and test node type ({!r}) which
are not allowed.
"""


class CustomHTMLWriter(html.SmartyPantsHTMLTranslator):
    """Custom HTML writer.

    This makes sure that code blocks are all tested. It does this by
    asserting that a code block has a language other than Python **OR**
    that the code block has test node type ``doctest``.
    """

    def visit_literal_block(self, node):
        """Visit a ``literal_block`` node.

        This verifies the state of each literal / code block.
        """
        language = node.attributes.get('language', '')
        test_type = node.attributes.get('testnodetype', '')
        if test_type != 'doctest':
            if language.lower() in ('', 'python'):
                msg = _LITERAL_ERR_TEMPLATE.format(
                    node.rawsource, language, test_type)
                raise errors.ExtensionError(msg)
        # The base classes are not new-style, so we can't use super().
        return html.SmartyPantsHTMLTranslator.visit_literal_block(self, node)


def setup(app):
    """Set-up this extension.

    Args:
        app (sphinx.application.Sphinx): A running Sphinx app.
    """
    app.set_translator('html', CustomHTMLWriter)
