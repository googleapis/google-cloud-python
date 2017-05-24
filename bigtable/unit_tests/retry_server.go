package main

import (
	"golang.org/x/net/context"
	"cloud.google.com/go/bigtable"
	"cloud.google.com/go/bigtable/bttest"
	"google.golang.org/grpc"
	"google.golang.org/api/option"
	btpb "google.golang.org/genproto/googleapis/bigtable/v2"
	rpcpb "google.golang.org/genproto/googleapis/rpc/status"
	"strings"
	"flag"
	"os"
	"bufio"
	"log"
	"reflect"
	"github.com/golang/protobuf/ptypes/wrappers"
	"google.golang.org/grpc/codes"
	"fmt"
)

var (
	scriptFile = flag.String("script", "", "the file containing the script")
	codeMap = make(map[string]codes.Code)
	failed = false
)

type serverScript struct {
	actions []string
	idx int
}

func init() {
	codes := []codes.Code{
		codes.OK, codes.Canceled, codes.Unknown, codes.InvalidArgument,
		codes.DeadlineExceeded, codes.NotFound, codes.AlreadyExists, codes.PermissionDenied,
		codes.Unauthenticated, codes.ResourceExhausted, codes.Unauthenticated, codes.ResourceExhausted,
		codes.FailedPrecondition, codes.Aborted, codes.OutOfRange, codes.Unimplemented,
		codes.Internal, codes.Unavailable, codes.DataLoss}
	for _, code := range codes {
		codeMap[code.String()] = code
	}
}

func (s *serverScript) serverAction() []string {
	return s.nextAction("SERVER:")
}

func (s *serverScript) expectAction() []string {
	return s.nextAction("EXPECT:")
}

func (s *serverScript) isFinished() bool {
	return s.idx == len(s.actions)
}

func (s *serverScript) nextAction(prefix string) []string {
	if s.isFinished() {
		return nil
	}

	a := s.actions[s.idx]
	if strings.HasPrefix(a, prefix) {
		s.idx++
		return strings.Split(a, " ")[1:]
	}
	return nil
}

func main() {
	flag.Parse()

	var actions []string
	if file, err := os.Open(*scriptFile); err == nil {
		defer file.Close()

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Text()
			if len(strings.TrimSpace(line)) == 0 ||
					strings.HasPrefix(line, "#") ||
					strings.HasPrefix(line, "CLIENT:") {
				// Comment
				continue
			}
			actions = append(actions, strings.TrimSpace(line))
		}

		// check for errors
		if err = scanner.Err(); err != nil {
			log.Fatal(err)
		}
	} else {
		log.Fatal(err)
	}

	ctx := context.Background()
	script := serverScript{actions:actions}

	// Create the interceptor that will do all of our work.
	interceptor := func(srv interface{}, ss grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
		if failed {
			return grpc.Errorf(codes.Canceled, "The test has failed")
		}
		if strings.HasSuffix(info.FullMethod, "MutateRows") || strings.HasSuffix(info.FullMethod, "ReadRows") {
			fmt.Printf("DEBUG: %v\n", info)
			action := script.expectAction()
			op := action[0]
			fmt.Printf("Expect: %s\n", op)
			switch op {
			case "SCAN":
				if !strings.HasSuffix(info.FullMethod, "ReadRows") {
					fail("Expected %v, received call to %v", action, info.FullMethod)
				}
				validateScan(action, ss)
			case "READ":
				if !strings.HasSuffix(info.FullMethod, "ReadRows") {
					fail("Expected %v, received call to %v", action, info.FullMethod)
				}
				validateRead(strings.Split(action[1], ","), ss)
			case "WRITE":
				if !strings.HasSuffix(info.FullMethod, "MutateRows") {
					fail("Expected %v, received call to %v", action, info.FullMethod)
				}
				validateWrite(strings.Split(action[1], ","), ss)
			}

			for {
				action = script.serverAction()
				if action == nil {
					break
				}
				log.Printf("Action: %s\n", action)
				switch action[0] {
				case "READ_RESPONSE":
					writeReadRowsResponse(ss,  strings.Split(action[1], ",")...)
				case "WRITE_RESPONSE":
					writeMutateRowsResponse(ss,  strings.Split(action[1], ",")...)
				case "ERROR":
					return grpc.Errorf(codeMap[action[1]], "")
				default:
					fail("Invalid action during response: %v", action)
				}
			}
			if script.isFinished() && !failed {
				fmt.Println("PASS")
			}
			return nil
		} else {
			// Delegate to the handler for other operations (but there shouldn't be any)
			return handler(ctx, ss)
		}
	}

	cleaner, err := setupFakeServer(grpc.StreamInterceptor(interceptor))
	if err != nil {
		fmt.Println("FAIL")
		log.Fatal(err)
	}
	defer cleaner()
	select {}
}

