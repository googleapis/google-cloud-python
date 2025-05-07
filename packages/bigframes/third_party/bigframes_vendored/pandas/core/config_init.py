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

display_options_doc = """
Encapsulates the configuration for displaying objects.

**Examples:**

Define Repr mode to "deferred" will prevent job execution in repr.

    >>> import bigframes.pandas as bpd
    >>> df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

    >>> bpd.options.display.repr_mode = "deferred"
    >>> df.head(20) # will no longer run the job
    Computation deferred. Computation will process 28.9 kB

Users can also get a dry run of the job by accessing the query_job property before they've run the job. This will return a dry run instance of the job they can inspect.

    >>> df.query_job.total_bytes_processed
    28947

User can execute the job by calling .to_pandas()

    >>> # df.to_pandas()

Reset repr_mode option

    >>> bpd.options.display.repr_mode = "head"

Can also set the progress_bar option to see the progress bar in terminal,

    >>> bpd.options.display.progress_bar = "terminal"

notebook,

    >>> bpd.options.display.progress_bar = "notebook"

or just remove it.

    >>> bpd.options.display.progress_bar = None

Setting to default value "auto" will detect and show progress bar automatically.

    >>> bpd.options.display.progress_bar = "auto"

Attributes:
    max_columns (int, default 20):
        If `max_columns` is exceeded, switch to truncate view.
    max_rows (int, default 25):
        If `max_rows` is exceeded, switch to truncate view.
    progress_bar (Optional(str), default "auto"):
        Determines if progress bars are shown during job runs.
        Valid values are `auto`, `notebook`, and `terminal`. Set
        to `None` to remove progress bars.
    repr_mode (Literal[`head`, `deferred`]):
        `head`:
            Execute, download, and display results (limited to head) from
            Dataframe and Series objects during repr.
        `deferred`:
            Prevent executions from repr statements in DataFrame and Series objects.
            Instead, estimated bytes processed will be shown. DataFrame and Series
            objects can still be computed with methods that explicitly execute and
            download results.
    max_info_columns (int):
        max_info_columns is used in DataFrame.info method to decide if
        information in each column will be printed.
    max_info_rows (int or None):
        df.info() will usually show null-counts for each column.
        For large frames, this can be quite slow. max_info_rows and max_info_cols
        limit this null check only to frames with smaller dimensions than
        specified.
    memory_usage (bool):
        This specifies if the memory usage of a DataFrame should be displayed when
        df.info() is called. Valid values True,False,
    blob_display (bool):
        Whether to display the blob content in notebook DataFrame preview. Default True.
    blob_display_width (int or None):
        Width in pixels that the blob constrained to.
    blob_display_height (int or None):
        Height in pixels that the blob constrained to.
"""

sampling_options_doc = """
Encapsulates the configuration for data sampling.

Attributes:
    max_download_size (int, default 500):
        Download size threshold in MB. If value set to None, the download size
        won't be checked.
    enable_downsampling (bool, default False):
        Whether to enable downsampling, If max_download_size is exceeded when
        downloading data (e.g., to_pandas()), the data will be downsampled
        if enable_downsampling is True, otherwise, an error will be raised.
    sampling_method (str, default "uniform"):
        Downsampling algorithms to be chosen from, the choices are:
        "head": This algorithm returns a portion of the data from
        the beginning. It is fast and requires minimal computations
        to perform the downsampling.; "uniform": This algorithm returns
        uniform random samples of the data.
    random_state (int, default None):
        The seed for the uniform downsampling algorithm. If provided,
        the uniform method may take longer to execute and require more
        computation.
"""
