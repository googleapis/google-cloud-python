# This makefile builds the protos needed for cross-language Firestore tests.

# Assume protoc is on the path. The proto compiler must be one that
# supports proto3 syntax.
PROTOC = protoc

# Dependent repos.
PROTOBUF_REPO = $(HOME)/git-repos/protobuf
GOOGLEAPIS_REPO = $(HOME)/git-repos/googleapis

TESTS_REPO = $(HOME)/git-repos/gcp/google-cloud-common

TMPDIR = /tmp/python-fs-proto
TMPDIR_FS = $(TMPDIR)/google/cloud/firestore_v1beta1/proto

.PHONY: sync-protos gen-protos

gen-protos: sync-protos tweak-protos
	# TODO(jba): Put the generated proto somewhere more suitable.
	$(PROTOC) --python_out=google/cloud/firestore_v1beta1/proto \
		-I $(TMPDIR) \
		-I $(PROTOBUF_REPO)/src \
		-I $(GOOGLEAPIS_REPO) \
		$(TMPDIR)/*.proto

tweak-protos:
	mkdir -p $(TMPDIR_FS)
	cp $(GOOGLEAPIS_REPO)/google/firestore/v1beta1/*.proto $(TMPDIR_FS)
	sed -i -e 's@google/firestore/v1beta1@google/cloud/firestore_v1beta1/proto@' $(TMPDIR_FS)/*.proto
	cp $(TESTS_REPO)/testing/firestore/proto/*.proto $(TMPDIR)
	sed -i -e 's@google/firestore/v1beta1@google/cloud/firestore_v1beta1/proto@' $(TMPDIR)/*.proto

sync-protos:
	cd $(PROTOBUF_REPO); git pull
	cd $(GOOGLEAPIS_REPO); git pull
	cd $(TESTS_REPO); git pull
