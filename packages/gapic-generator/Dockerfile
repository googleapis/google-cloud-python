FROM python:3.12-slim

# Install system packages.
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    pandoc \
  && rm -rf /var/lib/apt/lists/*

# Add protoc and our common protos.
COPY --from=gcr.io/gapic-images/api-common-protos:latest /usr/local/bin/protoc /usr/local/bin/protoc
COPY --from=gcr.io/gapic-images/api-common-protos:latest /protos/ /protos/

# Add our code to the Docker image.
ADD . /usr/src/gapic-generator-python/

# Install the tool within the image.
RUN pip install /usr/src/gapic-generator-python

# Define the generator as an entry point.
ENTRYPOINT ["/usr/src/gapic-generator-python/docker-entrypoint.sh"]
