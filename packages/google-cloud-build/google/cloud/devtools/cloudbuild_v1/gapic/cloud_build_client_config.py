config = {
    "interfaces": {
        "google.devtools.cloudbuild.v1.CloudBuild": {
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
                "ListBuilds": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteBuildTrigger": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateBuild": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetBuild": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CancelBuild": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "RetryBuild": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "CreateBuildTrigger": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetBuildTrigger": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListBuildTriggers": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "UpdateBuildTrigger": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "RunBuildTrigger": {
                    "timeout_millis": 180000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "CreateWorkerPool": {
                    "timeout_millis": 320000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetWorkerPool": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "DeleteWorkerPool": {
                    "timeout_millis": 320000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateWorkerPool": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "ListWorkerPools": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
