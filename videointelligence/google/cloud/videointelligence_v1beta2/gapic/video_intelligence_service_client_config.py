config = {
    "interfaces": {
        "google.cloud.videointelligence.v1beta2.VideoIntelligenceService": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": []
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 1000,
                    "retry_delay_multiplier": 2.5,
                    "max_retry_delay_millis": 120000,
                    "initial_rpc_timeout_millis": 120000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 120000,
                    "total_timeout_millis": 600000
                }
            },
            "methods": {
                "AnnotateVideo": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
