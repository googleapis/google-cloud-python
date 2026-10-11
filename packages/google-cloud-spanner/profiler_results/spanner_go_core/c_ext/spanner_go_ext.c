#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#if defined(__has_include) && __has_include(<Python.h>)
#define Py_LIMITED_API 0x03090000
#include <Python.h>
#else
/* Self-contained PEP 384 Stable ABI (abi3) declarations for Linux x86_64
 * when python3-dev system headers are not installed. Uses only functions
 * guaranteed by CPython's stable ABI across Python 3.8 - 3.14+.
 */
typedef ssize_t Py_ssize_t;
typedef struct _object {
    Py_ssize_t ob_refcnt;
    void* ob_type;
} PyObject;

typedef struct _ts PyThreadState;
typedef PyObject* (*PyCFunction)(PyObject*, PyObject*);

#define METH_VARARGS 0x0001
#define METH_NOARGS  0x0004
#define PYTHON_ABI_VERSION 3

typedef struct PyMethodDef {
    const char* ml_name;
    PyCFunction ml_meth;
    int ml_flags;
    const char* ml_doc;
} PyMethodDef;

typedef struct PyModuleDef_Base {
    PyObject ob_base;
    PyObject* (*m_init)(void);
    Py_ssize_t m_index;
    PyObject* m_copy;
} PyModuleDef_Base;

#define PyModuleDef_HEAD_INIT { { 1, NULL }, NULL, 0, NULL }

typedef struct PyModuleDef {
    PyModuleDef_Base m_base;
    const char* m_name;
    const char* m_doc;
    Py_ssize_t m_size;
    PyMethodDef* m_methods;
    void* m_slots;
    void* m_traverse;
    void* m_clear;
    void* m_free;
} PyModuleDef;

extern PyObject _Py_NoneStruct;
#define Py_None (&_Py_NoneStruct)

extern PyObject* PyExc_RuntimeError;

extern void Py_IncRef(PyObject*);
extern void Py_DecRef(PyObject*);
#define Py_INCREF(op) Py_IncRef((PyObject*)(op))
#define Py_DECREF(op) Py_DecRef((PyObject*)(op))
#define Py_RETURN_NONE do { Py_IncRef(Py_None); return Py_None; } while (0)
#define Py_UNUSED(name) _unused_##name __attribute__((unused))

extern PyThreadState* PyEval_SaveThread(void);
extern void PyEval_RestoreThread(PyThreadState*);
#define Py_BEGIN_ALLOW_THREADS { PyThreadState *_save; _save = PyEval_SaveThread();
#define Py_END_ALLOW_THREADS   PyEval_RestoreThread(_save); }

extern int PyArg_ParseTuple(PyObject*, const char*, ...);
extern void PyErr_SetString(PyObject*, const char*);
extern PyObject* PyErr_Format(PyObject*, const char*, ...);
extern PyObject* PyLong_FromLong(long);
extern PyObject* PyLong_FromUnsignedLongLong(unsigned long long);
extern PyObject* PyFloat_FromDouble(double);
extern PyObject* PyBool_FromLong(long);
extern PyObject* PyUnicode_FromStringAndSize(const char*, Py_ssize_t);
extern PyObject* PyList_New(Py_ssize_t size);
extern int PyList_SetItem(PyObject*, Py_ssize_t, PyObject*);
extern int PyList_Append(PyObject*, PyObject*);
extern PyObject* PyTuple_New(Py_ssize_t size);
extern int PyTuple_SetItem(PyObject*, Py_ssize_t, PyObject*);
extern PyObject* PyModule_Create2(PyModuleDef*, int apiver);
#define PyModule_Create(m) PyModule_Create2((m), PYTHON_ABI_VERSION)
#define PyMODINIT_FUNC __attribute__((visibility("default"))) PyObject*
#endif

typedef enum {
    CELL_KIND_NULL = 0,
    CELL_KIND_BOOL = 1,
    CELL_KIND_NUMBER = 2,
    CELL_KIND_STRING = 3
} CellKind;

