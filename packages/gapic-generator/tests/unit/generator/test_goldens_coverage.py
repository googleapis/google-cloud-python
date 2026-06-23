import os
from pathlib import Path
from typing import Any, Dict, List
import yaml
import pytest
from google.protobuf import descriptor_pb2
from gapic.schema.api import API
from gapic.generator import Generator
from gapic.utils import Options


def load_test_configs() -> Dict[str, Dict[str, Any]]:
    """Loads declarative test configurations from a YAML manifest.

    Allows developers to specify another configuration or proto set by defining
    COVERAGE_CONFIGS_FILE environment variable pointing to their custom YAML manifest.
    """
    default_config_path = Path(__file__).parent / "coverage_configs.yaml"
    config_file_path = os.environ.get("COVERAGE_CONFIGS_FILE", str(default_config_path))
    
    config_path = Path(config_file_path)
    if not config_path.exists():
        pytest.fail(f"Test configs manifest not found at: {config_path.absolute()}")

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
    
    return data.get("configs", {})


CONFIGS = load_test_configs()


@pytest.mark.parametrize("config_name,config", CONFIGS.items())
def test_render_goldens_for_coverage(config_name: str, config: Dict[str, Any]) -> None:
    """Validate that pre-compiled FileDescriptorSets are correctly parsed and rendered.

    This test runs the Generator over configured descriptor sets to ensure high
    template coverage upstream and verifies that all expected core files are produced.
    """
    # Dynamically resolve the descriptor path at test execution time.
    desc_path_str = os.environ.get(config.get("env_var", "SHOWCASE_DESC_PATH"), config.get("default_path", "/tmp/showcase.desc"))
    desc_path = Path(desc_path_str)

    if not desc_path.exists():
        pytest.fail(
            f"Required descriptor file not found: {desc_path.absolute()}\n"
            f"Ensure SHOWCASE_DESC_PATH or config env_var is set correctly."
        )


    # Parse the FileDescriptorSet
    fds = descriptor_pb2.FileDescriptorSet.FromString(desc_path.read_bytes())
    
    exclude_files = config.get("exclude_files", [])
    files_to_build = [
        f for f in fds.file
        if not any(excluded in f.name for excluded in exclude_files)
    ]

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
