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

#ifndef NANOARROW_H_INCLUDED
#define NANOARROW_H_INCLUDED

#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

// Arrow C Data Interface specification definitions
#ifndef ARROW_C_DATA_INTERFACE
#define ARROW_C_DATA_INTERFACE

#define ARROW_FLAG_DICTIONARY_ORDERED 1
#define ARROW_FLAG_NULLABLE 2
#define ARROW_FLAG_MAP_KEYS_SORTED 4

struct ArrowSchema {
    const char* format;
    const char* name;
    const char* metadata;
    int64_t flags;
    int64_t n_children;
    struct ArrowSchema** children;
    struct ArrowSchema* dictionary;
    void (*release)(struct ArrowSchema*);
    void* private_data;
};

struct ArrowArray {
    int64_t length;
    int64_t null_count;
    int64_t offset;
    int64_t n_buffers;
    int64_t n_children;
    const void** buffers;
    struct ArrowArray** children;
    struct ArrowArray* dictionary;
    void (*release)(struct ArrowArray*);
    void* private_data;
};

#endif  // ARROW_C_DATA_INTERFACE

enum ArrowType {
    NANOARROW_TYPE_UNINITIALIZED = 0,
    NANOARROW_TYPE_NA = 1,
    NANOARROW_TYPE_BOOL = 2,
    NANOARROW_TYPE_INT8 = 3,
    NANOARROW_TYPE_UINT8 = 4,
    NANOARROW_TYPE_INT16 = 5,
    NANOARROW_TYPE_UINT16 = 6,
    NANOARROW_TYPE_INT32 = 7,
    NANOARROW_TYPE_UINT32 = 8,
    NANOARROW_TYPE_INT64 = 9,
    NANOARROW_TYPE_UINT64 = 10,
    NANOARROW_TYPE_FLOAT = 11,
    NANOARROW_TYPE_DOUBLE = 12,
    NANOARROW_TYPE_STRING = 13,
    NANOARROW_TYPE_BINARY = 14,
    NANOARROW_TYPE_DATE32 = 15,
    NANOARROW_TYPE_TIMESTAMP = 16,
    NANOARROW_TYPE_DECIMAL128 = 17,
    NANOARROW_TYPE_LIST = 18,
    NANOARROW_TYPE_STRUCT = 19
};

struct ArrowError {
    char message[1024];
};

struct ArrowStringView {
    const char* data;
    int64_t size_bytes;
};

struct ArrowBufferView {
    const void* data;
    int64_t size_bytes;
};

struct ArrowDecimal128 {
    uint8_t bytes[16];
};

struct ArrowBuffer {
    uint8_t* data;
    int64_t size_bytes;
    int64_t capacity_bytes;
};

struct ArrowBitmap {
    struct ArrowBuffer buffer;
    int64_t null_count;
};

struct ArrowArrayPrivateData {
    enum ArrowType type;
    struct ArrowBitmap bitmap;
    struct ArrowBuffer buffer1;  // Offsets (for string/binary/list) or data (for primitive)
    struct ArrowBuffer buffer2;  // Data (for string/binary)
};

// Buffer functions
void ArrowBufferInit(struct ArrowBuffer* buffer);
int ArrowBufferReserve(struct ArrowBuffer* buffer, int64_t additional_bytes);
int ArrowBufferAppend(struct ArrowBuffer* buffer, const void* data, int64_t size_bytes);
int ArrowBufferAppendFill(struct ArrowBuffer* buffer, uint8_t value, int64_t size_bytes);
void ArrowBufferReset(struct ArrowBuffer* buffer);

// Bitmap functions
void ArrowBitmapInit(struct ArrowBitmap* bitmap);
int ArrowBitmapReserve(struct ArrowBitmap* bitmap, int64_t additional_elements);
int ArrowBitmapAppend(struct ArrowBitmap* bitmap, uint8_t is_valid, int64_t count);
static inline void ArrowBitmapSet(struct ArrowBitmap* bitmap, int64_t index, uint8_t is_valid) {
    if (is_valid) {
        bitmap->buffer.data[index / 8] |= (uint8_t)(1 << (index % 8));
    } else {
        bitmap->buffer.data[index / 8] &= (uint8_t)~(1 << (index % 8));
        bitmap->null_count++;
    }
}
void ArrowBitmapReset(struct ArrowBitmap* bitmap);

// Schema functions
void ArrowSchemaInit(struct ArrowSchema* schema, enum ArrowType type);
int ArrowSchemaSetFormat(struct ArrowSchema* schema, const char* format);
int ArrowSchemaSetName(struct ArrowSchema* schema, const char* name);
int ArrowSchemaAllocateChildren(struct ArrowSchema* schema, int64_t n_children);
void ArrowSchemaRelease(struct ArrowSchema* schema);

// Array functions
int ArrowArrayInitFromSchema(struct ArrowArray* array, struct ArrowSchema* schema, struct ArrowError* error);
int ArrowArrayStartAppending(struct ArrowArray* array);
int ArrowArrayAppendNull(struct ArrowArray* array, int64_t n);
int ArrowArrayAppendInt(struct ArrowArray* array, int64_t value);
int ArrowArrayAppendDouble(struct ArrowArray* array, double value);
int ArrowArrayAppendFloat(struct ArrowArray* array, float value);
int ArrowArrayAppendBool(struct ArrowArray* array, uint8_t value);
int ArrowArrayAppendString(struct ArrowArray* array, struct ArrowStringView value);
int ArrowArrayAppendBytes(struct ArrowArray* array, struct ArrowBufferView value);
int ArrowArrayAppendDecimal128(struct ArrowArray* array, struct ArrowDecimal128 value);
int ArrowArrayAppendList(struct ArrowArray* array);
int ArrowArrayAppendStruct(struct ArrowArray* array);
int ArrowArrayFinishBuildingDefault(struct ArrowArray* array, struct ArrowError* error);
void ArrowArrayRelease(struct ArrowArray* array);

#ifdef __cplusplus
}
#endif

#endif  // NANOARROW_H_INCLUDED
