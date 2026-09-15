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

#include "nanoarrow.h"
#include <stdio.h>
#include <stdarg.h>

void ArrowErrorSet(struct ArrowError* error, const char* fmt, ...) {
    if (error == NULL) return;
    va_list args;
    va_start(args, fmt);
    vsnprintf(error->message, sizeof(error->message), fmt, args);
    va_end(args);
}

void ArrowBufferInit(struct ArrowBuffer* buffer) {
    buffer->data = NULL;
    buffer->size_bytes = 0;
    buffer->capacity_bytes = 0;
}

int ArrowBufferReserve(struct ArrowBuffer* buffer, int64_t additional_bytes) {
    int64_t target_capacity = buffer->size_bytes + additional_bytes;
    if (target_capacity <= buffer->capacity_bytes) {
        return 0;
    }
    int64_t new_capacity = buffer->capacity_bytes == 0 ? 64 : buffer->capacity_bytes * 2;
    while (new_capacity < target_capacity) {
        new_capacity *= 2;
    }
    uint8_t* new_data = (uint8_t*)realloc(buffer->data, (size_t)new_capacity);
    if (new_data == NULL) {
        return -1;
    }
    buffer->data = new_data;
    buffer->capacity_bytes = new_capacity;
    return 0;
}

int ArrowBufferAppend(struct ArrowBuffer* buffer, const void* data, int64_t size_bytes) {
    if (ArrowBufferReserve(buffer, size_bytes) != 0) {
        return -1;
    }
    if (data != NULL && size_bytes > 0) {
        memcpy(buffer->data + buffer->size_bytes, data, (size_t)size_bytes);
    }
    buffer->size_bytes += size_bytes;
    return 0;
}

int ArrowBufferAppendFill(struct ArrowBuffer* buffer, uint8_t value, int64_t size_bytes) {
    if (ArrowBufferReserve(buffer, size_bytes) != 0) {
        return -1;
    }
    if (size_bytes > 0) {
        memset(buffer->data + buffer->size_bytes, value, (size_t)size_bytes);
    }
    buffer->size_bytes += size_bytes;
    return 0;
}

void ArrowBufferReset(struct ArrowBuffer* buffer) {
    if (buffer->data != NULL) {
        free(buffer->data);
        buffer->data = NULL;
    }
    buffer->size_bytes = 0;
    buffer->capacity_bytes = 0;
}

void ArrowBitmapInit(struct ArrowBitmap* bitmap) {
    ArrowBufferInit(&bitmap->buffer);
    bitmap->null_count = 0;
}

int ArrowBitmapReserve(struct ArrowBitmap* bitmap, int64_t additional_elements) {
    int64_t current_elements = bitmap->buffer.size_bytes * 8;
    int64_t target_elements = current_elements + additional_elements;
    int64_t target_bytes = (target_elements + 7) / 8;
    return ArrowBufferReserve(&bitmap->buffer, target_bytes - bitmap->buffer.size_bytes);
}

int ArrowBitmapAppend(struct ArrowBitmap* bitmap, uint8_t is_valid, int64_t count) {
    for (int64_t i = 0; i < count; i++) {
        int64_t bit_index = bitmap->buffer.size_bytes * 8;
        if (bit_index % 8 == 0) {
            uint8_t zero = 0;
            if (ArrowBufferAppend(&bitmap->buffer, &zero, 1) != 0) {
                return -1;
            }
        }
        int64_t byte_pos = bitmap->buffer.size_bytes - 1;
        int bit_pos = (int)((bit_index) % 8);
        if (is_valid) {
            bitmap->buffer.data[byte_pos] |= (uint8_t)(1 << bit_pos);
        } else {
            bitmap->null_count++;
        }
    }
    return 0;
}

void ArrowBitmapReset(struct ArrowBitmap* bitmap) {
    ArrowBufferReset(&bitmap->buffer);
    bitmap->null_count = 0;
}

static char* nanoarrow_strdup(const char* s) {
    if (s == NULL) return NULL;
    size_t len = strlen(s);
    char* copy = (char*)malloc(len + 1);
    if (copy) {
        memcpy(copy, s, len + 1);
    }
    return copy;
}

