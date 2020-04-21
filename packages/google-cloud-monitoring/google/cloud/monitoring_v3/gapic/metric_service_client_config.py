config = {
    "interfaces": {
        "google.monitoring.v3.MetricService": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 30000,
                    "rpc_timeout_multiplier": 1.3,
                    "max_rpc_timeout_millis": 90000,
                    "total_timeout_millis": 600000,
                }
            },
            "methods": {
                "ListMonitoredResourceDescriptors": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetMonitoredResourceDescriptor": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListMetricDescriptors": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetMetricDescriptor": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateMetricDescriptor": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "DeleteMetricDescriptor": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListTimeSeries": {
                    "timeout_millis": 90000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateTimeSeries": {
                    "timeout_millis": 12000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
