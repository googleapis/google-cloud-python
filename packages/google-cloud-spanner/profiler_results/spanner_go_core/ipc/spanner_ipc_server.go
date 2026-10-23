//go:build spanner_ipc_server

// Spanner Go Shared Core - IPC sidecar entry point.
//
// This file is NOT part of the FFI build. build_ipc_core.sh stages a temporary copy of the
// *unmodified* Go Shared Core sources used by the FFI library (main.go, client.go, decode.go,
// go.mod, go.sum), strips only the empty `func main() {}` stub that -buildmode=c-shared needs,
// adds this file, and builds a standalone sidecar executable with the same toolchain and the
// same dependency versions as libspanner_go.so.
//
// Every query served by the sidecar therefore runs the exact same Go Shared Core code as the
// FFI flow:
//
//	InitGoCoreClient          -> NewCoreClient (same gRPC channel pool, TLS, auth, windows)
//	executeStreamingSqlInternal -> same request build, timingProtoCodec, chunk assembly, retries,
//	                               buildCBatch zero-copy CSpannerCell + string-arena encoding
//	FreeSpannerBatch
//
// The ONLY difference vs FFI is the boundary. Instead of handing the CSpannerBatch pointer to an
// in-process CPython extension, the sidecar ships the batch's cells array and string arena
// verbatim over a Unix domain socket with a single writev() (no re-encoding, no JSON, no
// protobuf), and the Python IPC extension materializes the same Python objects as the FFI
// extension's batch_to_pylist().
//
// Wire protocol (little-endian, same host/ABI on both sides):
//
//	Request  header (32 bytes): magic u32 | version u16 | op u16 | handle u64 |
//	                            session_len u32 | sql_len u32 | param_len u32 | aux u32
//	         body             : session bytes | sql bytes | param bytes
//	Response header (48 bytes): magic u32 | version u16 | op u16 | status i32 | row_count i32 |
//	                            col_count i32 | attempt_count i32 | cells_bytes u64 |
//	                            arena_bytes u64 | extra_bytes u32 | cell_size u32
//	         body             : CSpannerCell[row_count*col_count] | string arena | extra bytes
package main

/*
#include <stdint.h>
#include <stdlib.h>
*/
import "C"

import (
	"bufio"
	"encoding/binary"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net"
	"os"
	"os/signal"
	"runtime"
	"runtime/debug"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"syscall"
	"time"
	"unsafe"

	spannerpb "cloud.google.com/go/spanner/apiv1/spannerpb"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/structpb"
)

const (
	ipcMagic       uint32 = 0x4F475053 // "SPGO"
	ipcVersion     uint16 = 1
	ipcReqHdrSize         = 32
	ipcRespHdrSize        = 48
	ipcMaxBody            = 16 << 20

	ipcOpExecute         uint16 = 1
	ipcOpInit            uint16 = 2
	ipcOpClose           uint16 = 3
	ipcOpStats           uint16 = 4
	ipcOpResetStats      uint16 = 5
	ipcOpPing            uint16 = 6
	ipcOpShutdown        uint16 = 7
	ipcOpProfStart       uint16 = 8
	ipcOpProfStop        uint16 = 9
	ipcOpInfo            uint16 = 10
	ipcOpExecuteLowMaint uint16 = 11 // Low-maintenance pure-Go JSON flow (zero C.malloc/unsafe, plain goroutines)

	ipcStatusProtocolError int32 = -1
	ipcStatusInitFailed    int32 = -2
	ipcStatusUnsupported   int32 = -3
	ipcStatusPanic         int32 = -4

	// Must match CellKind / CSpannerBatch.format in main.go's cgo preamble.
	ipcCellKindString         = 3
	ipcBatchFormatNativeCells = 1

	ipcHex = "0123456789abcdef"
)

var (
	ipcSockBuf      int
	ipcLockOSThread bool
	ipcListener     *net.UnixListener
	ipcClosing      atomic.Bool
	ipcShutdownOnce sync.Once
	ipcJSONBufPool  = sync.Pool{
		New: func() interface{} {
			b := make([]byte, 0, 4096)
			return &b
		},
	}
)

