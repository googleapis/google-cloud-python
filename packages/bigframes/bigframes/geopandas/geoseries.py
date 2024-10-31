# Copyright 2024 Google LLC
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
from __future__ import annotations

import bigframes_vendored.geopandas.geoseries as vendored_geoseries
import geopandas.array  # type: ignore

import bigframes.series


class GeoSeries(vendored_geoseries.GeoSeries, bigframes.series.Series):
    __doc__ = vendored_geoseries.GeoSeries.__doc__

    def __init__(self, data=None, index=None, **kwargs):
        super().__init__(
            data=data, index=index, dtype=geopandas.array.GeometryDtype(), **kwargs
        )
