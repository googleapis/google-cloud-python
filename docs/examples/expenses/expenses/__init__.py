import datetime
import os

from gcloud import datastore
from gcloud.datastore.key import Key
from gcloud.datastore.entity import Entity
from gcloud.datastore.query import Query


class DuplicateReport(Exception):
    """Attempt to create a report which already exists."""


class InvalidReport(Exception):
    """Attempt to update / delete an invalide report."""


class NoSuchReport(InvalidReport):
    """Attempt to update / delete a report which does not already exist."""


class BadReportStatus(InvalidReport):
    """Attempt to update / delete an already-approved/rejected report."""


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

def _purge_report_items(dataset, report):
    # Delete any existing items belonging to report
    query = Query('Expense Item', dataset)
    count = 0
    for existing in query.ancestor(report.key()).fetch():
        existing.delete()
        count += 1
    return count

def _upsert_report(dataset, employee_id, report_id, rows):
    employee = get_employee(dataset, employee_id)
    report = get_report(dataset, employee_id, report_id)
    _purge_report_items(dataset, report)
    # Add items based on rows.
    report_path = report.key().path()
    for i, row in enumerate(rows):
        path = report_path + [{'kind': 'Expense Item', 'id': i + 1}]
        key = Key(dataset, path=path)
        item = Entity(dataset, 'Expense Item').key(key)
        for k, v in row.items():
            item[k] = v
        item.save()
    return report

def create_report(employee_id, report_id, rows, description):
    dataset = get_dataset()
    if get_report(dataset, employee_id, report_id, False) is not None:
        raise DuplicateReport()
    with dataset.transaction():
        report = _upsert_report(dataset, employee_id, report_id, rows)
        report['status'] = 'pending'
        if description is not None:
            report['description'] = description
        report['created'] = report['updated'] = datetime.datetime.utcnow()
        report.save()

def update_report(employee_id, report_id, rows, description):
    dataset = get_dataset()
    with dataset.transaction():
        report = get_report(dataset, employee_id, report_id, False)
        if report is None:
            raise InvalidReport()
        if report['status'] != 'pending':
            raise BadReportStatus(report['status'])
        _upsert_report(dataset, employee_id, report_id, rows)
        if description is not None:
            report['description'] = description
        report['updated'] = datetime.datetime.utcnow()

def delete_report(employee_id, report_id):
    dataset = get_dataset()
    report = get_report(dataset, employee_id, report_id, False)
    if report is None:
        raise NoSuchReport()
    if report['status'] != 'pending':
        raise BadReportStatus(report['status'])
    with dataset.transaction():
        count = _purge_report_items(dataset, report)
        report.delete()
    return count