typedef struct {
    uint8_t kind;
    uint8_t bool_val;
    uint16_t _pad;
    uint32_t str_len;
    double number_val;
    const char* str_val;
} CSpannerCell;

typedef struct {
    int format;
    char* json_rows;
    CSpannerCell* cells;
    int row_count;
    int col_count;
    char* string_arena;
    char* server_timing;
    int attempt_count;
    char* error_msg;
    int error_code;
    int is_last;
} CSpannerBatch;

typedef uintptr_t (*InitGoCoreClientFn)(int channelCount);
typedef void (*CloseGoCoreClientFn)(uintptr_t handle);
typedef CSpannerBatch* (*ExecuteStreamingSqlSyncFn)(uintptr_t handle, const char* session, const char* sql, const char* paramId);
typedef void (*FreeSpannerBatchFn)(CSpannerBatch* batch);
typedef int (*StartGoCPUProfileFn)(const char* path);
typedef void (*StopGoCPUProfileFn)(void);
typedef int (*GetAsyncNotifyFDFn)(void);
typedef void (*SubmitStreamingSqlAsyncFn)(uintptr_t handle, uint64_t reqId, const char* session, const char* sql, const char* paramId);
typedef CSpannerBatch* (*PopCompletedAsyncFn)(uint64_t* outReqId);
typedef void (*ResetGoCoreStatsFn)(void);
typedef void (*GetGoCoreStatsFn)(uint64_t* outStats);

static void* g_go_lib = NULL;
static InitGoCoreClientFn g_init_client = NULL;
static CloseGoCoreClientFn g_close_client = NULL;
static ExecuteStreamingSqlSyncFn g_exec_sync = NULL;
static FreeSpannerBatchFn g_free_batch = NULL;
static StartGoCPUProfileFn g_start_prof = NULL;
static StopGoCPUProfileFn g_stop_prof = NULL;
static GetAsyncNotifyFDFn g_get_notify_fd = NULL;
static SubmitStreamingSqlAsyncFn g_submit_async = NULL;
static PopCompletedAsyncFn g_pop_completed = NULL;
static ResetGoCoreStatsFn g_reset_stats = NULL;
static GetGoCoreStatsFn g_get_stats = NULL;
static uint64_t g_c_pylist_decode_ns = 0;

static inline uint64_t c_thread_cputime_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

static int ensure_go_lib_loaded(void) {
    if (g_go_lib != NULL) {
        return 0;
    }

    Dl_info info;
    char lib_path[4096];
    lib_path[0] = '\0';

    if (dladdr((void*)ensure_go_lib_loaded, &info) && info.dli_fname) {
        const char* slash = strrchr(info.dli_fname, '/');
        if (slash) {
            size_t dir_len = (size_t)(slash - info.dli_fname);
            if (dir_len + 32 < sizeof(lib_path)) {
                memcpy(lib_path, info.dli_fname, dir_len);
                lib_path[dir_len] = '\0';
                strcat(lib_path, "/libspanner_go.so");
            }
        }
    }

    if (lib_path[0] != '\0') {
        g_go_lib = dlopen(lib_path, RTLD_NOW | RTLD_GLOBAL);
    }
    if (!g_go_lib) {
        g_go_lib = dlopen("libspanner_go.so", RTLD_NOW | RTLD_GLOBAL);
    }
    if (!g_go_lib) {
        PyErr_Format(PyExc_RuntimeError, "Failed to load libspanner_go.so: %s", dlerror());
        return -1;
    }

    g_init_client = (InitGoCoreClientFn)dlsym(g_go_lib, "InitGoCoreClient");
    g_close_client = (CloseGoCoreClientFn)dlsym(g_go_lib, "CloseGoCoreClient");
    g_exec_sync = (ExecuteStreamingSqlSyncFn)dlsym(g_go_lib, "ExecuteStreamingSqlSync");
    g_free_batch = (FreeSpannerBatchFn)dlsym(g_go_lib, "FreeSpannerBatch");
    g_start_prof = (StartGoCPUProfileFn)dlsym(g_go_lib, "StartGoCPUProfile");
    g_stop_prof = (StopGoCPUProfileFn)dlsym(g_go_lib, "StopGoCPUProfile");
    g_get_notify_fd = (GetAsyncNotifyFDFn)dlsym(g_go_lib, "GetAsyncNotifyFD");
    g_submit_async = (SubmitStreamingSqlAsyncFn)dlsym(g_go_lib, "SubmitStreamingSqlAsync");
    g_pop_completed = (PopCompletedAsyncFn)dlsym(g_go_lib, "PopCompletedAsync");
    g_reset_stats = (ResetGoCoreStatsFn)dlsym(g_go_lib, "ResetGoCoreStats");
    g_get_stats = (GetGoCoreStatsFn)dlsym(g_go_lib, "GetGoCoreStats");

    if (!g_init_client || !g_close_client || !g_exec_sync || !g_free_batch) {
        PyErr_SetString(PyExc_RuntimeError, "Missing required symbols in libspanner_go.so");
        return -1;
    }
    return 0;
}

