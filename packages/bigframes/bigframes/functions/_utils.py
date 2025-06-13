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


import hashlib
import json
import sys
import typing
from typing import cast, Optional, Set

import cloudpickle
import google.api_core.exceptions
from google.cloud import bigquery, functions_v2
import numpy
import pandas
import pyarrow

import bigframes.formatting_helpers as bf_formatting
from bigframes.functions import function_typing

# Naming convention for the function artifacts
_BIGFRAMES_FUNCTION_PREFIX = "bigframes"
_BQ_FUNCTION_NAME_SEPERATOR = "_"
_GCF_FUNCTION_NAME_SEPERATOR = "-"

# Protocol version 4 is available in python version 3.4 and above
# https://docs.python.org/3/library/pickle.html#data-stream-format
_pickle_protocol_version = 4


def get_remote_function_locations(bq_location):
    """Get BQ location and cloud functions region given a BQ client."""
    # TODO(shobs, b/274647164): Find the best way to determine default location.
    # For now let's assume that if no BQ location is set in the client then it
    # defaults to US multi region
    bq_location = bq_location.lower() if bq_location else "us"

    # Cloud function should be in the same region as the bigquery remote function
    cloud_function_region = bq_location

    # BigQuery has multi region but cloud functions does not.
    # Any region in the multi region that supports cloud functions should work
    # https://cloud.google.com/functions/docs/locations
    if bq_location == "us":
        cloud_function_region = "us-central1"
    elif bq_location == "eu":
        cloud_function_region = "europe-west1"

    return bq_location, cloud_function_region


def _get_updated_package_requirements(
    package_requirements=None, is_row_processor=False, capture_references=True
):
    requirements = []
    if capture_references:
        requirements.append(f"cloudpickle=={cloudpickle.__version__}")

    if is_row_processor:
        # bigframes function will send an entire row of data as json, which
        # would be converted to a pandas series and processed Ensure numpy
        # versions match to avoid unpickling problems. See internal issue
        # b/347934471.
        requirements.append(f"numpy=={numpy.__version__}")
        requirements.append(f"pandas=={pandas.__version__}")
        requirements.append(f"pyarrow=={pyarrow.__version__}")

    if package_requirements:
        requirements.extend(package_requirements)

    requirements = sorted(requirements)
    return requirements


def _clean_up_by_session_id(
    bqclient: bigquery.Client,
    gcfclient: functions_v2.FunctionServiceClient,
    dataset: bigquery.DatasetReference,
    session_id: str,
):
    """Delete remote function artifacts for a session id, where the session id
    was not necessarily created in the current runtime. This is useful if the
    user worked with a BigQuery DataFrames session previously and remembered the
    session id, and now wants to clean up its temporary resources at a later
    point in time.
    """

    # First clean up the BQ remote functions and then the underlying cloud
    # functions, so that at no point we are left with a remote function that is
    # pointing to a cloud function that does not exist

    endpoints_to_be_deleted: Set[str] = set()
    match_prefix = "".join(
        [
            _BIGFRAMES_FUNCTION_PREFIX,
            _BQ_FUNCTION_NAME_SEPERATOR,
            session_id,
            _BQ_FUNCTION_NAME_SEPERATOR,
        ]
    )
    for routine in bqclient.list_routines(dataset):
        routine = cast(bigquery.Routine, routine)

        # skip past the routines not belonging to the given session id, or
        # non-remote-function routines
        if (
            routine.type_ != bigquery.RoutineType.SCALAR_FUNCTION
            or not cast(str, routine.routine_id).startswith(match_prefix)
            or not routine.remote_function_options
            or not routine.remote_function_options.endpoint
        ):
            continue

        # Let's forgive the edge case possibility that the BQ remote function
        # may have been deleted at the same time directly by the user
        bqclient.delete_routine(routine, not_found_ok=True)
        endpoints_to_be_deleted.add(routine.remote_function_options.endpoint)

    # Now clean up the cloud functions
    bq_location = bqclient.get_dataset(dataset).location
    bq_location, gcf_location = get_remote_function_locations(bq_location)
    parent_path = gcfclient.common_location_path(
        project=dataset.project, location=gcf_location
    )
    for gcf in gcfclient.list_functions(parent=parent_path):
        # skip past the cloud functions not attached to any BQ remote function
        # belonging to the given session id
        if gcf.service_config.uri not in endpoints_to_be_deleted:
            continue

        # Let's forgive the edge case possibility that the cloud function
        # may have been deleted at the same time directly by the user
        try:
            gcfclient.delete_function(name=gcf.name)
        except google.api_core.exceptions.NotFound:
            pass


