# Copyright 2019 Google LLC
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

from typing import Tuple
import dataclasses
import os
import warnings


@dataclasses.dataclass(frozen=True)
class Options:
    """A representation of CLI options passed through protoc.

    To maximize interoperability with other languages, we are permissive
    on unrecognized arguments (essentially, we throw them away, but we do
    warn if it looks like it was meant for us).
    """
    templates: Tuple[str]

    @classmethod
    def build(cls, opt_string: str) -> 'Options':
        """Build an Options instance based on a protoc opt string.

        Args:
            opt_string (str): A string, as passed from the protoc interface
                (through ``--python_gapic_opt``). If multiple options are
                passed, then protoc joins the values with ``,``.
                By convention, we use ``key=value`` strings for such
                options, with an absent value defaulting to ``True``.

        Returns:
            ~.Options: The Options instance.
        """
        # Parse out every option beginning with `python-gapic`
        opts = {}
        for opt in opt_string.split(','):
            # Parse out the key and value.
            value = True
            if '=' in opt:
                opt, value = opt.split('=')

            # Throw away options not meant for us.
            if not opt.startswith('python-gapic-'):
                continue

            # Set the option.
            # Just assume everything is a list at this point, and the
            # final instantiation step can de-list-ify where appropriate.
            opts.setdefault(opt, [])
            opts[opt].append(value)

        # If templates are specified, one of the specified directories
        # may be our default; perform that replacement.
        templates = opts.pop('python-gapic-templates', ['DEFAULT'])
        while 'DEFAULT' in templates:
            templates[templates.index('DEFAULT')] = os.path.realpath(
                os.path.join(os.path.dirname(__file__), '..', 'templates'),
            )

        # Build the options instance.
        answer = Options(
            templates=tuple([os.path.expanduser(i) for i in templates]),
        )

        # If there are any options remaining, then we failed to recognize
        # them -- complain.
        for key in opts.keys():
            warnings.warn(f'Unrecognized option: `{key}`.')

        # Done; return the built options.
        return answer