func ipcAppendJSONString(dst []byte, s string) []byte {
	dst = append(dst, '"')
	start := 0
	for i := 0; i < len(s); i++ {
		c := s[i]
		if c >= 0x20 && c != '"' && c != '\\' {
			continue
		}
		if start < i {
			dst = append(dst, s[start:i]...)
		}
		switch c {
		case '"', '\\':
			dst = append(dst, '\\', c)
		case '\b':
			dst = append(dst, '\\', 'b')
		case '\f':
			dst = append(dst, '\\', 'f')
		case '\n':
			dst = append(dst, '\\', 'n')
		case '\r':
			dst = append(dst, '\\', 'r')
		case '\t':
			dst = append(dst, '\\', 't')
		default:
			dst = append(dst, '\\', 'u', '0', '0', ipcHex[c>>4], ipcHex[c&0x0f])
		}
		start = i + 1
	}
	if start < len(s) {
		dst = append(dst, s[start:]...)
	}
	return append(dst, '"')
}

func ipcAppendJSONValue(dst []byte, val *structpb.Value, fieldType *spannerpb.Type) []byte {
	if val == nil {
		return append(dst, "null"...)
	}
	switch k := val.Kind.(type) {
	case *structpb.Value_NullValue:
		return append(dst, "null"...)
	case *structpb.Value_BoolValue:
		if k.BoolValue {
			return append(dst, "true"...)
		}
		return append(dst, "false"...)
	case *structpb.Value_NumberValue:
		return strconv.AppendFloat(dst, k.NumberValue, 'f', -1, 64)
	case *structpb.Value_StringValue:
		return ipcAppendJSONString(dst, k.StringValue)
	case *structpb.Value_ListValue:
		if k.ListValue == nil {
			return append(dst, "[]"...)
		}
		var elemType *spannerpb.Type
		if fieldType != nil {
			elemType = fieldType.ArrayElementType
		}
		dst = append(dst, '[')
		for i, v := range k.ListValue.Values {
			if i > 0 {
				dst = append(dst, ',')
			}
			dst = ipcAppendJSONValue(dst, v, elemType)
		}
		return append(dst, ']')
	case *structpb.Value_StructValue:
		if k.StructValue == nil {
			return append(dst, "{}"...)
		}
		dst = append(dst, '{')
		first := true
		if fieldType != nil && fieldType.StructType != nil {
			for _, f := range fieldType.StructType.Fields {
				if !first {
					dst = append(dst, ',')
				}
				first = false
				dst = ipcAppendJSONString(dst, f.Name)
				dst = append(dst, ':')
				if v, ok := k.StructValue.Fields[f.Name]; ok {
					dst = ipcAppendJSONValue(dst, v, f.Type)
				} else {
					dst = append(dst, "null"...)
				}
			}
		} else {
			for fName, fVal := range k.StructValue.Fields {
				if !first {
					dst = append(dst, ',')
				}
				first = false
				dst = ipcAppendJSONString(dst, fName)
				dst = append(dst, ':')
				dst = ipcAppendJSONValue(dst, fVal, nil)
			}
		}
		return append(dst, '}')
	default:
		return append(dst, "null"...)
	}
}

func ipcAppendJSONBatch(dst []byte, batch [][]*structpb.Value, rowType []*spannerpb.StructType_Field) []byte {
	dst = append(dst, '[')
	for r, row := range batch {
		if r > 0 {
			dst = append(dst, ',')
		}
		dst = append(dst, '[')
		for c, val := range row {
			if c > 0 {
				dst = append(dst, ',')
			}
			var ft *spannerpb.Type
			if c < len(rowType) {
				ft = rowType[c].Type
			}
			dst = ipcAppendJSONValue(dst, val, ft)
		}
		dst = append(dst, ']')
	}
	return append(dst, ']')
}

