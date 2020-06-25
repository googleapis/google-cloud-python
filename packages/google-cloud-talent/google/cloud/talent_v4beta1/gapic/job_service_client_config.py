config = {
    "interfaces": {
        "google.cloud.talent.v4beta1.JobService": {
            "retry_codes": {
                "no_retry_codes": [],
                "no_retry_3_codes": [],
                "retry_policy_3_codes": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
            },
            "retry_params": {
                "no_retry_3_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 0.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 30000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 30000,
                    "total_timeout_millis": 30000,
                },
                "retry_policy_3_params": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
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
            },
            "methods": {
                "CreateJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_3_codes",
                    "retry_params_name": "no_retry_3_params",
                },
                "BatchCreateJobs": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_3_codes",
                    "retry_params_name": "no_retry_3_params",
                },
                "GetJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "UpdateJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_3_codes",
                    "retry_params_name": "no_retry_3_params",
                },
                "BatchUpdateJobs": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_3_codes",
                    "retry_params_name": "no_retry_3_params",
                },
                "DeleteJob": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "BatchDeleteJobs": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_3_codes",
                    "retry_params_name": "no_retry_3_params",
                },
                "ListJobs": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_3_codes",
                    "retry_params_name": "retry_policy_3_params",
                },
                "SearchJobs": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_3_codes",
                    "retry_params_name": "no_retry_3_params",
                },
                "SearchJobsForAlert": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_3_codes",
                    "retry_params_name": "no_retry_3_params",
                },
            },
        }
    }
}
