package main

/*
#include <stdlib.h>
#include <stdint.h>

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
    int format; // 0 = JSON string, 1 = Direct Native Cells
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

typedef void (*StreamDataCallback)(void* user_data, CSpannerBatch* batch);

static void bridge_callback(
    StreamDataCallback cb,
    void* user_data,
    CSpannerBatch* batch
) {
    if (cb != NULL) {
        cb(user_data, batch);
    }
}
*/
import "C"

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"runtime/pprof"
	"strings"
	"sync"
	"sync/atomic"
	"syscall"
	"unsafe"

	spannerpb "cloud.google.com/go/spanner/apiv1/spannerpb"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/structpb"
)

type completedAsyncItem struct {
	reqID uint64
	batch *C.CSpannerBatch
}

var (
	clientRegistryMutex sync.RWMutex
	clientRegistry      = make(map[uintptr]*CoreClient)
	nextClientId        uintptr = 1
	logEncodingOnce     sync.Once

	profMu   sync.Mutex
	profFile *os.File

	asyncOnce      sync.Once
	asyncReadFD    int = -1
	asyncWriteFD   int = -1
	asyncMu        sync.Mutex
	asyncCompleted []completedAsyncItem

	statCallCount       uint64
	statChunkCount      uint64
	statReqBuildNs      uint64
	statStreamInitNs    uint64
	statRecvProtoNs     uint64
	statChunkAssembleNs uint64
	statArenaEncodeNs   uint64
)

func goThreadCPUTimeNs() uint64 {
	var ts syscall.Timespec
	_, _, _ = syscall.Syscall(syscall.SYS_CLOCK_GETTIME, 3 /* CLOCK_THREAD_CPUTIME_ID */, uintptr(unsafe.Pointer(&ts)), 0)
	return uint64(ts.Sec)*1000000000 + uint64(ts.Nsec)
}

func registerClient(client *CoreClient) uintptr {
	clientRegistryMutex.Lock()
	defer clientRegistryMutex.Unlock()
	id := nextClientId
	nextClientId++
	clientRegistry[id] = client
	return id
}

func getClient(id uintptr) *CoreClient {
	clientRegistryMutex.RLock()
	defer clientRegistryMutex.RUnlock()
	return clientRegistry[id]
}

func unregisterClient(id uintptr) *CoreClient {
	clientRegistryMutex.Lock()
	defer clientRegistryMutex.Unlock()
	client := clientRegistry[id]
	delete(clientRegistry, id)
	return client
}

//export InitGoCoreClient
func InitGoCoreClient(channelCount C.int) C.uintptr_t {
	client, err := NewCoreClient(int(channelCount))
	if err != nil {
		return 0
	}
	id := registerClient(client)
	return C.uintptr_t(id)
}

//export CloseGoCoreClient
func CloseGoCoreClient(handle C.uintptr_t) {
	client := unregisterClient(uintptr(handle))
	if client != nil {
		client.Close()
	}
}

//export StartGoCPUProfile
func StartGoCPUProfile(path *C.char) C.int {
	profMu.Lock()
	defer profMu.Unlock()
	if profFile != nil {
		pprof.StopCPUProfile()
		_ = profFile.Close()
		profFile = nil
	}
	p := C.GoString(path)
	f, err := os.Create(p)
	if err != nil {
		return -1
	}
	if err := pprof.StartCPUProfile(f); err != nil {
		_ = f.Close()
		return -2
	}
	profFile = f
	return 0
}

//export StopGoCPUProfile
func StopGoCPUProfile() {
	profMu.Lock()
	defer profMu.Unlock()
	if profFile != nil {
		pprof.StopCPUProfile()
		_ = profFile.Close()
		profFile = nil
	}
}

