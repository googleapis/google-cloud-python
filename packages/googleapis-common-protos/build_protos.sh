

#!/bin/bash
set -e

# 3.20.2 is the lower version of protoc for protobuf 3.x which is supported
# https://protobuf.dev/support/version-support/#python
rm -rf google/api/*pb2.py*
rm -rf google/api/protobuf3/*pb2.py*
rm -rf protoc-20

wget https://github.com/protocolbuffers/protobuf/releases/download/v3.20.2/protoc-3.20.2-linux-x86_64.zip --backups=1
unzip protoc-3.20.2-linux-x86_64.zip -d protoc-20
protoc-20/bin/protoc --version

# Generates the *.py files from the protos.
for proto_name in google/api/*.proto
do
    dir_name=$(echo $proto_name | sed 's@\/[^/]*$@@')
    protoc-20/bin/protoc \
    --proto_path=. \
    --python_out=. \
    --pyi_out=. \
    $proto_name
done

for proto_name in google/api/*pb2.py*
do
    mv $proto_name google/api/protobuf3
done


# 22.0 is the lower version of protoc for protobuf 4.x
# https://protobuf.dev/support/version-support/#python
rm -rf google/api/*pb2.py*
rm -rf google/api/protobuf4/*pb2.py*
rm -rf protoc-22

wget https://github.com/protocolbuffers/protobuf/releases/download/v22.0/protoc-22.0-linux-x86_64.zip --backups=1
unzip protoc-22.0-linux-x86_64.zip -d protoc-22
protoc-22/bin/protoc --version

# Generates the *.py files from the protos.
for proto_name in google/api/*.proto
do
    dir_name=$(echo $proto_name | sed 's@\/[^/]*$@@')
    protoc-22/bin/protoc \
    --proto_path=. \
    --python_out=. \
    --pyi_out=. \
    $proto_name
done

for proto_name in google/api/*pb2.py*
do
    mv $proto_name google/api/protobuf4
done




# 26.0 is the lower version of protoc for protobuf 5.x
# https://protobuf.dev/support/version-support/#python
rm -rf google/api/*pb2.py*
rm -rf google/api/protobuf5/*pb2.py*
rm -rf protoc-26

wget https://github.com/protocolbuffers/protobuf/releases/download/v26.0/protoc-26.0-linux-x86_64.zip --backups=1
unzip protoc-26.0-linux-x86_64.zip -d protoc-26
protoc-26/bin/protoc --version

# Generates the *.py files from the protos.
for proto_name in google/api/*.proto
do
    dir_name=$(echo $proto_name | sed 's@\/[^/]*$@@')
    protoc-26/bin/protoc \
    --proto_path=. \
    --python_out=. \
    --pyi_out=. \
    $proto_name
done

for proto_name in google/api/*pb2.py*
do
    mv $proto_name google/api/protobuf5
done



# 30.0 is the lower version of protoc for protobuf 6.x
# https://protobuf.dev/support/version-support/#python
rm -rf google/api/*pb2.py*
rm -rf google/api/protobuf6/*pb2.py*
rm -rf protoc-30

wget https://github.com/protocolbuffers/protobuf/releases/download/v30.0/protoc-30.0-linux-x86_64.zip --backups=1
unzip protoc-30.0-linux-x86_64.zip -d protoc-30
protoc-30/bin/protoc --version

# Generates the *.py files from the protos.
for proto_name in google/api/*.proto
do
    dir_name=$(echo $proto_name | sed 's@\/[^/]*$@@')
    protoc-30/bin/protoc \
    --proto_path=. \
    --python_out=. \
    --pyi_out=. \
    $proto_name
done

for proto_name in google/api/*pb2.py*
do
    mv $proto_name google/api/protobuf6
done