void ArrowSchemaRelease(struct ArrowSchema* schema) {
    if (schema == NULL || schema->release == NULL) {
        return;
    }
    if (schema->format != NULL) {
        free((void*)schema->format);
        schema->format = NULL;
    }
    if (schema->name != NULL) {
        free((void*)schema->name);
        schema->name = NULL;
    }
    if (schema->metadata != NULL) {
        free((void*)schema->metadata);
        schema->metadata = NULL;
    }
    if (schema->children != NULL) {
        for (int64_t i = 0; i < schema->n_children; i++) {
            if (schema->children[i] != NULL) {
                if (schema->children[i]->release != NULL) {
                    schema->children[i]->release(schema->children[i]);
                }
                free(schema->children[i]);
            }
        }
        free(schema->children);
        schema->children = NULL;
    }
    if (schema->dictionary != NULL) {
        if (schema->dictionary->release != NULL) {
            schema->dictionary->release(schema->dictionary);
        }
        free(schema->dictionary);
        schema->dictionary = NULL;
    }
    schema->release = NULL;
}

void ArrowSchemaInit(struct ArrowSchema* schema, enum ArrowType type) {
    schema->format = NULL;
    schema->name = NULL;
    schema->metadata = NULL;
    schema->flags = ARROW_FLAG_NULLABLE;
    schema->n_children = 0;
    schema->children = NULL;
    schema->dictionary = NULL;
    schema->release = &ArrowSchemaRelease;
    schema->private_data = NULL;

    switch (type) {
        case NANOARROW_TYPE_BOOL:
            ArrowSchemaSetFormat(schema, "b");
            break;
        case NANOARROW_TYPE_INT8:
            ArrowSchemaSetFormat(schema, "c");
            break;
        case NANOARROW_TYPE_UINT8:
            ArrowSchemaSetFormat(schema, "C");
            break;
        case NANOARROW_TYPE_INT16:
            ArrowSchemaSetFormat(schema, "s");
            break;
        case NANOARROW_TYPE_UINT16:
            ArrowSchemaSetFormat(schema, "S");
            break;
        case NANOARROW_TYPE_INT32:
            ArrowSchemaSetFormat(schema, "i");
            break;
        case NANOARROW_TYPE_UINT32:
            ArrowSchemaSetFormat(schema, "I");
            break;
        case NANOARROW_TYPE_INT64:
            ArrowSchemaSetFormat(schema, "l");
            break;
        case NANOARROW_TYPE_UINT64:
            ArrowSchemaSetFormat(schema, "L");
            break;
        case NANOARROW_TYPE_FLOAT:
            ArrowSchemaSetFormat(schema, "f");
            break;
        case NANOARROW_TYPE_DOUBLE:
            ArrowSchemaSetFormat(schema, "g");
            break;
        case NANOARROW_TYPE_STRING:
            ArrowSchemaSetFormat(schema, "u");
            break;
        case NANOARROW_TYPE_BINARY:
            ArrowSchemaSetFormat(schema, "z");
            break;
        case NANOARROW_TYPE_DATE32:
            ArrowSchemaSetFormat(schema, "tdD");
            break;
        case NANOARROW_TYPE_TIMESTAMP:
            ArrowSchemaSetFormat(schema, "tsu:UTC");
            break;
        case NANOARROW_TYPE_DECIMAL128:
            ArrowSchemaSetFormat(schema, "d:38,9");
            break;
        case NANOARROW_TYPE_LIST:
            ArrowSchemaSetFormat(schema, "+l");
            break;
        case NANOARROW_TYPE_STRUCT:
            ArrowSchemaSetFormat(schema, "+s");
            break;
        case NANOARROW_TYPE_NA:
            ArrowSchemaSetFormat(schema, "n");
            break;
        default:
            ArrowSchemaSetFormat(schema, "n");
            break;
    }
}

int ArrowSchemaSetFormat(struct ArrowSchema* schema, const char* format) {
    if (schema->format != NULL) {
        free((void*)schema->format);
    }
    schema->format = nanoarrow_strdup(format);
    return schema->format == NULL ? -1 : 0;
}

int ArrowSchemaSetName(struct ArrowSchema* schema, const char* name) {
    if (schema->name != NULL) {
        free((void*)schema->name);
    }
    schema->name = nanoarrow_strdup(name);
    return schema->name == NULL ? -1 : 0;
}