func isDirectDeserializationEnabled() bool {
	val := os.Getenv("SPANNER_GO_DIRECT_DESERIALIZATION")
	enabled := val != "false" && val != "0"
	logEncodingOnce.Do(func() {
		if enabled {
			fmt.Println("[Spanner-Go] Direct native cells encoding is ACTIVE (zero-copy C arena)")
		} else {
			fmt.Println("[Spanner-Go] Legacy JSON parsing is ACTIVE")
		}
	})
	return enabled
}

func writeBatchJson(batch [][]*structpb.Value, rowType []*spannerpb.StructType_Field) *C.char {
	if len(batch) == 0 {
		return nil
	}
	var buf bytes.Buffer
	buf.WriteByte('[')
	for i, row := range batch {
		if i > 0 {
			buf.WriteByte(',')
		}
		buf.WriteByte('[')
		for j, cell := range row {
			if j > 0 {
				buf.WriteByte(',')
			}
			var fieldType *spannerpb.Type
			if j < len(rowType) {
				fieldType = rowType[j].Type
			}
			writeValueJson(&buf, cell, fieldType)
		}
		buf.WriteByte(']')
	}
	buf.WriteByte(']')
	return C.CString(buf.String())
}

func buildCBatch(
	batch [][]*structpb.Value,
	rowType []*spannerpb.StructType_Field,
	serverTiming string,
	attemptCount int,
	errMsg string,
	errCode int,
	isLast bool,
) *C.CSpannerBatch {
	cBatch := (*C.CSpannerBatch)(C.calloc(1, C.size_t(unsafe.Sizeof(C.CSpannerBatch{}))))

	if isLast {
		cBatch.is_last = 1
	}
	cBatch.attempt_count = C.int(attemptCount)
	cBatch.error_code = C.int(errCode)

	if errMsg != "" {
		cBatch.error_msg = C.CString(errMsg)
	}
	if serverTiming != "" {
		cBatch.server_timing = C.CString(serverTiming)
	}

	rowCount := len(batch)
	cBatch.row_count = C.int(rowCount)

	if rowCount > 0 {
		colCount := len(batch[0])
		cBatch.col_count = C.int(colCount)

		if isDirectDeserializationEnabled() {
			cBatch.format = 1 // Native cells

			totalCells := rowCount * colCount
			totalStringBytes := 0

			for _, row := range batch {
				for _, cell := range row {
					if cell != nil {
						if strVal, ok := cell.Kind.(*structpb.Value_StringValue); ok {
							totalStringBytes += len(strVal.StringValue)
						}
					}
				}
			}

			if totalCells > 0 {
				cBatch.cells = (*C.CSpannerCell)(C.malloc(C.size_t(totalCells) * C.size_t(unsafe.Sizeof(C.CSpannerCell{}))))
				cellsSlice := (*[1 << 28]C.CSpannerCell)(unsafe.Pointer(cBatch.cells))[:totalCells:totalCells]

				var arenaBytes []byte
				if totalStringBytes > 0 {
					cBatch.string_arena = (*C.char)(C.malloc(C.size_t(totalStringBytes)))
					arenaBytes = (*[1 << 28]byte)(unsafe.Pointer(cBatch.string_arena))[:totalStringBytes:totalStringBytes]
				}
				arenaOffset := 0

				for r, row := range batch {
					for c, val := range row {
						idx := r*colCount + c
						cell := &cellsSlice[idx]
						if val == nil {
							cell.kind = C.CELL_KIND_NULL
							continue
						}

						switch k := val.Kind.(type) {
						case *structpb.Value_NullValue:
							cell.kind = C.CELL_KIND_NULL
						case *structpb.Value_BoolValue:
							cell.kind = C.CELL_KIND_BOOL
							if k.BoolValue {
								cell.bool_val = 1
							} else {
								cell.bool_val = 0
							}
						case *structpb.Value_NumberValue:
							cell.kind = C.CELL_KIND_NUMBER
							cell.number_val = C.double(k.NumberValue)
						case *structpb.Value_StringValue:
							cell.kind = C.CELL_KIND_STRING
							strLen := len(k.StringValue)
							cell.str_len = C.uint32_t(strLen)
							if strLen > 0 {
								copy(arenaBytes[arenaOffset:arenaOffset+strLen], k.StringValue)
								cell.str_val = (*C.char)(unsafe.Pointer(&arenaBytes[arenaOffset]))
								arenaOffset += strLen
							} else {
								cell.str_val = nil
							}
						default:
							cell.kind = C.CELL_KIND_NULL
						}
					}
				}
			}
		} else {
			cBatch.format = 0
			cBatch.json_rows = writeBatchJson(batch, rowType)
		}
	}

	return cBatch
}

