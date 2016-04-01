GENERATED_DIR=$(shell pwd)/generated_python
BIGTABLE_DIR=$(shell pwd)/gcloud/bigtable/_generated
DATASTORE_DIR=$(shell pwd)/gcloud/datastore/_generated
GRPC_PLUGIN=grpc_python_plugin
PROTOC_CMD=protoc
BIGTABLE_PROTOS_DIR=$(shell pwd)/cloud-bigtable-client/bigtable-protos/src/main/proto
GOOGLEAPIS_PROTOS_DIR=$(shell pwd)/googleapis-pb

help:
	@echo 'Makefile for gcloud-python Bigtable protos                      '
	@echo '                                                                '
	@echo '   make generate                 Generates the protobuf modules '
	@echo '   make check_generate           Checks that generate succeeded '
	@echo '   make clean                    Clean generated files          '

generate:
	# Retrieve git repos that have our *.proto files.
	[ -d cloud-bigtable-client ] || git clone https://github.com/GoogleCloudPlatform/cloud-bigtable-client --depth=1
	cd cloud-bigtable-client && git pull origin master
	[ -d googleapis-pb ] || git clone https://github.com/google/googleapis googleapis-pb --depth=1
	cd googleapis-pb && git pull origin master
	# Make the directory where our *_pb2.py files will go.
	mkdir -p $(GENERATED_DIR)
	# Generate all *_pb2.py files that require gRPC.
	$(PROTOC_CMD) \
	    --proto_path=$(BIGTABLE_PROTOS_DIR) \
	    --python_out=$(GENERATED_DIR) \
	    --plugin=protoc-gen-grpc=$(GRPC_PLUGIN) \
	    --grpc_out=$(GENERATED_DIR) \
	    $(BIGTABLE_PROTOS_DIR)/google/bigtable/v1/bigtable_service.proto \
	    $(BIGTABLE_PROTOS_DIR)/google/bigtable/admin/cluster/v1/bigtable_cluster_service.proto \
	    $(BIGTABLE_PROTOS_DIR)/google/bigtable/admin/table/v1/bigtable_table_service.proto
	# Generate all *_pb2.py files that do not require gRPC.
	$(PROTOC_CMD) \
	    --proto_path=$(BIGTABLE_PROTOS_DIR) \
	    --proto_path=$(GOOGLEAPIS_PROTOS_DIR) \
	    --python_out=$(GENERATED_DIR) \
	    $(BIGTABLE_PROTOS_DIR)/google/bigtable/v1/bigtable_data.proto \
	    $(BIGTABLE_PROTOS_DIR)/google/bigtable/v1/bigtable_service_messages.proto \
	    $(BIGTABLE_PROTOS_DIR)/google/bigtable/admin/cluster/v1/bigtable_cluster_data.proto \
	    $(BIGTABLE_PROTOS_DIR)/google/bigtable/admin/cluster/v1/bigtable_cluster_service_messages.proto \
	    $(BIGTABLE_PROTOS_DIR)/google/bigtable/admin/table/v1/bigtable_table_data.proto \
	    $(BIGTABLE_PROTOS_DIR)/google/bigtable/admin/table/v1/bigtable_table_service_messages.proto \
	    $(GOOGLEAPIS_PROTOS_DIR)/google/datastore/v1beta3/datastore.proto \
	    $(GOOGLEAPIS_PROTOS_DIR)/google/datastore/v1beta3/entity.proto \
	    $(GOOGLEAPIS_PROTOS_DIR)/google/datastore/v1beta3/query.proto
	# Move the newly generated *_pb2.py files into our library.
	mv $(GENERATED_DIR)/google/bigtable/v1/* $(BIGTABLE_DIR)
	mv $(GENERATED_DIR)/google/bigtable/admin/cluster/v1/* $(BIGTABLE_DIR)
	mv $(GENERATED_DIR)/google/bigtable/admin/table/v1/* $(BIGTABLE_DIR)
	mv $(GENERATED_DIR)/google/datastore/v1beta3/* $(DATASTORE_DIR)
	# Remove all existing *.proto files before we replace
	rm -f $(BIGTABLE_DIR)/*.proto
	rm -f $(DATASTORE_DIR)/*.proto
	# Copy over the *.proto files into our library.
	cp $(BIGTABLE_PROTOS_DIR)/google/bigtable/v1/*.proto $(BIGTABLE_DIR)
	cp $(BIGTABLE_PROTOS_DIR)/google/bigtable/admin/cluster/v1/*.proto $(BIGTABLE_DIR)
	cp $(BIGTABLE_PROTOS_DIR)/google/bigtable/admin/table/v1/*.proto $(BIGTABLE_DIR)
	cp $(BIGTABLE_PROTOS_DIR)/google/longrunning/operations.proto $(BIGTABLE_DIR)
	cp $(GOOGLEAPIS_PROTOS_DIR)/google/datastore/v1beta3/*.proto $(DATASTORE_DIR)
	# Rename all *.proto files in our library with an
	# underscore and remove executable bit.
	cd $(BIGTABLE_DIR) && \
	    for filename in *.proto; do \
	        chmod -x $$filename ; \
	        mv $$filename _$$filename ; \
	    done
	cd $(DATASTORE_DIR) && \
	    for filename in *.proto; do \
	        chmod -x $$filename ; \
	        mv $$filename _$$filename ; \
	    done
	# Separate the gRPC parts of the operations service from the
	# non-gRPC parts so that the protos from `googleapis-common-protos`
	# can be used without gRPC.
	python scripts/make_operations_grpc.py
	# Separate the gRPC parts of the datastore service from the
	# non-gRPC parts so that the protos can be used without gRPC.
	python scripts/make_datastore_grpc.py
	# Rewrite the imports in the generated *_pb2.py files.
	python scripts/rewrite_imports.py

check_generate:
	python scripts/check_generate.py

clean:
	rm -fr cloud-bigtable-client $(GENERATED_DIR)

.PHONY: generate check_generate clean
