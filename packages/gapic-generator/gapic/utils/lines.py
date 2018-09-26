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
    first = ''
    if offset > 0:
        initial = textwrap.wrap(text,
            break_long_words=False,
            width=width - offset,
        )
        first = f'{initial[0]}\n'
        text = ' '.join(initial[1:])

    # Wrap the remainder of the string at the desired width.
    return '{first}{text}'.format(
        first=first,
        text=textwrap.fill(
            break_long_words=False,
            initial_indent=' ' * indent if first else '',
            subsequent_indent=' ' * indent,
            text=text,
            width=width,
        ),
    ).rstrip('\n')
