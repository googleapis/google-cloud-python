# Copyright 2026 Google LLC
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

from IPython.core import magic_arguments  # type: ignore
from IPython.core.getipython import get_ipython
from IPython.display import display

import bigframes.pandas


@magic_arguments.magic_arguments()
@magic_arguments.argument(
    "destination_var",
    nargs="?",
    help=("If provided, save the output to this variable instead of displaying it."),
)
@magic_arguments.argument(
    "--dry_run",
    action="store_true",
    default=False,
    help=(
        "Sets query to be a dry run to estimate costs. "
        "Defaults to executing the query instead of dry run if this argument is not used."
        "Does not work with engine 'bigframes'. "
    ),
)
def _cell_magic(line, cell):
    ipython = get_ipython()
    args = magic_arguments.parse_argstring(_cell_magic, line)
    if not cell:
        print("Query is missing.")
        return
    pyformat_args = ipython.user_ns
    dataframe = bigframes.pandas._read_gbq_colab(
        cell, pyformat_args=pyformat_args, dry_run=args.dry_run
    )
    if args.destination_var:
        ipython.push({args.destination_var: dataframe})
    else:
        with bigframes.option_context(
            "display.repr_mode",
            "anywidget",
        ):
            display(dataframe)
    return
