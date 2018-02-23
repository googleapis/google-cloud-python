config = {
    "interfaces": {
        "google.logging.v2.LoggingServiceV2": {
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
                },
                "list": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.2,
                    "max_retry_delay_millis": 1000,
                    "initial_rpc_timeout_millis": 2000,
                    "rpc_timeout_multiplier": 1.5,
                    "max_rpc_timeout_millis": 10000,
                    "total_timeout_millis": 20000
                }
            },
            "methods": {
                "DeleteLog": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "WriteLogEntries": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                    "bundling": {
                        "element_count_threshold": 1000,
                        "request_byte_threshold": 1048576,
                        "delay_threshold_millis": 50
                    }
                },
                "ListLogEntries": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "list"
                },
                "ListMonitoredResourceDescriptors": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListLogs": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