// ipcExecuteStreamingSqlPureGo executes the exact same Spanner gRPC stream, retry loop, and
// chunk assembly as executeStreamingSqlInternal, but encodes the result batch into pure-Go JSON
// bytes (dst) with zero C.malloc, zero C.free, and zero unsafe pointers.
func ipcExecuteStreamingSqlPureGo(
	handle uintptr,
	sessionStr string,
	sqlStr string,
	paramIdStr string,
	dst []byte,
) (jsonOut []byte, rowCount int, colCount int, attemptCount int, errCode int, errMsg string) {
	client := getClient(handle)
	if client == nil {
		return dst[:0], 0, 0, 1, int(codes.InvalidArgument), "Invalid or closed CoreClient handle"
	}

	dbPrefix := sessionStr
	if idx := strings.Index(sessionStr, "/sessions/"); idx != -1 {
		dbPrefix = sessionStr[:idx]
	}

	var lastResumeToken []byte
	var rowType []*spannerpb.StructType_Field
	var pendingValue *structpb.Value
	var currentRow []*structpb.Value
	batch := make([][]*structpb.Value, 0, 16)

	for {
		attemptCount++
		token, err := client.GetToken()
		if err != nil {
			return dst[:0], 0, 0, attemptCount, int(codes.Unauthenticated), fmt.Sprintf("Failed to get GCP auth token: %v", err)
		}

		tReq0 := goThreadCPUTimeNs()
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
		if err != nil {
			st, _ := status.FromError(err)
			if (st.Code() == codes.Unavailable || st.Code() == codes.Internal) && len(lastResumeToken) > 0 {
				continue
			}
			return dst[:0], 0, 0, attemptCount, int(st.Code()), st.Message()
		}

		shouldRetry := false
		for {
			chunk, err := stream.Recv()
			if err == io.EOF {
				break
			}
			if err != nil {
				st, _ := status.FromError(err)
				if (st.Code() == codes.Unavailable || st.Code() == codes.Internal) && len(lastResumeToken) > 0 {
					shouldRetry = true
					break
				}
				return dst[:0], 0, 0, attemptCount, int(st.Code()), st.Message()
			}

			tAsm0 := goThreadCPUTimeNs()
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
			if tAsm1 >= tAsm0 {
				atomic.AddUint64(&statChunkAssembleNs, tAsm1-tAsm0)
			}
		}

		if shouldRetry {
			continue
		}

		tEnc0 := goThreadCPUTimeNs()
		if pendingValue != nil {
			currentRow = append(currentRow, pendingValue)
			pendingValue = nil
		}
		if len(currentRow) > 0 {
			batch = append(batch, currentRow)
			currentRow = nil
		}

		rowCount = len(batch)
		if rowCount > 0 {
			colCount = len(batch[0])
		}
		jsonOut = ipcAppendJSONBatch(dst[:0], batch, rowType)
		tEnc1 := goThreadCPUTimeNs()
		if tEnc1 >= tEnc0 {
			atomic.AddUint64(&statArenaEncodeNs, tEnc1-tEnc0)
		}
		atomic.AddUint64(&statCallCount, 1)
		return jsonOut, rowCount, colCount, attemptCount, 0, ""
	}
}

func ipcPutRespHeader(h []byte, op uint16, status, rows, cols, attempts int32,
	cellsBytes, arenaBytes uint64, extraBytes, cellSize uint32) {
	binary.LittleEndian.PutUint32(h[0:4], ipcMagic)
	binary.LittleEndian.PutUint16(h[4:6], ipcVersion)
	binary.LittleEndian.PutUint16(h[6:8], op)
	binary.LittleEndian.PutUint32(h[8:12], uint32(status))
	binary.LittleEndian.PutUint32(h[12:16], uint32(rows))
	binary.LittleEndian.PutUint32(h[16:20], uint32(cols))
	binary.LittleEndian.PutUint32(h[20:24], uint32(attempts))
	binary.LittleEndian.PutUint64(h[24:32], cellsBytes)
	binary.LittleEndian.PutUint64(h[32:40], arenaBytes)
	binary.LittleEndian.PutUint32(h[40:44], extraBytes)
	binary.LittleEndian.PutUint32(h[44:48], cellSize)
}

// ipcWriteSimple writes a response header followed by an optional extra payload.
func ipcWriteSimple(conn *net.UnixConn, hdr []byte, op uint16, status int32, extra []byte) error {
	ipcPutRespHeader(hdr, op, status, 0, 0, 0, 0, 0, uint32(len(extra)), 0)
	bufs := net.Buffers{hdr, extra}
	_, err := bufs.WriteTo(conn)
	return err
}

func ipcShutdown() {
	ipcShutdownOnce.Do(func() {
		ipcClosing.Store(true)
		if ipcListener != nil {
			_ = ipcListener.Close() // also unlinks the socket path (SetUnlinkOnClose)
		}
	})
}

