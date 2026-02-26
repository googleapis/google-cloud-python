# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/config_init.py
"""
This module is imported from the pandas package __init__.py file
in order to ensure that the core.config options registered here will
be available as soon as the user loads the package. if register_option
is invoked inside specific modules, they will not be registered until that
module is imported, which may or may not be a problem.

If you need to make sure options are available even before a certain
module is imported, register them here rather than in the module.

"""

from __future__ import annotations

import dataclasses
from typing import Literal, Optional


@dataclasses.dataclass
class DisplayOptions:
    """
    Encapsulates the configuration for displaying objects.

    **Examples:**

    Define Repr mode to "deferred" will prevent job execution in repr.

        >>> import bigframes.pandas as bpd
        >>> df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

        >>> bpd.options.display.repr_mode = "deferred"  # doctest: +SKIP
        >>> df.head(20) # will no longer run the job  # doctest: +SKIP
        Computation deferred. Computation will process 28.9 kB

    Users can also get a dry run of the job by accessing the query_job property before they've run the job. This will return a dry run instance of the job they can inspect.

        >>> df.query_job.total_bytes_processed  # doctest: +SKIP
        28947

    User can execute the job by calling .to_pandas()

        >>> # df.to_pandas()

    Reset repr_mode option

        >>> bpd.options.display.repr_mode = "head"  # doctest: +SKIP

    Can also set the progress_bar option to see the progress bar in terminal,

        >>> bpd.options.display.progress_bar = "terminal"  # doctest: +SKIP

    notebook,

        >>> bpd.options.display.progress_bar = "notebook"  # doctest: +SKIP

    or just remove it.

    Setting to default value "auto" will detect and show progress bar automatically.

        >>> bpd.options.display.progress_bar = "auto"  # doctest: +SKIP
    """

    # Options borrowed from pandas.
    max_columns: int = 20
    """
    Maximum number of columns to display. Default 20.

    If `max_columns` is exceeded, switch to truncate view.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.max_columns = 50  # doctest: +SKIP
    """

    max_rows: int = 10
    """
    Maximum number of rows to display. Default 10.

    If `max_rows` is exceeded, switch to truncate view.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.max_rows = 50  # doctest: +SKIP
    """

    precision: int = 6
    """
    Controls the floating point output precision. Defaults to 6.

    See :attr:`pandas.options.display.precision`.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.precision = 2  # doctest: +SKIP
    """

    # Options unique to BigQuery DataFrames.
    progress_bar: Optional[str] = "auto"
    """
    Determines if progress bars are shown during job runs. Default "auto".

    Valid values are `auto`, `notebook`, and `terminal`. Set
    to `None` to remove progress bars.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.progress_bar = "terminal"  # doctest: +SKIP
    """

    repr_mode: Literal["head", "deferred", "anywidget"] = "head"
    """
    Determines how to display a DataFrame or Series. Default "head".

    `head`
        Execute, download, and display results (limited to head) from
        Dataframe and Series objects during repr.

    `deferred`
        Prevent executions from repr statements in DataFrame and Series objects.
        Instead, estimated bytes processed will be shown. DataFrame and Series
        objects can still be computed with methods that explicitly execute and
        download results.

    `anywidget`
        Display as interactive widget using `anywidget` library.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.repr_mode = "deferred"  # doctest: +SKIP
    """

    render_mode: Literal["plaintext", "html", "anywidget"] = "html"
    """
    Determines how to visualize a DataFrame or Series. Default "html".

    `plaintext`
        Display as plain text.

    `html`
        Display as HTML table.

    `anywidget`
        Display as interactive widget using `anywidget` library.
    """

    max_colwidth: Optional[int] = 50
    """
    The maximum width in characters of a column in the repr. Default 50.

    When the column overflows, a "..." placeholder is embedded in the output. A
    'None' value means unlimited.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.max_colwidth = 20  # doctest: +SKIP
    """

    max_info_columns: int = 100
    """
    Used in DataFrame.info method to decide if information in each column will
    be printed. Default 100.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.max_info_columns = 50  # doctest: +SKIP
    """

    max_info_rows: Optional[int] = 200_000
    """
    Limit null check in ``df.info()`` only to frames with smaller dimensions than
    max_info_rows. Default 200,000.

    df.info() will usually show null-counts for each column.
    For large frames, this can be quite slow. max_info_rows and max_info_cols
    limit this null check only to frames with smaller dimensions than
    specified.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.max_info_rows = 100  # doctest: +SKIP
    """

    memory_usage: bool = True
    """
    If True, memory usage of a DataFrame should be displayed when
    df.info() is called. Default True.

    Valid values True, False.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.memory_usage = False  # doctest: +SKIP
    """

    blob_display: bool = True
    """
    If True, display the blob content in notebook DataFrame preview. Default
    True.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.blob_display = True  # doctest: +SKIP
    """

    blob_display_width: Optional[int] = None
    """
    Width in pixels that the blob constrained to. Default None..

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.blob_display_width = 100  # doctest: +SKIP
    """
    blob_display_height: Optional[int] = None
    """
    Height in pixels that the blob constrained to. Default None..

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.blob_display_height = 100  # doctest: +SKIP
    """
