"""Module to provide implicit behavior based on enviroment.

Acts as a mutable namespace to allow the datastore package to
imply the current dataset and connection from the enviroment.
"""


DATASET_ID = None
"""Module global to allow persistent implied dataset ID from enviroment."""

DATASET = None
"""Module global to allow persistent implied dataset from enviroment."""

CONNECTION = None
"""Module global to allow persistent implied connection from enviroment."""
