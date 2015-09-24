GENERATED_DIR=$(shell pwd)/generated_python
FINAL_DIR=gcloud/bigtable/_generated
BREW_PREFIX=$(shell brew --prefix)
LD_LIBRARY_PATH=$(BREW_PREFIX)/lib
GRPC_PLUGIN=$(BREW_PREFIX)/bin/grpc_python_plugin

help:
	@echo 'Makefile for gcloud-python Bigtable protos                      '
	@echo '                                                                '
	@echo '   make generate                 Generates the protobuf modules '
	@echo '   make check_generate           Checks that generate succeeded '
	@echo '   make clean                    Clean generated files          '

generate:
	[ -d cloud-bigtable-client ] || git clone https://github.com/GoogleCloudPlatform/cloud-bigtable-client
	cd cloud-bigtable-client && git pull origin master
	mkdir -p $(GENERATED_DIR)
	# Data API
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) google/bigtable/v1/*.proto
	mv $(GENERATED_DIR)/google/bigtable/v1/* $(FINAL_DIR)
	# Cluster API
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    google/bigtable/admin/cluster/v1/*.proto
	mv $(GENERATED_DIR)/google/bigtable/admin/cluster/v1/* $(FINAL_DIR)
	# Table API
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    google/bigtable/admin/table/v1/*.proto
	mv $(GENERATED_DIR)/google/bigtable/admin/table/v1/* $(FINAL_DIR)
	# Auxiliary protos
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    google/api/*.proto
	mv $(GENERATED_DIR)/google/api/* $(FINAL_DIR)
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    google/protobuf/any.proto
	mv $(GENERATED_DIR)/google/protobuf/any_pb2.py $(FINAL_DIR)
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    google/protobuf/duration.proto
	mv $(GENERATED_DIR)/google/protobuf/duration_pb2.py $(FINAL_DIR)
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    google/protobuf/empty.proto
	mv $(GENERATED_DIR)/google/protobuf/empty_pb2.py $(FINAL_DIR)
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    google/protobuf/timestamp.proto
	mv $(GENERATED_DIR)/google/protobuf/timestamp_pb2.py $(FINAL_DIR)
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    google/longrunning/operations.proto
	mv $(GENERATED_DIR)/google/longrunning/operations_pb2.py $(FINAL_DIR)
	cd cloud-bigtable-client/bigtable-protos/src/main/proto && \
	    protoc --python_out=$(GENERATED_DIR) --grpc_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    google/rpc/status.proto
	mv $(GENERATED_DIR)/google/rpc/status_pb2.py $(FINAL_DIR)
	python scripts/rewrite_imports.py

check_generate:
	python scripts/check_generate.py

clean:
	rm -fr cloud-bigtable-client $(GENERATED_DIR)

.PHONY: generate check_generate clean
