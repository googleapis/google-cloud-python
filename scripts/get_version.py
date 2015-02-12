"""Simple script to get the gcloud version."""
from pkg_resources import get_distribution
print get_distribution('gcloud').version
