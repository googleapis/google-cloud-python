# package
import os

from gcloud import datastore
from gcloud.datastore.key import Key
from gcloud.datastore.entity import Entity
from gcloud.datastore.query import Query


class DuplicateReport(Exception):
    """Attempt to create a report which already exists."""


class InvalidReport(Exception):
    """Attempt to update a report which does not already exist."""


def get_dataset():
    client_email = os.environ['GCLOUD_TESTS_CLIENT_EMAIL']
    private_key_path = os.environ['GCLOUD_TESTS_KEY_FILE']
    dataset_id = os.environ['GCLOUD_TESTS_DATASET_ID']
    conn = datastore.get_connection(client_email, private_key_path)
    return conn.dataset(dataset_id)

def get_employee(dataset, employee_id, create=True):
    key = Key(dataset, path=[{'kind': 'Employee', 'name': employee_id}])
    employee = dataset.get_entity(key)
    if employee is None and create:
        employee = dataset.entity('Employee').key(key)
        employee.save()
    return employee

def get_report(dataset, employee_id, report_id, create=True):
    key = Key(dataset,
              path=[{'kind': 'Employee', 'name': employee_id},
                    {'kind': 'Expense Report', 'name': report_id},
                   ])
    report = dataset.get_entity(key)
    if report is None and create:
        report = dataset.entity('Report').key(key)
        report.save()
    return report

def _upsert_report(dataset, employee_id, report_id, rows):
    with dataset.transaction():
        employee = get_employee(dataset, employee_id)
        report = get_report(dataset, employee_id, report_id)
        query = Query('Expense Item', dataset)
        # Delete any existing items.
        for existing in query.ancestor(report.key()).fetch():
            existing.delete()
        # Add items based on rows.
        report_path = report.key().path()
        for i, row in enumerate(rows):
            path = report_path + [{'kind': 'Expense Item', 'id': i + 1}]
            key = Key(dataset, path=path)
            item = Entity(dataset, 'Expense Item').key(key)
            for k, v in row.items():
                item[k] = v
            item.save()

def create_report(employee_id, report_id, rows):
    dataset = get_dataset()
    if get_report(dataset, employee_id, report_id, False) is not None:
        raise DuplicateReport()
    _upsert_report(dataset, employee_id, report_id, rows)

def update_report(employee_id, report_id, rows):
    dataset = get_dataset()
    if get_report(dataset, employee_id, report_id, False) is None:
        raise InvalidReport()
    _upsert_report(dataset, employee_id, report_id, rows)