// ipcServeConn serves one client connection. The Python IPC extension keeps one connection per
// client thread and issues one request at a time on it, mirroring the FFI flow where each Python
// thread performs one blocking ExecuteStreamingSqlSync call at a time.
func ipcServeConn(conn *net.UnixConn) {
	defer conn.Close()
	if ipcSockBuf > 0 {
		_ = conn.SetReadBuffer(ipcSockBuf)
		_ = conn.SetWriteBuffer(ipcSockBuf)
	}
	br := bufio.NewReaderSize(conn, 64<<10)
	var reqHdr [ipcReqHdrSize]byte
	respHdr := make([]byte, ipcRespHdrSize)
	var body []byte
	defer func() {
		if r := recover(); r != nil {
			msg := fmt.Sprintf("Spanner Go IPC sidecar recovered panic: %v", r)
			_ = ipcWriteSimple(conn, respHdr, 0, ipcStatusPanic, []byte(msg))
		}
	}()

	for {
		if _, err := io.ReadFull(br, reqHdr[:]); err != nil {
			return // client closed the connection
		}
		magic := binary.LittleEndian.Uint32(reqHdr[0:4])
		version := binary.LittleEndian.Uint16(reqHdr[4:6])
		op := binary.LittleEndian.Uint16(reqHdr[6:8])
		handle := binary.LittleEndian.Uint64(reqHdr[8:16])
		sessLen := int(binary.LittleEndian.Uint32(reqHdr[16:20]))
		sqlLen := int(binary.LittleEndian.Uint32(reqHdr[20:24]))
		paramLen := int(binary.LittleEndian.Uint32(reqHdr[24:28]))
		aux := binary.LittleEndian.Uint32(reqHdr[28:32])
		total := sessLen + sqlLen + paramLen
		if magic != ipcMagic || version != ipcVersion || sessLen < 0 || sqlLen < 0 || paramLen < 0 ||
			total > ipcMaxBody {
			_ = ipcWriteSimple(conn, respHdr, op, ipcStatusProtocolError, []byte("bad request header"))
			return
		}
		if cap(body) < total {
			body = make([]byte, total)
		}
		body = body[:total]
		if _, err := io.ReadFull(br, body); err != nil {
			return
		}

		var err error
		switch op {
		case ipcOpExecute:
			session := string(body[:sessLen])
			sql := string(body[sessLen : sessLen+sqlLen])
			param := string(body[sessLen+sqlLen:])

			// Same Go Shared Core entry point that the FFI export ExecuteStreamingSqlSync wraps.
			// With -lock-os-thread the call runs on a goroutine wired to its OS thread for the whole
			// call, reproducing the FFI execution model (a cgo callback goroutine is locked to the
			// calling Python thread, so every network wait is a locked-M park/handoff). Without it
			// the sidecar uses plain goroutines (the natural Go sidecar model).
			if ipcLockOSThread {
				runtime.LockOSThread()
			}
			batch := executeStreamingSqlInternal(uintptr(handle), session, sql, param)
			if ipcLockOSThread {
				runtime.UnlockOSThread()
			}

			status := int32(batch.error_code)
			attempts := int32(batch.attempt_count)
			if status != 0 {
				msg := "Unknown Spanner Go Shared Core error"
				if batch.error_msg != nil {
					msg = C.GoString(batch.error_msg)
				}
				ipcPutRespHeader(respHdr, op, status, 0, 0, attempts, 0, 0, uint32(len(msg)), 0)
				bufs := net.Buffers{respHdr, []byte(msg)}
				_, err = bufs.WriteTo(conn)
			} else {
				rows := int(batch.row_count)
				cols := int(batch.col_count)
				nCells := rows * cols
				cellSize := int(unsafe.Sizeof(*batch.cells))
				var cellBytes, arenaBytes []byte
				supported := true
				if nCells > 0 {
					if int(batch.format) != ipcBatchFormatNativeCells || batch.cells == nil {
						supported = false
					} else {
						// Ship the exact C-heap CSpannerCell array produced by buildCBatch. The string
						// arena length is not stored in CSpannerBatch, so derive it from the cells
						// (buildCBatch packs non-empty strings contiguously in row-major cell order).
						cells := unsafe.Slice(batch.cells, nCells)
						arenaLen := 0
						for i := range cells {
							if cells[i].kind == ipcCellKindString {
								arenaLen += int(cells[i].str_len)
							}
						}
						cellBytes = unsafe.Slice((*byte)(unsafe.Pointer(batch.cells)), nCells*cellSize)
						if arenaLen > 0 && batch.string_arena != nil {
							arenaBytes = unsafe.Slice((*byte)(unsafe.Pointer(batch.string_arena)), arenaLen)
						}
					}
				}
				if supported {
					ipcPutRespHeader(respHdr, op, 0, int32(rows), int32(cols), attempts,
						uint64(len(cellBytes)), uint64(len(arenaBytes)), 0, uint32(cellSize))
					// writev(header, cells, arena) straight from the C heap: zero re-encoding copies.
					bufs := net.Buffers{respHdr, cellBytes, arenaBytes}
					_, err = bufs.WriteTo(conn)
				} else {
					err = ipcWriteSimple(conn, respHdr, op, ipcStatusUnsupported,
						[]byte("IPC flow requires SPANNER_GO_DIRECT_DESERIALIZATION (native cells), same as FFI batch_to_pylist"))
				}
			}
			FreeSpannerBatch(batch)

		case ipcOpExecuteLowMaint:
			// Low-Maintenance IPC path: 100% pure-Go execution + zero-reflection JSON encoding into a
			// pooled byte slice (zero C.malloc, zero C.free, zero unsafe C structs, plain goroutines).
			session := string(body[:sessLen])
			sql := string(body[sessLen : sessLen+sqlLen])
			param := string(body[sessLen+sqlLen:])

			bufPtr := ipcJSONBufPool.Get().(*[]byte)
			jsonBytes, rows, cols, attempts, errCode, errMsg := ipcExecuteStreamingSqlPureGo(
				uintptr(handle), session, sql, param, (*bufPtr)[:0],
			)
			if errCode != 0 {
				if errMsg == "" {
					errMsg = "Unknown Spanner Go Shared Core error"
				}
				ipcPutRespHeader(respHdr, op, int32(errCode), 0, 0, int32(attempts), 0, 0, uint32(len(errMsg)), 0)
				bufs := net.Buffers{respHdr, []byte(errMsg)}
				_, err = bufs.WriteTo(conn)
			} else {
				ipcPutRespHeader(respHdr, op, 0, int32(rows), int32(cols), int32(attempts),
					0, uint64(len(jsonBytes)), 0, 0)
				bufs := net.Buffers{respHdr, jsonBytes}
				_, err = bufs.WriteTo(conn)
			}
			if cap(jsonBytes) <= 2<<20 {
				*bufPtr = jsonBytes[:0]
				ipcJSONBufPool.Put(bufPtr)
			}

		case ipcOpInit:
			h := uint64(InitGoCoreClient(C.int(int32(aux))))
			var extra [8]byte
			binary.LittleEndian.PutUint64(extra[:], h)
			status := int32(0)
			if h == 0 {
				status = ipcStatusInitFailed
			}
			err = ipcWriteSimple(conn, respHdr, op, status, extra[:])

		case ipcOpClose:
			CloseGoCoreClient(C.uintptr_t(handle))
			err = ipcWriteSimple(conn, respHdr, op, 0, nil)

		case ipcOpStats:
			var ru syscall.Rusage
			_ = syscall.Getrusage(syscall.RUSAGE_SELF, &ru)
			var gs [7]C.uint64_t
			GetGoCoreStats(&gs[0])
			vals := [...]uint64{
				uint64(ru.Utime.Sec)*1000000 + uint64(ru.Utime.Usec),
				uint64(ru.Stime.Sec)*1000000 + uint64(ru.Stime.Usec),
				uint64(gs[0]), uint64(gs[1]), uint64(gs[2]), uint64(gs[3]),
				uint64(gs[4]), uint64(gs[5]), uint64(gs[6]),
				uint64(runtime.NumGoroutine()),
				uint64(ru.Maxrss),
				uint64(ru.Nvcsw),
				uint64(ru.Nivcsw),
				uint64(runtime.GOMAXPROCS(0)),
				uint64(runtime.NumCPU()),
				uint64(os.Getpid()),
			}
			extra := make([]byte, 8*len(vals))
			for i, v := range vals {
				binary.LittleEndian.PutUint64(extra[8*i:], v)
			}
			err = ipcWriteSimple(conn, respHdr, op, 0, extra)

		case ipcOpResetStats:
			ResetGoCoreStats()
			err = ipcWriteSimple(conn, respHdr, op, 0, nil)

		case ipcOpPing:
			err = ipcWriteSimple(conn, respHdr, op, 0, nil)

		case ipcOpProfStart:
			cs := C.CString(string(body[:sessLen]))
			rc := int32(StartGoCPUProfile(cs))
			C.free(unsafe.Pointer(cs))
			err = ipcWriteSimple(conn, respHdr, op, rc, nil)

		case ipcOpProfStop:
			StopGoCPUProfile()
			err = ipcWriteSimple(conn, respHdr, op, 0, nil)

		case ipcOpInfo:
			info := map[string]interface{}{
				"go_version":     runtime.Version(),
				"gomaxprocs":     runtime.GOMAXPROCS(0),
				"num_cpu":        runtime.NumCPU(),
				"pid":            os.Getpid(),
				"sockbuf":        ipcSockBuf,
				"lock_os_thread": ipcLockOSThread,
			}
			if bi, ok := debug.ReadBuildInfo(); ok {
				deps := make(map[string]string, len(bi.Deps))
				for _, d := range bi.Deps {
					deps[d.Path] = d.Version
				}
				info["main_module"] = bi.Main.Path
				info["deps"] = deps
			}
			payload, _ := json.Marshal(info)
			err = ipcWriteSimple(conn, respHdr, op, 0, payload)

		case ipcOpShutdown:
			err = ipcWriteSimple(conn, respHdr, op, 0, nil)
			go func() {
				time.Sleep(20 * time.Millisecond)
				ipcShutdown()
			}()

		default:
			err = ipcWriteSimple(conn, respHdr, op, ipcStatusProtocolError, []byte("unknown op"))
		}
		if cap(body) > 64<<10 {
			body = nil // do not permanently retain large request buffers on idle connections
		}
		if err != nil {
			return
		}
	}
}

