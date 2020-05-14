config = {
    "interfaces": {
        "google.spanner.admin.database.v1.DatabaseAdmin": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 1000,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 600000,
                }
            },
            "methods": {
                "CreateDatabase": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetDatabase": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "UpdateDatabaseDdl": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DropDatabase": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetDatabaseDdl": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "SetIamPolicy": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetIamPolicy": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "TestIamPermissions": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "CreateBackup": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetBackup": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "UpdateBackup": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "DeleteBackup": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListBackups": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "RestoreDatabase": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "ListDatabaseOperations": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListBackupOperations": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListDatabases": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
