import os
from pathlib import Path
from typing import Any, Dict
import pytest
from google.protobuf import descriptor_pb2
from gapic.schema.api import API
from gapic.generator import Generator
from gapic.utils import Options


CUSTOM_YAML = """type: google.api.Service
config_version: 3
name: localhost
title: Showcase API

apis:
- name: google.showcase.v1beta1.Echo
- name: google.iam.v1.IAMPolicy
- name: google.cloud.location.Locations
- name: google.longrunning.Operations

http:
  rules:
  - selector: google.cloud.location.Locations.GetLocation
    get: '/v1beta1/{name=projects/*/locations/*}'
  - selector: google.cloud.location.Locations.ListLocations
    get: '/v1beta1/{name=projects/*}/locations'
  - selector: google.iam.v1.IAMPolicy.GetIamPolicy
    get: '/v1beta1/{resource=projects/*/locations/*/triggers/*}:getIamPolicy'
  - selector: google.iam.v1.IAMPolicy.SetIamPolicy
    post: '/v1beta1/{resource=projects/*/locations/*/triggers/*}:setIamPolicy'
    body: '*'
  - selector: google.iam.v1.IAMPolicy.TestIamPermissions
    post: '/v1beta1/{resource=projects/*/locations/*/triggers/*}:testIamPermissions'
    body: '*'
"""

# Define configuration metadata without binding the exact runtime path at import time.
CONFIGS: Dict[str, Dict[str, Any]] = {
    "showcase": {
        "env_var": "SHOWCASE_DESC_PATH",
        "default_path": "/tmp/showcase.desc",
        "package": "google.showcase.v1beta1",
        "opts": "transport=grpc+rest,service-yaml=tests/integration/showcase_v1beta1.yaml,add-iam-methods=true,samples=tests/integration/showcase_samples.yaml,rest-async-io-enabled=true",
        "use_retry": True,
        "expected_file_keywords": [
            "client.py",
            "async_client.py",
            "pagers.py",
            "transports",
        ],
    },
    "showcase_retry_snippets": {
        "env_var": "SHOWCASE_DESC_PATH",
        "default_path": "/tmp/showcase.desc",
        "package": "google.showcase.v1beta1",
        "opts": "transport=grpc+rest,service-yaml=tests/integration/showcase_v1beta1.yaml,add-iam-methods=true,autogen-snippets=true,rest-async-io-enabled=true",
        "use_retry": True,
        "expected_file_keywords": [
            "client.py",
            "async_client.py",
            "pagers.py",
            "transports",
        ],
    },
    "showcase_no_iam_no_rest_async": {
        "env_var": "SHOWCASE_DESC_PATH",
        "default_path": "/tmp/showcase.desc",
        "package": "google.showcase.v1beta1",
        "opts": "transport=grpc+rest,service-yaml=/tmp/showcase_no_iam_no_rest_async.yaml,add-iam-methods=false,rest-async-io-enabled=false",
        "use_retry": True,
        "exclude_identity": True,
        "custom_yaml": CUSTOM_YAML,
        "expected_file_keywords": [
            "client.py",
            "pagers.py",
            "transports",
        ],
    },
    "showcase_pure_grpc": {
        "env_var": "SHOWCASE_DESC_PATH",
        "default_path": "/tmp/showcase.desc",
        "package": "google.showcase.v1beta1",
        "opts": "transport=grpc,service-yaml=tests/integration/showcase_v1beta1.yaml,add-iam-methods=false",
        "use_retry": True,
        "expected_file_keywords": [
            "client.py",
            "transports",
        ],
    },
}


@pytest.mark.parametrize("config_name,config", CONFIGS.items())
def test_render_goldens_for_coverage(config_name: str, config: Dict[str, Any]) -> None:
    """Validate that pre-compiled FileDescriptorSets are correctly parsed and rendered.

    This test runs the Generator over configured descriptor sets to ensure high
    template coverage upstream and verifies that all expected core files are produced.
    """
    # Dynamically resolve the descriptor path at test execution time.
    desc_path_str = os.environ.get(config["env_var"], config["default_path"])
    desc_path = Path(desc_path_str)

    if not desc_path.exists():
        pytest.fail(
            f"Required descriptor file not found: {desc_path.absolute()}\n"
            f"Ensure {config['env_var']} is set or compile the descriptor set before running this test."
        )

    if config.get("custom_yaml"):
        Path("/tmp/showcase_no_iam_no_rest_async.yaml").write_text(config["custom_yaml"])

    # Parse the FileDescriptorSet
    fds = descriptor_pb2.FileDescriptorSet.FromString(desc_path.read_bytes())
    files_to_build = [f for f in fds.file if not config.get("exclude_identity") or "identity.proto" not in f.name]

    opts_str = config["opts"]
    if config.get("use_retry"):
        retry_path = os.environ.get("SHOWCASE_GRPC_SERVICE_CONFIG", "/tmp/showcase_grpc_service_config.json")
        if os.path.exists(retry_path):
            opts_str += f",retry-config={retry_path}"

    opts = Options.build(opts_str)
    api_schema = API.build(files_to_build, package=config["package"], opts=opts)

    generator = Generator(opts)
    res = generator.get_response(api_schema=api_schema, opts=opts)

    # Validate the CodeGeneratorResponse
    assert not res.error, f"Generator returned an error: {res.error}"
    assert len(res.file) > 0, "Generator failed to produce any files."

    # Perform structural validation to ensure core client components were generated
    generated_filenames = {f.name for f in res.file}
    for keyword in config["expected_file_keywords"]:
        assert any(keyword in filename for filename in generated_filenames), (
            f"Expected file matching '{keyword}' was not generated.\n"
            f"Generated files: {sorted(generated_filenames)}"
        )

    # Ensure none of the generated files are completely empty
    for generated_file in res.file:
        assert generated_file.content.strip(), f"Generated file '{generated_file.name}' is empty."