//export FreeSpannerBatch
func FreeSpannerBatch(batch *C.CSpannerBatch) {
	if batch == nil {
		return
	}
	if batch.json_rows != nil {
		C.free(unsafe.Pointer(batch.json_rows))
	}
	if batch.cells != nil {
		C.free(unsafe.Pointer(batch.cells))
	}
	if batch.string_arena != nil {
		C.free(unsafe.Pointer(batch.string_arena))
	}
	if batch.server_timing != nil {
		C.free(unsafe.Pointer(batch.server_timing))
	}
	if batch.error_msg != nil {
		C.free(unsafe.Pointer(batch.error_msg))
	}
	C.free(unsafe.Pointer(batch))
}

//export ExecuteStreamingSqlSync
func ExecuteStreamingSqlSync(
	handle C.uintptr_t,
	sessionPtr *C.char,
	sqlPtr *C.char,
	paramIdPtr *C.char,
) *C.CSpannerBatch {
	sessionStr := C.GoString(sessionPtr)
	sqlStr := C.GoString(sqlPtr)
	paramIdStr := ""
	if paramIdPtr != nil {
		paramIdStr = C.GoString(paramIdPtr)
	}
	return executeStreamingSqlInternal(uintptr(handle), sessionStr, sqlStr, paramIdStr)
}

