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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format

from google.cloud.securitycentermanagement_v1.types import security_center_management

from .base import DEFAULT_CLIENT_INFO, SecurityCenterManagementTransport


class _BaseSecurityCenterManagementRestTransport(SecurityCenterManagementTransport):
    """Base REST backend transport for SecurityCenterManagement.

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
        host: str = "securitycentermanagement.googleapis.com",
        credentials: Optional[Any] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.
        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'securitycentermanagement.googleapis.com').
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

    class _BaseCreateEventThreatDetectionCustomModule:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/eventThreatDetectionCustomModules",
                    "body": "event_threat_detection_custom_module",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=folders/*/locations/*}/eventThreatDetectionCustomModules",
                    "body": "event_threat_detection_custom_module",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=organizations/*/locations/*}/eventThreatDetectionCustomModules",
                    "body": "event_threat_detection_custom_module",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.CreateEventThreatDetectionCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseCreateEventThreatDetectionCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseCreateSecurityHealthAnalyticsCustomModule:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/securityHealthAnalyticsCustomModules",
                    "body": "security_health_analytics_custom_module",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=folders/*/locations/*}/securityHealthAnalyticsCustomModules",
                    "body": "security_health_analytics_custom_module",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=organizations/*/locations/*}/securityHealthAnalyticsCustomModules",
                    "body": "security_health_analytics_custom_module",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.CreateSecurityHealthAnalyticsCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseCreateSecurityHealthAnalyticsCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseDeleteEventThreatDetectionCustomModule:
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
                    "uri": "/v1/{name=projects/*/locations/*/eventThreatDetectionCustomModules/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=folders/*/locations/*/eventThreatDetectionCustomModules/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=organizations/*/locations/*/eventThreatDetectionCustomModules/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.DeleteEventThreatDetectionCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseDeleteEventThreatDetectionCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseDeleteSecurityHealthAnalyticsCustomModule:
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
                    "uri": "/v1/{name=projects/*/locations/*/securityHealthAnalyticsCustomModules/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=folders/*/locations/*/securityHealthAnalyticsCustomModules/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=organizations/*/locations/*/securityHealthAnalyticsCustomModules/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.DeleteSecurityHealthAnalyticsCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseDeleteSecurityHealthAnalyticsCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseGetEffectiveEventThreatDetectionCustomModule:
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
                    "uri": "/v1/{name=projects/*/locations/*/effectiveEventThreatDetectionCustomModules/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/locations/*/effectiveEventThreatDetectionCustomModules/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/locations/*/effectiveEventThreatDetectionCustomModules/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.GetEffectiveEventThreatDetectionCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveEventThreatDetectionCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseGetEffectiveSecurityHealthAnalyticsCustomModule:
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
                    "uri": "/v1/{name=projects/*/locations/*/effectiveSecurityHealthAnalyticsCustomModules/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/locations/*/effectiveSecurityHealthAnalyticsCustomModules/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/locations/*/effectiveSecurityHealthAnalyticsCustomModules/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseGetEffectiveSecurityHealthAnalyticsCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseGetEventThreatDetectionCustomModule:
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
                    "uri": "/v1/{name=projects/*/locations/*/eventThreatDetectionCustomModules/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/locations/*/eventThreatDetectionCustomModules/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/locations/*/eventThreatDetectionCustomModules/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.GetEventThreatDetectionCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseGetEventThreatDetectionCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseGetSecurityCenterService:
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
                    "uri": "/v1/{name=projects/*/locations/*/securityCenterServices/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/locations/*/securityCenterServices/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/locations/*/securityCenterServices/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.GetSecurityCenterServiceRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseGetSecurityCenterService._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseGetSecurityHealthAnalyticsCustomModule:
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
                    "uri": "/v1/{name=projects/*/locations/*/securityHealthAnalyticsCustomModules/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/locations/*/securityHealthAnalyticsCustomModules/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/locations/*/securityHealthAnalyticsCustomModules/*}",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.GetSecurityHealthAnalyticsCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseGetSecurityHealthAnalyticsCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseListDescendantEventThreatDetectionCustomModules:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/eventThreatDetectionCustomModules:listDescendant",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*/locations/*}/eventThreatDetectionCustomModules:listDescendant",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/eventThreatDetectionCustomModules:listDescendant",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.ListDescendantEventThreatDetectionCustomModulesRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseListDescendantEventThreatDetectionCustomModules._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseListDescendantSecurityHealthAnalyticsCustomModules:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/securityHealthAnalyticsCustomModules:listDescendant",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*/locations/*}/securityHealthAnalyticsCustomModules:listDescendant",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/securityHealthAnalyticsCustomModules:listDescendant",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.ListDescendantSecurityHealthAnalyticsCustomModulesRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseListDescendantSecurityHealthAnalyticsCustomModules._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseListEffectiveEventThreatDetectionCustomModules:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/effectiveEventThreatDetectionCustomModules",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*/locations/*}/effectiveEventThreatDetectionCustomModules",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/effectiveEventThreatDetectionCustomModules",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.ListEffectiveEventThreatDetectionCustomModulesRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseListEffectiveEventThreatDetectionCustomModules._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseListEffectiveSecurityHealthAnalyticsCustomModules:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/effectiveSecurityHealthAnalyticsCustomModules",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*/locations/*}/effectiveSecurityHealthAnalyticsCustomModules",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/effectiveSecurityHealthAnalyticsCustomModules",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseListEffectiveSecurityHealthAnalyticsCustomModules._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseListEventThreatDetectionCustomModules:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/eventThreatDetectionCustomModules",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*/locations/*}/eventThreatDetectionCustomModules",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/eventThreatDetectionCustomModules",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.ListEventThreatDetectionCustomModulesRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseListEventThreatDetectionCustomModules._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseListSecurityCenterServices:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/securityCenterServices",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*/locations/*}/securityCenterServices",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/securityCenterServices",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = (
                security_center_management.ListSecurityCenterServicesRequest.pb(request)
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
                _BaseSecurityCenterManagementRestTransport._BaseListSecurityCenterServices._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseListSecurityHealthAnalyticsCustomModules:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/securityHealthAnalyticsCustomModules",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*/locations/*}/securityHealthAnalyticsCustomModules",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/securityHealthAnalyticsCustomModules",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.ListSecurityHealthAnalyticsCustomModulesRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseListSecurityHealthAnalyticsCustomModules._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseSimulateSecurityHealthAnalyticsCustomModule:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/securityHealthAnalyticsCustomModules:simulate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=folders/*/locations/*}/securityHealthAnalyticsCustomModules:simulate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=organizations/*/locations/*}/securityHealthAnalyticsCustomModules:simulate",
                    "body": "*",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.SimulateSecurityHealthAnalyticsCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseSimulateSecurityHealthAnalyticsCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseUpdateEventThreatDetectionCustomModule:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

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
                    "uri": "/v1/{event_threat_detection_custom_module.name=projects/*/locations/*/eventThreatDetectionCustomModules/*}",
                    "body": "event_threat_detection_custom_module",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{event_threat_detection_custom_module.name=folders/*/locations/*/eventThreatDetectionCustomModules/*}",
                    "body": "event_threat_detection_custom_module",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{event_threat_detection_custom_module.name=organizations/*/locations/*/eventThreatDetectionCustomModules/*}",
                    "body": "event_threat_detection_custom_module",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.UpdateEventThreatDetectionCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseUpdateEventThreatDetectionCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseUpdateSecurityCenterService:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

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
                    "uri": "/v1/{security_center_service.name=projects/*/locations/*/securityCenterServices/*}",
                    "body": "security_center_service",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{security_center_service.name=folders/*/locations/*/securityCenterServices/*}",
                    "body": "security_center_service",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{security_center_service.name=organizations/*/locations/*/securityCenterServices/*}",
                    "body": "security_center_service",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = (
                security_center_management.UpdateSecurityCenterServiceRequest.pb(
                    request
                )
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
                _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityCenterService._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseUpdateSecurityHealthAnalyticsCustomModule:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

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
                    "uri": "/v1/{security_health_analytics_custom_module.name=projects/*/locations/*/securityHealthAnalyticsCustomModules/*}",
                    "body": "security_health_analytics_custom_module",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{security_health_analytics_custom_module.name=folders/*/locations/*/securityHealthAnalyticsCustomModules/*}",
                    "body": "security_health_analytics_custom_module",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{security_health_analytics_custom_module.name=organizations/*/locations/*/securityHealthAnalyticsCustomModules/*}",
                    "body": "security_health_analytics_custom_module",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.UpdateSecurityHealthAnalyticsCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseUpdateSecurityHealthAnalyticsCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseValidateEventThreatDetectionCustomModule:
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
                    "uri": "/v1/{parent=projects/*/locations/*}/eventThreatDetectionCustomModules:validate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=folders/*/locations/*}/eventThreatDetectionCustomModules:validate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=organizations/*/locations/*}/eventThreatDetectionCustomModules:validate",
                    "body": "*",
                },
            ]
            return http_options

        @staticmethod
        def _get_transcoded_request(http_options, request):
            pb_request = security_center_management.ValidateEventThreatDetectionCustomModuleRequest.pb(
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
                _BaseSecurityCenterManagementRestTransport._BaseValidateEventThreatDetectionCustomModule._get_unset_required_fields(
                    query_params
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"
            return query_params

    class _BaseGetLocation:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}",
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

    class _BaseListLocations:
        def __hash__(self):  # pragma: NO COVER
            return NotImplementedError("__hash__ must be implemented.")

        @staticmethod
        def _get_http_options():
            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/locations",
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


__all__ = ("_BaseSecurityCenterManagementRestTransport",)
