import datetime
import os

from gcloud import datastore
from gcloud.datastore.key import Key
from gcloud.datastore.entity import Entity
from gcloud.datastore.query import Query


class DuplicateReport(Exception):
    """Attempt to create a report which already exists."""


class NoSuchReport(Exception):
    """Attempt to update / delete a report which does not already exist."""


class BadReportStatus(Exception):
    """Attempt to update / delete an already-approved/rejected report."""


def _get_dataset():
    client_email = os.environ['GCLOUD_TESTS_CLIENT_EMAIL']
    private_key_path = os.environ['GCLOUD_TESTS_KEY_FILE']
    dataset_id = os.environ['GCLOUD_TESTS_DATASET_ID']
    return datastore.get_dataset(dataset_id, client_email, private_key_path)


def _get_employee(dataset, employee_id, create=True):
    key = Key(path=[
        {'kind': 'Employee', 'name': employee_id},
        ])
    employee = dataset.get_entity(key)
    if employee is None and create:
        employee = dataset.entity('Employee').key(key)
        employee.save()
    return employee


def _get_report(dataset, employee_id, report_id, create=True):
    key = Key(path=[
        {'kind': 'Employee', 'name': employee_id},
        {'kind': 'Expense Report', 'name': report_id},
        ])
    report = dataset.get_entity(key)
    if report is None and create:
        report = dataset.entity('Report').key(key)
        report.save()
    return report


def _fetch_report_items(dataset, report):
    query = Query('Expense Item', dataset)
    for item in query.ancestor(report.key()).fetch():
        yield item


def _report_info(report):
    path = report.key().path()
    employee_id = path[0]['name']
    report_id = path[1]['name']
    created = report['created'].strftime('%Y-%m-%d')
    updated = report['updated'].strftime('%Y-%m-%d')
    status = report['status']
    if status == 'paid':
        memo = report['check_number']
    elif status == 'rejected':
        memo = report['rejected_reason']
    else:
        memo = ''
    return {
        'employee_id': employee_id,
        'report_id': report_id,
        'created': created,
        'updated': updated,
        'status': status,
        'description': report.get('description', ''),
        'memo': memo,
        }


def _purge_report_items(dataset, report):
    # Delete any existing items belonging to report
    count = 0
    for item in _fetch_report_items(dataset, report):
        item.delete()
        count += 1
    return count


def _upsert_report(dataset, employee_id, report_id, rows):
    _get_employee(dataset, employee_id)  # force existence
    report = _get_report(dataset, employee_id, report_id)
    _purge_report_items(dataset, report)
    # Add items based on rows.
    report_path = report.key().path()
    for i, row in enumerate(rows):
        path = report_path + [{'kind': 'Expense Item', 'id': i + 1}]
        key = Key(path=path)
        item = Entity(dataset, 'Expense Item').key(key)
        for k, v in row.items():
            item[k] = v
        item.save()
    return report


def list_reports(employee_id=None, status=None):
    dataset = _get_dataset()
    query = Query('Expense Report', dataset)
    if employee_id is not None:
        key = Key(path=[{'kind': 'Employee', 'name': employee_id}])
        query = query.ancestor(key)
    if status is not None:
        query = query.filter('status =', status)
    for report in query.fetch():
        yield _report_info(report)


def get_report_info(employee_id, report_id):
    dataset = _get_dataset()
    report = _get_report(dataset, employee_id, report_id, False)
    if report is None:
        raise NoSuchReport()
    info = _report_info(report)
    info['items'] = [dict(x) for x in _fetch_report_items(dataset, report)]
    return info


def create_report(employee_id, report_id, rows, description):
    dataset = _get_dataset()
    with dataset.transaction():
        if _get_report(dataset, employee_id, report_id, False) is not None:
            raise DuplicateReport()
        report = _upsert_report(dataset, employee_id, report_id, rows)
        report['status'] = 'pending'
        if description is not None:
            report['description'] = description
        report['created'] = report['updated'] = datetime.datetime.utcnow()
        report.save()


def update_report(employee_id, report_id, rows, description):
    dataset = _get_dataset()
    with dataset.transaction():
        report = _get_report(dataset, employee_id, report_id, False)
        if report is None:
            raise NoSuchReport()
        if report['status'] != 'pending':
            raise BadReportStatus(report['status'])
        _upsert_report(dataset, employee_id, report_id, rows)
        if description is not None:
            report['description'] = description
        report['updated'] = datetime.datetime.utcnow()
        report.save()


def delete_report(employee_id, report_id, force):
    dataset = _get_dataset()
    with dataset.transaction():
        report = _get_report(dataset, employee_id, report_id, False)
        if report is None:
            raise NoSuchReport()
        if report['status'] != 'pending' and not force:
            raise BadReportStatus(report['status'])
        count = _purge_report_items(dataset, report)
        report.delete()
    return count


def approve_report(employee_id, report_id, check_number):
    dataset = _get_dataset()
    with dataset.transaction():
        report = _get_report(dataset, employee_id, report_id, False)
        if report is None:
            raise NoSuchReport()
        if report['status'] != 'pending':
            raise BadReportStatus(report['status'])
        report['updated'] = datetime.datetime.utcnow()
        report['status'] = 'paid'
        report['check_number'] = check_number
        report.save()


def reject_report(employee_id, report_id, reason):
    dataset = _get_dataset()
    with dataset.transaction():
        report = _get_report(dataset, employee_id, report_id, False)
        if report is None:
            raise NoSuchReport()
        if report['status'] != 'pending':
            raise BadReportStatus(report['status'])
        report['updated'] = datetime.datetime.utcnow()
        report['status'] = 'rejected'
        report['reason'] = reason
        report.save()
