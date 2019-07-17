# This makefile builds the protos needed for cross-language Firestore tests.

# Assume protoc is on the path. The proto compiler must be one that
# supports proto3 syntax.
PROTOC = protoc

# Dependent repos.
REPO_DIR=$(HOME)/git-repos
PROTOBUF_REPO = $(REPO_DIR)/protobuf
GOOGLEAPIS_REPO = $(REPO_DIR)/googleapis

TMPDIR = /tmp/cloud-audit-proto
TMPDIR_FS = $(TMPDIR)/google/cloud/audit/proto

.PHONY: sync-protos gen-protos

gen-protos: sync-protos tweak-protos
	# TODO(jba): Put the generated proto somewhere more suitable.
	$(PROTOC) --python_out=. \
		-I $(TMPDIR) \
		-I $(PROTOBUF_REPO)/src \
		-I $(GOOGLEAPIS_REPO) \
		$(TMPDIR_FS)/*.proto
	nox -e blacken

tweak-protos:
	mkdir -p $(TMPDIR_FS)
	cp $(GOOGLEAPIS_REPO)/google/cloud/audit/*.proto $(TMPDIR_FS)

sync-protos:
	cd $(PROTOBUF_REPO); git pull
	cd $(GOOGLEAPIS_REPO); git pull
