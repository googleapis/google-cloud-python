/*
 * spanner_ipc_ext.c - CPython (abi3) client for the Spanner Go Shared Core IPC sidecar.
 *
 * This extension is the IPC twin of the FFI extension (../../c_ext/spanner_go_ext.c, which is
 * NOT modified). It keeps the FFI call shape and per-row work identical so that the two flows
 * differ ONLY in the boundary they cross:
 *
 *   FFI: Python -> spanner_go_ext.execute_streaming_sql(handle, session, sql, param)
 *          -> [GIL released] in-process cgo call ExecuteStreamingSqlSync() -> CSpannerBatch* (C heap)
 *          -> batch_to_pylist(): PyUnicode/PyFloat/PyBool/None per CSpannerCell
 *
 *   IPC: Python -> spanner_ipc_ext.execute_streaming_sql(handle, session, sql, param)
 *          -> [GIL released] send() request over AF_UNIX to the Go sidecar, which runs the SAME
 *             executeStreamingSqlInternal()/buildCBatch() and writev()s the CSpannerCell array +
 *             string arena verbatim -> recv() into a local buffer
 *          -> response_to_pylist(): the same PyUnicode/PyFloat/PyBool/None per CSpannerCell
 *
 * Each Python thread uses its own persistent connection (created lazily, pthread-specific),
 * so a thread performs one blocking request at a time - exactly like a thread blocked in the
 * FFI cgo call.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <pthread.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/un.h>
#include <time.h>
#include <unistd.h>

#if defined(__has_include) && __has_include(<Python.h>)
#define Py_LIMITED_API 0x03090000
#include <Python.h>
#else
/* Self-contained PEP 384 Stable ABI (abi3) declarations for Linux x86_64 when python3-dev
 * headers are not installed (same approach as the FFI extension). */
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
extern PyObject* PyExc_OSError;

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
extern PyObject* PyErr_NoMemory(void);
extern PyObject* PyLong_FromLong(long);
extern PyObject* PyLong_FromUnsignedLongLong(unsigned long long);
extern PyObject* PyFloat_FromDouble(double);
extern PyObject* PyBool_FromLong(long);
extern PyObject* PyUnicode_FromStringAndSize(const char*, Py_ssize_t);
extern PyObject* PyList_New(Py_ssize_t size);
extern int PyList_SetItem(PyObject*, Py_ssize_t, PyObject*);
extern PyObject* PyTuple_New(Py_ssize_t size);
extern int PyTuple_SetItem(PyObject*, Py_ssize_t, PyObject*);
extern PyObject* PyModule_Create2(PyModuleDef*, int apiver);
#define PyModule_Create(m) PyModule_Create2((m), PYTHON_ABI_VERSION)
#define PyMODINIT_FUNC __attribute__((visibility("default"))) PyObject*
#endif

/* ------------------------------------------------------------------------------------------ */
/* Shared Core data layout (must match main.go's cgo preamble / the FFI extension).            */
/* ------------------------------------------------------------------------------------------ */
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
    const char* str_val; /* sidecar-process pointer: never dereferenced here */
} CSpannerCell;

_Static_assert(sizeof(CSpannerCell) == 24, "CSpannerCell layout must match the Go Shared Core");

/* ------------------------------------------------------------------------------------------ */
/* Wire protocol (must match ipc/spanner_ipc_server.go).                                       */
/* ------------------------------------------------------------------------------------------ */
#define IPC_MAGIC 0x4F475053u /* "SPGO" */
#define IPC_VERSION 1
#define IPC_INLINE_BUF 16384
#define IPC_MAX_PAYLOAD (1ULL << 31)
#define IPC_CLIENT_MAGIC 0x53504943u

enum {
    OP_EXECUTE = 1,
    OP_INIT = 2,
    OP_CLOSE = 3,
    OP_STATS = 4,
    OP_RESET_STATS = 5,
    OP_PING = 6,
    OP_SHUTDOWN = 7,
    OP_PROF_START = 8,
    OP_PROF_STOP = 9,
    OP_INFO = 10
};

#pragma pack(push, 1)
typedef struct {
    uint32_t magic;
    uint16_t version;
    uint16_t op;
    uint64_t handle;
    uint32_t session_len;
    uint32_t sql_len;
    uint32_t param_len;
    uint32_t aux;
} IpcReqHeader;

typedef struct {
    uint32_t magic;
    uint16_t version;
    uint16_t op;
    int32_t status;
    int32_t row_count;
    int32_t col_count;
    int32_t attempt_count;
    uint64_t cells_bytes;
    uint64_t arena_bytes;
    uint32_t extra_bytes;
    uint32_t cell_size;
} IpcRespHeader;
#pragma pack(pop)

