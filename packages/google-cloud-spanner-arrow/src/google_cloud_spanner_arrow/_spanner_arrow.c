// Copyright 2026 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "nanoarrow/nanoarrow.h"
#include <ctype.h>
#include <math.h>
#include <stdbool.h>

// Spanner TypeCode enum constants (matching google.cloud.spanner_v1.types.TypeCode)
#define SPANNER_TYPE_UNSPECIFIED 0
#define SPANNER_TYPE_BOOL 1
#define SPANNER_TYPE_INT64 2
#define SPANNER_TYPE_FLOAT64 3
#define SPANNER_TYPE_TIMESTAMP 4
#define SPANNER_TYPE_DATE 5
#define SPANNER_TYPE_STRING 6
#define SPANNER_TYPE_BYTES 7
#define SPANNER_TYPE_ARRAY 8
#define SPANNER_TYPE_STRUCT 9
#define SPANNER_TYPE_NUMERIC 10
#define SPANNER_TYPE_JSON 11
#define SPANNER_TYPE_PROTO 13
#define SPANNER_TYPE_ENUM 14
#define SPANNER_TYPE_FLOAT32 15
#define SPANNER_TYPE_INTERVAL 16
#define SPANNER_TYPE_UUID 17

static const int8_t base64_decode_table[256] = {
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1,  0, -1, -1,
    -1,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,
    -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
};

static size_t base64_decode(const char* src, size_t src_len, uint8_t* dst) {
    if (src_len == 0 || src == NULL || dst == NULL) return 0;
    size_t out_len = 0;
    uint32_t buf = 0;
    int bits = 0;

    for (size_t i = 0; i < src_len; i++) {
        unsigned char c = (unsigned char)src[i];
        if (c == '=') break;
        int8_t val = base64_decode_table[c];
        if (val < 0) continue;
        buf = (buf << 6) | (uint32_t)val;
        bits += 6;
        if (bits >= 8) {
            bits -= 8;
            dst[out_len++] = (uint8_t)((buf >> bits) & 0xFF);
        }
    }
    return out_len;
}

static int32_t parse_date32_fast(const char* str, size_t len) {
    if (len < 10 || str == NULL) return 0;
    int year = (str[0]-'0')*1000 + (str[1]-'0')*100 + (str[2]-'0')*10 + (str[3]-'0');
    int month = (str[5]-'0')*10 + (str[6]-'0');
    int day = (str[8]-'0')*10 + (str[9]-'0');

    year -= (month <= 2);
    const int era = (year >= 0 ? year : year - 399) / 400;
    const unsigned yoe = (unsigned)(year - era * 400);
    const unsigned doy = (153 * (month + (month > 2 ? -3 : 9)) + 2) / 5 + day - 1;
    const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return (int32_t)(era * 146097 + (int)doe - 719468);
}

static int64_t parse_timestamp_us_fast(const char* str, size_t len) {
    if (len < 19 || str == NULL) return 0;
    int32_t days = parse_date32_fast(str, len);
    int hour = (str[11]-'0')*10 + (str[12]-'0');
    int min = (str[14]-'0')*10 + (str[15]-'0');
    int sec = (str[17]-'0')*10 + (str[18]-'0');

    int64_t total_us = ((int64_t)days * 86400LL + (int64_t)hour * 3600LL + (int64_t)min * 60LL + (int64_t)sec) * 1000000LL;

    if (len > 19 && str[19] == '.') {
        size_t idx = 20;
        int64_t frac_us = 0;
        int digits = 0;
        while (idx < len && isdigit((unsigned char)str[idx]) && digits < 6) {
            frac_us = frac_us * 10 + (str[idx] - '0');
            digits++;
            idx++;
        }
        while (digits < 6) {
            frac_us *= 10;
            digits++;
        }
        total_us += frac_us;
    }
    return total_us;
}