static PyObject* batch_to_pylist(CSpannerBatch* batch) {
    uint64_t t0 = c_thread_cputime_ns();
    int row_count = batch->row_count;
    int col_count = batch->col_count;
    PyObject* rows_list = PyList_New(row_count);
    if (!rows_list) {
        return NULL;
    }

    CSpannerCell* cells = batch->cells;
    for (int r = 0; r < row_count; r++) {
        PyObject* row_obj = PyList_New(col_count);
        if (!row_obj) {
            Py_DECREF(rows_list);
            return NULL;
        }
        int base_idx = r * col_count;
        for (int c = 0; c < col_count; c++) {
            CSpannerCell* cell = &cells[base_idx + c];
            PyObject* val_obj = NULL;
            switch (cell->kind) {
                case CELL_KIND_STRING:
                    if (cell->str_val && cell->str_len > 0) {
                        val_obj = PyUnicode_FromStringAndSize(cell->str_val, (Py_ssize_t)cell->str_len);
                    } else {
                        val_obj = PyUnicode_FromStringAndSize("", 0);
                    }
                    break;
                case CELL_KIND_NUMBER:
                    val_obj = PyFloat_FromDouble(cell->number_val);
                    break;
                case CELL_KIND_BOOL:
                    val_obj = PyBool_FromLong(cell->bool_val ? 1 : 0);
                    break;
                case CELL_KIND_NULL:
                default:
                    Py_INCREF(Py_None);
                    val_obj = Py_None;
                    break;
            }
            if (!val_obj) {
                Py_DECREF(row_obj);
                Py_DECREF(rows_list);
                return NULL;
            }
            PyList_SetItem(row_obj, c, val_obj);
        }
        PyList_SetItem(rows_list, r, row_obj);
    }
    uint64_t t1 = c_thread_cputime_ns();
    if (t1 >= t0) {
        __atomic_add_fetch(&g_c_pylist_decode_ns, t1 - t0, __ATOMIC_RELAXED);
    }
    return rows_list;
}

static PyObject* py_init_client(PyObject* self, PyObject* args) {
    int channel_count = 4;
    if (!PyArg_ParseTuple(args, "|i", &channel_count)) {
        return NULL;
    }
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }
    uintptr_t handle = 0;
    Py_BEGIN_ALLOW_THREADS
    handle = g_init_client(channel_count);
    Py_END_ALLOW_THREADS

    if (handle == 0) {
        PyErr_SetString(PyExc_RuntimeError, "InitGoCoreClient failed to initialize Go Spanner client");
        return NULL;
    }
    return PyLong_FromUnsignedLongLong((unsigned long long)handle);
}

