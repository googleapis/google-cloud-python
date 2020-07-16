config = {
    "interfaces": {
        "google.cloud.dataproc.v1beta2.ClusterController": {
            "retry_codes": {
                "no_retry_codes": [],
                "retry_policy_3_codes": [
                    "INTERNAL",
                    "DEADLINE_EXCEEDED",
                    "UNAVAILABLE",
                ],
                "retry_policy_2_codes": ["UNAVAILABLE"],
            },
            "retry_params": {
                "retry_policy_2_params": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 300000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 300000,
                    "total_timeout_millis": 300000,
                },
                "retry_policy_3_params": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 300000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 300000,
                    "total_timeout_millis": 300000,
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
            },
            "methods": {
                "CreateCluster": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "retry_policy_2_codes",
                    "retry_params_name": "retry_policy_2_params",
                },
                "UpdateCluster": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "retry_policy_2_codes",
                    "retry_params_name": "retry_policy_2_params",
                },
                "DeleteCluster": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "retry_policy_2_codes",
                    "retry_params_name": "retry_policy_2_params",
                },
                "DiagnoseCluster": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "retry_policy_2_codes",
                    "retry_params_name": "retry_policy_2_params",
                },
                "GetCluster": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "ListClusters": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
            },
        }
    }
}
