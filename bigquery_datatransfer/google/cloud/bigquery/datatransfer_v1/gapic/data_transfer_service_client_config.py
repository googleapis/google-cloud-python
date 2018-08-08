config = {
    "interfaces": {
        "google.cloud.bigquery.datatransfer.v1.DataTransferService": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": []
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 20000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 20000,
                    "total_timeout_millis": 600000
                }
            },
            "methods": {
                "GetDataSource": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListDataSources": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "CreateTransferConfig": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "UpdateTransferConfig": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "DeleteTransferConfig": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "GetTransferConfig": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListTransferConfigs": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ScheduleTransferRuns": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "GetTransferRun": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "DeleteTransferRun": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListTransferRuns": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListTransferLogs": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "CheckValidCreds": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