int ArrowSchemaAllocateChildren(struct ArrowSchema* schema, int64_t n_children) {
    schema->n_children = n_children;
    schema->children = (struct ArrowSchema**)calloc((size_t)n_children, sizeof(struct ArrowSchema*));
    if (schema->children == NULL) {
        return -1;
    }
    for (int64_t i = 0; i < n_children; i++) {
        schema->children[i] = (struct ArrowSchema*)calloc(1, sizeof(struct ArrowSchema));
        if (schema->children[i] == NULL) {
            return -1;
        }
        ArrowSchemaInit(schema->children[i], NANOARROW_TYPE_UNINITIALIZED);
    }
    return 0;
}

void ArrowArrayRelease(struct ArrowArray* array) {
    if (array == NULL || array->release == NULL) {
        return;
    }
    if (array->private_data != NULL) {
        struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
        ArrowBitmapReset(&private_data->bitmap);
        ArrowBufferReset(&private_data->buffer1);
        ArrowBufferReset(&private_data->buffer2);
        free(private_data);
        array->private_data = NULL;
    }
    if (array->buffers != NULL) {
        free((void*)array->buffers);
        array->buffers = NULL;
    }
    if (array->children != NULL) {
        for (int64_t i = 0; i < array->n_children; i++) {
            if (array->children[i] != NULL) {
                if (array->children[i]->release != NULL) {
                    array->children[i]->release(array->children[i]);
                }
                free(array->children[i]);
            }
        }
        free(array->children);
        array->children = NULL;
    }
    if (array->dictionary != NULL) {
        if (array->dictionary->release != NULL) {
            array->dictionary->release(array->dictionary);
        }
        free(array->dictionary);
        array->dictionary = NULL;
    }
    array->release = NULL;
}

static enum ArrowType type_from_format(const char* format) {
    if (format == NULL) return NANOARROW_TYPE_UNINITIALIZED;
    if (strcmp(format, "b") == 0) return NANOARROW_TYPE_BOOL;
    if (strcmp(format, "c") == 0) return NANOARROW_TYPE_INT8;
    if (strcmp(format, "C") == 0) return NANOARROW_TYPE_UINT8;
    if (strcmp(format, "s") == 0) return NANOARROW_TYPE_INT16;
    if (strcmp(format, "S") == 0) return NANOARROW_TYPE_UINT16;
    if (strcmp(format, "i") == 0) return NANOARROW_TYPE_INT32;
    if (strcmp(format, "I") == 0) return NANOARROW_TYPE_UINT32;
    if (strcmp(format, "l") == 0) return NANOARROW_TYPE_INT64;
    if (strcmp(format, "L") == 0) return NANOARROW_TYPE_UINT64;
    if (strcmp(format, "f") == 0) return NANOARROW_TYPE_FLOAT;
    if (strcmp(format, "g") == 0) return NANOARROW_TYPE_DOUBLE;
    if (strcmp(format, "u") == 0) return NANOARROW_TYPE_STRING;
    if (strcmp(format, "z") == 0) return NANOARROW_TYPE_BINARY;
    if (strcmp(format, "tdD") == 0) return NANOARROW_TYPE_DATE32;
    if (strncmp(format, "ts", 2) == 0) return NANOARROW_TYPE_TIMESTAMP;
    if (strncmp(format, "d:", 2) == 0) return NANOARROW_TYPE_DECIMAL128;
    if (strcmp(format, "+l") == 0) return NANOARROW_TYPE_LIST;
    if (strcmp(format, "+s") == 0) return NANOARROW_TYPE_STRUCT;
    if (strcmp(format, "n") == 0) return NANOARROW_TYPE_NA;
    return NANOARROW_TYPE_UNINITIALIZED;
}

