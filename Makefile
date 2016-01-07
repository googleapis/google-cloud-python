GENERATED_DIR=$(shell pwd)/generated_python
FINAL_DIR=$(shell pwd)/gcloud/bigtable/_generated
GRPC_PLUGIN=grpc_python_plugin
PROTOC_CMD=protoc
PROTOS_DIR=$(shell pwd)/cloud-bigtable-client/bigtable-protos/src/main/proto

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
	# Generate all *_pb2.py files that require gRPC.
	$(PROTOC_CMD) \
	    --proto_path=$(PROTOS_DIR) \
	    --python_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    --grpc_out=$(GENERATED_DIR) \
	    $(PROTOS_DIR)/google/bigtable/v1/bigtable_service.proto \
	    $(PROTOS_DIR)/google/bigtable/admin/cluster/v1/bigtable_cluster_service.proto \
	    $(PROTOS_DIR)/google/bigtable/admin/table/v1/bigtable_table_service.proto
	# Generate all *_pb2.py files that do not require gRPC.
	$(PROTOC_CMD) \
	    --proto_path=$(PROTOS_DIR) \
	    --python_out=$(GENERATED_DIR) \
	    $(PROTOS_DIR)/google/bigtable/v1/bigtable_data.proto \
	    $(PROTOS_DIR)/google/bigtable/v1/bigtable_service_messages.proto \
	    $(PROTOS_DIR)/google/bigtable/admin/cluster/v1/bigtable_cluster_data.proto \
	    $(PROTOS_DIR)/google/bigtable/admin/cluster/v1/bigtable_cluster_service_messages.proto \
	    $(PROTOS_DIR)/google/bigtable/admin/table/v1/bigtable_table_data.proto \
	    $(PROTOS_DIR)/google/bigtable/admin/table/v1/bigtable_table_service_messages.proto
	# Move the newly generated *_pb2.py files into our library.
	mv $(GENERATED_DIR)/google/bigtable/v1/* $(FINAL_DIR)
	mv $(GENERATED_DIR)/google/bigtable/admin/cluster/v1/* $(FINAL_DIR)
	mv $(GENERATED_DIR)/google/bigtable/admin/table/v1/* $(FINAL_DIR)
	# Remove all existing *.proto files before we replace
	rm -f $(FINAL_DIR)/*.proto
	# Copy over the *.proto files into our library.
	cp $(PROTOS_DIR)/google/bigtable/v1/*.proto $(FINAL_DIR)
	cp $(PROTOS_DIR)/google/bigtable/admin/cluster/v1/*.proto $(FINAL_DIR)
	cp $(PROTOS_DIR)/google/bigtable/admin/table/v1/*.proto $(FINAL_DIR)
	cp $(PROTOS_DIR)/google/longrunning/operations.proto $(FINAL_DIR)
	# Rename all *.proto files in our library with an
	# underscore and remove executable bit.
	cd $(FINAL_DIR) && \
	    for filename in *.proto; do \
	        chmod -x $$filename ; \
	        mv $$filename _$$filename ; \
	    done
	# Separate the gRPC parts of the operations service from the
	# non-gRPC parts so that the protos from `googleapis-common-protos`
	# can be used without gRPC.
	python scripts/make_operations_grpc.py
	# Rewrite the imports in the generated *_pb2.py files.
	python scripts/rewrite_imports.py

check_generate:
	python scripts/check_generate.py

clean:
	rm -fr cloud-bigtable-client $(GENERATED_DIR)

.PHONY: generate check_generate clean