func executeStreamingSqlInternal(
	handle uintptr,
	sessionStr string,
	sqlStr string,
	paramIdStr string,
) *C.CSpannerBatch {
	t0 := goThreadCPUTimeNs()
	client := getClient(handle)
	if client == nil {
		return buildCBatch(nil, nil, "", 1, "Invalid or closed CoreClient handle", int(codes.InvalidArgument), true)
	}

	dbPrefix := sessionStr
	if idx := strings.Index(sessionStr, "/sessions/"); idx != -1 {
		dbPrefix = sessionStr[:idx]
	}

	var lastResumeToken []byte
	attemptCount := 0

	var rowType []*spannerpb.StructType_Field
	var pendingValue *structpb.Value
	var currentRow []*structpb.Value
	batch := make([][]*structpb.Value, 0, 16)

	for {
		attemptCount++
		tReq0 := t0
		if attemptCount > 1 {
			tReq0 = goThreadCPUTimeNs()
		}

		req := spannerpb.ExecuteSqlRequest{
			Session: sessionStr,
			Sql:     sqlStr,
		}
		if paramIdStr != "" {
			req.Params = &structpb.Struct{
				Fields: map[string]*structpb.Value{
					"id": structpb.NewStringValue(paramIdStr),
				},
			}
			req.ParamTypes = map[string]*spannerpb.Type{
				"id": {Code: spannerpb.TypeCode_STRING},
			}
		}
		if len(lastResumeToken) > 0 {
			req.ResumeToken = lastResumeToken
		}

		token, err := client.GetToken()
		if err != nil {
			return buildCBatch(nil, nil, "", attemptCount, fmt.Sprintf("Failed to get GCP auth token: %v", err), int(codes.Unauthenticated), true)
		}

		md := metadata.Pairs(
			"google-cloud-resource-prefix", dbPrefix,
			"x-goog-request-params", "session="+sessionStr,
		)
		if token != nil && token.AccessToken != "" {
			md.Set("authorization", "Bearer "+token.AccessToken)
		}

		ctx := metadata.NewOutgoingContext(client.ctx, md)
		tReq1 := goThreadCPUTimeNs()
		if tReq1 >= tReq0 {
			atomic.AddUint64(&statReqBuildNs, tReq1-tReq0)
		}

		stream, err := client.ExecuteStreamingSql(ctx, &req)
		tInit1 := goThreadCPUTimeNs()
		if tInit1 >= tReq1 {
			atomic.AddUint64(&statStreamInitNs, tInit1-tReq1)
		}
		if err != nil {
			st, _ := status.FromError(err)
			if (st.Code() == codes.Unavailable || st.Code() == codes.Internal) && len(lastResumeToken) > 0 {
				continue
			}
			return buildCBatch(nil, nil, "", attemptCount, st.Message(), int(st.Code()), true)
		}

		serverTiming := ""
		if headerMD, err := stream.Header(); err == nil {
			if vals := headerMD.Get("server-timing"); len(vals) > 0 {
				serverTiming = vals[0]
			}
		}

		shouldRetry := false

		for {
			tRecv0 := goThreadCPUTimeNs()
			chunk, err := stream.Recv()
			tRecv1 := goThreadCPUTimeNs()
			if tRecv1 >= tRecv0 && (tRecv1-tRecv0) < 500000000 {
				atomic.AddUint64(&statRecvProtoNs, tRecv1-tRecv0)
			}
			if err == io.EOF {
				break
			}
			if err != nil {
				st, _ := status.FromError(err)
				if (st.Code() == codes.Unavailable || st.Code() == codes.Internal) && len(lastResumeToken) > 0 {
					shouldRetry = true
					break
				}
				return buildCBatch(nil, nil, serverTiming, attemptCount, st.Message(), int(st.Code()), true)
			}

			atomic.AddUint64(&statChunkCount, 1)

			if len(chunk.ResumeToken) > 0 {
				lastResumeToken = chunk.ResumeToken
			}

			if rowType == nil && chunk.Metadata != nil && chunk.Metadata.RowType != nil {
				rowType = chunk.Metadata.RowType.Fields
			}

			numFields := len(rowType)
			vals := chunk.Values

			if pendingValue != nil {
				if len(vals) > 0 {
					first := vals[0]
					vals = vals[1:]
					merged := mergeProtoValues(pendingValue, first)
					pendingValue = nil

					currentRow = append(currentRow, merged)
					if numFields > 0 && len(currentRow) == numFields {
						batch = append(batch, currentRow)
						currentRow = make([]*structpb.Value, 0, numFields)
					}
				}
			}

			if chunk.ChunkedValue && len(vals) > 0 {
				pendingValue = vals[len(vals)-1]
				vals = vals[:len(vals)-1]
			}

			for _, val := range vals {
				currentRow = append(currentRow, val)
				if numFields > 0 && len(currentRow) == numFields {
					batch = append(batch, currentRow)
					currentRow = make([]*structpb.Value, 0, numFields)
				}
			}
			tAsm1 := goThreadCPUTimeNs()
			if tAsm1 >= tRecv1 {
				atomic.AddUint64(&statChunkAssembleNs, tAsm1-tRecv1)
			}
		}

		if shouldRetry {
			continue
		}

		tEnc0 := goThreadCPUTimeNs()
		if trailerMD := stream.Trailer(); trailerMD != nil {
			if vals := trailerMD.Get("server-timing"); len(vals) > 0 {
				serverTiming = vals[0]
			}
		}

		if pendingValue != nil {
			currentRow = append(currentRow, pendingValue)
			pendingValue = nil
		}
		if len(currentRow) > 0 {
			batch = append(batch, currentRow)
			currentRow = nil
		}

		resBatch := buildCBatch(batch, rowType, serverTiming, attemptCount, "", 0, true)
		tEnc1 := goThreadCPUTimeNs()
		if tEnc1 >= tEnc0 {
			atomic.AddUint64(&statArenaEncodeNs, tEnc1-tEnc0)
		}
		atomic.AddUint64(&statCallCount, 1)
		return resBatch
	}
}

