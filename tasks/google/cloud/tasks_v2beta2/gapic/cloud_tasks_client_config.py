config = {
    "interfaces": {
        "google.cloud.tasks.v2beta2.CloudTasks": {
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
                "ListQueues": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "GetQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "CreateQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "UpdateQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "DeleteQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "PurgeQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "PauseQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "ResumeQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "GetIamPolicy": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "SetIamPolicy": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "TestIamPermissions": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListTasks": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "GetTask": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "CreateTask": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "DeleteTask": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "LeaseTasks": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "AcknowledgeTask": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "RenewLease": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "CancelLease": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "RunTask": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
