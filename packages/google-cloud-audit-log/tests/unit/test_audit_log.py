from google.cloud.audit import audit_log_pb2


def test_create_audit_log():
    # just check that the import works
    # and that an AuditLog instance can be instantiated
    audit_log_pb2.AuditLog()