_Static_assert(sizeof(IpcReqHeader) == 32, "request header must be 32 bytes");
_Static_assert(sizeof(IpcRespHeader) == 48, "response header must be 48 bytes");

typedef struct {
    IpcRespHeader hdr;
    char* payload;       /* cells | arena | extra (inline buffer, connection buffer or heap) */
    char* heap;          /* non-NULL only for one-off heap buffers that the caller must free */
    uint64_t payload_len;
    uint64_t recv_calls; /* number of recv() hops needed to move this response */
} IpcResponse;

/* Large responses (heavy reads) are received into a per-connection buffer that is reused across
 * requests (a standard IPC client design: no per-response malloc/page-faulting). Buffers larger
 * than this are not retained. */
#define IPC_RETAIN_MAX (16ULL << 20)

/* ------------------------------------------------------------------------------------------ */
/* Client-side counters (the IPC analogue of the FFI extension's c_pylist_decode_ns counter).  */
/* ------------------------------------------------------------------------------------------ */
static uint64_t g_stat_requests = 0;
static uint64_t g_stat_bytes_sent = 0;
static uint64_t g_stat_bytes_recv = 0;
static uint64_t g_stat_send_calls = 0;
static uint64_t g_stat_recv_calls = 0;
static uint64_t g_stat_decode_ns = 0;
static uint64_t g_stat_connects = 0;
static uint64_t g_stat_heap_responses = 0;

#define STAT_ADD(v, n) __atomic_add_fetch(&(v), (uint64_t)(n), __ATOMIC_RELAXED)
#define STAT_LOAD(v) __atomic_load_n(&(v), __ATOMIC_RELAXED)
#define STAT_RESET(v) __atomic_store_n(&(v), 0, __ATOMIC_RELAXED)

static inline uint64_t thread_cputime_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

/* ------------------------------------------------------------------------------------------ */
/* Client handle with per-thread persistent connections.                                       */
/* ------------------------------------------------------------------------------------------ */
struct IpcClient;

typedef struct IpcConn {
    int fd;
    char* rbuf;   /* reusable receive buffer for large responses (owned by this thread's connection) */
    size_t rcap;
    struct IpcConn* prev;
    struct IpcConn* next;
    struct IpcClient* owner;
} IpcConn;

typedef struct IpcClient {
    uint32_t magic;
    int closed;
    char path[sizeof(((struct sockaddr_un*)0)->sun_path)];
    int sockbuf;
    uint64_t server_handle;   /* Go CoreClient handle inside the sidecar (InitGoCoreClient) */
    pthread_key_t key;        /* per-thread IpcConn* */
    pthread_mutex_t mu;       /* guards conns list */
    IpcConn* conns;
    int ctl_fd;               /* control connection for INIT/CLOSE/STATS (guarded by ctl_mu) */
    pthread_mutex_t ctl_mu;
} IpcClient;

static void conn_list_remove_locked(IpcClient* cl, IpcConn* c) {
    if (c->prev) c->prev->next = c->next; else if (cl->conns == c) cl->conns = c->next;
    if (c->next) c->next->prev = c->prev;
    c->prev = c->next = NULL;
}

/* Client handles are small integers indexing this registry (never raw pointers). IpcClient structs
 * are intentionally never freed: a worker thread that exits after close_client may still run its
 * pthread destructor, which must find valid memory. */
#define IPC_MAX_CLIENTS 1024
static IpcClient* g_clients[IPC_MAX_CLIENTS];
static int g_nclients = 0;
static pthread_mutex_t g_clients_mu = PTHREAD_MUTEX_INITIALIZER;

/* pthread-specific destructor: runs when a client thread exits; the owning thread closes its fd. */
static void thread_conn_destructor(void* p) {
    IpcConn* c = (IpcConn*)p;
    if (!c) return;
    IpcClient* cl = c->owner;
    pthread_mutex_lock(&cl->mu);
    conn_list_remove_locked(cl, c);
    pthread_mutex_unlock(&cl->mu);
    if (c->fd >= 0) close(c->fd);
    free(c->rbuf);
    free(c);
}