static void parse_decimal128_fast(const char* str, size_t len, struct ArrowDecimal128* out) {
    memset(out->bytes, 0, 16);
    if (len == 0 || str == NULL) return;

    int sign = 1;
    size_t i = 0;
    if (str[0] == '-') {
        sign = -1;
        i = 1;
    } else if (str[0] == '+') {
        i = 1;
    }

#if defined(__SIZEOF_INT128__)
    unsigned __int128 whole = 0;
    unsigned __int128 frac = 0;
    int frac_digits = 0;
    bool in_frac = false;

    for (; i < len; i++) {
        char c = str[i];
        if (c == '.') {
            in_frac = true;
            continue;
        }
        if (isdigit((unsigned char)c)) {
            if (!in_frac) {
                whole = whole * 10 + (c - '0');
            } else if (frac_digits < 9) {
                frac = frac * 10 + (c - '0');
                frac_digits++;
            }
        }
    }
    while (frac_digits < 9) {
        frac *= 10;
        frac_digits++;
    }
    unsigned __int128 scale_multiplier = 1000000000ULL;
    unsigned __int128 total = whole * scale_multiplier + frac;
    __int128 final_val = (sign < 0) ? -((__int128)total) : ((__int128)total);
    memcpy(out->bytes, &final_val, 16);
#else
    int64_t whole = 0;
    int64_t frac = 0;
    int frac_digits = 0;
    bool in_frac = false;
    for (; i < len; i++) {
        char c = str[i];
        if (c == '.') {
            in_frac = true;
            continue;
        }
        if (isdigit((unsigned char)c)) {
            if (!in_frac) {
                whole = whole * 10 + (c - '0');
            } else if (frac_digits < 9) {
                frac = frac * 10 + (c - '0');
                frac_digits++;
            }
        }
    }
    while (frac_digits < 9) {
        frac *= 10;
        frac_digits++;
    }
    int64_t total = (whole * 1000000000LL + frac) * sign;
    memcpy(out->bytes, &total, 8);
    if (sign < 0) {
        memset(out->bytes + 8, 0xFF, 8);
    }
#endif
}

static void configure_field_schema(struct ArrowSchema* schema, PyObject* f_obj) {
    const char* col_name = "col";
    int type_code = SPANNER_TYPE_STRING;
    PyObject* children_obj = NULL;

    if (PyTuple_Check(f_obj) && PyTuple_Size(f_obj) >= 2) {
        PyObject* name_obj = PyTuple_GET_ITEM(f_obj, 0);
        PyObject* type_obj = PyTuple_GET_ITEM(f_obj, 1);
        if (PyUnicode_Check(name_obj)) {
            col_name = PyUnicode_AsUTF8(name_obj);
        }
        if (PyLong_Check(type_obj)) {
            type_code = (int)PyLong_AsLong(type_obj);
        }
        if (PyTuple_Size(f_obj) >= 3) {
            children_obj = PyTuple_GET_ITEM(f_obj, 2);
        }
    }

    ArrowSchemaSetName(schema, col_name);
    schema->flags = ARROW_FLAG_NULLABLE;
    schema->release = &ArrowSchemaRelease;

    switch (type_code) {
        case SPANNER_TYPE_BOOL:
            ArrowSchemaSetFormat(schema, "b");
            break;
        case SPANNER_TYPE_INT64:
        case SPANNER_TYPE_ENUM:
            ArrowSchemaSetFormat(schema, "l");
            break;
        case SPANNER_TYPE_FLOAT32:
            ArrowSchemaSetFormat(schema, "f");
            break;
        case SPANNER_TYPE_FLOAT64:
            ArrowSchemaSetFormat(schema, "g");
            break;
        case SPANNER_TYPE_STRING:
        case SPANNER_TYPE_JSON:
        case SPANNER_TYPE_INTERVAL:
        case SPANNER_TYPE_UUID:
            ArrowSchemaSetFormat(schema, "u");
            break;
        case SPANNER_TYPE_BYTES:
        case SPANNER_TYPE_PROTO:
            ArrowSchemaSetFormat(schema, "z");
            break;
        case SPANNER_TYPE_DATE:
            ArrowSchemaSetFormat(schema, "tdD");
            break;
        case SPANNER_TYPE_TIMESTAMP:
            ArrowSchemaSetFormat(schema, "tsu:UTC");
            break;
        case SPANNER_TYPE_NUMERIC:
            ArrowSchemaSetFormat(schema, "d:38,9");
            break;
        case SPANNER_TYPE_ARRAY:
            ArrowSchemaSetFormat(schema, "+l");
            ArrowSchemaAllocateChildren(schema, 1);
            if (children_obj != NULL) {
                configure_field_schema(schema->children[0], children_obj);
            } else {
                ArrowSchemaSetName(schema->children[0], "item");
                ArrowSchemaSetFormat(schema->children[0], "u");
            }
            break;
        case SPANNER_TYPE_STRUCT:
            ArrowSchemaSetFormat(schema, "+s");
            if (children_obj != NULL && PySequence_Check(children_obj)) {
                Py_ssize_t n_sub = PySequence_Size(children_obj);
                ArrowSchemaAllocateChildren(schema, (int64_t)n_sub);
                for (Py_ssize_t s = 0; s < n_sub; s++) {
                    PyObject* sub_item = PySequence_GetItem(children_obj, s);
                    configure_field_schema(schema->children[s], sub_item);
                    Py_XDECREF(sub_item);
                }
            }
            break;
        default:
            ArrowSchemaSetFormat(schema, "u");
            break;
    }
}

