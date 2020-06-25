config = {
    "interfaces": {
        "google.cloud.tasks.v2.CloudTasks": {
            "retry_codes": {
                "retry_policy_1_codes": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "no_retry_codes": [],
                "no_retry_1_codes": [],
            },
            "retry_params": {
                "retry_policy_1_params": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 10000,
                    "initial_rpc_timeout_millis": 10000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 10000,
                    "total_timeout_millis": 10000,
                },
                "no_retry_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 0.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 0,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 0,
                    "total_timeout_millis": 0,
                },
                "no_retry_1_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 0.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 10000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 10000,
                    "total_timeout_millis": 10000,
                },
            },
            "methods": {
                "ListQueues": {
                    "timeout_millis": 15000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "GetQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "CreateQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "UpdateQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "DeleteQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "PurgeQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "PauseQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "ResumeQueue": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "GetIamPolicy": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "SetIamPolicy": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "TestIamPermissions": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ListTasks": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "GetTask": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "CreateTask": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "DeleteTask": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "RunTask": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
            },
        }
    }
}
