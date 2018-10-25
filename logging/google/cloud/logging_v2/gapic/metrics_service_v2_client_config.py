config = {
    "interfaces": {
        "google.logging.v2.MetricsServiceV2": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "INTERNAL", "UNAVAILABLE"],
                "non_idempotent": []
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.2,
                    "max_retry_delay_millis": 1000,
                    "initial_rpc_timeout_millis": 20000,
                    "rpc_timeout_multiplier": 1.5,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 90000
                }
            },
            "methods": {
                "ListLogMetrics": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "GetLogMetric": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "CreateLogMetric": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "UpdateLogMetric": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "DeleteLogMetric": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
