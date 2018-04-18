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


def subsequent_indent(text: str, prefix: str) -> str:
    """Decorates the text string with the given prefix on hanging lines.

    A "hanging" line is any line except for the first one. After prefixing,
    if any lines end in whitespace, that whitespace is stripped.

    This is provided to all templates as the ``subsequent_indent`` filter.

    Args:
        text (str): The text string.
        prefix (str): The prefix to use.

    Returns:
        str: The string with all hanging lines prefixed.
    """
    lines = text.split('\n')
    lines[1:] = [f'{prefix}{s}'.rstrip() for s in lines[1:]]
    return '\n'.join(lines)


def wrap(text: str, width: int, initial_width: int = None,
         subsequent_indent: str = '', antecedent_trailer: str = '') -> str:
    """Wrap the given string to the given width.

    This uses :meth:`textwrap.fill` under the hood, but provides functionality
    for the initial width, as well as a common line ending for every line
    but the last.

    This is provided to all templates as the ``wrap`` filter.

    Args:
        text (str): The initial text string.
        width (int): The width at which to wrap the text. If either
            ``subsequent_indent`` or ``antecedent_trailer`` are provided,
            their width will be automatically counted against this.
        initial_width (int): Optional. The width of the first line, if
            different. Defaults to the value of ``width``.
        subsequent_indent (str): A string to be prepended to every line
            except the first.
        antecedent_trailer (str): A string to be appended to every line
            except the last.

    Returns:
        str: The wrapped string.
    """
    initial_width = initial_width or width

    # Sanity check: If there is empty text, abort.
    if not text:
        return ''

    # Reduce the values by the length of the trailing string, if any.
    width -= len(antecedent_trailer)
    initial_width -= len(antecedent_trailer)

    # If the initial width is different, break off the beginning of the
    # string.
    first = ''
    if initial_width != width:
        initial = textwrap.wrap(text, width=initial_width)
        first = f'{initial[0]}\n'
        text = ' '.join(initial[1:])

        # Sanity check: If that was the only line, abort here, *without*
        # the antecedent trailer.
        if not text:
            return initial[0]

    # Wrap the remainder of the string at the desired width.
    text = first + textwrap.fill(
        initial_indent=subsequent_indent if first else '',
        subsequent_indent=subsequent_indent,
        text=text,
        width=width,
    )

    # Replace all the line endings with the antecedent trailer,
    # and return the resulting string.
    return text.replace('\n', f'{antecedent_trailer}\n')