int ArrowArrayInitFromSchema(struct ArrowArray* array, struct ArrowSchema* schema, struct ArrowError* error) {
    array->length = 0;
    array->null_count = 0;
    array->offset = 0;
    array->n_buffers = 0;
    array->n_children = 0;
    array->buffers = NULL;
    array->children = NULL;
    array->dictionary = NULL;
    array->release = &ArrowArrayRelease;
    array->private_data = NULL;

    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)calloc(1, sizeof(struct ArrowArrayPrivateData));
    if (private_data == NULL) {
        ArrowErrorSet(error, "Failed to allocate private data for ArrowArray");
        return -1;
    }
    ArrowBitmapInit(&private_data->bitmap);
    ArrowBufferInit(&private_data->buffer1);
    ArrowBufferInit(&private_data->buffer2);
    private_data->type = type_from_format(schema->format);
    array->private_data = private_data;

    switch (private_data->type) {
        case NANOARROW_TYPE_BOOL:
        case NANOARROW_TYPE_INT8:
        case NANOARROW_TYPE_UINT8:
        case NANOARROW_TYPE_INT16:
        case NANOARROW_TYPE_UINT16:
        case NANOARROW_TYPE_INT32:
        case NANOARROW_TYPE_UINT32:
        case NANOARROW_TYPE_INT64:
        case NANOARROW_TYPE_UINT64:
        case NANOARROW_TYPE_FLOAT:
        case NANOARROW_TYPE_DOUBLE:
        case NANOARROW_TYPE_DATE32:
        case NANOARROW_TYPE_TIMESTAMP:
        case NANOARROW_TYPE_DECIMAL128:
            array->n_buffers = 2;
            array->buffers = (const void**)calloc(2, sizeof(void*));
            break;
        case NANOARROW_TYPE_STRING:
        case NANOARROW_TYPE_BINARY:
            array->n_buffers = 3;
            array->buffers = (const void**)calloc(3, sizeof(void*));
            break;
        case NANOARROW_TYPE_STRUCT:
            array->n_buffers = 1;
            array->buffers = (const void**)calloc(1, sizeof(void*));
            if (schema->n_children > 0) {
                array->n_children = schema->n_children;
                array->children = (struct ArrowArray**)calloc((size_t)schema->n_children, sizeof(struct ArrowArray*));
                for (int64_t i = 0; i < schema->n_children; i++) {
                    array->children[i] = (struct ArrowArray*)calloc(1, sizeof(struct ArrowArray));
                    if (ArrowArrayInitFromSchema(array->children[i], schema->children[i], error) != 0) {
                        return -1;
                    }
                }
            }
            break;
        case NANOARROW_TYPE_LIST:
            array->n_buffers = 2;
            array->buffers = (const void**)calloc(2, sizeof(void*));
            if (schema->n_children == 1) {
                array->n_children = 1;
                array->children = (struct ArrowArray**)calloc(1, sizeof(struct ArrowArray*));
                array->children[0] = (struct ArrowArray*)calloc(1, sizeof(struct ArrowArray));
                if (ArrowArrayInitFromSchema(array->children[0], schema->children[0], error) != 0) {
                    return -1;
                }
            }
            break;
        case NANOARROW_TYPE_NA:
            array->n_buffers = 0;
            break;
        default:
            array->n_buffers = 2;
            array->buffers = (const void**)calloc(2, sizeof(void*));
            break;
    }
    return 0;
}

int ArrowArrayStartAppending(struct ArrowArray* array) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;

    if (private_data->type == NANOARROW_TYPE_STRING ||
        private_data->type == NANOARROW_TYPE_BINARY ||
        private_data->type == NANOARROW_TYPE_LIST) {
        int32_t zero_offset = 0;
        if (ArrowBufferAppend(&private_data->buffer1, &zero_offset, sizeof(int32_t)) != 0) {
            return -1;
        }
    }
    if (array->n_children > 0 && array->children != NULL) {
        for (int64_t i = 0; i < array->n_children; i++) {
            if (ArrowArrayStartAppending(array->children[i]) != 0) {
                return -1;
            }
        }
    }
    return 0;
}