//export ResetGoCoreStats
func ResetGoCoreStats() {
	atomic.StoreUint64(&statCallCount, 0)
	atomic.StoreUint64(&statChunkCount, 0)
	atomic.StoreUint64(&statReqBuildNs, 0)
	atomic.StoreUint64(&statStreamInitNs, 0)
	atomic.StoreUint64(&statRecvProtoNs, 0)
	atomic.StoreUint64(&statChunkAssembleNs, 0)
	atomic.StoreUint64(&statArenaEncodeNs, 0)
}

//export GetGoCoreStats
func GetGoCoreStats(outStats *C.uint64_t) {
	if outStats == nil {
		return
	}
	slice := unsafe.Slice((*uint64)(unsafe.Pointer(outStats)), 7)
	slice[0] = atomic.LoadUint64(&statCallCount)
	slice[1] = atomic.LoadUint64(&statChunkCount)
	slice[2] = atomic.LoadUint64(&statReqBuildNs)
	slice[3] = atomic.LoadUint64(&statStreamInitNs)
	slice[4] = atomic.LoadUint64(&statRecvProtoNs)
	slice[5] = atomic.LoadUint64(&statChunkAssembleNs)
	slice[6] = atomic.LoadUint64(&statArenaEncodeNs)
}

//export GetAsyncNotifyFD
func GetAsyncNotifyFD() C.int {
	asyncOnce.Do(func() {
		var p [2]int
		if err := syscall.Pipe2(p[:], syscall.O_NONBLOCK|syscall.O_CLOEXEC); err == nil {
			asyncReadFD = p[0]
			asyncWriteFD = p[1]
		}
	})
	return C.int(asyncReadFD)
}

//export SubmitStreamingSqlAsync
func SubmitStreamingSqlAsync(
	handle C.uintptr_t,
	reqID C.uint64_t,
	sessionPtr *C.char,
	sqlPtr *C.char,
	paramIdPtr *C.char,
) {
	sessionStr := C.GoString(sessionPtr)
	sqlStr := C.GoString(sqlPtr)
	paramIdStr := ""
	if paramIdPtr != nil {
		paramIdStr = C.GoString(paramIdPtr)
	}
	h := uintptr(handle)
	id := uint64(reqID)

	go func() {
		b := executeStreamingSqlInternal(h, sessionStr, sqlStr, paramIdStr)
		asyncMu.Lock()
		wasEmpty := len(asyncCompleted) == 0
		asyncCompleted = append(asyncCompleted, completedAsyncItem{reqID: id, batch: b})
		asyncMu.Unlock()
		if wasEmpty && asyncWriteFD >= 0 {
			var one [1]byte = [1]byte{1}
			_, _ = syscall.Write(asyncWriteFD, one[:])
		}
	}()
}

//export PopCompletedAsync
func PopCompletedAsync(outReqID *C.uint64_t) *C.CSpannerBatch {
	asyncMu.Lock()
	defer asyncMu.Unlock()
	if len(asyncCompleted) == 0 {
		if asyncReadFD >= 0 {
			var drain [64]byte
			_, _ = syscall.Read(asyncReadFD, drain[:])
		}
		return nil
	}
	item := asyncCompleted[0]
	asyncCompleted = asyncCompleted[1:]
	if len(asyncCompleted) == 0 && asyncReadFD >= 0 {
		var drain [64]byte
		_, _ = syscall.Read(asyncReadFD, drain[:])
	}
	*outReqID = C.uint64_t(item.reqID)
	return item.batch
}

func main() {}
