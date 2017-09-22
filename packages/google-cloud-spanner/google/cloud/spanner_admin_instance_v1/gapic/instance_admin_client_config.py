config = {
    "interfaces": {
        "google.spanner.admin.instance.v1.InstanceAdmin": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": []
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 1000,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 600000
                }
            },
            "methods": {
                "ListInstanceConfigs": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "GetInstanceConfig": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListInstances": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "GetInstance": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "CreateInstance": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "UpdateInstance": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "DeleteInstance": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "SetIamPolicy": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "GetIamPolicy": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "TestIamPermissions": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