func validateScan(action []string, ss grpc.ServerStream) {
	// Look for one or more ranges
	var wantRanges []*btpb.RowRange
	for _, r := range action[1:] {
		startEnd := strings.Split(r[1:len(r)-1], ",")
		rr := btpb.RowRange{}
		if strings.HasPrefix(r, "[") {
			rr.StartKey = &btpb.RowRange_StartKeyClosed{[]byte(startEnd[0])}
		} else if strings.HasPrefix(r, "(") {
			rr.StartKey = &btpb.RowRange_StartKeyOpen{[]byte(startEnd[0])}
		} else {
			fail("Invalid range: %v", r)
		}

		if strings.HasSuffix(r, "]") {
			rr.EndKey = &btpb.RowRange_EndKeyClosed{[]byte(startEnd[1])}
		} else if strings.HasSuffix(r, ")") {
			rr.EndKey = &btpb.RowRange_EndKeyOpen{[]byte(startEnd[1])}
		} else {
			fail("Invalid range: %v", r)
		}
		wantRanges = append(wantRanges, &rr)
	}

	req := new(btpb.ReadRowsRequest)
	ss.RecvMsg(req)

	want := &btpb.RowSet{RowRanges: wantRanges}
	if !reflect.DeepEqual(want, req.Rows) {
		fail("Invalid scan. got: %v\nwant: %v\n",req.Rows, want)
	}
}

func validateWrite(keys []string, ss grpc.ServerStream) {
	want := make([][]byte, len(keys))
	for i, row := range keys {
		want[i] = []byte(row)
	}

	req := new(btpb.MutateRowsRequest)
	ss.RecvMsg(req)

	var got [][]byte
	for _, entry := range req.Entries {
		got = append(got, entry.RowKey)
	}

	if !reflect.DeepEqual(got, want) {
		fail("Invalid write. got: %v\nwant: %v\n", got, want)
	}
}

func validateRead(keys []string, ss grpc.ServerStream) {
	keyBytes := make([][]byte, len(keys))
	for i, row := range keys {
		keyBytes[i] = []byte(row)
	}
	want := &btpb.RowSet{RowKeys:keyBytes}

	req := new(btpb.ReadRowsRequest)
	ss.RecvMsg(req)

	if !reflect.DeepEqual(want, req.Rows) {
		fail("Invalid read. got: %v\nwant: %v\n", req.Rows, want)
	}
}

func writeReadRowsResponse(ss grpc.ServerStream, rowKeys ...string) error {
	var chunks []*btpb.ReadRowsResponse_CellChunk
	for _, key := range rowKeys {
		chunks = append(chunks, &btpb.ReadRowsResponse_CellChunk{
			RowKey:     []byte(key),
			FamilyName: &wrappers.StringValue{Value: "fm"},
			Qualifier:  &wrappers.BytesValue{Value: []byte("col")},
			RowStatus:  &btpb.ReadRowsResponse_CellChunk_CommitRow{CommitRow: true},
		})
	}
	return ss.SendMsg(&btpb.ReadRowsResponse{Chunks: chunks})
}

func writeMutateRowsResponse(ss grpc.ServerStream, codes ...string) error {
	res := &btpb.MutateRowsResponse{Entries: make([]*btpb.MutateRowsResponse_Entry, len(codes))}
	for i, code := range codes {
		res.Entries[i] = &btpb.MutateRowsResponse_Entry{
			Index:  int64(i),
			Status: &rpcpb.Status{Code: int32(codeMap[code]), Message: ""},
		}
	}
	return ss.SendMsg(res)
}

func fail(format string, v ...interface{}) {
	log.Printf(format, v...)
	fmt.Println("FAIL")
	failed = true
}

func setupFakeServer(opt ...grpc.ServerOption) (cleanup func(), err error) {
	srv, err := bttest.NewServer("127.0.0.1:", opt...)
	if err != nil {
		return nil, err
	}
	conn, err := grpc.Dial(srv.Addr, grpc.WithInsecure())
	if err != nil {
		return nil, err
	}

	client, err := bigtable.NewClient(context.Background(), "client", "instance", option.WithGRPCConn(conn))
	if err != nil {
		return nil, err
	}

	adminClient, err := bigtable.NewAdminClient(context.Background(), "client", "instance", option.WithGRPCConn(conn))
	if err != nil {
		return nil, err
	}
	if err := adminClient.CreateTable(context.Background(), "table"); err != nil {
		return nil, err
	}
	if err := adminClient.CreateColumnFamily(context.Background(), "table", "cf"); err != nil {
		return nil, err
	}

	fmt.Println(srv.Addr)

	cleanupFunc := func() {
		adminClient.Close()
		client.Close()
		srv.Close()
	}
	return cleanupFunc, nil
}