int ArrowArrayAppendNull(struct ArrowArray* array, int64_t n) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;

    for (int64_t i = 0; i < n; i++) {
        if (ArrowBitmapAppend(&private_data->bitmap, 0, 1) != 0) return -1;
        array->length++;

        switch (private_data->type) {
            case NANOARROW_TYPE_BOOL: {
                int64_t bit_idx = private_data->buffer1.size_bytes * 8;
                if (bit_idx % 8 == 0) {
                    uint8_t zero = 0;
                    ArrowBufferAppend(&private_data->buffer1, &zero, 1);
                }
                break;
            }
            case NANOARROW_TYPE_INT8:
            case NANOARROW_TYPE_UINT8: {
                uint8_t zero = 0;
                ArrowBufferAppend(&private_data->buffer1, &zero, 1);
                break;
            }
            case NANOARROW_TYPE_INT16:
            case NANOARROW_TYPE_UINT16: {
                int16_t zero = 0;
                ArrowBufferAppend(&private_data->buffer1, &zero, 2);
                break;
            }
            case NANOARROW_TYPE_INT32:
            case NANOARROW_TYPE_UINT32:
            case NANOARROW_TYPE_DATE32: {
                int32_t zero = 0;
                ArrowBufferAppend(&private_data->buffer1, &zero, 4);
                break;
            }
            case NANOARROW_TYPE_INT64:
            case NANOARROW_TYPE_UINT64:
            case NANOARROW_TYPE_TIMESTAMP: {
                int64_t zero = 0;
                ArrowBufferAppend(&private_data->buffer1, &zero, 8);
                break;
            }
            case NANOARROW_TYPE_FLOAT: {
                float zero = 0.0f;
                ArrowBufferAppend(&private_data->buffer1, &zero, 4);
                break;
            }
            case NANOARROW_TYPE_DOUBLE: {
                double zero = 0.0;
                ArrowBufferAppend(&private_data->buffer1, &zero, 8);
                break;
            }
            case NANOARROW_TYPE_DECIMAL128: {
                uint8_t zero[16] = {0};
                ArrowBufferAppend(&private_data->buffer1, zero, 16);
                break;
            }
            case NANOARROW_TYPE_STRING:
            case NANOARROW_TYPE_BINARY: {
                int32_t current_offset = (int32_t)private_data->buffer2.size_bytes;
                ArrowBufferAppend(&private_data->buffer1, &current_offset, sizeof(int32_t));
                break;
            }
            case NANOARROW_TYPE_LIST: {
                int32_t child_len = array->n_children > 0 ? (int32_t)array->children[0]->length : 0;
                ArrowBufferAppend(&private_data->buffer1, &child_len, sizeof(int32_t));
                break;
            }
            case NANOARROW_TYPE_STRUCT: {
                // For struct null, append null to children
                if (array->n_children > 0 && array->children != NULL) {
                    for (int64_t c = 0; c < array->n_children; c++) {
                        ArrowArrayAppendNull(array->children[c], 1);
                    }
                }
                break;
            }
            default:
                break;
        }
    }
    return 0;
}

int ArrowArrayAppendInt(struct ArrowArray* array, int64_t value) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;
    if (ArrowBitmapAppend(&private_data->bitmap, 1, 1) != 0) return -1;
    array->length++;

    switch (private_data->type) {
        case NANOARROW_TYPE_INT8: {
            int8_t v = (int8_t)value;
            return ArrowBufferAppend(&private_data->buffer1, &v, sizeof(int8_t));
        }
        case NANOARROW_TYPE_INT16: {
            int16_t v = (int16_t)value;
            return ArrowBufferAppend(&private_data->buffer1, &v, sizeof(int16_t));
        }
        case NANOARROW_TYPE_INT32:
        case NANOARROW_TYPE_DATE32: {
            int32_t v = (int32_t)value;
            return ArrowBufferAppend(&private_data->buffer1, &v, sizeof(int32_t));
        }
        case NANOARROW_TYPE_INT64:
        case NANOARROW_TYPE_TIMESTAMP: {
            return ArrowBufferAppend(&private_data->buffer1, &value, sizeof(int64_t));
        }
        default:
            return ArrowBufferAppend(&private_data->buffer1, &value, sizeof(int64_t));
    }
}

int ArrowArrayAppendDouble(struct ArrowArray* array, double value) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;
    if (ArrowBitmapAppend(&private_data->bitmap, 1, 1) != 0) return -1;
    array->length++;
    return ArrowBufferAppend(&private_data->buffer1, &value, sizeof(double));
}

int ArrowArrayAppendFloat(struct ArrowArray* array, float value) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;
    if (ArrowBitmapAppend(&private_data->bitmap, 1, 1) != 0) return -1;
    array->length++;
    return ArrowBufferAppend(&private_data->buffer1, &value, sizeof(float));
}

int ArrowArrayAppendBool(struct ArrowArray* array, uint8_t value) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;
    if (ArrowBitmapAppend(&private_data->bitmap, 1, 1) != 0) return -1;

    int64_t bit_index = array->length;
    array->length++;
    if (bit_index % 8 == 0) {
        uint8_t zero = 0;
        if (ArrowBufferAppend(&private_data->buffer1, &zero, 1) != 0) {
            return -1;
        }
    }
    int64_t byte_pos = private_data->buffer1.size_bytes - 1;
    int bit_pos = (int)(bit_index % 8);
    if (value) {
        private_data->buffer1.data[byte_pos] |= (uint8_t)(1 << bit_pos);
    }
    return 0;
}