static int ipc_connect(const char* path, int sockbuf) {
    int fd = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (fd < 0) return -1;
    if (sockbuf > 0) {
        (void)setsockopt(fd, SOL_SOCKET, SO_SNDBUF, &sockbuf, sizeof(sockbuf));
        (void)setsockopt(fd, SOL_SOCKET, SO_RCVBUF, &sockbuf, sizeof(sockbuf));
    }
    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    size_t len = strlen(path);
    if (len >= sizeof(addr.sun_path)) {
        close(fd);
        errno = ENAMETOOLONG;
        return -1;
    }
    memcpy(addr.sun_path, path, len + 1);
    int interrupted = 0;
    for (;;) {
        if (connect(fd, (struct sockaddr*)&addr, sizeof(addr)) == 0) break;
        if (errno == EINTR) {
            interrupted = 1; /* the connect continues asynchronously; a retry reports its outcome */
            continue;
        }
        if (interrupted && errno == EISCONN) break;
        int e = errno;
        close(fd);
        errno = e;
        return -1;
    }
    STAT_ADD(g_stat_connects, 1);
    return fd;
}

static int send_all(int fd, const char* buf, size_t len) {
    size_t off = 0;
    while (off < len) {
        ssize_t n = send(fd, buf + off, len - off, MSG_NOSIGNAL);
        if (n < 0) {
            if (errno == EINTR) continue;
            return -1;
        }
        off += (size_t)n;
        STAT_ADD(g_stat_send_calls, 1);
    }
    STAT_ADD(g_stat_bytes_sent, len);
    return 0;
}

/* Reads one response. Small responses (point selects) are read with a single greedy recv()
 * into the caller's inline buffer; large responses (heavy reads) continue directly into the
 * connection's reusable buffer (or a one-off heap buffer when conn == NULL / huge) and need
 * several recv() hops across the boundary. */
static int recv_response(int fd, char* inline_buf, IpcConn* conn, IpcResponse* out) {
    size_t have = 0;
    out->heap = NULL;
    out->payload = NULL;
    out->payload_len = 0;
    out->recv_calls = 0;
    while (have < sizeof(IpcRespHeader)) {
        ssize_t n = recv(fd, inline_buf + have, IPC_INLINE_BUF - have, 0);
        if (n == 0) {
            errno = ECONNRESET;
            return -1;
        }
        if (n < 0) {
            if (errno == EINTR) continue;
            return -1;
        }
        have += (size_t)n;
        out->recv_calls++;
    }
    memcpy(&out->hdr, inline_buf, sizeof(IpcRespHeader));
    if (out->hdr.magic != IPC_MAGIC || out->hdr.version != IPC_VERSION) {
        errno = EPROTO;
        return -1;
    }
    /* Bound every length field before summing (no u64 overflow on corrupt headers). */
    if (out->hdr.cells_bytes > IPC_MAX_PAYLOAD || out->hdr.arena_bytes > IPC_MAX_PAYLOAD ||
        (uint64_t)out->hdr.extra_bytes > IPC_MAX_PAYLOAD) {
        errno = EMSGSIZE;
        return -1;
    }
    uint64_t total = out->hdr.cells_bytes + out->hdr.arena_bytes + (uint64_t)out->hdr.extra_bytes;
    if (total > IPC_MAX_PAYLOAD) {
        errno = EMSGSIZE;
        return -1;
    }
    size_t got = have - sizeof(IpcRespHeader);
    if ((uint64_t)got > total) {
        errno = EPROTO; /* one outstanding request per connection: never more than one response */
        return -1;
    }
    char* dst;
    if (total <= (uint64_t)(IPC_INLINE_BUF - sizeof(IpcRespHeader))) {
        dst = inline_buf + sizeof(IpcRespHeader);
    } else if (conn != NULL && total <= IPC_RETAIN_MAX) {
        if (conn->rcap < total) {
            size_t want = (size_t)((total + 65535) & ~(uint64_t)65535);
            char* nb = (char*)realloc(conn->rbuf, want);
            if (!nb) {
                errno = ENOMEM;
                return -1;
            }
            conn->rbuf = nb;
            conn->rcap = want;
        }
        memcpy(conn->rbuf, inline_buf + sizeof(IpcRespHeader), got);
        dst = conn->rbuf;
    } else {
        out->heap = (char*)malloc((size_t)total);
        if (!out->heap) {
            errno = ENOMEM;
            return -1;
        }
        memcpy(out->heap, inline_buf + sizeof(IpcRespHeader), got);
        dst = out->heap;
    }
    while ((uint64_t)got < total) {
        ssize_t n = recv(fd, dst + got, (size_t)(total - got), 0);
        if (n == 0) {
            errno = ECONNRESET;
            goto fail;
        }
        if (n < 0) {
            if (errno == EINTR) continue;
            goto fail;
        }
        got += (size_t)n;
        out->recv_calls++;
    }
    out->payload = dst;
    out->payload_len = total;
    return 0;
fail:
    {
        int e = errno;
        free(out->heap);
        out->heap = NULL;
        errno = e;
        return -1;
    }
}

