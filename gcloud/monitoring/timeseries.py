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

"""Time series in the `Google Monitoring API (V3)`_.

.. _Google Monitoring API (V3):
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries
"""

# Features intentionally omitted from this first version of the client library:
#   - Creating time series.
#   - Natural representation of distribution values.

import collections
import copy
import datetime
import itertools

import six

from gcloud.monitoring.metric import Metric
from gcloud.monitoring.resource import Resource

TOP_RESOURCE_LABELS = [
    'project_id',
    'aws_account',
    'location',
    'region',
    'zone',
]


class Query(object):
    """Query object for listing time series.

    The preferred way to construct a query object is using the
    :meth:`~gcloud.monitoring.client.Client.query` method
    of the :class:`~gcloud.monitoring.client.Client` class.

    :type client: :class:`gcloud.monitoring.client.Client`
    :param client: The client to use.

    :type metric_type: string
    :param metric_type: The metric type name. The default value is
        ``"compute.googleapis.com/instance/cpu/utilization"``, but
        please note that this default value is provided only for
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
        :meth:`~gcloud.monitoring.timeseries.Query.select_interval`
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
        :meth:`~gcloud.monitoring.timeseries.Query.select_interval`.

    .. _supported metrics: https://cloud.google.com/monitoring/api/metrics
    """

    DEFAULT_METRIC_TYPE = 'compute.googleapis.com/instance/cpu/utilization'

    def __init__(self, client,
                 metric_type=DEFAULT_METRIC_TYPE,
                 end_time=None, days=0, hours=0, minutes=0):
        start_time = None
        if days or hours or minutes:
            if end_time is None:
                end_time = datetime.datetime.utcnow().replace(second=0,
                                                              microsecond=0)
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
    def filter(self):
        """The filter string.

        This is constructed from the metric type, the resource type, and
        selectors for the group ID, monitored projects, resource labels,
        and metric labels.
        """
        return str(self._filter)

    def select_interval(self, end_time, start_time=None):
        """Copy the query and set the query time interval.

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

        :param args: Raw filter expression strings to include in the
            conjunction. If just one is provided and no keyword arguments
            are provided, it can be a disjunction.

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

        :param args: Raw filter expression strings to include in the
            conjunction. If just one is provided and no keyword arguments
            are provided, it can be a disjunction.

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

        If ``per_series_aligner`` is not ``"ALIGN_NONE"``, each time series
        will contain data points only on the period boundaries.

        Example::

            query = query.align('ALIGN_MEAN', minutes=5)

        :type per_series_aligner: string
        :param per_series_aligner: The approach to be used to align
            individual time series. For example: ``"ALIGN_MEAN"``.
            See the `supported aligners`_.

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

    def reduce(self, cross_series_reducer, group_by_fields=()):
        """Copy the query and add cross-series reduction.

        :type cross_series_reducer: string
        :param cross_series_reducer: The approach to be used to combine
            time series. For example: ``"REDUCE_MEAN"``.
            See the `supported reducers`_.

        :type group_by_fields: string or list of strings
        :param group_by_fields: An optional field or set of fields
            to be preserved by the reduction. For example, a value of
            ``"resource.zone"`` will result in one time series per zone.
            The default is to aggregate all of the time series into just one.

        :rtype: :class:`Query`
        :returns: The new query object.

        .. _supported reducers:
            https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
            projects.timeSeries/list#Reducer
        """
        if isinstance(group_by_fields, six.string_types):
            group_by_fields = [group_by_fields]

        new_query = self.copy()
        new_query._cross_series_reducer = cross_series_reducer
        new_query._group_by_fields = group_by_fields
        return new_query

    def iter(self, headers_only=False, _page_size=None):
        """Yield all time series objects selected by the query.

        Note that the :class:`Query` object itself is an iterable, such that
        the following are equivalent::

            for timeseries in query: ...
            for timeseries in query.iter(): ...

        :type headers_only: boolean
        :param headers_only:
             Whether to omit the point data from the time series objects.

        :type _page_size: integer or None
        :param _page_size:
            An optional positive number specifying the maximum number of
            points to return per page. This can be used to control how far
            the iterator reads ahead.

        :rtype: iterator over :class:`TimeSeries`
        :returns: Time series objects, containing points ordered from oldest
            to newest.
        :raises: :exc:`ValueError` if the query time interval has not been
            specified.
        """
        if self._end_time is None:
            raise ValueError('Query time interval not specified.')

        path = '/projects/{project}/timeSeries'.format(
            project=self._client.project)

        def _fragments():
            page_token = None
            while True:
                params = self._build_query_params(
                    headers_only=headers_only,
                    page_size=_page_size,
                    page_token=page_token,
                )
                response = self._client.connection.api_request(
                    method='GET',
                    path=path,
                    query_params=params,
                )
                for info in response.get('timeSeries', []):
                    yield TimeSeries._from_dict(info)

                page_token = response.get('nextPageToken')
                if not page_token:
                    break

        for timeseries, fragments in itertools.groupby(
                _fragments(),
                lambda fragment: fragment._replace(points=None)):
            points = list(itertools.chain.from_iterable(
                fragment.points for fragment in fragments))
            points.reverse()  # Order from oldest to newest.
            yield timeseries._replace(points=points)

    def _build_query_params(self, headers_only, page_size, page_token):
        """Assemble the list of key-value pairs for the URL query string.

        We use a list of key-value pairs instead of a ``dict`` to allow for
        repeated fields.

        :type headers_only: boolean
        :param headers_only:
             Whether to omit the point data from the ``TimeSeries`` objects.

        :type page_size: integer or None
        :param page_size: A limit on the number of points to return per page.

        :type page_token: string or None
        :param page_token: A token to continue the retrieval.

        :rtype: list of tuples
        :returns:
            A list of key-value pairs suitable for passing to ``urlencode``.
        """
        params = {'filter': self.filter}

        params['interval.endTime'] = _format_timestamp(self._end_time)
        if self._start_time is not None:
            params['interval.startTime'] = _format_timestamp(self._start_time)

        if self._per_series_aligner is not None:
            params['aggregation.perSeriesAligner'] = self._per_series_aligner

        if self._alignment_period_seconds is not None:
            alignment_period = '{}s'.format(self._alignment_period_seconds)
            params['aggregation.alignmentPeriod'] = alignment_period

        if self._cross_series_reducer is not None:
            params['aggregation.crossSeriesReducer'] = \
                self._cross_series_reducer

        if headers_only:
            params['view'] = 'HEADERS'

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        # Convert to a list of tuples before adding repeated fields.
        params = list(six.iteritems(params))

        if self._group_by_fields:
            params.extend(('aggregation.groupByFields', field)
                          for field in self._group_by_fields)

        return sorted(params)

    def as_dataframe(self, label=None, labels=None):
        """Return all the selected time series as a ``pandas`` dataframe.

        .. note::

            Use of this method requires that you have ``pandas`` installed.

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
        import pandas   # pylint: disable=import-error

        if label is not None and labels is not None:
            raise ValueError('Cannot specify both "label" and "labels".')
        elif not (labels or labels is None):
            raise ValueError('"labels" must be non-empty or None.')

        columns = []
        headers = []
        for time_series in self:
            pandas_series = pandas.Series(
                data=[p.value for p in time_series.points],
                index=[p.end_time for p in time_series.points],
            )
            columns.append(pandas_series)
            headers.append(time_series._replace(points=None))

        # Implement a smart default of using all available labels.
        if label is None and labels is None:
            resource_labels = set(itertools.chain.from_iterable(
                header.resource.labels for header in headers))
            metric_labels = set(itertools.chain.from_iterable(
                header.metric.labels for header in headers))
            labels = (['resource_type'] +
                      _sorted_resource_labels(resource_labels) +
                      sorted(metric_labels))

        # Assemble the columns into a DataFrame.
        dataframe = pandas.DataFrame(columns).T

        # Convert the timestamp strings into a DatetimeIndex.
        dataframe.index = pandas.to_datetime(dataframe.index)

        # Build a column Index or MultiIndex from the label values. Do not
        # include level names in the column header if the user requested a
        # single-level header by specifying "label".
        level_names = labels or None
        label_keys = labels or [label]
        dataframe.columns = pandas.MultiIndex.from_arrays(
            [[header.labels.get(key, '') for header in headers]
             for key in label_keys],
            names=level_names)

        # Sort the rows just in case (since the API doesn't guarantee the
        # ordering), and sort the columns lexicographically.
        return dataframe.sort_index(axis=0).sort_index(axis=1)

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


