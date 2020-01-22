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

import textwrap
from typing import Iterable


def sort_lines(text: str, dedupe: bool = True) -> str:
    """Sort the individual lines of a block of text.

    Args:
        dedupe (bool): Remove duplicate lines with the same text.
            Useful for dealing with import statements in templates.
    """
    # Preserve leading or trailing newlines.
    leading = '\n' if text.startswith('\n') else ''
    trailing = '\n' if text.endswith('\n') else ''

    # Split the text into individual lines, throwing away any empty lines.
    lines: Iterable[str] = (i for i in text.strip().split('\n') if i.strip())

    # De-duplicate the lines if requested.
    if dedupe:
        lines = set(lines)

    # Return the final string.
    answer = '\n'.join(sorted(lines))
    return f'{leading}{answer}{trailing}'


def wrap(text: str, width: int, *, offset: int = None, indent: int = 0) -> str:
    """Wrap the given string to the given width.

    This uses :meth:`textwrap.fill` under the hood, but provides useful
    offset functionality for Jinja templates.

    This is provided to all templates as the ``wrap`` filter.

    Args:
        text (str): The initial text string.
        width (int): The width at which to wrap the text. If offset is
            provided, these are automatically counted against this.
        offset (int): The offset for the first line of text.
            This value is subtracted from ``width`` for the first line
            only, and is intended to represent the vertical position of
            the first line as already present in the template.
            Defaults to the value of ``indent``.
        indent (int): The number of spaces to indent all lines after the
            first one.

    Returns:
        str: The wrapped string.
    """
    # Sanity check: If there is empty text, abort.
    if not text:
        return ''

    # If the offset is None, default it to the indent value.
    if offset is None:
        offset = indent

    # Protocol buffers preserves single initial spaces after line breaks
    # when parsing comments (such as the space before the "w" in "when" here).
    # Re-wrapping causes these to be two spaces; correct for this.
    text = text.replace('\n ', '\n')

    # Break off the first line of the string to address non-zero offsets.
    first = text.split('\n')[0] + '\n'
    if len(first) > width - offset:
        initial = textwrap.wrap(first,
                                break_long_words=False,
                                width=width - offset,
                                )
        # Strip the first \n from the text so it is not misidentified as an
        # intentionally short line below.
        text = text.replace('\n', ' ', 1)

        # Save the new `first` line.
        first = f'{initial[0]}\n'
    text = text[len(first):].strip()
    if not text:
        return first.strip()

    # Tokenize the rest of the text to try to preserve line breaks
    # that semantically matter.
    tokens = []
    token = ''
    for line in text.split('\n'):
        token += line + '\n'
        if len(line) < width * 0.75:
            tokens.append(token)
            token = ''
    if token:
        tokens.append(token)

    # Wrap the remainder of the string at the desired width.
    return '{first}{text}'.format(
        first=first,
        text='\n'.join([textwrap.fill(
            break_long_words=False,
            initial_indent=' ' * indent,
            subsequent_indent=' ' * indent,
            text=token,
            width=width,
        ) for token in tokens]),
    ).rstrip('\n')