/* One request/response exchange (no GIL handling; callers release the GIL around it). */
static int ipc_roundtrip(int fd, uint16_t op, uint64_t handle, uint32_t aux,
                         const char* s1, size_t l1, const char* s2, size_t l2,
                         const char* s3, size_t l3, char* req_stack, size_t req_stack_cap,
                         char* inline_buf, IpcConn* conn, IpcResponse* resp) {
    size_t req_len = sizeof(IpcReqHeader) + l1 + l2 + l3;
    char* req = req_len <= req_stack_cap ? req_stack : (char*)malloc(req_len);
    if (!req) {
        errno = ENOMEM;
        return -1;
    }
    IpcReqHeader rq;
    rq.magic = IPC_MAGIC;
    rq.version = IPC_VERSION;
    rq.op = op;
    rq.handle = handle;
    rq.session_len = (uint32_t)l1;
    rq.sql_len = (uint32_t)l2;
    rq.param_len = (uint32_t)l3;
    rq.aux = aux;
    memcpy(req, &rq, sizeof(rq));
    size_t off = sizeof(rq);
    if (l1) { memcpy(req + off, s1, l1); off += l1; }
    if (l2) { memcpy(req + off, s2, l2); off += l2; }
    if (l3) { memcpy(req + off, s3, l3); off += l3; }
    int rc = send_all(fd, req, req_len);
    int e = errno;
    if (req != req_stack) free(req);
    if (rc != 0) {
        errno = e;
        return -1;
    }
    return recv_response(fd, inline_buf, conn, resp);
}

static IpcClient* client_from_handle(unsigned long long handle) {
    IpcClient* cl = NULL;
    pthread_mutex_lock(&g_clients_mu);
    if (handle >= 1 && handle <= (unsigned long long)g_nclients) {
        cl = g_clients[handle - 1];
    }
    pthread_mutex_unlock(&g_clients_mu);
    if (!cl || cl->magic != IPC_CLIENT_MAGIC || __atomic_load_n(&cl->closed, __ATOMIC_ACQUIRE)) {
        PyErr_SetString(PyExc_RuntimeError, "invalid or closed Spanner Go IPC client handle");
        return NULL;
    }
    return cl;
}

static IpcConn* get_thread_conn(IpcClient* cl) {
    IpcConn* c = (IpcConn*)pthread_getspecific(cl->key);
    if (c) return c;
    int fd, err = 0;
    Py_BEGIN_ALLOW_THREADS
    fd = ipc_connect(cl->path, cl->sockbuf);
    if (fd < 0) err = errno;
    Py_END_ALLOW_THREADS
    if (fd < 0) {
        PyErr_Format(PyExc_RuntimeError, "Spanner Go IPC connect(%s) failed: %s", cl->path, strerror(err));
        return NULL;
    }
    c = (IpcConn*)calloc(1, sizeof(IpcConn));
    if (!c) {
        close(fd);
        PyErr_NoMemory();
        return NULL;
    }
    c->fd = fd;
    c->owner = cl;
    pthread_mutex_lock(&cl->mu);
    c->next = cl->conns;
    if (cl->conns) cl->conns->prev = c;
    cl->conns = c;
    pthread_mutex_unlock(&cl->mu);
    pthread_setspecific(cl->key, c);
    return c;
}

static void drop_thread_conn(IpcClient* cl, IpcConn* c) {
    pthread_setspecific(cl->key, NULL);
    pthread_mutex_lock(&cl->mu);
    conn_list_remove_locked(cl, c);
    pthread_mutex_unlock(&cl->mu);
    if (c->fd >= 0) close(c->fd);
    free(c->rbuf);
    free(c);
}

/* Identical per-cell CPython object construction to the FFI extension's batch_to_pylist(),
 * except that string pointers are recomputed as offsets into the received string arena. */
