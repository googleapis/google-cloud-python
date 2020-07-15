config = {
    "interfaces": {
        "google.spanner.v1.Spanner": {
            "retry_codes": {
                "retry_policy_1_codes": ["UNAVAILABLE"],
                "no_retry_codes": [],
                "retry_policy_3_codes": ["UNAVAILABLE"],
                "retry_policy_2_codes": ["UNAVAILABLE"],
                "no_retry_1_codes": [],
            },
            "retry_params": {
                "retry_policy_1_params": {
                    "initial_retry_delay_millis": 250,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 3600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 3600000,
                    "total_timeout_millis": 3600000,
                },
                "retry_policy_3_params": {
                    "initial_retry_delay_millis": 250,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 30000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 30000,
                    "total_timeout_millis": 30000,
                },
                "retry_policy_2_params": {
                    "initial_retry_delay_millis": 250,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 32000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 60000,
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
            },
            "methods": {
                "CreateSession": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "BatchCreateSessions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retry_policy_2_codes",
                    "retry_params_name": "retry_policy_2_params",
                },
                "GetSession": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "ListSessions": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "DeleteSession": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "ExecuteSql": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "ExecuteStreamingSql": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "ExecuteBatchDml": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "Read": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "StreamingRead": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "BeginTransaction": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "Commit": {
                    "timeout_millis": 3600000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "Rollback": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "PartitionQuery": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "PartitionRead": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
            },
        }
    }
}