func main() {
	socketPath := flag.String("socket", "", "Unix domain socket path to listen on")
	parentPid := flag.Int("parent-pid", 0, "exit when this process is no longer our parent (0 = disabled)")
	lifelineFD := flag.Int("lifeline-fd", -1, "inherited pipe FD: exit when parent process closes all write ends (portable, process-level)")
	flag.IntVar(&ipcSockBuf, "sockbuf", 0, "SO_SNDBUF/SO_RCVBUF bytes for accepted connections (0 = OS default)")
	flag.BoolVar(&ipcLockOSThread, "lock-os-thread", false,
		"run each Go Shared Core call with runtime.LockOSThread (FFI-equivalent execution model)")
	flag.Parse()
	if *socketPath == "" {
		fmt.Fprintln(os.Stderr, "spanner_ipc_server: -socket is required")
		os.Exit(2)
	}
	if *lifelineFD >= 0 {
		// Portable, process-level parent lifecycle monitor: EOF triggers only when the entire parent
		// process exits (even on SIGKILL), avoiding the Linux PR_SET_PDEATHSIG worker-thread-exit trap.
		lf := os.NewFile(uintptr(*lifelineFD), "lifeline")
		go func() {
			var b [1]byte
			_, _ = lf.Read(b[:])
			_ = lf.Close()
			ipcShutdown()
			os.Exit(0)
		}()
	} else {
		// Terminate together with the benchmark process that spawned us (no orphaned sidecars). The
		// getppid() check closes the race where the parent died before PR_SET_PDEATHSIG took effect.
		_, _, _ = syscall.RawSyscall(syscall.SYS_PRCTL, syscall.PR_SET_PDEATHSIG, uintptr(syscall.SIGTERM), 0)
		if *parentPid > 0 && os.Getppid() != *parentPid {
			fmt.Fprintln(os.Stderr, "spanner_ipc_server: parent already exited")
			os.Exit(3)
		}
	}

	_ = os.Remove(*socketPath)
	ln, err := net.ListenUnix("unix", &net.UnixAddr{Name: *socketPath, Net: "unix"})
	if err != nil {
		fmt.Fprintf(os.Stderr, "spanner_ipc_server: listen %s: %v\n", *socketPath, err)
		os.Exit(1)
	}
	_ = os.Chmod(*socketPath, 0600)
	ln.SetUnlinkOnClose(true)
	ipcListener = ln

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-sigCh
		ipcShutdown()
	}()

	fmt.Printf("SPANNER_GO_IPC_READY pid=%d socket=%s go=%s gomaxprocs=%d lock_os_thread=%t\n",
		os.Getpid(), *socketPath, runtime.Version(), runtime.GOMAXPROCS(0), ipcLockOSThread)

	for {
		conn, err := ln.AcceptUnix()
		if err != nil {
			if ipcClosing.Load() {
				return
			}
			time.Sleep(10 * time.Millisecond) // transient accept error (e.g. EMFILE): back off
			continue
		}
		go ipcServeConn(conn)
	}
}