static PyObject* response_to_pylist(const IpcResponse* resp) {
    uint64_t t0 = thread_cputime_ns();
    const IpcRespHeader* h = &resp->hdr;
    int row_count = h->row_count;
    int col_count = h->col_count;
    if (row_count < 0 || col_count < 0) {
        PyErr_SetString(PyExc_RuntimeError, "Spanner Go IPC: negative row/column count");
        return NULL;
    }
    uint64_t n_cells = (uint64_t)row_count * (uint64_t)col_count; /* < 2^62: no overflow */
    if (n_cells > 0 &&
        (h->cell_size != sizeof(CSpannerCell) || n_cells > IPC_MAX_PAYLOAD / sizeof(CSpannerCell) ||
         h->cells_bytes != n_cells * sizeof(CSpannerCell) || h->cells_bytes + h->arena_bytes > resp->payload_len)) {
        PyErr_SetString(PyExc_RuntimeError, "Spanner Go IPC: CSpannerCell layout mismatch");
        return NULL;
    }
    const CSpannerCell* cells = (const CSpannerCell*)resp->payload;
    const char* arena = resp->payload + h->cells_bytes;
    uint64_t arena_len = h->arena_bytes;
    uint64_t arena_off = 0;

    PyObject* rows_list = PyList_New(row_count);
    if (!rows_list) {
        return NULL;
    }
    for (int r = 0; r < row_count; r++) {
        PyObject* row_obj = PyList_New(col_count);
        if (!row_obj) {
            Py_DECREF(rows_list);
            return NULL;
        }
        int base_idx = r * col_count;
        for (int c = 0; c < col_count; c++) {
            const CSpannerCell* cell = &cells[base_idx + c];
            PyObject* val_obj = NULL;
            switch (cell->kind) {
                case CELL_KIND_STRING:
                    if (cell->str_len > 0) {
                        if (arena_off + cell->str_len > arena_len) {
                            Py_DECREF(row_obj);
                            Py_DECREF(rows_list);
                            PyErr_SetString(PyExc_RuntimeError, "Spanner Go IPC: string arena overflow");
                            return NULL;
                        }
                        val_obj = PyUnicode_FromStringAndSize(arena + arena_off, (Py_ssize_t)cell->str_len);
                        arena_off += cell->str_len;
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
    uint64_t t1 = thread_cputime_ns();
    if (t1 >= t0) {
        STAT_ADD(g_stat_decode_ns, t1 - t0);
    }
    return rows_list;
}

static PyObject* raise_status_error(const IpcResponse* resp) {
    const char* msg_ptr = resp->payload ? resp->payload + resp->hdr.cells_bytes + resp->hdr.arena_bytes : "";
    size_t msg_len = resp->payload ? resp->hdr.extra_bytes : 0;
    char* msg = (char*)malloc(msg_len + 1);
    if (!msg) return PyErr_NoMemory();
    if (msg_len) memcpy(msg, msg_ptr, msg_len);
    msg[msg_len] = '\0';
    if (resp->hdr.status > 0) {
        /* Same message format as the FFI extension for Go Shared Core RPC errors. */
        PyErr_Format(PyExc_RuntimeError, "Spanner Go Shared Core RPC error (%d): %s", (int)resp->hdr.status, msg);
    } else {
        PyErr_Format(PyExc_RuntimeError, "Spanner Go IPC server error (%d): %s", (int)resp->hdr.status, msg);
    }
    free(msg);
    return NULL;
}

/* ------------------------------------------------------------------------------------------ */
/* Hot path                                                                                     */
/* ------------------------------------------------------------------------------------------ */
static PyObject* py_execute_streaming_sql(PyObject* self, PyObject* args) {
    unsigned long long handle = 0;
    const char* session = NULL;
    const char* sql = NULL;
    const char* param_id = "";
    if (!PyArg_ParseTuple(args, "Kss|s", &handle, &session, &sql, &param_id)) {
        return NULL;
    }
    IpcClient* cl = client_from_handle(handle);
    if (!cl) return NULL;
    IpcConn* conn = get_thread_conn(cl);
    if (!conn) return NULL;

    size_t sl = strlen(session), ql = strlen(sql), pl = strlen(param_id);
    char req_stack[2048];
    uint64_t inline_storage[IPC_INLINE_BUF / sizeof(uint64_t)]; /* 8-byte aligned cells */
    IpcResponse resp;
    int rc, err = 0;

    Py_BEGIN_ALLOW_THREADS
    rc = ipc_roundtrip(conn->fd, OP_EXECUTE, cl->server_handle, 0, session, sl, sql, ql, param_id, pl,
                       req_stack, sizeof(req_stack), (char*)inline_storage, conn, &resp);
    if (rc != 0) err = errno;
    Py_END_ALLOW_THREADS

    if (rc != 0) {
        drop_thread_conn(cl, conn);
        PyErr_Format(PyExc_RuntimeError, "Spanner Go IPC request failed: %s", strerror(err));
        return NULL;
    }
    STAT_ADD(g_stat_requests, 1);
    STAT_ADD(g_stat_bytes_recv, sizeof(IpcRespHeader) + resp.payload_len);
    STAT_ADD(g_stat_recv_calls, resp.recv_calls);
    if (resp.heap) STAT_ADD(g_stat_heap_responses, 1);

    PyObject* result;
    if (resp.hdr.status != 0) {
        result = raise_status_error(&resp);
    } else {
        result = response_to_pylist(&resp);
    }
    free(resp.heap);
    return result;
}

/* ------------------------------------------------------------------------------------------ */
/* Control plane                                                                                */
/* ------------------------------------------------------------------------------------------ */
static int ctl_call(IpcClient* cl, uint16_t op, uint64_t handle, uint32_t aux, const char* body,
                    char* inline_buf, IpcResponse* resp, int* err_out) {
    char req_stack[1024];
    size_t bl = body ? strlen(body) : 0;
    int rc;
    pthread_mutex_lock(&cl->ctl_mu);
    rc = ipc_roundtrip(cl->ctl_fd, op, handle, aux, body, bl, NULL, 0, NULL, 0, req_stack,
                       sizeof(req_stack), inline_buf, NULL, resp);
    if (rc != 0) *err_out = errno;
    pthread_mutex_unlock(&cl->ctl_mu);
    return rc;
}

static PyObject* py_open_client(PyObject* self, PyObject* args) {
    const char* path = NULL;
    int channel_count = 4;
    int sockbuf = 0;
    if (!PyArg_ParseTuple(args, "s|ii", &path, &channel_count, &sockbuf)) {
        return NULL;
    }
    if (strlen(path) >= sizeof(((struct sockaddr_un*)0)->sun_path)) {
        PyErr_SetString(PyExc_RuntimeError, "Spanner Go IPC socket path too long");
        return NULL;
    }
    IpcClient* cl = (IpcClient*)calloc(1, sizeof(IpcClient));
    if (!cl) return PyErr_NoMemory();
    cl->magic = IPC_CLIENT_MAGIC;
    strcpy(cl->path, path);
    cl->sockbuf = sockbuf;
    cl->ctl_fd = -1;
    pthread_mutex_init(&cl->mu, NULL);
    pthread_mutex_init(&cl->ctl_mu, NULL);
    if (pthread_key_create(&cl->key, thread_conn_destructor) != 0) {
        free(cl);
        PyErr_SetString(PyExc_RuntimeError, "pthread_key_create failed");
        return NULL;
    }

    uint64_t inline_storage[IPC_INLINE_BUF / sizeof(uint64_t)];
    IpcResponse resp;
    int fd, rc = -1, err = 0;
    Py_BEGIN_ALLOW_THREADS
    fd = ipc_connect(cl->path, sockbuf);
    if (fd < 0) {
        err = errno;
    } else {
        cl->ctl_fd = fd;
        rc = ctl_call(cl, OP_INIT, 0, (uint32_t)channel_count, NULL, (char*)inline_storage, &resp, &err);
    }
    Py_END_ALLOW_THREADS

    if (fd < 0 || rc != 0) {
        if (fd >= 0) close(fd);
        pthread_key_delete(cl->key);
        free(cl);
        PyErr_Format(PyExc_RuntimeError, "Spanner Go IPC open_client(%s) failed: %s", path, strerror(err));
        return NULL;
    }
    if (resp.hdr.status != 0 || resp.payload_len < 8) {
        PyObject* r = resp.hdr.status != 0 ? raise_status_error(&resp) : NULL;
        if (!r && resp.hdr.status == 0) {
            PyErr_SetString(PyExc_RuntimeError, "Spanner Go IPC INIT returned a malformed response");
        }
        free(resp.heap);
        close(fd);
        pthread_key_delete(cl->key);
        free(cl);
        return NULL;
    }
    memcpy(&cl->server_handle, resp.payload, 8);
    free(resp.heap);

    pthread_mutex_lock(&g_clients_mu);
    if (g_nclients >= IPC_MAX_CLIENTS) {
        pthread_mutex_unlock(&g_clients_mu);
        close(fd);
        PyErr_SetString(PyExc_RuntimeError, "too many Spanner Go IPC clients opened in this process");
        return NULL;
    }
    g_clients[g_nclients++] = cl;
    unsigned long long handle = (unsigned long long)g_nclients; /* 1-based registry index */
    pthread_mutex_unlock(&g_clients_mu);
    return PyLong_FromUnsignedLongLong(handle);
}

static PyObject* py_close_client(PyObject* self, PyObject* args) {
    unsigned long long handle = 0;
    if (!PyArg_ParseTuple(args, "K", &handle)) return NULL;
    IpcClient* cl = client_from_handle(handle);
    if (!cl) return NULL;
    uint64_t inline_storage[IPC_INLINE_BUF / sizeof(uint64_t)];
    IpcResponse resp;
    int rc, err = 0;
    Py_BEGIN_ALLOW_THREADS
    rc = ctl_call(cl, OP_CLOSE, cl->server_handle, 0, NULL, (char*)inline_storage, &resp, &err);
    Py_END_ALLOW_THREADS
    if (rc == 0) free(resp.heap);

    /* Mark closed first (new calls fail fast), then shut down - but do not close - every per-thread
     * connection: the owning thread closes its own fd (next use or pthread destructor at thread exit),
     * so an fd number can never be recycled under a thread that is mid-request. The pthread key is not
     * deleted so those destructors still run, and the IpcClient memory is never freed. */
    __atomic_store_n(&cl->closed, 1, __ATOMIC_RELEASE);
    pthread_mutex_lock(&cl->mu);
    for (IpcConn* c = cl->conns; c; c = c->next) {
        if (c->fd >= 0) {
            shutdown(c->fd, SHUT_RDWR);
        }
    }
    pthread_mutex_unlock(&cl->mu);
    pthread_mutex_lock(&cl->ctl_mu);
    if (cl->ctl_fd >= 0) {
        close(cl->ctl_fd);
        cl->ctl_fd = -1;
    }
    pthread_mutex_unlock(&cl->ctl_mu);
    if (rc != 0) {
        PyErr_Format(PyExc_RuntimeError, "Spanner Go IPC close_client failed: %s", strerror(err));
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject* simple_ctl(PyObject* args, uint16_t op, int want_payload) {
    unsigned long long handle = 0;
    const char* body = NULL;
    if (!PyArg_ParseTuple(args, "K|s", &handle, &body)) return NULL;
    IpcClient* cl = client_from_handle(handle);
    if (!cl) return NULL;
    uint64_t inline_storage[IPC_INLINE_BUF / sizeof(uint64_t)];
    IpcResponse resp;
    int rc, err = 0;
    Py_BEGIN_ALLOW_THREADS
    rc = ctl_call(cl, op, cl->server_handle, 0, body, (char*)inline_storage, &resp, &err);
    Py_END_ALLOW_THREADS
    if (rc != 0) {
        PyErr_Format(PyExc_RuntimeError, "Spanner Go IPC control op %d failed: %s", (int)op, strerror(err));
        return NULL;
    }
    PyObject* result = NULL;
    if (op == OP_PROF_START) {
        result = PyLong_FromLong((long)resp.hdr.status);
    } else if (resp.hdr.status != 0) {
        result = raise_status_error(&resp);
    } else if (want_payload == 1) { /* tuple of u64 */
        size_t n = (size_t)(resp.payload_len / 8);
        result = PyTuple_New((Py_ssize_t)n);
        for (size_t i = 0; result && i < n; i++) {
            uint64_t v;
            memcpy(&v, resp.payload + 8 * i, 8);
            PyTuple_SetItem(result, (Py_ssize_t)i, PyLong_FromUnsignedLongLong((unsigned long long)v));
        }
    } else if (want_payload == 2) { /* utf-8 string */
        result = PyUnicode_FromStringAndSize(resp.payload ? resp.payload : "", (Py_ssize_t)resp.payload_len);
    } else {
        Py_INCREF(Py_None);
        result = Py_None;
    }
    free(resp.heap);
    return result;
}

static PyObject* py_server_stats(PyObject* self, PyObject* args) { return simple_ctl(args, OP_STATS, 1); }
static PyObject* py_reset_server_stats(PyObject* self, PyObject* args) { return simple_ctl(args, OP_RESET_STATS, 0); }
static PyObject* py_server_info(PyObject* self, PyObject* args) { return simple_ctl(args, OP_INFO, 2); }
static PyObject* py_server_prof_start(PyObject* self, PyObject* args) { return simple_ctl(args, OP_PROF_START, 0); }
static PyObject* py_server_prof_stop(PyObject* self, PyObject* args) { return simple_ctl(args, OP_PROF_STOP, 0); }

/* One-shot ops on a temporary connection (no client handle needed). */
static PyObject* oneshot(PyObject* args, uint16_t op) {
    const char* path = NULL;
    if (!PyArg_ParseTuple(args, "s", &path)) return NULL;
    char req_stack[256];
    uint64_t inline_storage[IPC_INLINE_BUF / sizeof(uint64_t)];
    IpcResponse resp;
    int ok = 0;
    Py_BEGIN_ALLOW_THREADS
    int fd = ipc_connect(path, 0);
    if (fd >= 0) {
        if (ipc_roundtrip(fd, op, 0, 0, NULL, 0, NULL, 0, NULL, 0, req_stack, sizeof(req_stack),
                          (char*)inline_storage, NULL, &resp) == 0) {
            ok = resp.hdr.status == 0;
            free(resp.heap);
        }
        close(fd);
    }
    Py_END_ALLOW_THREADS
    return PyBool_FromLong(ok);
}

static PyObject* py_ping(PyObject* self, PyObject* args) { return oneshot(args, OP_PING); }
static PyObject* py_shutdown_server(PyObject* self, PyObject* args) { return oneshot(args, OP_SHUTDOWN); }

static PyObject* py_client_stats(PyObject* self, PyObject* Py_UNUSED(ignored)) {
    uint64_t vals[8] = {
        STAT_LOAD(g_stat_requests),   STAT_LOAD(g_stat_bytes_sent), STAT_LOAD(g_stat_bytes_recv),
        STAT_LOAD(g_stat_send_calls), STAT_LOAD(g_stat_recv_calls), STAT_LOAD(g_stat_decode_ns),
        STAT_LOAD(g_stat_connects),   STAT_LOAD(g_stat_heap_responses),
    };
    PyObject* tup = PyTuple_New(8);
    if (!tup) return NULL;
    for (int i = 0; i < 8; i++) {
        PyTuple_SetItem(tup, i, PyLong_FromUnsignedLongLong((unsigned long long)vals[i]));
    }
    return tup;
}

static PyObject* py_reset_client_stats(PyObject* self, PyObject* Py_UNUSED(ignored)) {
    STAT_RESET(g_stat_requests);
    STAT_RESET(g_stat_bytes_sent);
    STAT_RESET(g_stat_bytes_recv);
    STAT_RESET(g_stat_send_calls);
    STAT_RESET(g_stat_recv_calls);
    STAT_RESET(g_stat_decode_ns);
    STAT_RESET(g_stat_connects);
    STAT_RESET(g_stat_heap_responses);
    Py_RETURN_NONE;
}

static PyMethodDef SpannerIpcExtMethods[] = {
    {"open_client", py_open_client, METH_VARARGS,
     "open_client(socket_path, channel_count=4, sockbuf=0) -> handle. Creates a Go CoreClient inside the sidecar (InitGoCoreClient)."},
    {"close_client", py_close_client, METH_VARARGS, "close_client(handle). CloseGoCoreClient inside the sidecar and close connections."},
    {"execute_streaming_sql", py_execute_streaming_sql, METH_VARARGS,
     "execute_streaming_sql(handle, session, sql, param_id='') -> list of rows (GIL released for the whole IPC round trip)."},
    {"server_stats", py_server_stats, METH_VARARGS,
     "server_stats(handle) -> (utime_us, stime_us, 7 Go core counters, goroutines, maxrss_kb, nvcsw, nivcsw, gomaxprocs, num_cpu, pid)."},
    {"reset_server_stats", py_reset_server_stats, METH_VARARGS, "reset_server_stats(handle). ResetGoCoreStats inside the sidecar."},
    {"server_info", py_server_info, METH_VARARGS, "server_info(handle) -> JSON string (Go version, deps, GOMAXPROCS)."},
    {"server_prof_start", py_server_prof_start, METH_VARARGS, "server_prof_start(handle, path) -> rc. StartGoCPUProfile inside the sidecar."},
    {"server_prof_stop", py_server_prof_stop, METH_VARARGS, "server_prof_stop(handle). StopGoCPUProfile inside the sidecar."},
    {"ping", py_ping, METH_VARARGS, "ping(socket_path) -> bool."},
    {"shutdown_server", py_shutdown_server, METH_VARARGS, "shutdown_server(socket_path) -> bool."},
    {"client_stats", py_client_stats, METH_NOARGS,
     "client_stats() -> (requests, bytes_sent, bytes_recv, send_calls, recv_calls, decode_ns, connects, heap_responses)."},
    {"reset_client_stats", py_reset_client_stats, METH_NOARGS, "reset_client_stats()."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef spanner_ipc_ext_module = {
    PyModuleDef_HEAD_INIT,
    "spanner_ipc_ext",
    "CPython Stable ABI client for the Spanner Go Shared Core IPC sidecar (Unix domain socket)",
    -1,
    SpannerIpcExtMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_spanner_ipc_ext(void) {
    return PyModule_Create(&spanner_ipc_ext_module);
}
