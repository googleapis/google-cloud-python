# Copyright 2026 Google LLC
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

from bigframes.functions import Udf
from bigframes.functions.udf_def import BigqueryUdf, PythonUdf
from bigframes.operations import base_ops, remote_function_ops


def func_to_op(op) -> base_ops.NaryOp:
    """
    Convert various bigframes, python functions into bigframes operations.

    This should handle anything that might be passed to eg map, combine, other pandas methods that take a function.

    It should raise a TypeError if the object is not a supported type.

    Args:
        op: The object to convert.

    Returns:
        A bigframes operations.
    """
    # TODO: Handle numpy ufuncs, builtin functions, etc.
    if isinstance(op, Udf):
        if isinstance(op.udf_def, BigqueryUdf):
            return remote_function_ops.RemoteFunctionOp(function_def=op.udf_def)
        elif isinstance(op.udf_def, PythonUdf):
            return remote_function_ops.PythonUdfOp(function_def=op.udf_def)
    else:
        raise TypeError(f"Unsupported function type: {op}")