int ArrowArrayAppendString(struct ArrowArray* array, struct ArrowStringView value) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;
    if (ArrowBitmapAppend(&private_data->bitmap, 1, 1) != 0) return -1;
    array->length++;

    if (value.data != NULL && value.size_bytes > 0) {
        if (ArrowBufferAppend(&private_data->buffer2, value.data, value.size_bytes) != 0) {
            return -1;
        }
    }
    int32_t new_offset = (int32_t)private_data->buffer2.size_bytes;
    return ArrowBufferAppend(&private_data->buffer1, &new_offset, sizeof(int32_t));
}

int ArrowArrayAppendBytes(struct ArrowArray* array, struct ArrowBufferView value) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;
    if (ArrowBitmapAppend(&private_data->bitmap, 1, 1) != 0) return -1;
    array->length++;

    if (value.data != NULL && value.size_bytes > 0) {
        if (ArrowBufferAppend(&private_data->buffer2, value.data, value.size_bytes) != 0) {
            return -1;
        }
    }
    int32_t new_offset = (int32_t)private_data->buffer2.size_bytes;
    return ArrowBufferAppend(&private_data->buffer1, &new_offset, sizeof(int32_t));
}

int ArrowArrayAppendDecimal128(struct ArrowArray* array, struct ArrowDecimal128 value) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;
    if (ArrowBitmapAppend(&private_data->bitmap, 1, 1) != 0) return -1;
    array->length++;
    return ArrowBufferAppend(&private_data->buffer1, value.bytes, sizeof(value.bytes));
}

int ArrowArrayAppendList(struct ArrowArray* array) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;
    if (ArrowBitmapAppend(&private_data->bitmap, 1, 1) != 0) return -1;
    array->length++;
    int32_t child_len = array->n_children > 0 ? (int32_t)array->children[0]->length : 0;
    return ArrowBufferAppend(&private_data->buffer1, &child_len, sizeof(int32_t));
}

int ArrowArrayAppendStruct(struct ArrowArray* array) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return -1;
    if (ArrowBitmapAppend(&private_data->bitmap, 1, 1) != 0) return -1;
    array->length++;
    return 0;
}

int ArrowArrayFinishBuildingDefault(struct ArrowArray* array, struct ArrowError* error) {
    struct ArrowArrayPrivateData* private_data = (struct ArrowArrayPrivateData*)array->private_data;
    if (private_data == NULL) return 0;

    array->null_count = private_data->bitmap.null_count;

    switch (private_data->type) {
        case NANOARROW_TYPE_BOOL:
        case NANOARROW_TYPE_INT8:
        case NANOARROW_TYPE_UINT8:
        case NANOARROW_TYPE_INT16:
        case NANOARROW_TYPE_UINT16:
        case NANOARROW_TYPE_INT32:
        case NANOARROW_TYPE_UINT32:
        case NANOARROW_TYPE_INT64:
        case NANOARROW_TYPE_UINT64:
        case NANOARROW_TYPE_FLOAT:
        case NANOARROW_TYPE_DOUBLE:
        case NANOARROW_TYPE_DATE32:
        case NANOARROW_TYPE_TIMESTAMP:
        case NANOARROW_TYPE_DECIMAL128:
            array->buffers[0] = (array->null_count > 0) ? private_data->bitmap.buffer.data : NULL;
            array->buffers[1] = private_data->buffer1.data;
            break;
        case NANOARROW_TYPE_STRING:
        case NANOARROW_TYPE_BINARY:
            array->buffers[0] = (array->null_count > 0) ? private_data->bitmap.buffer.data : NULL;
            array->buffers[1] = private_data->buffer1.data;
            array->buffers[2] = private_data->buffer2.data;
            break;
        case NANOARROW_TYPE_STRUCT:
            array->buffers[0] = (array->null_count > 0) ? private_data->bitmap.buffer.data : NULL;
            for (int64_t i = 0; i < array->n_children; i++) {
                if (ArrowArrayFinishBuildingDefault(array->children[i], error) != 0) {
                    return -1;
                }
            }
            break;
        case NANOARROW_TYPE_LIST:
            array->buffers[0] = (array->null_count > 0) ? private_data->bitmap.buffer.data : NULL;
            array->buffers[1] = private_data->buffer1.data;
            if (array->n_children == 1) {
                if (ArrowArrayFinishBuildingDefault(array->children[0], error) != 0) {
                    return -1;
                }
            }
            break;
        default:
            break;
    }
    return 0;
}
