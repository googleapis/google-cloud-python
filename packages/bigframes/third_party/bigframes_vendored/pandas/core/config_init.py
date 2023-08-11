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
Encapsulates configuration for displaying objects.

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
            dataframe and series objects during repr.
        `deferred`:
            Prevent executions from repr statements in dataframe and series objects.
            Instead estimated bytes processed will be shown. Dataframe and Series
            objects can still be computed with methods that explicitly execute and
            download results.
"""

sampling_options_doc = """
Encapsulates configuration for data sampling.

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
