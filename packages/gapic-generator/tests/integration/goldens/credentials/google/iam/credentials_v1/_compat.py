# # Copyright 2026 Google LLC
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

"""A compatibility module for older versions of google-api-core."""

import functools
import json
import operator
import os
import re
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from google.auth.exceptions import MutualTLSChannelError
import google.protobuf.message


try:
    from google.api_core.universe import (  # type: ignore
        get_default_mtls_endpoint,
        get_api_endpoint,
        get_universe_domain,
    )
except ImportError:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/google-cloud-python/issues/17813): Universe domain support was introduced in google-api-core 2.18.0.
    # Remove these fallback definitions when google-api-core >= 2.18.0 becomes the minimum required version in generated client setup dependencies.
    def get_default_mtls_endpoint(api_endpoint: Optional[str]) -> Optional[str]:
        """Converts api endpoint to mTLS endpoint."""
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        if m is None:
            # Could not parse api_endpoint; return as-is.
            return api_endpoint

        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    def get_api_endpoint(  # type: ignore[misc]
        api_override: Optional[str],
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]],
        universe_domain: str,
        use_mtls_endpoint: str,
        default_universe: str,
        default_mtls_endpoint: Optional[str],
        default_endpoint_template: str,
    ) -> str:
        """Return the API endpoint used by the client."""
        api_endpoint: Optional[str] = None
        if api_override is not None:
            api_endpoint = api_override
        elif use_mtls_endpoint == "always" or (use_mtls_endpoint == "auto" and client_cert_source):
            if universe_domain != default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {default_universe}."
                )
            api_endpoint = default_mtls_endpoint
        else:
            api_endpoint = default_endpoint_template.format(UNIVERSE_DOMAIN=universe_domain)
        return api_endpoint  # type: ignore[return-value]

    def get_universe_domain(  # type: ignore[misc]
        *potential_universes: Optional[str],
        default_universe: str = "googleapis.com",
    ) -> str:
        """Return the universe domain used by the client."""
        resolved = next(
            (x.strip() for x in potential_universes if x is not None),
            default_universe,
        )
        if not resolved:
            raise ValueError("Universe Domain cannot be an empty string.")
        return resolved


try:
    from google.api_core.gapic_v1.config import (  # type: ignore
        use_client_cert_effective,
        get_client_cert_source,
        read_environment_variables,
    )
