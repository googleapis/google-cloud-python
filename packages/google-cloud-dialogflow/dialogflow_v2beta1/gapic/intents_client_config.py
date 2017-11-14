config = {
    "interfaces": {
        "google.cloud.dialogflow.v2beta1.Intents": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": []
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 20000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 20000,
                    "total_timeout_millis": 600000
                }
            },
            "methods": {
                "ListIntents": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "GetIntent": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "CreateIntent": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "UpdateIntent": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "DeleteIntent": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "BatchUpdateIntents": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "BatchDeleteIntents": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
