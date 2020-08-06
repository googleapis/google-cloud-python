config = {
    "interfaces": {
        "google.devtools.cloudtrace.v1.TraceService": {
            "retry_codes": {
                "retry_policy_1_codes": ["UNAVAILABLE", "DEADLINE_EXCEEDED"],
                "no_retry_codes": [],
            },
            "retry_params": {
                "retry_policy_1_params": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.2,
                    "max_retry_delay_millis": 1000,
                    "initial_rpc_timeout_millis": 45000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 45000,
                    "total_timeout_millis": 45000,
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
                "PatchTraces": {
                    "timeout_millis": 45000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ListTraces": {
                    "timeout_millis": 45000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "GetTrace": {
                    "timeout_millis": 45000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
            },
        }
    }
}
