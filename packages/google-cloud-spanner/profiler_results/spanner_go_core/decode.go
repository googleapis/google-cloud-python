package main

import (
	"bytes"
	"encoding/json"
	"strconv"

	spannerpb "cloud.google.com/go/spanner/apiv1/spannerpb"
	"google.golang.org/protobuf/types/known/structpb"
)

// writeValueJson encodes a protobuf Value directly into a bytes.Buffer in valid JSON format
// matching the strictly-typed Spanner specifications without reflection or intermediate heap boxing.
func writeValueJson(buf *bytes.Buffer, val *structpb.Value, fieldType *spannerpb.Type) {
	if val == nil {
		buf.WriteString("null")
		return
	}

	switch k := val.Kind.(type) {
	case *structpb.Value_NullValue:
		buf.WriteString("null")
	case *structpb.Value_BoolValue:
		if k.BoolValue {
			buf.WriteString("true")
		} else {
			buf.WriteString("false")
		}
	case *structpb.Value_NumberValue:
		buf.WriteString(strconv.FormatFloat(k.NumberValue, 'f', -1, 64))
	case *structpb.Value_StringValue:
		// Spanner TypeCodes: INT64, NUMERIC, TIMESTAMP, DATE, BYTES, JSON, STRING
		// All Spanner primitive strings/numbers are serialized as JSON strings matching Rust prototype
		jsonEscapeString(buf, k.StringValue)
	case *structpb.Value_ListValue:
		if k.ListValue == nil {
			buf.WriteString("[]")
			return
		}
		var elemType *spannerpb.Type
		if fieldType != nil && fieldType.ArrayElementType != nil {
			elemType = fieldType.ArrayElementType
		}
		buf.WriteByte('[')
		for i, v := range k.ListValue.Values {
			if i > 0 {
				buf.WriteByte(',')
			}
			writeValueJson(buf, v, elemType)
		}
		buf.WriteByte(']')
	case *structpb.Value_StructValue:
		if k.StructValue == nil {
			buf.WriteString("{}")
			return
		}
		buf.WriteByte('{')
		first := true
		if fieldType != nil && fieldType.StructType != nil {
			for _, f := range fieldType.StructType.Fields {
				if !first {
					buf.WriteByte(',')
				}
				first = false
				jsonEscapeString(buf, f.Name)
				buf.WriteByte(':')
				if v, ok := k.StructValue.Fields[f.Name]; ok {
					writeValueJson(buf, v, f.Type)
				} else {
					buf.WriteString("null")
				}
			}
		} else {
			for fName, fVal := range k.StructValue.Fields {
				if !first {
					buf.WriteByte(',')
				}
				first = false
				jsonEscapeString(buf, fName)
				buf.WriteByte(':')
				writeValueJson(buf, fVal, nil)
			}
		}
		buf.WriteByte('}')
	default:
		buf.WriteString("null")
	}
}

func jsonEscapeString(buf *bytes.Buffer, s string) {
	b, err := json.Marshal(s)
	if err == nil {
		buf.Write(b)
	} else {
		buf.WriteString(`""`)
	}
}

// mergeProtoValues recursively merges chunked Protobuf values across streaming chunks,
// matching Rust's merge_proto_values implementation.
func mergeProtoValues(head *structpb.Value, tail *structpb.Value) *structpb.Value {
	if head == nil {
		return tail
	}
	if tail == nil {
		return head
	}

	switch h := head.Kind.(type) {
	case *structpb.Value_StringValue:
		if t, ok := tail.Kind.(*structpb.Value_StringValue); ok {
			h.StringValue += t.StringValue
		}
	case *structpb.Value_ListValue:
		if t, ok := tail.Kind.(*structpb.Value_ListValue); ok {
			if h.ListValue == nil {
				head.Kind = tail.Kind
				return head
			}
			if t.ListValue == nil {
				return head
			}
			if len(h.ListValue.Values) > 0 && len(t.ListValue.Values) > 0 {
				lastIdx := len(h.ListValue.Values) - 1
				merged := mergeProtoValues(h.ListValue.Values[lastIdx], t.ListValue.Values[0])
				h.ListValue.Values[lastIdx] = merged
				h.ListValue.Values = append(h.ListValue.Values, t.ListValue.Values[1:]...)
			} else {
				h.ListValue.Values = append(h.ListValue.Values, t.ListValue.Values...)
			}
		}
	case *structpb.Value_StructValue:
		if t, ok := tail.Kind.(*structpb.Value_StructValue); ok {
			if h.StructValue == nil {
				head.Kind = tail.Kind
				return head
			}
			if t.StructValue == nil {
				return head
			}
			if h.StructValue.Fields == nil {
				h.StructValue.Fields = make(map[string]*structpb.Value)
			}
			for k, v := range t.StructValue.Fields {
				if existing, exists := h.StructValue.Fields[k]; exists {
					h.StructValue.Fields[k] = mergeProtoValues(existing, v)
				} else {
					h.StructValue.Fields[k] = v
				}
			}
		}
	}
	return head
}