static PyObject* py_close_client(PyObject* self, PyObject* args) {
    unsigned long long handle = 0;
    if (!PyArg_ParseTuple(args, "K", &handle)) {
        return NULL;
    }
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }
    Py_BEGIN_ALLOW_THREADS
    g_close_client((uintptr_t)handle);
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

static PyObject* py_start_cpu_profile(PyObject* self, PyObject* args) {
    const char* path = NULL;
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }
    int rc = -1;
    if (g_start_prof) {
        rc = g_start_prof(path);
    }
    return PyLong_FromLong(rc);
}

static PyObject* py_stop_cpu_profile(PyObject* self, PyObject* Py_UNUSED(ignored)) {
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }
    if (g_stop_prof) {
        Py_BEGIN_ALLOW_THREADS
        g_stop_prof();
        Py_END_ALLOW_THREADS
    }
    Py_RETURN_NONE;
}

static PyObject* py_execute_streaming_sql(PyObject* self, PyObject* args) {
    unsigned long long handle = 0;
    const char* session = NULL;
    const char* sql = NULL;
    const char* param_id = "";

    if (!PyArg_ParseTuple(args, "Kss|s", &handle, &session, &sql, &param_id)) {
        return NULL;
    }
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }

    CSpannerBatch* batch = NULL;
    Py_BEGIN_ALLOW_THREADS
    batch = g_exec_sync((uintptr_t)handle, session, sql, param_id);
    Py_END_ALLOW_THREADS

    if (!batch) {
        PyErr_SetString(PyExc_RuntimeError, "ExecuteStreamingSqlSync returned NULL batch");
        return NULL;
    }

    if (batch->error_code != 0) {
        const char* msg = batch->error_msg ? batch->error_msg : "Unknown Spanner Go Shared Core error";
        PyErr_Format(PyExc_RuntimeError, "Spanner Go Shared Core RPC error (%d): %s", batch->error_code, msg);
        g_free_batch(batch);
        return NULL;
    }

    PyObject* rows_list = batch_to_pylist(batch);
    g_free_batch(batch);
    return rows_list;
}

static PyObject* py_get_notify_fd(PyObject* self, PyObject* Py_UNUSED(ignored)) {
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }
    if (!g_get_notify_fd) {
        PyErr_SetString(PyExc_RuntimeError, "GetAsyncNotifyFD symbol not found");
        return NULL;
    }
    int fd = g_get_notify_fd();
    return PyLong_FromLong(fd);
}

static PyObject* py_submit_async(PyObject* self, PyObject* args) {
    unsigned long long handle = 0;
    unsigned long long req_id = 0;
    const char* session = NULL;
    const char* sql = NULL;
    const char* param_id = "";

    if (!PyArg_ParseTuple(args, "KKss|s", &handle, &req_id, &session, &sql, &param_id)) {
        return NULL;
    }
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }
    if (!g_submit_async) {
        PyErr_SetString(PyExc_RuntimeError, "SubmitStreamingSqlAsync symbol not found");
        return NULL;
    }
    g_submit_async((uintptr_t)handle, (uint64_t)req_id, session, sql, param_id);
    Py_RETURN_NONE;
}