// --------------------------------------------------------------------------
// Python Object Cell Ingestion
// --------------------------------------------------------------------------

static int append_python_cell(struct ArrowArray* col_array, PyObject* cell, PyObject* f_obj) {
    int type_code = SPANNER_TYPE_STRING;
    PyObject* children_obj = NULL;

    if (PyTuple_Check(f_obj) && PyTuple_Size(f_obj) >= 2) {
        PyObject* type_obj = PyTuple_GET_ITEM(f_obj, 1);
        if (PyLong_Check(type_obj)) {
            type_code = (int)PyLong_AsLong(type_obj);
        }
        if (PyTuple_Size(f_obj) >= 3) {
            children_obj = PyTuple_GET_ITEM(f_obj, 2);
        }
    }

    if (cell == NULL || cell == Py_None) {
        return ArrowArrayAppendNull(col_array, 1);
    }

    if (PyObject_HasAttrString(cell, "WhichOneof")) {
        PyObject* kind_obj = PyObject_CallMethod(cell, "WhichOneof", "s", "kind");
        if (kind_obj == NULL || kind_obj == Py_None) {
            Py_XDECREF(kind_obj);
            return ArrowArrayAppendNull(col_array, 1);
        }
        const char* kind = PyUnicode_AsUTF8(kind_obj);
        if (kind == NULL || strcmp(kind, "null_value") == 0) {
            Py_DECREF(kind_obj);
            return ArrowArrayAppendNull(col_array, 1);
        }
        if (strcmp(kind, "bool_value") == 0) {
            PyObject* val_obj = PyObject_GetAttrString(cell, "bool_value");
            int b = PyObject_IsTrue(val_obj);
            Py_XDECREF(val_obj);
            Py_DECREF(kind_obj);
            return ArrowArrayAppendBool(col_array, (uint8_t)b);
        }
        if (strcmp(kind, "number_value") == 0) {
            PyObject* val_obj = PyObject_GetAttrString(cell, "number_value");
            double d = PyFloat_AsDouble(val_obj);
            Py_XDECREF(val_obj);
            Py_DECREF(kind_obj);
            if (type_code == SPANNER_TYPE_FLOAT32) {
                return ArrowArrayAppendFloat(col_array, (float)d);
            }
            return ArrowArrayAppendDouble(col_array, d);
        }
        if (strcmp(kind, "string_value") == 0) {
            PyObject* val_obj = PyObject_GetAttrString(cell, "string_value");
            Py_ssize_t str_len = 0;
            const char* str_val = PyUnicode_AsUTF8AndSize(val_obj, &str_len);
            int ret = 0;

            if (str_val == NULL) {
                Py_XDECREF(val_obj);
                Py_DECREF(kind_obj);
                return ArrowArrayAppendNull(col_array, 1);
            }

            switch (type_code) {
                case SPANNER_TYPE_INT64:
                case SPANNER_TYPE_ENUM: {
                    int64_t val = (int64_t)strtoll(str_val, NULL, 10);
                    ret = ArrowArrayAppendInt(col_array, val);
                    break;
                }
                case SPANNER_TYPE_FLOAT64: {
                    double val = 0.0;
                    if (strcmp(str_val, "NaN") == 0) {
                        val = NAN;
                    } else if (strcmp(str_val, "Infinity") == 0) {
                        val = INFINITY;
                    } else if (strcmp(str_val, "-Infinity") == 0) {
                        val = -INFINITY;
                    } else {
                        val = strtod(str_val, NULL);
                    }
                    ret = ArrowArrayAppendDouble(col_array, val);
                    break;
                }
                case SPANNER_TYPE_FLOAT32: {
                    float val = 0.0f;
                    if (strcmp(str_val, "NaN") == 0) {
                        val = (float)NAN;
                    } else if (strcmp(str_val, "Infinity") == 0) {
                        val = (float)INFINITY;
                    } else if (strcmp(str_val, "-Infinity") == 0) {
                        val = (float)-INFINITY;
                    } else {
                        val = strtof(str_val, NULL);
                    }
                    ret = ArrowArrayAppendFloat(col_array, val);
                    break;
                }
                case SPANNER_TYPE_BYTES:
                case SPANNER_TYPE_PROTO: {
                    size_t max_decoded = (size_t)(str_len * 3 / 4 + 4);
                    uint8_t* decode_buf = (uint8_t*)malloc(max_decoded);
                    if (decode_buf != NULL) {
                        size_t decoded_len = base64_decode(str_val, (size_t)str_len, decode_buf);
                        struct ArrowBufferView view = {decode_buf, (int64_t)decoded_len};
                        ret = ArrowArrayAppendBytes(col_array, view);
                        free(decode_buf);
                    } else {
                        ret = ArrowArrayAppendNull(col_array, 1);
                    }
                    break;
                }
                case SPANNER_TYPE_DATE: {
                    int32_t days = parse_date32_fast(str_val, (size_t)str_len);
                    ret = ArrowArrayAppendInt(col_array, days);
                    break;
                }
                case SPANNER_TYPE_TIMESTAMP: {
                    int64_t ts_us = parse_timestamp_us_fast(str_val, (size_t)str_len);
                    ret = ArrowArrayAppendInt(col_array, ts_us);
                    break;
                }
                case SPANNER_TYPE_NUMERIC: {
                    struct ArrowDecimal128 dec;
                    parse_decimal128_fast(str_val, (size_t)str_len, &dec);
                    ret = ArrowArrayAppendDecimal128(col_array, dec);
                    break;
                }
                default: {
                    struct ArrowStringView view = {str_val, (int64_t)str_len};
                    ret = ArrowArrayAppendString(col_array, view);
                    break;
                }
            }
            Py_XDECREF(val_obj);
            Py_DECREF(kind_obj);
            return ret;
        }
        if (strcmp(kind, "list_value") == 0) {
            PyObject* val_obj = PyObject_GetAttrString(cell, "list_value");
            PyObject* values_list = val_obj ? PyObject_GetAttrString(val_obj, "values") : NULL;
            if (values_list && PySequence_Check(values_list)) {
                Py_ssize_t list_len = PySequence_Size(values_list);
                for (Py_ssize_t li = 0; li < list_len; li++) {
                    PyObject* elem = PySequence_GetItem(values_list, li);
                    if (col_array->n_children > 0) {
                        append_python_cell(col_array->children[0], elem, children_obj);
                    }
                    Py_XDECREF(elem);
                }
            }
            Py_XDECREF(values_list);
            Py_XDECREF(val_obj);
            Py_DECREF(kind_obj);
            return ArrowArrayAppendList(col_array);
        }
        if (strcmp(kind, "struct_value") == 0) {
            PyObject* val_obj = PyObject_GetAttrString(cell, "struct_value");
            PyObject* fields_dict = val_obj ? PyObject_GetAttrString(val_obj, "fields") : NULL;
            if (fields_dict && children_obj && PySequence_Check(children_obj)) {
                Py_ssize_t n_sub = PySequence_Size(children_obj);
                for (Py_ssize_t s = 0; s < n_sub; s++) {
                    PyObject* sub_info = PySequence_GetItem(children_obj, s);
                    PyObject* sub_name = PyTuple_GET_ITEM(sub_info, 0);
                    PyObject* sub_val = PyObject_GetItem(fields_dict, sub_name);
                    if (sub_val == NULL) {
                        PyErr_Clear();
                        sub_val = Py_None;
                        Py_INCREF(sub_val);
                    }
                    if (s < col_array->n_children) {
                        append_python_cell(col_array->children[s], sub_val, sub_info);
                    }
                    Py_XDECREF(sub_val);
                    Py_XDECREF(sub_info);
                }
            }
            Py_XDECREF(fields_dict);
            Py_XDECREF(val_obj);
            Py_DECREF(kind_obj);
            return ArrowArrayAppendStruct(col_array);
        }
        Py_DECREF(kind_obj);
        return ArrowArrayAppendNull(col_array, 1);
    }

    if (PyBool_Check(cell)) {
        return ArrowArrayAppendBool(col_array, cell == Py_True ? 1 : 0);
    }
    if (PyLong_Check(cell)) {
        int64_t v = (int64_t)PyLong_AsLongLong(cell);
        if (type_code == SPANNER_TYPE_DATE) {
            return ArrowArrayAppendInt(col_array, (int32_t)v);
        }
        return ArrowArrayAppendInt(col_array, v);
    }
    if (PyFloat_Check(cell)) {
        double d = PyFloat_AS_DOUBLE(cell);
        if (type_code == SPANNER_TYPE_FLOAT32) {
            return ArrowArrayAppendFloat(col_array, (float)d);
        }
        return ArrowArrayAppendDouble(col_array, d);
    }
    if (PyBytes_Check(cell)) {
        Py_ssize_t b_len = PyBytes_GET_SIZE(cell);
        const char* b_data = PyBytes_AS_STRING(cell);
        struct ArrowBufferView view = {b_data, (int64_t)b_len};
        return ArrowArrayAppendBytes(col_array, view);
    }
    if (PyUnicode_Check(cell)) {
        Py_ssize_t str_len = 0;
        const char* str_val = PyUnicode_AsUTF8AndSize(cell, &str_len);
        if (str_val == NULL) {
            return ArrowArrayAppendNull(col_array, 1);
        }
        switch (type_code) {
            case SPANNER_TYPE_INT64:
            case SPANNER_TYPE_ENUM: {
                int64_t val = (int64_t)strtoll(str_val, NULL, 10);
                return ArrowArrayAppendInt(col_array, val);
            }
            case SPANNER_TYPE_FLOAT64: {
                double val = strtod(str_val, NULL);
                return ArrowArrayAppendDouble(col_array, val);
            }
            case SPANNER_TYPE_FLOAT32: {
                float val = strtof(str_val, NULL);
                return ArrowArrayAppendFloat(col_array, val);
            }
            case SPANNER_TYPE_BYTES:
            case SPANNER_TYPE_PROTO: {
                size_t max_decoded = (size_t)(str_len * 3 / 4 + 4);
                uint8_t* decode_buf = (uint8_t*)malloc(max_decoded);
                if (decode_buf != NULL) {
                    size_t decoded_len = base64_decode(str_val, (size_t)str_len, decode_buf);
                    struct ArrowBufferView view = {decode_buf, (int64_t)decoded_len};
                    int ret = ArrowArrayAppendBytes(col_array, view);
                    free(decode_buf);
                    return ret;
                }
                return ArrowArrayAppendNull(col_array, 1);
            }
            case SPANNER_TYPE_DATE: {
                int32_t days = parse_date32_fast(str_val, (size_t)str_len);
                return ArrowArrayAppendInt(col_array, days);
            }
            case SPANNER_TYPE_TIMESTAMP: {
                int64_t ts_us = parse_timestamp_us_fast(str_val, (size_t)str_len);
                return ArrowArrayAppendInt(col_array, ts_us);
            }
            case SPANNER_TYPE_NUMERIC: {
                struct ArrowDecimal128 dec;
                parse_decimal128_fast(str_val, (size_t)str_len, &dec);
                return ArrowArrayAppendDecimal128(col_array, dec);
            }
            default: {
                struct ArrowStringView view = {str_val, (int64_t)str_len};
                return ArrowArrayAppendString(col_array, view);
            }
        }
    }

    return ArrowArrayAppendNull(col_array, 1);
}

