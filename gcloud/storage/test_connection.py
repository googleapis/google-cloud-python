import unittest2

from gcloud.storage.connection import Connection


class TestConnection(unittest2.TestCase):

  def test_init(self):
    connection = Connection('project-name')
    self.assertEqual('project-name', connection.project_name)
