config = {
    "interfaces": {
        "google.bigtable.admin.v2.BigtableInstanceAdmin": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "idempotent_params": {
                    "initial_retry_delay_millis": 1000,
                    "retry_delay_multiplier": 2.0,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 600000,
                },
                "non_idempotent_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 1.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 60000,
                },
                "non_idempotent_heavy_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 1.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 300000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 300000,
                    "total_timeout_millis": 300000,
                },
            },
            "methods": {
                "CreateInstance": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_heavy_params",
                },
                "GetInstance": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "ListInstances": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "UpdateInstance": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "PartialUpdateInstance": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "DeleteInstance": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "CreateCluster": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "GetCluster": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "ListClusters": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "UpdateCluster": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "DeleteCluster": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "CreateAppProfile": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "GetAppProfile": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "ListAppProfiles": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "UpdateAppProfile": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "DeleteAppProfile": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "GetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "SetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "TestIamPermissions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
            },
        }
    }
}