static PyObject* py_rows_to_c_batch(PyObject* self, PyObject* args) {
    PyObject* py_fields;
    PyObject* py_rows;

    if (!PyArg_ParseTuple(args, "OO", &py_fields, &py_rows)) {
        return NULL;
    }

    if (!PySequence_Check(py_fields) || !PySequence_Check(py_rows)) {
        PyErr_SetString(PyExc_TypeError, "fields and rows must be sequences");
        return NULL;
    }

    Py_ssize_t num_cols = PySequence_Size(py_fields);
    Py_ssize_t num_rows = PySequence_Size(py_rows);

    struct ArrowSchema* out_schema = (struct ArrowSchema*)calloc(1, sizeof(struct ArrowSchema));
    struct ArrowArray* out_array = (struct ArrowArray*)calloc(1, sizeof(struct ArrowArray));
    struct ArrowError error;

    if (out_schema == NULL || out_array == NULL) {
        if (out_schema) free(out_schema);
        if (out_array) free(out_array);
        PyErr_NoMemory();
        return NULL;
    }

    ArrowSchemaInit(out_schema, NANOARROW_TYPE_STRUCT);
    ArrowSchemaAllocateChildren(out_schema, (int64_t)num_cols);

    for (Py_ssize_t i = 0; i < num_cols; i++) {
        PyObject* f = PySequence_GetItem(py_fields, i);
        configure_field_schema(out_schema->children[i], f);
        Py_XDECREF(f);
    }

    if (ArrowArrayInitFromSchema(out_array, out_schema, &error) != 0) {
        ArrowSchemaRelease(out_schema);
        free(out_schema);
        free(out_array);
        PyErr_Format(PyExc_RuntimeError, "Failed to init ArrowArray: %s", error.message);
        return NULL;
    }

    ArrowArrayStartAppending(out_array);

    for (Py_ssize_t r = 0; r < num_rows; r++) {
        PyObject* row = PySequence_GetItem(py_rows, r);
        if (row != NULL && PySequence_Check(row)) {
            Py_ssize_t row_len = PySequence_Size(row);
            for (Py_ssize_t c = 0; c < num_cols; c++) {
                PyObject* f_info = PySequence_GetItem(py_fields, c);
                PyObject* cell = (c < row_len) ? PySequence_GetItem(row, c) : NULL;
                append_python_cell(out_array->children[c], cell, f_info);
                Py_XDECREF(cell);
                Py_XDECREF(f_info);
            }
            out_array->length++;
        }
        Py_XDECREF(row);
    }

    if (ArrowArrayFinishBuildingDefault(out_array, &error) != 0) {
        ArrowArrayRelease(out_array);
        ArrowSchemaRelease(out_schema);
        free(out_array);
        free(out_schema);
        PyErr_Format(PyExc_RuntimeError, "Failed to finish ArrowArray: %s", error.message);
        return NULL;
    }

    uintptr_t array_ptr = (uintptr_t)out_array;
    uintptr_t schema_ptr = (uintptr_t)out_schema;

    return Py_BuildValue("(KK)", (unsigned long long)array_ptr, (unsigned long long)schema_ptr);
}

