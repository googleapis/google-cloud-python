# -*- coding: utf-8 -*-
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
#
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1, path_template
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format

from google.cloud.discoveryengine_v1beta.types import (
    site_search_engine,
    site_search_engine_service,
)

from .base import DEFAULT_CLIENT_INFO, SiteSearchEngineServiceTransport


class _BaseSiteSearchEngineServiceRestTransport(SiteSearchEngineServiceTransport):
    """Base REST backend transport for SiteSearchEngineService.

    Note: This class is not meant to be used directly. Use its sync and
    async sub-classes instead.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "discoveryengine.googleapis.com",
        credentials: Optional[Any] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.
        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'discoveryengine.googleapis.com').
            credentials (Optional[Any]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

    class _BaseBatchCreateTargetSites:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=projects/*/locations/*/dataStores/*/siteSearchEngine}/targetSites:batchCreate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/targetSites:batchCreate",
                    "body": "*",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.BatchCreateTargetSitesRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_request_body_json(transcoded_request):
            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            return body

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseBatchCreateTargetSites._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseBatchVerifyTargetSites:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:batchVerifyTargetSites",
                    "body": "*",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.BatchVerifyTargetSitesRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_request_body_json(transcoded_request):
            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            return body

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseBatchVerifyTargetSites._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseCreateTargetSite:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=projects/*/locations/*/dataStores/*/siteSearchEngine}/targetSites",
                    "body": "target_site",
                },
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/targetSites",
                    "body": "target_site",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.CreateTargetSiteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_request_body_json(transcoded_request):
            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            return body

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseCreateTargetSite._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseDeleteTargetSite:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/siteSearchEngine/targetSites/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.DeleteTargetSiteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseDeleteTargetSite._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseDisableAdvancedSiteSearch:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{site_search_engine=projects/*/locations/*/dataStores/*/siteSearchEngine}:disableAdvancedSiteSearch",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta/{site_search_engine=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:disableAdvancedSiteSearch",
                    "body": "*",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.DisableAdvancedSiteSearchRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_request_body_json(transcoded_request):
            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            return body

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseDisableAdvancedSiteSearch._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseEnableAdvancedSiteSearch:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{site_search_engine=projects/*/locations/*/dataStores/*/siteSearchEngine}:enableAdvancedSiteSearch",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta/{site_search_engine=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:enableAdvancedSiteSearch",
                    "body": "*",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.EnableAdvancedSiteSearchRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_request_body_json(transcoded_request):
            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            return body

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseEnableAdvancedSiteSearch._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseFetchDomainVerificationStatus:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{site_search_engine=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:fetchDomainVerificationStatus",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = (
                site_search_engine_service.FetchDomainVerificationStatusRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseFetchDomainVerificationStatus._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseGetSiteSearchEngine:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/siteSearchEngine}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.GetSiteSearchEngineRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseGetSiteSearchEngine._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseGetTargetSite:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/siteSearchEngine/targetSites/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.GetTargetSiteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseGetTargetSite._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseListTargetSites:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=projects/*/locations/*/dataStores/*/siteSearchEngine}/targetSites",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/targetSites",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.ListTargetSitesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseListTargetSites._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseRecrawlUris:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{site_search_engine=projects/*/locations/*/dataStores/*/siteSearchEngine}:recrawlUris",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta/{site_search_engine=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:recrawlUris",
                    "body": "*",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.RecrawlUrisRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_request_body_json(transcoded_request):
            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            return body

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseRecrawlUris._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseUpdateTargetSite:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta/{target_site.name=projects/*/locations/*/dataStores/*/siteSearchEngine/targetSites/*}",
                    "body": "target_site",
                },
                {
                    "method": "patch",
                    "uri": "/v1beta/{target_site.name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/*}",
                    "body": "target_site",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = site_search_engine_service.UpdateTargetSiteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)
            return transcoded_request

        @staticmethod
        def _get_request_body_json(transcoded_request):
            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            return body

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(
                _BaseSiteSearchEngineServiceRestTransport._BaseUpdateTargetSite._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseCancelOperation:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}:cancel",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}:cancel",
                    "body": "*",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)
            return transcoded_request

        @staticmethod
        def _get_request_body_json(transcoded_request):
            body = json.dumps(transcoded_request["body"])
            return body

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))
            return query_params

    class _BaseGetOperation:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataConnector/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/models/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/engines/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/models/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/evaluations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/sampleQuerySets/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/operations/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)
            return transcoded_request

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))
            return query_params

    class _BaseListOperations:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataConnector}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/models/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*/engines/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/collections/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/branches/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/models/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*}/operations",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)
            return transcoded_request

        @staticmethod
        def _get_query_params_json(transcoded_request):
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))
            return query_params


__all__ = ("_BaseSiteSearchEngineServiceRestTransport",)
