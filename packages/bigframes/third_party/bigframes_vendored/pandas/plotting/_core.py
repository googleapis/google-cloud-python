import typing

from bigframes import constants


class PlotAccessor:
    """
    Make plots of Series or DataFrame with the `matplotlib` backend.

    **Examples:**
    For Series:

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.progress_bar = None
        >>> ser = bpd.Series([1, 2, 3, 3])
        >>> plot = ser.plot(kind='hist', title="My plot")

    For DataFrame:

        >>> df = bpd.DataFrame({'length': [1.5, 0.5, 1.2, 0.9, 3],
        ...                   'width': [0.7, 0.2, 0.15, 0.2, 1.1]},
        ...                   index=['pig', 'rabbit', 'duck', 'chicken', 'horse'])
        >>> plot = df.plot(title="DataFrame Plot")

    Args:
        data (Series or DataFrame):
            The object for which the method is called.
        kind (str):
            The kind of plot to produce:

            - 'line' : line plot (default)
            - 'hist' : histogram
            - 'area' : area plot
            - 'scatter' : scatter plot (DataFrame only)

        **kwargs:
            Options to pass to `pandas.DataFrame.plot` method. See pandas
            documentation online for more on these arguments.

    Returns:
            matplotlib.axes.Axes or np.ndarray of them:
                An ndarray is returned with one :class:`matplotlib.axes.Axes`
                per column when ``subplots=True``.
    """

    def hist(
        self, by: typing.Optional[typing.Sequence[str]] = None, bins: int = 10, **kwargs
    ):
        """
        Draw one histogram of the DataFrame’s columns.

        A histogram is a representation of the distribution of data.
        This function groups the values of all given Series in the DataFrame
        into bins and draws all bins in one :class:`matplotlib.axes.Axes`.
        This is useful when the DataFrame's Series are in a similar scale.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame(np.random.randint(1, 7, 6000), columns=['one'])
            >>> df['two'] = np.random.randint(1, 7, 6000) + np.random.randint(1, 7, 6000)
            >>> ax = df.plot.hist(bins=12, alpha=0.5)

        Args:
            by (str or sequence, optional):
                Column in the DataFrame to group by. It is not supported yet.
            bins (int, default 10):
                Number of histogram bins to be used.
            **kwargs:
                Additional keyword arguments are documented in
                :meth:`DataFrame.plot`.

        Returns:
            class:`matplotlib.AxesSubplot`: A histogram plot.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def line(
        self,
        x: typing.Optional[typing.Hashable] = None,
        y: typing.Optional[typing.Hashable] = None,
        **kwargs,
    ):
        """
        Plot Series or DataFrame as lines. This function is useful to plot lines
        using DataFrame's values as coordinates.

        This function calls `pandas.plot` to generate a plot with a random sample
        of items. For consistent results, the random sampling is reproducible.
        Use the `sampling_random_state` parameter to modify the sampling seed.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame(
            ...     {
            ...         'one': [1, 2, 3, 4],
            ...         'three': [3, 6, 9, 12],
            ...         'reverse_ten': [40, 30, 20, 10],
            ...     }
            ... )
            >>> ax = df.plot.line(x='one')

        Args:
            x (label or position, optional):
                Allows plotting of one column versus another. If not specified,
                the index of the DataFrame is used.
            y (label or position, optional):
                Allows plotting of one column versus another. If not specified,
                all numerical columns are used.
            color (str, array-like, or dict, optional):
                The color for each of the DataFrame's columns. Possible values are:

                - A single color string referred to by name, RGB or RGBA code,
                    for instance 'red' or '#a98d19'.

                - A sequence of color strings referred to by name, RGB or RGBA
                    code, which will be used for each column recursively. For
                    instance ['green','yellow'] each column's %(kind)s will be filled in
                    green or yellow, alternatively. If there is only a single column to
                    be plotted, then only the first color from the color list will be
                    used.

                - A dict of the form {column name : color}, so that each column will be
                    colored accordingly. For example, if your columns are called `a` and
                    `b`, then passing {'a': 'green', 'b': 'red'} will color %(kind)ss for
                    column `a` in green and %(kind)ss for column `b` in red.
            sampling_n (int, default 100):
                Number of random items for plotting.
            sampling_random_state (int, default 0):
                Seed for random number generator.
            **kwargs:
                Additional keyword arguments are documented in
                :meth:`DataFrame.plot`.

        Returns:
            matplotlib.axes.Axes or np.ndarray of them:
                An ndarray is returned with one :class:`matplotlib.axes.Axes`
                per column when ``subplots=True``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def area(
        self,
        x: typing.Optional[typing.Hashable] = None,
        y: typing.Optional[typing.Hashable] = None,
        stacked: bool = True,
        **kwargs,
    ):
        """
        Draw a stacked area plot. An area plot displays quantitative data visually.

        This function calls `pandas.plot` to generate a plot with a random sample
        of items. For consistent results, the random sampling is reproducible.
        Use the `sampling_random_state` parameter to modify the sampling seed.

        **Examples:**

        Draw an area plot based on basic business metrics:

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame(
            ...     {
            ...         'sales': [3, 2, 3, 9, 10, 6],
            ...         'signups': [5, 5, 6, 12, 14, 13],
            ...         'visits': [20, 42, 28, 62, 81, 50],
            ...     },
            ...     index=["01-31", "02-28", "03-31", "04-30", "05-31", "06-30"]
            ... )
            >>> ax = df.plot.area()

        Area plots are stacked by default. To produce an unstacked plot,
        pass ``stacked=False``:

            >>> ax = df.plot.area(stacked=False)

        Draw an area plot for a single column:

            >>> ax = df.plot.area(y='sales')

        Draw with a different `x`:

            >>> df = bpd.DataFrame({
            ...     'sales': [3, 2, 3],
            ...     'visits': [20, 42, 28],
            ...     'day': [1, 2, 3],
            ... })
            >>> ax = df.plot.area(x='day')

        Args:
            x (label or position, optional):
                Coordinates for the X axis. By default uses the index.
            y (label or position, optional):
                Column to plot. By default uses all columns.
            stacked (bool, default True):
                Area plots are stacked by default. Set to False to create a
                unstacked plot.
            sampling_n (int, default 100):
                Number of random items for plotting.
            sampling_random_state (int, default 0):
                Seed for random number generator.
            **kwargs:
                Additional keyword arguments are documented in
                :meth:`DataFrame.plot`.

        Returns:
            matplotlib.axes.Axes or numpy.ndarray:
                Area plot, or array of area plots if subplots is True.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def bar(
        self,
        x: typing.Optional[typing.Hashable] = None,
        y: typing.Optional[typing.Hashable] = None,
        **kwargs,
    ):
        """
        Draw a vertical bar plot.

        This function calls `pandas.plot` to generate a plot with a random sample
        of items. For consistent results, the random sampling is reproducible.
        Use the `sampling_random_state` parameter to modify the sampling seed.

        **Examples:**

        Basic plot.

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
            >>> ax = df.plot.bar(x='lab', y='val', rot=0)

        Plot a whole dataframe to a bar plot. Each column is assigned a distinct color,
        and each row is nested in a group along the horizontal axis.

            >>> speed = [0.1, 17.5, 40, 48, 52, 69, 88]
            >>> lifespan = [2, 8, 70, 1.5, 25, 12, 28]
            >>> index = ['snail', 'pig', 'elephant',
            ...          'rabbit', 'giraffe', 'coyote', 'horse']
            >>> df = bpd.DataFrame({'speed': speed, 'lifespan': lifespan}, index=index)
            >>> ax = df.plot.bar(rot=0)

        Plot stacked bar charts for the DataFrame.

            >>> ax = df.plot.bar(stacked=True)

        If you don’t like the default colours, you can specify how you’d like each column
        to be colored.

            >>> axes = df.plot.bar(
            ...     rot=0, subplots=True, color={"speed": "red", "lifespan": "green"}
            ... )

        Args:
            x (label or position, optional):
                Allows plotting of one column versus another. If not specified, the index
                of the DataFrame is used.
            y (label or position, optional):
                Allows plotting of one column versus another. If not specified, all numerical
                columns are used.
            **kwargs:
                Additional keyword arguments are documented in
                :meth:`DataFrame.plot`.

        Returns:
            matplotlib.axes.Axes or numpy.ndarray:
                Area plot, or array of area plots if subplots is True.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def scatter(
        self,
        x: typing.Optional[typing.Hashable] = None,
        y: typing.Optional[typing.Hashable] = None,
        s: typing.Union[typing.Hashable, typing.Sequence[typing.Hashable]] = None,
        c: typing.Union[typing.Hashable, typing.Sequence[typing.Hashable]] = None,
        **kwargs,
    ):
        """
        Create a scatter plot with varying marker point size and color.

        This function calls `pandas.plot` to generate a plot with a random sample
        of items. For consistent results, the random sampling is reproducible.
        Use the `sampling_random_state` parameter to modify the sampling seed.

        **Examples:**

        Let's see how to draw a scatter plot using coordinates from the values
        in a DataFrame's columns.

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame([[5.1, 3.5, 0], [4.9, 3.0, 0], [7.0, 3.2, 1],
            ...                    [6.4, 3.2, 1], [5.9, 3.0, 2]],
            ...                   columns=['length', 'width', 'species'])
            >>> ax1 = df.plot.scatter(x='length',
            ...                       y='width',
            ...                       c='DarkBlue')

        And now with the color determined by a column as well.

            >>> ax2 = df.plot.scatter(x='length',
            ...                       y='width',
            ...                       c='species',
            ...                       colormap='viridis')

        Args:
            x (int or str):
                The column name or column position to be used as horizontal
                coordinates for each point.
            y (int or str):
                The column name or column position to be used as vertical
                coordinates for each point.
            s (str, scalar or array-like, optional):
                The size of each point. Possible values are:

                - A string with the name of the column to be used for marker's size.
                - A single scalar so all points have the same size.

            c (str, int or array-like, optional):
                The color of each point. Possible values are:

                - A single color string referred to by name, RGB or RGBA code,
                  for instance 'red' or '#a98d19'.
                - A column name or position whose values will be used to color the
                  marker points according to a colormap.

            sampling_n (int, default 100):
                Number of random items for plotting.
            sampling_random_state (int, default 0):
                Seed for random number generator.
            **kwargs:
                Additional keyword arguments are documented in
                :meth:`DataFrame.plot`.

        Returns:
            matplotlib.axes.Axes or np.ndarray of them:
                An ndarray is returned with one :class:`matplotlib.axes.Axes`
                per column when ``subplots=True``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
