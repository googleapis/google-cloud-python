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
	"sync"
	"sync/atomic"
	"syscall"
	"time"
	"unsafe"
)

const (
	ipcMagic       uint32 = 0x4F475053 // "SPGO"
	ipcVersion     uint16 = 1
	ipcReqHdrSize         = 32
	ipcRespHdrSize        = 48
	ipcMaxBody            = 16 << 20

	ipcOpExecute    uint16 = 1
	ipcOpInit       uint16 = 2
	ipcOpClose      uint16 = 3
	ipcOpStats      uint16 = 4
	ipcOpResetStats uint16 = 5
	ipcOpPing       uint16 = 6
	ipcOpShutdown   uint16 = 7
	ipcOpProfStart  uint16 = 8
	ipcOpProfStop   uint16 = 9
	ipcOpInfo       uint16 = 10

	ipcStatusProtocolError int32 = -1
	ipcStatusInitFailed    int32 = -2
	ipcStatusUnsupported   int32 = -3

	// Must match CellKind / CSpannerBatch.format in main.go's cgo preamble.
	ipcCellKindString         = 3
	ipcBatchFormatNativeCells = 1
)

var (
	ipcSockBuf      int
	ipcLockOSThread bool
	ipcListener     *net.UnixListener
	ipcClosing      atomic.Bool
	ipcShutdownOnce sync.Once
)

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
		if err != nil {
			return
		}
	}
}

func main() {
	socketPath := flag.String("socket", "", "Unix domain socket path to listen on")
	parentPid := flag.Int("parent-pid", 0, "exit when this process is no longer our parent (0 = disabled)")
	flag.IntVar(&ipcSockBuf, "sockbuf", 0, "SO_SNDBUF/SO_RCVBUF bytes for accepted connections (0 = OS default)")
	flag.BoolVar(&ipcLockOSThread, "lock-os-thread", false,
		"run each Go Shared Core call with runtime.LockOSThread (FFI-equivalent execution model)")
	flag.Parse()
	if *socketPath == "" {
		fmt.Fprintln(os.Stderr, "spanner_ipc_server: -socket is required")
		os.Exit(2)
	}
	// Terminate together with the benchmark process that spawned us (no orphaned sidecars). The
	// getppid() check closes the race where the parent died before PR_SET_PDEATHSIG took effect.
	_, _, _ = syscall.RawSyscall(syscall.SYS_PRCTL, syscall.PR_SET_PDEATHSIG, uintptr(syscall.SIGTERM), 0)
	if *parentPid > 0 && os.Getppid() != *parentPid {
		fmt.Fprintln(os.Stderr, "spanner_ipc_server: parent already exited")
		os.Exit(3)
	}

	_ = os.Remove(*socketPath)
	ln, err := net.ListenUnix("unix", &net.UnixAddr{Name: *socketPath, Net: "unix"})
	if err != nil {
		fmt.Fprintf(os.Stderr, "spanner_ipc_server: listen %s: %v\n", *socketPath, err)
		os.Exit(1)
	}
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
