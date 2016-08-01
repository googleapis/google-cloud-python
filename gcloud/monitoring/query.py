# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Time series query for the `Google Stackdriver Monitoring API (V3)`_.

.. _Google Stackdriver Monitoring API (V3):
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
    projects.timeSeries/list
"""

import copy
import datetime
import itertools

import six

from gcloud._helpers import _datetime_to_rfc3339
from gcloud.monitoring._dataframe import _build_dataframe
from gcloud.monitoring.timeseries import TimeSeries

_UTCNOW = datetime.datetime.utcnow  # To be replaced by tests.


class Aligner(object):
    """Allowed values for the `supported aligners`_."""

    ALIGN_NONE = 'ALIGN_NONE'
    ALIGN_DELTA = 'ALIGN_DELTA'
    ALIGN_RATE = 'ALIGN_RATE'
    ALIGN_INTERPOLATE = 'ALIGN_INTERPOLATE'
    ALIGN_NEXT_OLDER = 'ALIGN_NEXT_OLDER'
    ALIGN_MIN = 'ALIGN_MIN'
    ALIGN_MAX = 'ALIGN_MAX'
    ALIGN_MEAN = 'ALIGN_MEAN'
    ALIGN_COUNT = 'ALIGN_COUNT'
    ALIGN_SUM = 'ALIGN_SUM'
    ALIGN_STDDEV = 'ALIGN_STDDEV'
    ALIGN_COUNT_TRUE = 'ALIGN_COUNT_TRUE'
    ALIGN_FRACTION_TRUE = 'ALIGN_FRACTION_TRUE'


class Reducer(object):
    """Allowed values for the `supported reducers`_."""

    REDUCE_NONE = 'REDUCE_NONE'
    REDUCE_MEAN = 'REDUCE_MEAN'
    REDUCE_MIN = 'REDUCE_MIN'
    REDUCE_MAX = 'REDUCE_MAX'
    REDUCE_SUM = 'REDUCE_SUM'
    REDUCE_STDDEV = 'REDUCE_STDDEV'
    REDUCE_COUNT = 'REDUCE_COUNT'
    REDUCE_COUNT_TRUE = 'REDUCE_COUNT_TRUE'
    REDUCE_FRACTION_TRUE = 'REDUCE_FRACTION_TRUE'
    REDUCE_PERCENTILE_99 = 'REDUCE_PERCENTILE_99'
    REDUCE_PERCENTILE_95 = 'REDUCE_PERCENTILE_95'
    REDUCE_PERCENTILE_50 = 'REDUCE_PERCENTILE_50'
    REDUCE_PERCENTILE_05 = 'REDUCE_PERCENTILE_05'


class Query(object):
    """Query object for retrieving metric data.

    The preferred way to construct a query object is using the
    :meth:`~gcloud.monitoring.client.Client.query` method
    of the :class:`~gcloud.monitoring.client.Client` class.

    :type client: :class:`gcloud.monitoring.client.Client`
    :param client: The client to use.

    :type metric_type: string
    :param metric_type: The metric type name. The default value is
        :data:`Query.DEFAULT_METRIC_TYPE
        <gcloud.monitoring.query.Query.DEFAULT_METRIC_TYPE>`,
        but please note that this default value is provided only for
        demonstration purposes and is subject to change. See the
        `supported metrics`_.

    :type end_time: :class:`datetime.datetime` or None
    :param end_time: The end time (inclusive) of the time interval
        for which results should be returned, as a datetime object.
        The default is the start of the current minute.

        The start time (exclusive) is determined by combining the
        values of  ``days``, ``hours``, and ``minutes``, and
        subtracting the resulting duration from the end time.

        It is also allowed to omit the end time and duration here,
        in which case
        :meth:`~gcloud.monitoring.query.Query.select_interval`
        must be called before the query is executed.

    :type days: integer
    :param days: The number of days in the time interval.

    :type hours: integer
    :param hours: The number of hours in the time interval.

    :type minutes: integer
    :param minutes: The number of minutes in the time interval.

    :raises: :exc:`ValueError` if ``end_time`` is specified but
        ``days``, ``hours``, and ``minutes`` are all zero.
        If you really want to specify a point in time, use
        :meth:`~gcloud.monitoring.query.Query.select_interval`.

    .. _supported metrics: https://cloud.google.com/monitoring/api/metrics
    """

    DEFAULT_METRIC_TYPE = 'compute.googleapis.com/instance/cpu/utilization'

    def __init__(self, client,
                 metric_type=DEFAULT_METRIC_TYPE,
                 end_time=None, days=0, hours=0, minutes=0):
        start_time = None
        if days or hours or minutes:
            if end_time is None:
                end_time = _UTCNOW().replace(second=0, microsecond=0)
            start_time = end_time - datetime.timedelta(days=days,
                                                       hours=hours,
                                                       minutes=minutes)
        elif end_time is not None:
            raise ValueError('Non-zero duration required for time interval.')

        self._client = client
        self._end_time = end_time
        self._start_time = start_time
        self._filter = _Filter(metric_type)

        self._per_series_aligner = None
        self._alignment_period_seconds = None
        self._cross_series_reducer = None
        self._group_by_fields = ()

    def __iter__(self):
        return self.iter()

    @property
    def metric_type(self):
        """The metric type name."""
        return self._filter.metric_type

    @property
    def filter(self):
        """The filter string.

        This is constructed from the metric type, the resource type, and
        selectors for the group ID, monitored projects, resource labels,
        and metric labels.
        """
        return str(self._filter)

    def select_interval(self, end_time, start_time=None):
        """Copy the query and set the query time interval.

        Example::

            import datetime

            now = datetime.datetime.utcnow()
            query = query.select_interval(
                end_time=now,
                start_time=now - datetime.timedelta(minutes=5))

        As a convenience, you can alternatively specify the end time and
        an interval duration when you create the query initially.

        :type end_time: :class:`datetime.datetime`
        :param end_time: The end time (inclusive) of the time interval
            for which results should be returned, as a datetime object.

        :type start_time: :class:`datetime.datetime` or None
        :param start_time: The start time (exclusive) of the time interval
            for which results should be returned, as a datetime object.
            If not specified, the interval is a point in time.

        :rtype: :class:`Query`
        :returns: The new query object.
        """
        new_query = self.copy()
        new_query._end_time = end_time
        new_query._start_time = start_time
        return new_query

    def select_group(self, group_id):
        """Copy the query and add filtering by group.

        Example::

            query = query.select_group('1234567')

        :type group_id: string
        :param group_id: The ID of a group to filter by.

        :rtype: :class:`Query`
        :returns: The new query object.
        """
        new_query = self.copy()
        new_query._filter.group_id = group_id
        return new_query

    def select_projects(self, *args):
        """Copy the query and add filtering by monitored projects.

        This is only useful if the target project represents a Stackdriver
        account containing the specified monitored projects.

        Examples::

            query = query.select_projects('project-1')
            query = query.select_projects('project-1', 'project-2')

        :type args: tuple
        :param args: Project IDs limiting the resources to be included
            in the query.

        :rtype: :class:`Query`
        :returns: The new query object.
        """
        new_query = self.copy()
        new_query._filter.projects = args
        return new_query

    def select_resources(self, *args, **kwargs):
        """Copy the query and add filtering by resource labels.

        Examples::

            query = query.select_resources(zone='us-central1-a')
            query = query.select_resources(zone_prefix='europe-')
            query = query.select_resources(resource_type='gce_instance')

        A keyword argument ``<label>=<value>`` ordinarily generates a filter
        expression of the form::

            resource.label.<label> = "<value>"

        However, by adding ``"_prefix"`` or ``"_suffix"`` to the keyword,
        you can specify a partial match.

        ``<label>_prefix=<value>`` generates::

            resource.label.<label> = starts_with("<value>")

        ``<label>_suffix=<value>`` generates::

            resource.label.<label> = ends_with("<value>")

        As a special case, ``"resource_type"`` is treated as a special
        pseudo-label corresponding to the filter object ``resource.type``.
        For example, ``resource_type=<value>`` generates::

            resource.type = "<value>"

        See the `defined resource types`_.

        .. note::

            The label ``"instance_name"`` is a metric label,
            not a resource label. You would filter on it using
            ``select_metrics(instance_name=...)``.

        :type args: tuple
        :param args: Raw filter expression strings to include in the
            conjunction. If just one is provided and no keyword arguments
            are provided, it can be a disjunction.

        :type kwargs: dict
        :param kwargs: Label filters to include in the conjunction as
            described above.

        :rtype: :class:`Query`
        :returns: The new query object.

        .. _defined resource types:
            https://cloud.google.com/monitoring/api/v3/monitored-resources
        """
        new_query = self.copy()
        new_query._filter.select_resources(*args, **kwargs)
        return new_query

    def select_metrics(self, *args, **kwargs):
        """Copy the query and add filtering by metric labels.

        Examples::

            query = query.select_metrics(instance_name='myinstance')
            query = query.select_metrics(instance_name_prefix='mycluster-')

        A keyword argument ``<label>=<value>`` ordinarily generates a filter
        expression of the form::

            metric.label.<label> = "<value>"

        However, by adding ``"_prefix"`` or ``"_suffix"`` to the keyword,
        you can specify a partial match.

        ``<label>_prefix=<value>`` generates::

            metric.label.<label> = starts_with("<value>")

        ``<label>_suffix=<value>`` generates::

            metric.label.<label> = ends_with("<value>")

        :type args: tuple
        :param args: Raw filter expression strings to include in the
            conjunction. If just one is provided and no keyword arguments
            are provided, it can be a disjunction.

        :type kwargs: dict
        :param kwargs: Label filters to include in the conjunction as
            described above.

        :rtype: :class:`Query`
        :returns: The new query object.
        """
        new_query = self.copy()
        new_query._filter.select_metrics(*args, **kwargs)
        return new_query

    def align(self, per_series_aligner, seconds=0, minutes=0, hours=0):
        """Copy the query and add temporal alignment.

        If ``per_series_aligner`` is not :data:`Aligner.ALIGN_NONE`, each time
        series will contain data points only on the period boundaries.

        Example::

            query = query.align(Aligner.ALIGN_MEAN, minutes=5)

        It is also possible to specify the aligner as a literal string::

            query = query.align('ALIGN_MEAN', minutes=5)

        :type per_series_aligner: string
        :param per_series_aligner: The approach to be used to align
            individual time series. For example: :data:`Aligner.ALIGN_MEAN`.
            See :class:`Aligner` and the descriptions of the `supported
            aligners`_.

        :type seconds: integer
        :param seconds: The number of seconds in the alignment period.

        :type minutes: integer
        :param minutes: The number of minutes in the alignment period.

        :type hours: integer
        :param hours: The number of hours in the alignment period.

        :rtype: :class:`Query`
        :returns: The new query object.

        .. _supported aligners:
            https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
            projects.timeSeries/list#Aligner
        """
        new_query = self.copy()
        new_query._per_series_aligner = per_series_aligner
        new_query._alignment_period_seconds = seconds + 60 * (minutes +
                                                              60 * hours)
        return new_query

    def reduce(self, cross_series_reducer, *group_by_fields):
        """Copy the query and add cross-series reduction.

        Cross-series reduction combines time series by aggregating their
        data points.

        For example, you could request an aggregated time series for each
        combination of project and zone as follows::

            query = query.reduce(Reducer.REDUCE_MEAN,
                                 'resource.project_id', 'resource.zone')

        :type cross_series_reducer: string
        :param cross_series_reducer:
            The approach to be used to combine time series. For example:
            :data:`Reducer.REDUCE_MEAN`. See :class:`Reducer` and the
            descriptions of the `supported reducers`_.

        :type group_by_fields: strings
        :param group_by_fields:
            Fields to be preserved by the reduction. For example, specifying
            just ``"resource.zone"`` will result in one time series per zone.
            The default is to aggregate all of the time series into just one.

        :rtype: :class:`Query`
        :returns: The new query object.

        .. _supported reducers:
            https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
            projects.timeSeries/list#Reducer
        """
        new_query = self.copy()
        new_query._cross_series_reducer = cross_series_reducer
        new_query._group_by_fields = group_by_fields
        return new_query

    def iter(self, headers_only=False, page_size=None):
        """Yield all time series objects selected by the query.

        The generator returned iterates over
        :class:`~gcloud.monitoring.timeseries.TimeSeries` objects
        containing points ordered from oldest to newest.

        Note that the :class:`Query` object itself is an iterable, such that
        the following are equivalent::

            for timeseries in query:
                ...

            for timeseries in query.iter():
                ...

        :type headers_only: boolean
        :param headers_only:
             Whether to omit the point data from the time series objects.

        :type page_size: integer or None
        :param page_size:
            An optional positive number specifying the maximum number of
            points to return per page. This can be used to control how far
            the iterator reads ahead.

        :raises: :exc:`ValueError` if the query time interval has not been
            specified.
        """
        # The following use of groupby() relies on equality comparison
        # of time series as (named) tuples.
        for timeseries, fragments in itertools.groupby(
                self._iter_fragments(headers_only, page_size),
                lambda fragment: fragment.header()):
            points = list(itertools.chain.from_iterable(
                fragment.points for fragment in fragments))
            points.reverse()  # Order from oldest to newest.
            yield timeseries.header(points=points)

    def _iter_fragments(self, headers_only=False, page_size=None):
        """Yield all time series fragments selected by the query.

        There may be multiple fragments per time series. These will be
        contiguous.

        The parameters and return value are as for :meth:`Query.iter`.
        """
        if self._end_time is None:
            raise ValueError('Query time interval not specified.')

        path = '/projects/{project}/timeSeries/'.format(
            project=self._client.project)

        page_token = None
        while True:
            params = list(self._build_query_params(
                headers_only=headers_only,
                page_size=page_size,
                page_token=page_token,
            ))
            response = self._client.connection.api_request(
                method='GET',
                path=path,
                query_params=params,
            )
            for info in response.get('timeSeries', ()):
                yield TimeSeries._from_dict(info)

            page_token = response.get('nextPageToken')
            if not page_token:
                break

    def _build_query_params(self, headers_only=False,
                            page_size=None, page_token=None):
        """Yield key-value pairs for the URL query string.

        We use a series of key-value pairs (suitable for passing to
        ``urlencode``) instead of a ``dict`` to allow for repeated fields.

        :type headers_only: boolean
        :param headers_only:
             Whether to omit the point data from the
             :class:`~gcloud.monitoring.timeseries.TimeSeries` objects.

        :type page_size: integer or None
        :param page_size: A limit on the number of points to return per page.

        :type page_token: string or None
        :param page_token: A token to continue the retrieval.
        """
        yield 'filter', self.filter

        yield 'interval.endTime', _datetime_to_rfc3339(
            self._end_time, ignore_zone=False)

        if self._start_time is not None:
            yield 'interval.startTime', _datetime_to_rfc3339(
                self._start_time, ignore_zone=False)

        if self._per_series_aligner is not None:
            yield 'aggregation.perSeriesAligner', self._per_series_aligner

        if self._alignment_period_seconds is not None:
            alignment_period = '{period}s'.format(
                period=self._alignment_period_seconds)
            yield 'aggregation.alignmentPeriod', alignment_period

        if self._cross_series_reducer is not None:
            yield ('aggregation.crossSeriesReducer',
                   self._cross_series_reducer)

        for field in self._group_by_fields:
            yield 'aggregation.groupByFields', field

        if headers_only:
            yield 'view', 'HEADERS'

        if page_size is not None:
            yield 'pageSize', page_size

        if page_token is not None:
            yield 'pageToken', page_token

    def as_dataframe(self, label=None, labels=None):
        """Return all the selected time series as a :mod:`pandas` dataframe.

        .. note::

            Use of this method requires that you have :mod:`pandas` installed.

        Examples::

            # Generate a dataframe with a multi-level column header including
            # the resource type and all available resource and metric labels.
            # This can be useful for seeing what labels are available.
            dataframe = query.as_dataframe()

            # Generate a dataframe using a particular label for the column
            # names.
            dataframe = query.as_dataframe(label='instance_name')

            # Generate a dataframe with a multi-level column header.
            dataframe = query.as_dataframe(labels=['zone', 'instance_name'])

            # Generate a dataframe with a multi-level column header, assuming
            # the metric is issued by more than one type of resource.
            dataframe = query.as_dataframe(
                labels=['resource_type', 'instance_id'])

        :type label: string or None
        :param label: The label name to use for the dataframe header.
            This can be the name of a resource label or metric label
            (e.g., ``"instance_name"``), or the string ``"resource_type"``.

        :type labels: list of strings, or None
        :param labels: A list or tuple of label names to use for the dataframe
            header. If more than one label name is provided, the resulting
            dataframe will have a multi-level column header. Providing values
            for both ``label`` and ``labels`` is an error.

        :rtype: :class:`pandas.DataFrame`
        :returns: A dataframe where each column represents one time series.
        """
        return _build_dataframe(self, label, labels)  # pragma: NO COVER

    def copy(self):
        """Copy the query object.

        :rtype: :class:`Query`
        :returns: The new query object.
        """
        # Using copy.deepcopy() would be appropriate, except that we want
        # to copy self._client only as a reference.
        new_query = copy.copy(self)
        new_query._filter = copy.copy(self._filter)
        return new_query


class _Filter(object):
    """Helper for assembling a filter string."""

    def __init__(self, metric_type):
        self.metric_type = metric_type
        self.group_id = None
        self.projects = ()
        self.resource_label_filter = None
        self.metric_label_filter = None

    def select_resources(self, *args, **kwargs):
        """Select by resource labels.

        See :meth:`Query.select_resources`.
        """
        self.resource_label_filter = _build_label_filter('resource',
                                                         *args, **kwargs)

    def select_metrics(self, *args, **kwargs):
        """Select by metric labels.

        See :meth:`Query.select_metrics`.
        """
        self.metric_label_filter = _build_label_filter('metric',
                                                       *args, **kwargs)

    def __str__(self):
        filters = ['metric.type = "{type}"'.format(type=self.metric_type)]
        if self.group_id is not None:
            filters.append('group.id = "{id}"'.format(id=self.group_id))
        if self.projects:
            filters.append(
                ' OR '.join('project = "{project}"'.format(project=project)
                            for project in self.projects))
        if self.resource_label_filter:
            filters.append(self.resource_label_filter)
        if self.metric_label_filter:
            filters.append(self.metric_label_filter)

        # Parentheses are never actually required, because OR binds more
        # tightly than AND in the Monitoring API's filter syntax.
        return ' AND '.join(filters)


def _build_label_filter(category, *args, **kwargs):
    """Construct a filter string to filter on metric or resource labels."""
    terms = list(args)
    for key, value in six.iteritems(kwargs):
        if value is None:
            continue

        suffix = None
        if key.endswith('_prefix') or key.endswith('_suffix'):
            key, suffix = key.rsplit('_', 1)

        if category == 'resource' and key == 'resource_type':
            key = 'resource.type'
        else:
            key = '.'.join((category, 'label', key))

        if suffix == 'prefix':
            term = '{key} = starts_with("{value}")'
        elif suffix == 'suffix':
            term = '{key} = ends_with("{value}")'
        else:
            term = '{key} = "{value}"'

        terms.append(term.format(key=key, value=value))

    return ' AND '.join(sorted(terms))
