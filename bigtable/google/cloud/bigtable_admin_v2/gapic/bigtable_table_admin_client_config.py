config = {
    "interfaces": {
        "google.bigtable.admin.v2.BigtableTableAdmin": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "idempotent_params": {
                    "initial_retry_delay_millis": 1000,
                    "retry_delay_multiplier": 2.0,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 600000,
                },
                "non_idempotent_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 1.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 60000,
                },
                "non_idempotent_heavy_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 1.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 300000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 300000,
                    "total_timeout_millis": 300000,
                },
                "drop_row_range_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 1.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 3600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 3600000,
                    "total_timeout_millis": 3600000,
                },
            },
            "methods": {
                "CreateTable": {
                    "timeout_millis": 130000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_heavy_params",
                },
                "CreateTableFromSnapshot": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "ListTables": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "GetTable": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "DeleteTable": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "ModifyColumnFamilies": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_heavy_params",
                },
                "DropRowRange": {
                    "timeout_millis": 900000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "drop_row_range_params",
                },
                "GenerateConsistencyToken": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "CheckConsistency": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "GetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "SetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "TestIamPermissions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "SnapshotTable": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "GetSnapshot": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "ListSnapshots": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "DeleteSnapshot": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
            },
        }
    }
}
