# Copyright 2025 Google LLC
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

import numpy as np

from bigframes.operations import base_ops, generic_ops, numeric_ops

# Just parameterless unary ops for now
# TODO: Parameter mappings
NUMPY_TO_OP: dict[np.ufunc, base_ops.UnaryOp] = {
    np.sin: numeric_ops.sin_op,
    np.cos: numeric_ops.cos_op,
    np.tan: numeric_ops.tan_op,
    np.arcsin: numeric_ops.arcsin_op,
    np.arccos: numeric_ops.arccos_op,
    np.arctan: numeric_ops.arctan_op,
    np.sinh: numeric_ops.sinh_op,
    np.cosh: numeric_ops.cosh_op,
    np.tanh: numeric_ops.tanh_op,
    np.arcsinh: numeric_ops.arcsinh_op,
    np.arccosh: numeric_ops.arccosh_op,
    np.arctanh: numeric_ops.arctanh_op,
    np.exp: numeric_ops.exp_op,
    np.log: numeric_ops.ln_op,
    np.log10: numeric_ops.log10_op,
    np.sqrt: numeric_ops.sqrt_op,
    np.abs: numeric_ops.abs_op,
    np.floor: numeric_ops.floor_op,
    np.ceil: numeric_ops.ceil_op,
    np.log1p: numeric_ops.log1p_op,
    np.expm1: numeric_ops.expm1_op,
}


NUMPY_TO_BINOP: dict[np.ufunc, base_ops.BinaryOp] = {
    np.add: numeric_ops.add_op,
    np.subtract: numeric_ops.sub_op,
    np.multiply: numeric_ops.mul_op,
    np.divide: numeric_ops.div_op,
    np.power: numeric_ops.pow_op,
    np.arctan2: numeric_ops.arctan2_op,
    np.maximum: generic_ops.maximum_op,
    np.minimum: generic_ops.minimum_op,
}
