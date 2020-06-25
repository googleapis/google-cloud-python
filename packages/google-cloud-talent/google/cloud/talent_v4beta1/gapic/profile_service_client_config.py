config = {
    "interfaces": {
        "google.cloud.talent.v4beta1.ProfileService": {
            "retry_codes": {
                "retry_policy_4_codes": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "no_retry_2_codes": [],
                "no_retry_codes": [],
            },
            "retry_params": {
                "retry_policy_4_params": {
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
                "SearchProfiles": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "ListProfiles": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_4_codes",
                    "retry_params_name": "retry_policy_4_params",
                },
                "CreateProfile": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "GetProfile": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_4_codes",
                    "retry_params_name": "retry_policy_4_params",
                },
                "UpdateProfile": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "DeleteProfile": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "retry_policy_4_codes",
                    "retry_params_name": "retry_policy_4_params",
                },
            },
        }
    }
}