class TimeSeries(collections.namedtuple(
        'TimeSeries', 'metric resource metric_kind value_type points')):
    """A single time series of metric values.

    :type metric: :class:`~gcloud.monitoring.metric.Metric`
    :param metric: A metric object.

    :type resource: :class:`~gcloud.monitoring.resource.Resource`
    :param resource: A resource object.

    :type metric_kind: string
    :param metric_kind: The kind of measurement: ``"GAUGE"``, ``"DELTA"``,
        or ``"CUMULATIVE"``.

    :type value_type: string
    :param value_type: The value type of the metric: ``"BOOL"``, ``"INT64"``,
        ``"DOUBLE"``, ``"STRING"``, ``"DISTRIBUTION"``, or ``"MONEY"``.

    :type points: list of :class:`Point`
    :param points: A list of point objects.
    """

    @classmethod
    def _from_dict(cls, info):
        """Construct a time series from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`TimeSeries`
        :returns: A time series object.
        """
        metric = Metric._from_dict(info['metric'])
        resource = Resource._from_dict(info['resource'])
        metric_kind = info['metricKind']
        value_type = info['valueType']
        points = [Point._from_dict(p) for p in info.get('points', [])]
        return cls(metric, resource, metric_kind, value_type, points)

    @property
    def labels(self):
        """A single dictionary with values for all the labels.

        This combines ``resource.labels`` and ``metric.labels`` and also
        adds ``"resource_type"``.
        """
        # pylint: disable=attribute-defined-outside-init
        try:
            return self._labels
        except AttributeError:
            labels = {'resource_type': self.resource.type}
            labels.update(self.resource.labels)
            labels.update(self.metric.labels)
            self._labels = labels
            return self._labels

    def __repr__(self):
        """Return a representation string with the points elided."""
        return '\n'.join([
            'TimeSeries(',
            '    {},'.format(self.metric),
            '    {},'.format(self.resource),
            '    {}, {}, Number of points={})'.format(
                self.metric_kind, self.value_type, len(self.points)),
        ])


