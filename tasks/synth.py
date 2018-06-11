import synthtool as s
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# tasks has two product names, and a poorly named artman yaml
v2beta2_library = gapic._generate_code(
    'tasks', 'v2beta2', 'python',
    config_path='artman_cloudtasks.yaml',
    artman_output_name='cloud-tasks-v2beta2')

s.copy(v2beta2_library)

# Set Release Status
release_status = 'Development Status :: 3 - Alpha'
s.replace('setup.py',
          '(release_status = )(.*)$',
          f"\\1'{release_status}'")

# Add Dependencies
s.replace('setup.py',
          'dependencies = \[\n*(^.*,\n)+',
          "\\g<0>    'grpc-google-iam-v1<0.12dev,>=0.11.4',\n")

# Correct Naming of package
s.replace('**/*.rst',
          'google-cloud-cloud-tasks',
          'google-cloud-tasks')
s.replace('**/*.py',
          'google-cloud-cloud-tasks',
          'google-cloud-tasks')
s.replace('README.rst',
          '/cloud-tasks',
          '/tasks')

# Correct calls to routing_header
# https://github.com/googleapis/gapic-generator/issues/2016
s.replace(
    "google/cloud/*/gapic/*_client.py",
    "routing_header\(",
    "routing_header.to_grpc_metadata(")

# metadata in tests in none but should be empty list.
# https://github.com/googleapis/gapic-generator/issues/2014
s.replace(
    "google/cloud/*/gapic/*_client.py",
    'def .*\(([^\)]+)\n.*metadata=None\):\n\s+"""(.*\n)*?\s+"""\n',
    '\g<0>'
    '        if metadata is None:\n'
    '            metadata = []\n'
    '        metadata = list(metadata)\n')


# empty objects trying to get attrs
# https://github.com/googleapis/gapic-generator/issues/2015
s.replace(
    "google/cloud/*/gapic/*_client.py",
    "(^        )(routing_header = google.api_core.gapic_v1.routing_header"
    ".to_grpc_metadata\(\n)"
    "(\s+)(\[\('[a-z\_]*?\.name', )([a-z\_]*?)(.name\)\], \)\n)"
    "(\s+metadata.append\(routing_header\)\n)",
    "\g<1>if hasattr(\g<5>, 'name'):\n"
    "\g<1>    \g<2>\g<3>    \g<4>\g<5>\g<6>    \g<7>"
)
