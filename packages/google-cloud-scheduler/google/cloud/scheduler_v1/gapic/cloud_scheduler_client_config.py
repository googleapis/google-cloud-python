config = {
    "interfaces": {
        "google.cloud.scheduler.v1.CloudScheduler": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
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
                }
            },
            "methods": {
                "ListJobs": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "DeleteJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "PauseJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "ResumeJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "RunJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
