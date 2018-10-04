# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

import pypandoc

from gapic.utils.lines import wrap


def rst(text, width=72, indent=0, source_format='commonmark'):
    """Convert the given text to ReStructured Text.

    Args:
        text (str): The text to convert.
        width (int): The number of columns.
        source_format (str): The source format. This is ``commonmark`` by
            default, which is what is used by convention in protocol buffers.

    Returns:
        str: The same text, in RST format.
    """
    # Sanity check: If the text block does not appear to have any formatting,
    # do not convert it.
    # (This makes code generation significantly faster; calling out to pandoc
    # is by far the most expensive thing we do.)
    if not re.search(r'[|*`_[\]]', text):
        answer = wrap(text, width=width, indent=indent, offset=indent + 3)
    else:
        # Convert from CommonMark to ReStructured Text.
        answer = pypandoc.convert_text(text, 'rst',
            format=source_format,
            extra_args=['--columns=%d' % width],
        ).strip().replace('\n', f"\n{' ' * indent}")

    # Add a newline to the end of the document if any line breaks are
    # already present.
    #
    # This causes the closing """ to be on the subsequent line only when
    # appropriate.
    if '\n' in answer:
        answer += '\n' + ' ' * indent

    # Done; return the answer.
    return answer
