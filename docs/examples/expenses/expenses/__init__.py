# package
import os

from gcloud import datastore
from gcloud.datastore.key import Key
from gcloud.datastore.entity import Entity
from gcloud.datastore.query import Query

def get_dataset():
    client_email = os.environ['EXPENSES_CLIENT_EMAIL']
    private_key_path = os.environ['EXPENSES_PRIVATE_KEY_PATH']
    dataset_id = os.environ['EXPENSES_DATASET_ID']
    conn = datastore.get_connection(client_email, private_key_path)
    return conn.dataset(dataset_id)

def get_employee(dataset, employee_id):
    key = Key(dataset, path=[{'kind': 'Employee', 'name': employee_id}])
    employee = dataset.get_entity(key)
    if employee is None:
        employee = dataset.entity('Employee').key(key)
        employee.save()
    return employee

def get_report(dataset, employee_id, report_id):
    key = Key(dataset,
              path=[{'kind': 'Employee', 'name': employee_id},
                    {'kind': 'Expense Report', 'name': report_id},
                   ])
    report = dataset.get_entity(key)
    if report is None:
        report = dataset.entity('Report').key(key)
        report.save()
    return report

def upsert_report(employee_id, report_id, rows):
    dataset = get_dataset()
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