static PyObject* py_pop_completed(PyObject* self, PyObject* Py_UNUSED(ignored)) {
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }
    if (!g_pop_completed) {
        PyErr_SetString(PyExc_RuntimeError, "PopCompletedAsync symbol not found");
        return NULL;
    }
    PyObject* results = PyList_New(0);
    if (!results) {
        return NULL;
    }
    while (1) {
        uint64_t req_id = 0;
        CSpannerBatch* batch = g_pop_completed(&req_id);
        if (!batch) {
            break;
        }
        PyObject* item = PyTuple_New(3);
        if (!item) {
            g_free_batch(batch);
            Py_DECREF(results);
            return NULL;
        }
        PyTuple_SetItem(item, 0, PyLong_FromUnsignedLongLong((unsigned long long)req_id));
        if (batch->error_code != 0) {
            const char* msg = batch->error_msg ? batch->error_msg : "Unknown Spanner Go Shared Core error";
            Py_INCREF(Py_None);
            PyTuple_SetItem(item, 1, Py_None);
            PyTuple_SetItem(item, 2, PyUnicode_FromStringAndSize(msg, (Py_ssize_t)strlen(msg)));
        } else {
            PyObject* rows_list = batch_to_pylist(batch);
            if (!rows_list) {
                g_free_batch(batch);
                Py_DECREF(item);
                Py_DECREF(results);
                return NULL;
            }
            PyTuple_SetItem(item, 1, rows_list);
            Py_INCREF(Py_None);
            PyTuple_SetItem(item, 2, Py_None);
        }
        g_free_batch(batch);
        if (PyList_Append(results, item) < 0) {
            Py_DECREF(item);
            Py_DECREF(results);
            return NULL;
        }
        Py_DECREF(item);
    }
    return results;
}

static PyObject* py_reset_core_stats(PyObject* self, PyObject* Py_UNUSED(ignored)) {
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }
    __atomic_store_n(&g_c_pylist_decode_ns, 0, __ATOMIC_RELAXED);
    if (g_reset_stats) {
        g_reset_stats();
    }
    Py_RETURN_NONE;
}

static PyObject* py_get_core_stats(PyObject* self, PyObject* Py_UNUSED(ignored)) {
    if (ensure_go_lib_loaded() < 0) {
        return NULL;
    }
    uint64_t go_stats[7] = {0};
    if (g_get_stats) {
        g_get_stats(go_stats);
    }
    uint64_t c_decode_ns = __atomic_load_n(&g_c_pylist_decode_ns, __ATOMIC_RELAXED);
    PyObject* tup = PyTuple_New(8);
    if (!tup) {
        return NULL;
    }
    for (int i = 0; i < 7; i++) {
        PyTuple_SetItem(tup, i, PyLong_FromUnsignedLongLong((unsigned long long)go_stats[i]));
    }
    PyTuple_SetItem(tup, 7, PyLong_FromUnsignedLongLong((unsigned long long)c_decode_ns));
    return tup;
}

static PyMethodDef SpannerGoExtMethods[] = {
    {"init_client", py_init_client, METH_VARARGS, "Initialize Go Shared Core Spanner client pool."},
    {"close_client", py_close_client, METH_VARARGS, "Close Go Shared Core Spanner client pool."},
    {"execute_streaming_sql", py_execute_streaming_sql, METH_VARARGS, "Execute streaming SQL on Go Shared Core releasing the GIL."},
    {"get_notify_fd", py_get_notify_fd, METH_NOARGS, "Get non-blocking pipe FD for asyncio completion notifications."},
    {"submit_async", py_submit_async, METH_VARARGS, "Submit non-blocking streaming SQL request to Go Shared Core."},
    {"pop_completed", py_pop_completed, METH_NOARGS, "Pop all completed async streaming SQL batches from Go Shared Core."},
    {"start_cpu_profile", py_start_cpu_profile, METH_VARARGS, "Start Go runtime/pprof CPU profiler."},
    {"stop_cpu_profile", py_stop_cpu_profile, METH_NOARGS, "Stop Go runtime/pprof CPU profiler."},
    {"reset_core_stats", py_reset_core_stats, METH_NOARGS, "Reset cross-FFI C and Go Shared Core CPU phase counters."},
    {"get_core_stats", py_get_core_stats, METH_NOARGS, "Get cross-FFI C and Go Shared Core CPU phase counters."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef spanner_go_ext_module = {
    PyModuleDef_HEAD_INIT,
    "spanner_go_ext",
    "CPython Stable ABI C-extension bridging Python to Go Spanner Shared Core",
    -1,
    SpannerGoExtMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_spanner_go_ext(void) {
    return PyModule_Create(&spanner_go_ext_module);
}
