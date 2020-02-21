config = {
    "interfaces": {
        "google.cloud.bigquery.storage.v1.BigQueryRead": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "unary_streaming": ["UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 20000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 20000,
                    "total_timeout_millis": 600000,
                },
                "create_read_session": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 120000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 120000,
                    "total_timeout_millis": 600000,
                },
                "read_rows": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 86400000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 86400000,
                    "total_timeout_millis": 86400000,
                },
            },
            "methods": {
                "CreateReadSession": {
                    "timeout_millis": 120000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "create_read_session",
                },
                "ReadRows": {
                    "timeout_millis": 21600000,
                    "retry_codes_name": "unary_streaming",
                    "retry_params_name": "read_rows",
                },
                "SplitReadStream": {
                    "timeout_millis": 120000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