// --------------------------------------------------------------------------
// Direct Protobuf Wire Parser Helpers (No Python Object Allocations)
// --------------------------------------------------------------------------

static inline uint64_t decode_varint(const uint8_t** ptr, const uint8_t* end) {
    uint64_t result = 0;
    int shift = 0;
    const uint8_t* p = *ptr;
    while (p < end && shift < 64) {
        uint8_t byte = *p++;
        result |= ((uint64_t)(byte & 0x7F)) << shift;
        if ((byte & 0x80) == 0) {
            *ptr = p;
            return result;
        }
        shift += 7;
    }
    *ptr = p;
    return result;
}

static inline const uint8_t* read_length_delimited(const uint8_t** ptr, const uint8_t* end, uint64_t* out_len) {
    uint64_t len = decode_varint(ptr, end);
    *out_len = len;
    const uint8_t* slice = *ptr;
    *ptr += len;
    if (*ptr > end) {
        *ptr = end;
    }
    return slice;
}

static inline void skip_wire_field(const uint8_t** ptr, const uint8_t* end, int wire_type) {
    switch (wire_type) {
        case 0:
            decode_varint(ptr, end);
            break;
        case 1:
            *ptr += 8;
            if (*ptr > end) *ptr = end;
            break;
        case 2: {
            uint64_t len = decode_varint(ptr, end);
            *ptr += len;
            if (*ptr > end) *ptr = end;
            break;
        }
        case 5:
            *ptr += 4;
            if (*ptr > end) *ptr = end;
            break;
        default:
            *ptr = end;
            break;
    }
}