def _get_hash(def_, package_requirements=None):
    "Get hash (32 digits alphanumeric) of a function."
    # There is a known cell-id sensitivity of the cloudpickle serialization in
    # notebooks https://github.com/cloudpipe/cloudpickle/issues/538. Because of
    # this, if a cell contains a udf decorated with @remote_function, a unique
    # cloudpickle code is generated every time the cell is run, creating new
    # cloud artifacts every time. This is slow and wasteful.
    # A workaround of the same can be achieved by replacing the filename in the
    # code object to a static value
    # https://github.com/cloudpipe/cloudpickle/issues/120#issuecomment-338510661.
    #
    # To respect the user code/environment let's make this modification on a
    # copy of the udf, not on the original udf itself.
    def_copy = cloudpickle.loads(cloudpickle.dumps(def_))
    def_copy.__code__ = def_copy.__code__.replace(
        co_filename="bigframes_place_holder_filename"
    )

    def_repr = cloudpickle.dumps(def_copy, protocol=_pickle_protocol_version)
    if package_requirements:
        for p in sorted(package_requirements):
            def_repr += p.encode()
    return hashlib.md5(def_repr).hexdigest()


def routine_ref_to_string_for_query(routine_ref: bigquery.RoutineReference) -> str:
    return f"`{routine_ref.project}.{routine_ref.dataset_id}`.{routine_ref.routine_id}"


def get_cloud_function_name(function_hash, session_id=None, uniq_suffix=None):
    "Get a name for the cloud function for the given user defined function."
    parts = [_BIGFRAMES_FUNCTION_PREFIX]
    if session_id:
        parts.append(session_id)
    parts.append(function_hash)
    if uniq_suffix:
        parts.append(uniq_suffix)
    return _GCF_FUNCTION_NAME_SEPERATOR.join(parts)


def get_bigframes_function_name(function_hash, session_id, uniq_suffix=None):
    "Get a name for the bigframes function for the given user defined function."
    parts = [_BIGFRAMES_FUNCTION_PREFIX, session_id, function_hash]
    if uniq_suffix:
        parts.append(uniq_suffix)
    return _BQ_FUNCTION_NAME_SEPERATOR.join(parts)


def get_python_output_type_from_bigframes_metadata(
    metadata_text: str,
) -> Optional[type]:
    try:
        metadata_dict = json.loads(metadata_text)
    except (TypeError, json.decoder.JSONDecodeError):
        return None

    try:
        output_type = metadata_dict["value"]["python_array_output_type"]
    except KeyError:
        return None

    for (
        python_output_array_type
    ) in function_typing.RF_SUPPORTED_ARRAY_OUTPUT_PYTHON_TYPES:
        if python_output_array_type.__name__ == output_type:
            return list[python_output_array_type]  # type: ignore

    return None


def get_bigframes_metadata(*, python_output_type: Optional[type] = None) -> str:
    # Let's keep the actual metadata inside one level of nesting so that in
    # future we can use a top level key "version" (parallel to "value"), based
    # on which "value" can be interpreted according to the "version". The
    # absence of "version" should be interpreted as default version.
    inner_metadata = {}
    if typing.get_origin(python_output_type) is list:
        python_output_array_type = typing.get_args(python_output_type)[0]
        if (
            python_output_array_type
            in function_typing.RF_SUPPORTED_ARRAY_OUTPUT_PYTHON_TYPES
        ):
            inner_metadata[
                "python_array_output_type"
            ] = python_output_array_type.__name__

    metadata = {"value": inner_metadata}
    metadata_ser = json.dumps(metadata)

    # let's make sure the serialized value is deserializable
    if (
        get_python_output_type_from_bigframes_metadata(metadata_ser)
        != python_output_type
    ):
        raise bf_formatting.create_exception_with_feedback_link(
            ValueError, f"python_output_type {python_output_type} is not serializable."
        )

    return metadata_ser


def get_python_version(is_compat: bool = False) -> str:
    # Cloud Run functions use the 'compat' format (e.g., python311, see more
    # from https://cloud.google.com/functions/docs/runtime-support#python),
    # while managed functions use the standard format (e.g., python-3.11).
    major = sys.version_info.major
    minor = sys.version_info.minor
    return f"python{major}{minor}" if is_compat else f"python-{major}.{minor}"


def _build_unnest_post_routine(py_list_type: type[list]):
    sdk_type = function_typing.sdk_array_output_type_from_python_type(py_list_type)
    assert sdk_type.array_element_type is not None
    inner_sdk_type = sdk_type.array_element_type
    result_dtype = function_typing.sdk_type_to_bf_type(inner_sdk_type)

    def post_process(input):
        import bigframes.bigquery as bbq

        return bbq.json_extract_string_array(input, value_dtype=result_dtype)

    return post_process