class Point(collections.namedtuple('Point', 'end_time start_time value')):
    """A single point in a time series.

    :type end_time: string
    :param end_time: The end time in RFC3339 UTC "Zulu" format.

    :type start_time: string or None
    :param start_time: An optional start time in RFC3339 UTC "Zulu" format.

    :param value: The metric value. This can be a scalar or a distribution.
    """
    __slots__ = ()

    @classmethod
    def _from_dict(cls, info):
        """Construct a Point from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`Point`
        :returns: A point object.
        """
        end_time = info['interval']['endTime']
        start_time = info['interval'].get('startTime')
        value_type, value = next(six.iteritems(info['value']))
        if value_type == 'int64Value':
            value = int(value)  # Convert from string.

        return cls(end_time, start_time, value)


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
        filters = ['metric.type = "{}"'.format(self.metric_type)]
        if self.group_id is not None:
            filters.append('group.id = "{}"'.format(self.group_id))
        if self.projects:
            filters.append(' OR '.join('project = "{}"'.format(project)
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
    for key in kwargs:
        value = kwargs[key]
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
            term = '{} = starts_with("{}")'
        elif suffix == 'suffix':
            term = '{} = ends_with("{}")'
        else:
            term = '{} = "{}"'

        terms.append(term.format(key, value))

    return ' AND '.join(sorted(terms))


def _sorted_resource_labels(labels):
    """Sort label names, putting well-known resource labels first."""
    head = [label for label in TOP_RESOURCE_LABELS if label in labels]
    tail = sorted(label for label in labels
                  if label not in TOP_RESOURCE_LABELS)
    return head + tail


def _format_timestamp(timestamp):
    """Convert a datetime object to a string as required by the API.

    :type timestamp: :class:`datetime.datetime`
    :param timestamp: A datetime object.

    :rtype: string
    :returns: The formatted timestamp. For example:
        ``"2016-02-17T19:18:01.763000Z"``
    """
    if timestamp.tzinfo is not None:
        # Convert to UTC and remove the time zone info.
        timestamp = timestamp.replace(tzinfo=None) - timestamp.utcoffset()

    return timestamp.isoformat() + 'Z'
