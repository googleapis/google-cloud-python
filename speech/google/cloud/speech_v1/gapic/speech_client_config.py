config = {
    "interfaces": {
        "google.cloud.speech.v1.Speech": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 1000000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 1000000,
                    "total_timeout_millis": 5000000,
                }
            },
            "methods": {
                "Recognize": {
                    "timeout_millis": 200000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "LongRunningRecognize": {
                    "timeout_millis": 200000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "StreamingRecognize": {
                    "timeout_millis": 200000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
