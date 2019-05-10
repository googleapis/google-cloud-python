config = {
    "interfaces": {
        "google.devtools.cloudtrace.v2.TraceService": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.2,
                    "max_retry_delay_millis": 1000,
                    "initial_rpc_timeout_millis": 30000,
                    "rpc_timeout_multiplier": 1.5,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 120000,
                }
            },
            "methods": {
                "BatchWriteSpans": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "CreateSpan": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