static int append_wire_value(struct ArrowArray* col_array, int type_code, const uint8_t* p, const uint8_t* val_end) {
    if (p >= val_end) {
        return ArrowArrayAppendNull(col_array, 1);
    }

    while (p < val_end) {
        uint64_t tag = decode_varint(&p, val_end);
        int field_num = (int)(tag >> 3);
        int wire_type = (int)(tag & 0x07);

        if (field_num == 1 && wire_type == 0) {
            decode_varint(&p, val_end);
            return ArrowArrayAppendNull(col_array, 1);
        } else if (field_num == 2 && wire_type == 1) {
            if (p + 8 <= val_end) {
                double d;
                memcpy(&d, p, 8);
                p += 8;
                if (type_code == SPANNER_TYPE_FLOAT32) {
                    return ArrowArrayAppendFloat(col_array, (float)d);
                }
                return ArrowArrayAppendDouble(col_array, d);
            }
            return ArrowArrayAppendNull(col_array, 1);
        } else if (field_num == 3 && wire_type == 2) {
            uint64_t str_len = 0;
            const uint8_t* str_data = read_length_delimited(&p, val_end, &str_len);
            const char* str_val = (const char*)str_data;

            switch (type_code) {
                case SPANNER_TYPE_INT64:
                case SPANNER_TYPE_ENUM: {
                    int64_t val = (int64_t)strtoll(str_val, NULL, 10);
                    return ArrowArrayAppendInt(col_array, val);
                }
                case SPANNER_TYPE_FLOAT64: {
                    double val = 0.0;
                    if (str_len == 3 && strncmp(str_val, "NaN", 3) == 0) {
                        val = NAN;
                    } else if (str_len == 8 && strncmp(str_val, "Infinity", 8) == 0) {
                        val = INFINITY;
                    } else if (str_len == 9 && strncmp(str_val, "-Infinity", 9) == 0) {
                        val = -INFINITY;
                    } else {
                        val = strtod(str_val, NULL);
                    }
                    return ArrowArrayAppendDouble(col_array, val);
                }
                case SPANNER_TYPE_FLOAT32: {
                    float val = 0.0f;
                    if (str_len == 3 && strncmp(str_val, "NaN", 3) == 0) {
                        val = (float)NAN;
                    } else if (str_len == 8 && strncmp(str_val, "Infinity", 8) == 0) {
                        val = (float)INFINITY;
                    } else if (str_len == 9 && strncmp(str_val, "-Infinity", 9) == 0) {
                        val = (float)-INFINITY;
                    } else {
                        val = strtof(str_val, NULL);
                    }
                    return ArrowArrayAppendFloat(col_array, val);
                }
                case SPANNER_TYPE_BYTES:
                case SPANNER_TYPE_PROTO: {
                    size_t max_decoded = (size_t)(str_len * 3 / 4 + 4);
                    uint8_t* decode_buf = (uint8_t*)malloc(max_decoded);
                    if (decode_buf != NULL) {
                        size_t decoded_len = base64_decode(str_val, (size_t)str_len, decode_buf);
                        struct ArrowBufferView view = {decode_buf, (int64_t)decoded_len};
                        int ret = ArrowArrayAppendBytes(col_array, view);
                        free(decode_buf);
                        return ret;
                    }
                    return ArrowArrayAppendNull(col_array, 1);
                }
                case SPANNER_TYPE_DATE: {
                    int32_t days = parse_date32_fast(str_val, (size_t)str_len);
                    return ArrowArrayAppendInt(col_array, days);
                }
                case SPANNER_TYPE_TIMESTAMP: {
                    int64_t ts_us = parse_timestamp_us_fast(str_val, (size_t)str_len);
                    return ArrowArrayAppendInt(col_array, ts_us);
                }
                case SPANNER_TYPE_NUMERIC: {
                    struct ArrowDecimal128 dec;
                    parse_decimal128_fast(str_val, (size_t)str_len, &dec);
                    return ArrowArrayAppendDecimal128(col_array, dec);
                }
                default: {
                    struct ArrowStringView view = {str_val, (int64_t)str_len};
                    return ArrowArrayAppendString(col_array, view);
                }
            }
        } else if (field_num == 4 && wire_type == 0) {
            uint64_t b = decode_varint(&p, val_end);
            return ArrowArrayAppendBool(col_array, b ? 1 : 0);
        } else if (field_num == 6 && wire_type == 2) {
            uint64_t list_len = 0;
            const uint8_t* list_data = read_length_delimited(&p, val_end, &list_len);
            const uint8_t* lp = list_data;
            const uint8_t* lend = list_data + list_len;
            while (lp < lend) {
                uint64_t ltag = decode_varint(&lp, lend);
                if ((ltag >> 3) == 1 && (ltag & 0x07) == 2) {
                    uint64_t elem_len = 0;
                    const uint8_t* elem_data = read_length_delimited(&lp, lend, &elem_len);
                    if (col_array->n_children > 0) {
                        append_wire_value(col_array->children[0], SPANNER_TYPE_STRING, elem_data, elem_data + elem_len);
                    }
                } else {
                    skip_wire_field(&lp, lend, (int)(ltag & 0x07));
                }
            }
            return ArrowArrayAppendList(col_array);
        } else {
            skip_wire_field(&p, val_end, wire_type);
        }
    }
    return ArrowArrayAppendNull(col_array, 1);
}

