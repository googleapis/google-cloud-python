import os
import pytest
from google.protobuf import descriptor_pb2
from gapic.schema.api import API
from gapic.generator import Generator
from gapic.utils import Options

DESC_FILES = {
    os.environ.get("SHOWCASE_DESC_PATH", "/tmp/showcase.desc"): {
        "package": "google.showcase.v1beta1",
        "opts": "transport=grpc+rest,service-yaml=tests/integration/showcase_v1beta1.yaml,add-iam-methods=true,samples=tests/integration/showcase_samples.yaml,rest-async-io-enabled=true"
    },
}

@pytest.mark.parametrize("desc_path,config", DESC_FILES.items())
def test_render_goldens_for_coverage(desc_path, config):
    """
    This test parses the pre-compiled FileDescriptorSets for multiple goldens
    and runs the Generator over them to achieve high template coverage upstream.
    """
    if not os.path.exists(desc_path):
        pytest.skip(f"Descriptor not found: {desc_path}")
    
    with open(desc_path, "rb") as f:
        fds = descriptor_pb2.FileDescriptorSet.FromString(f.read())
    
    opts = Options.build(config["opts"])
    api_schema = API.build(fds.file, package=config["package"], opts=opts)
    
    generator = Generator(opts)
    res = generator.get_response(api_schema=api_schema, opts=opts)
    assert len(res.file) > 0
