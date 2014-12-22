"""Module to provide implicit behavior based on enviroment.

Acts as a mutable namespace to allow the datastore package to
imply the current dataset from the enviroment.

Also provides a base class for classes in the `datastore` package
which could utilize the implicit enviroment.
"""


DATASET = None
"""Module global to allow persistent implied dataset from enviroment."""


class _DatastoreBase(object):
    """Base for all classes in the datastore package.

    Uses the implicit DATASET object as a default dataset attached
    to the instances being created. Stores the dataset passed in
    on the protected (i.e. non-public) attribute `_dataset`.
    """

    def __init__(self, dataset=None):
        self._dataset = dataset or DATASET
