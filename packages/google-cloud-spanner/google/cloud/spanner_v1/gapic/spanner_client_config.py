config = {
    "interfaces": {
        "google.spanner.v1.Spanner": {
            "retry_codes": {
                "idempotent": ["UNAVAILABLE"],
                "non_idempotent": [],
                "long_running": ["UNAVAILABLE"],
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 250,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 600000,
                },
                "streaming": {
                    "initial_retry_delay_millis": 250,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 120000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 120000,
                    "total_timeout_millis": 1200000,
                },
                "long_running": {
                    "initial_retry_delay_millis": 250,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 3600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 3600000,
                    "total_timeout_millis": 3600000,
                },
            },
            "methods": {
                "CreateSession": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "BatchCreateSessions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetSession": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListSessions": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteSession": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ExecuteSql": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ExecuteStreamingSql": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "streaming",
                },
                "ExecuteBatchDml": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "Read": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "StreamingRead": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "streaming",
                },
                "BeginTransaction": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "Commit": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "long_running",
                    "retry_params_name": "long_running",
                },
                "Rollback": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "PartitionQuery": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "PartitionRead": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
