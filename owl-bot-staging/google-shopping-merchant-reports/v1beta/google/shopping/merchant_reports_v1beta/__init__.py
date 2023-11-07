# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
#
from google.shopping.merchant_reports_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.report_service import ReportServiceClient
from .services.report_service import ReportServiceAsyncClient

from .types.reports import BestSellersBrandView
from .types.reports import BestSellersProductClusterView
from .types.reports import CompetitiveVisibilityBenchmarkView
from .types.reports import CompetitiveVisibilityCompetitorView
from .types.reports import CompetitiveVisibilityTopMerchantView
from .types.reports import MarketingMethod
from .types.reports import PriceCompetitivenessProductView
from .types.reports import PriceInsightsProductView
from .types.reports import ProductPerformanceView
from .types.reports import ProductView
from .types.reports import RelativeDemand
from .types.reports import RelativeDemandChangeType
from .types.reports import ReportGranularity
from .types.reports import ReportRow
from .types.reports import SearchRequest
from .types.reports import SearchResponse
from .types.reports import TrafficSource

__all__ = (
    'ReportServiceAsyncClient',
'BestSellersBrandView',
'BestSellersProductClusterView',
'CompetitiveVisibilityBenchmarkView',
'CompetitiveVisibilityCompetitorView',
'CompetitiveVisibilityTopMerchantView',
'MarketingMethod',
'PriceCompetitivenessProductView',
'PriceInsightsProductView',
'ProductPerformanceView',
'ProductView',
'RelativeDemand',
'RelativeDemandChangeType',
'ReportGranularity',
'ReportRow',
'ReportServiceClient',
'SearchRequest',
'SearchResponse',
'TrafficSource',
)
