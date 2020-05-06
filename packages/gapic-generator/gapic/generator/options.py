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

from collections import defaultdict
from os import path
from typing import Any, DefaultDict, Dict, FrozenSet, List, Optional, Tuple

import dataclasses
import json
import os
import warnings

from gapic.samplegen_utils import utils as samplegen_utils


@dataclasses.dataclass(frozen=True)
class Options:
    """A representation of CLI options passed through protoc.

    To maximize interoperability with other languages, we are permissive
    on unrecognized arguments (essentially, we throw them away, but we do
    warn if it looks like it was meant for us).
    """
    name: str = ''
    namespace: Tuple[str, ...] = dataclasses.field(default=())
    retry: Optional[Dict[str, Any]] = None
    sample_configs: Tuple[str, ...] = dataclasses.field(default=())
    templates: Tuple[str, ...] = dataclasses.field(default=('DEFAULT',))
    lazy_import: bool = False
    old_naming: bool = False

    # Class constants
    PYTHON_GAPIC_PREFIX: str = 'python-gapic-'
    OPT_FLAGS: FrozenSet[str] = frozenset((
        'old-naming',           # TODO(dovs): Come up with a better comment
        'retry-config',         # takes a path
        'samples',              # output dir
        'lazy-import',          # requires >= 3.7
    ))

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

        Raises:
            gapic.samplegen_utils.types.InvalidConfig:
                If paths to files or directories that should contain sample
                configs are passed and no valid sample config is found.
        """
        # Parse out every option beginning with `python-gapic`
        opts: DefaultDict[str, List[str]] = defaultdict(list)
        for opt in opt_string.split(','):
            opt = opt.strip()
            # Parse out the key and value.
            value = 'true'
            if '=' in opt:
                opt, value = opt.split('=')

            # Save known, expected keys.
            if opt in cls.OPT_FLAGS:
                opts[opt].append(value)

            # Throw away other options not meant for us.
            if not opt.startswith(cls.PYTHON_GAPIC_PREFIX):
                continue

            # Set the option, using a key with the "python-gapic-" prefix
            # stripped.
            #
            # Just assume everything is a list at this point, and the
            # final instantiation step can de-list-ify where appropriate.
            opts[opt[len(cls.PYTHON_GAPIC_PREFIX):]].append(value)

        # If templates are specified, one of the specified directories
        # may be our default; perform that replacement.
        default_token = 'DEFAULT'
        templates = opts.pop('templates', [default_token])
        pwd = path.join(path.dirname(__file__), '..')
        default_path = path.realpath(path.join(pwd, 'templates'))

        def tweak_path(p):
            if p == default_token:
                return default_path

            if path.isabs(p):
                return path.normpath(p)

            return path.normpath(path.join(pwd, p))

        templates = [tweak_path(p) for p in templates]

        retry_cfg = None
        retry_paths = opts.pop('retry-config', None)
        if retry_paths:
            # Just use the last config specified.
            with open(retry_paths[-1]) as f:
                retry_cfg = json.load(f)

        # Build the options instance.
        sample_paths = opts.pop('samples', [])
        answer = Options(
            name=opts.pop('name', ['']).pop(),
            namespace=tuple(opts.pop('namespace', [])),
            retry=retry_cfg,
            sample_configs=tuple(
                cfg_path
                for s in sample_paths
                for cfg_path in samplegen_utils.generate_all_sample_fpaths(s)
            ),
            templates=tuple(path.expanduser(i) for i in templates),
            lazy_import=bool(opts.pop('lazy-import', False)),
            old_naming=bool(opts.pop('old-naming', False)),
        )

        # Note: if we ever need to recursively check directories for sample
        # configs, check that at least _one_ config is read in.

        # If there are any options remaining, then we failed to recognize
        # them -- complain.
        for key in opts.keys():
            warnings.warn(f'Unrecognized option: `python-gapic-{key}`.')

        # Done; return the built options.
        return answer
