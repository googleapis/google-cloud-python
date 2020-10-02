config = {
    "interfaces": {
        "google.cloud.videointelligence.v1p3beta1.StreamingVideoIntelligenceService": {
            "retry_codes": {
                "retry_policy_1_codes": ["UNAVAILABLE", "DEADLINE_EXCEEDED"],
                "no_retry_codes": [],
                "retry_policy_2_codes": ["UNAVAILABLE", "DEADLINE_EXCEEDED"],
            },
            "retry_params": {
                "retry_policy_1_params": {
                    "initial_retry_delay_millis": 1000,
                    "retry_delay_multiplier": 2.5,
                    "max_retry_delay_millis": 120000,
                    "initial_rpc_timeout_millis": 600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 600000,
                    "total_timeout_millis": 600000,
                },
                "retry_policy_2_params": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 10800000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 10800000,
                    "total_timeout_millis": 10800000,
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
                "StreamingAnnotateVideo": {
                    "timeout_millis": 10800000,
                    "retry_codes_name": "retry_policy_2_codes",
                    "retry_params_name": "retry_policy_2_params",
                }
            },
        }
    }
}