static void parse_single_wire_prs(
    const uint8_t* p,
    const uint8_t* end,
    int num_cols,
    const int* col_type_codes,
    struct ArrowArray* out_array,
    int* current_col_idx
) {
    while (p < end) {
        uint64_t tag = decode_varint(&p, end);
        int field_num = (int)(tag >> 3);
        int wire_type = (int)(tag & 0x07);

        if (field_num == 2 && wire_type == 2) {
            uint64_t val_len = 0;
            const uint8_t* val_data = read_length_delimited(&p, end, &val_len);
            int col_idx = *current_col_idx;
            append_wire_value(out_array->children[col_idx], col_type_codes[col_idx], val_data, val_data + val_len);
            col_idx++;
            if (col_idx == num_cols) {
                col_idx = 0;
                out_array->length++;
            }
            *current_col_idx = col_idx;
        } else {
            skip_wire_field(&p, end, wire_type);
        }
    }
}

static PyObject* py_wire_prs_to_c_batch(PyObject* self, PyObject* args) {
    PyObject* py_fields;
    PyObject* py_wire_chunks;

    if (!PyArg_ParseTuple(args, "OO", &py_fields, &py_wire_chunks)) {
        return NULL;
    }

    if (!PySequence_Check(py_fields) || !PySequence_Check(py_wire_chunks)) {
        PyErr_SetString(PyExc_TypeError, "fields and wire_chunks must be sequences");
        return NULL;
    }

    Py_ssize_t num_cols = PySequence_Size(py_fields);
    Py_ssize_t num_chunks = PySequence_Size(py_wire_chunks);

    int* type_codes = (int*)malloc(num_cols * sizeof(int));
    if (type_codes == NULL) {
        PyErr_NoMemory();
        return NULL;
    }

    struct ArrowSchema* out_schema = (struct ArrowSchema*)calloc(1, sizeof(struct ArrowSchema));
    struct ArrowArray* out_array = (struct ArrowArray*)calloc(1, sizeof(struct ArrowArray));
    struct ArrowError error;

    if (out_schema == NULL || out_array == NULL) {
        if (out_schema) free(out_schema);
        if (out_array) free(out_array);
        free(type_codes);
        PyErr_NoMemory();
        return NULL;
    }

    ArrowSchemaInit(out_schema, NANOARROW_TYPE_STRUCT);
    ArrowSchemaAllocateChildren(out_schema, (int64_t)num_cols);

    for (Py_ssize_t i = 0; i < num_cols; i++) {
        PyObject* f = PySequence_GetItem(py_fields, i);
        configure_field_schema(out_schema->children[i], f);
        type_codes[i] = SPANNER_TYPE_STRING;
        if (PyTuple_Check(f) && PyTuple_Size(f) >= 2) {
            PyObject* t_obj = PyTuple_GET_ITEM(f, 1);
            if (PyLong_Check(t_obj)) {
                type_codes[i] = (int)PyLong_AsLong(t_obj);
            }
        }
        Py_XDECREF(f);
    }

    if (ArrowArrayInitFromSchema(out_array, out_schema, &error) != 0) {
        ArrowSchemaRelease(out_schema);
        free(out_schema);
        free(out_array);
        free(type_codes);
        PyErr_Format(PyExc_RuntimeError, "Failed to init ArrowArray: %s", error.message);
        return NULL;
    }

    ArrowArrayStartAppending(out_array);

    typedef struct {
        const uint8_t* ptr;
        size_t len;
    } RawBuf;

    RawBuf* raw_buffers = (RawBuf*)malloc(num_chunks * sizeof(RawBuf));
    if (raw_buffers == NULL) {
        ArrowArrayRelease(out_array);
        ArrowSchemaRelease(out_schema);
        free(out_array);
        free(out_schema);
        free(type_codes);
        PyErr_NoMemory();
        return NULL;
    }

    for (Py_ssize_t i = 0; i < num_chunks; i++) {
        PyObject* chunk_obj = PySequence_GetItem(py_wire_chunks, i);
        if (chunk_obj != NULL && PyBytes_Check(chunk_obj)) {
            raw_buffers[i].ptr = (const uint8_t*)PyBytes_AS_STRING(chunk_obj);
            raw_buffers[i].len = (size_t)PyBytes_GET_SIZE(chunk_obj);
        } else {
            raw_buffers[i].ptr = NULL;
            raw_buffers[i].len = 0;
        }
        Py_XDECREF(chunk_obj);
    }

    Py_BEGIN_ALLOW_THREADS
    int current_col_idx = 0;
    for (Py_ssize_t i = 0; i < num_chunks; i++) {
        if (raw_buffers[i].ptr != NULL && raw_buffers[i].len > 0) {
            parse_single_wire_prs(
                raw_buffers[i].ptr,
                raw_buffers[i].ptr + raw_buffers[i].len,
                (int)num_cols,
                type_codes,
                out_array,
                &current_col_idx
            );
        }
    }
    Py_END_ALLOW_THREADS

    free(raw_buffers);
    free(type_codes);

    if (ArrowArrayFinishBuildingDefault(out_array, &error) != 0) {
        ArrowArrayRelease(out_array);
        ArrowSchemaRelease(out_schema);
        free(out_array);
        free(out_schema);
        PyErr_Format(PyExc_RuntimeError, "Failed to finish ArrowArray: %s", error.message);
        return NULL;
    }

    uintptr_t array_ptr = (uintptr_t)out_array;
    uintptr_t schema_ptr = (uintptr_t)out_schema;

    return Py_BuildValue("(KK)", (unsigned long long)array_ptr, (unsigned long long)schema_ptr);
}

static PyMethodDef SpannerArrowMethods[] = {
    {"rows_to_c_batch", py_rows_to_c_batch, METH_VARARGS,
     "Convert sequence of Spanner rows into Arrow C Data Interface pointers."},
    {"wire_prs_to_c_batch", py_wire_prs_to_c_batch, METH_VARARGS,
     "Convert raw protobuf wire PartialResultSet bytes directly into Arrow C Data Interface pointers without allocating Python objects."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef spannerarrowmodule = {
    PyModuleDef_HEAD_INIT,
    "_spanner_arrow",
    "High-performance native Apache Arrow accelerator for Google Cloud Spanner",
    -1,
    SpannerArrowMethods
};

PyMODINIT_FUNC PyInit__spanner_arrow(void) {
    return PyModule_Create(&spannerarrowmodule);
}
