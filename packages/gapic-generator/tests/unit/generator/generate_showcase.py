import argparse
import os
from pathlib import Path
import yaml
from google.protobuf import descriptor_pb2
from gapic.schema.api import API
from gapic.generator import Generator
from gapic.utils import Options


def main():
    parser = argparse.ArgumentParser(description="Generate Showcase code to disk for coverage and unit testing.")
    parser.add_argument("--variant", required=True, help="Name of the config variant to generate")
    parser.add_argument("--descriptor", required=True, help="Path to the compiled Showcase descriptor set")
    parser.add_argument("--output-dir", required=True, help="Output directory to write generated files to")
    args = parser.parse_args()

    # Load configuration
    config_file_path = Path(__file__).parent / "coverage_configs.yaml"
    with open(config_file_path, "r") as f:
        data = yaml.safe_load(f)
    
    configs = data.get("configs", {})
    if args.variant not in configs:
        raise ValueError(f"Variant '{args.variant}' not found in coverage_configs.yaml")
    
    config = configs[args.variant]
    desc_path = Path(args.descriptor)
    if not desc_path.exists():
        raise FileNotFoundError(f"Descriptor file not found: {desc_path.absolute()}")

    # Parse descriptor set
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

    if res.error:
        raise RuntimeError(f"Generator returned an error: {res.error}")

    # Write files to disk
    output_path = Path(args.output_dir)
    for f in res.file:
        file_path = output_path / f.name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(f.content)
    
    print(f"Successfully generated {len(res.file)} files to {output_path.absolute()}")


if __name__ == "__main__":
    main()