except ImportError:  # pragma: NO COVER
    from google.auth.transport import mtls  # type: ignore

    # TODO(https://github.com/googleapis/google-cloud-python/issues/17813): Remove these fallbacks when google-api-core >= 2.18.0 is the minimum required version.

    def use_client_cert_effective() -> bool:
        """Returns whether client certificate should be used for mTLS."""
        if hasattr(mtls, "should_use_client_cert"):
            return mtls.should_use_client_cert()
        else:
            use_client_cert_str = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false").lower()
            if use_client_cert_str not in ("true", "false"):
                raise ValueError(
                    "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be"
                    " either `true` or `false`"
                )
            return use_client_cert_str == "true"

    def get_client_cert_source(
        provided_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]],
        use_cert_flag: bool,
    ) -> Optional[Callable[[], Tuple[bytes, bytes]]]:
        """Return the client cert source to be used by the client."""
        client_cert_source = None
        if use_cert_flag:
            if provided_cert_source:
                client_cert_source = provided_cert_source
            elif (
                hasattr(mtls, "has_default_client_cert_source")
                and mtls.has_default_client_cert_source()
            ):
                client_cert_source = mtls.default_client_cert_source()
            else:
                raise ValueError(
                    "Client certificate is required for mTLS, but no client certificate source was provided or found."
                )
        return client_cert_source

    def read_environment_variables() -> Tuple[bool, str, Optional[str]]:
        """Returns the environment variables used by the client."""
        use_client_cert = use_client_cert_effective()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` "
                "must be `never`, `auto` or `always`"
            )
        return use_client_cert, use_mtls_endpoint, universe_domain_env


try:
    from google.api_core.gapic_v1.request import setup_request_id  # type: ignore
except ImportError:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/google-cloud-python/issues/17813): Request ID setup helper was introduced in google-api-core 2.26.0.
    # Remove this fallback definition when google-api-core >= 2.26.0 becomes the minimum required version in generated client setup dependencies.
    def setup_request_id(request: Any, field_name: str, is_proto3_optional: bool) -> None:
        """Populate a UUID4 field in the request if it is not already set.

        Args:
            request (Union[google.protobuf.message.Message, dict]): The request object.
            field_name (str): The name of the field to populate.
            is_proto3_optional (bool): Whether the field is proto3 optional.
        """
        if request is None:
            return

        request_id_val = str(uuid.uuid4())

        if isinstance(request, dict):
            if is_proto3_optional:
                if field_name not in request or request[field_name] is None:
                    request[field_name] = request_id_val
            elif not request.get(field_name):
                request[field_name] = request_id_val
            return

        if is_proto3_optional:
            try:
                # Pure protobuf messages
                if not request.HasField(field_name):
                    setattr(request, field_name, request_id_val)
            except (AttributeError, ValueError):
                # Proto-plus messages or other objects
                if hasattr(request, "_pb"):
                    try:
                        if not request._pb.HasField(field_name):
                            setattr(request, field_name, request_id_val)
                        return
                    except (AttributeError, ValueError):
                        pass
                if getattr(request, field_name, None) is None:
                    setattr(request, field_name, request_id_val)
        else:
            if not getattr(request, field_name, None):
                setattr(request, field_name, request_id_val)


try:
    from google.api_core.rest_helpers import (  # type: ignore
        flatten_query_params,
        transcode_request,
    )
except ImportError:  # pragma: NO COVER
    # TODO: Remove these fallbacks when google-api-core >= 2.18.0 is the minimum required version.
    from google.protobuf import json_format  # type: ignore
    from google.api_core import path_template  # type: ignore

    def flatten_query_params(obj: Any, strict: bool = False) -> List[Tuple[str, Any]]:  # type: ignore[misc]
        if obj is not None and not isinstance(obj, dict):
            raise TypeError("flatten_query_params must be called with dict object")
        return _flatten(obj, key_path=[], strict=strict)

    def _flatten(obj: Any, key_path: List[str], strict: bool = False) -> List[Tuple[str, Any]]:
        if obj is None:
            return []
        if isinstance(obj, dict):
            return _flatten_dict(obj, key_path=key_path, strict=strict)
        if isinstance(obj, list):
            return _flatten_list(obj, key_path=key_path, strict=strict)
        return _flatten_value(obj, key_path=key_path, strict=strict)

    def _is_primitive_value(obj: Any) -> bool:
        if obj is None:
            return False
        if isinstance(obj, (list, dict)):
            raise ValueError("query params may not contain repeated dicts or lists")
        return True

    def _flatten_value(obj: Any, key_path: List[str], strict: bool = False) -> List[Tuple[str, Any]]:
        return [(".".join(key_path), _canonicalize(obj, strict=strict))]

    def _flatten_dict(obj: Dict[str, Any], key_path: List[str], strict: bool = False) -> List[Tuple[str, Any]]:
        items = (
            _flatten(value, key_path=key_path + [key], strict=strict)
            for key, value in obj.items()
        )
        return functools.reduce(operator.concat, items, [])  # type: ignore[arg-type]

    def _flatten_list(elems: List[Any], key_path: List[str], strict: bool = False) -> List[Tuple[str, Any]]:
        items = (
            _flatten_value(elem, key_path=key_path, strict=strict)
            for elem in elems
            if _is_primitive_value(elem)
        )
        return functools.reduce(operator.concat, items, [])  # type: ignore[arg-type]

    def _canonicalize(obj: Any, strict: bool = False) -> Any:
        if strict:
            value = str(obj)
            if isinstance(obj, bool):
                value = value.lower()
            return value
        return obj

    def transcode_request(  # type: ignore[misc]
        http_options: List[Dict[str, str]],
        request: Any,
        required_fields_default_values: Optional[Dict[str, Any]] = None,
        rest_numeric_enums: bool = False,
    ) -> Tuple[Dict[str, Any], Optional[str], Dict[str, Any]]:
        pb_request = getattr(request, "_pb", request)
        transcoded_request = path_template.transcode(http_options, pb_request)

        body_json = None
        if transcoded_request.get("body") is not None:
            body_json = json_format.MessageToJson(
                transcoded_request["body"],
                use_integers_for_enums=rest_numeric_enums,
            )

        query_params_json = {}
        if transcoded_request.get("query_params") is not None:
            query_params_json = json.loads(json_format.MessageToJson(
                transcoded_request["query_params"],
                use_integers_for_enums=rest_numeric_enums,
            ))

        if required_fields_default_values:
            for k, v in required_fields_default_values.items():
                if k not in query_params_json:
                    query_params_json[k] = v

        if rest_numeric_enums:
            query_params_json["$alt"] = "json;enum-encoding=int"

        return transcoded_request, body_json, query_params_json