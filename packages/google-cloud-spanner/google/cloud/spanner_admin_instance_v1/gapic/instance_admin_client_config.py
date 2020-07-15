config = {
    "interfaces": {
        "google.spanner.admin.instance.v1.InstanceAdmin": {
            "retry_codes": {
                "retry_policy_1_codes": ["UNAVAILABLE", "DEADLINE_EXCEEDED"],
                "no_retry_2_codes": [],
                "no_retry_codes": [],
                "retry_policy_2_codes": ["UNAVAILABLE", "DEADLINE_EXCEEDED"],
                "no_retry_1_codes": [],
            },
            "retry_params": {
                "retry_policy_1_params": {
                    "initial_retry_delay_millis": 1000,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 3600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 3600000,
                    "total_timeout_millis": 3600000,
                },
                "retry_policy_2_params": {
                    "initial_retry_delay_millis": 1000,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 30000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 30000,
                    "total_timeout_millis": 30000,
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
                    "initial_rpc_timeout_millis": 3600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 3600000,
                    "total_timeout_millis": 3600000,
                },
                "no_retry_2_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 0.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 30000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 30000,
                    "total_timeout_millis": 30000,
                },
            },
            "methods": {
                "CreateInstance": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "UpdateInstance": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "ListInstanceConfigs": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "GetInstanceConfig": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ListInstances": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "GetInstance": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "DeleteInstance": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "SetIamPolicy": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "GetIamPolicy": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_2_codes",
                    "retry_params_name": "retry_policy_2_params",
                },
                "TestIamPermissions": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
            },
        }
    }
}
