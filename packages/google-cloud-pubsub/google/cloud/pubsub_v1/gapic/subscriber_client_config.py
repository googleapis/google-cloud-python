config = {
    "interfaces": {
        "google.pubsub.v1.Subscriber": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
                "pull": [
                    "CANCELLED", "DEADLINE_EXCEEDED", "INTERNAL",
                    "RESOURCE_EXHAUSTED", "UNAVAILABLE"
                ]
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 600000
                },
                "messaging": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 12000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 12000,
                    "total_timeout_millis": 600000
                },
                "streaming_messaging": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 600000,
                    "total_timeout_millis": 600000
                }
            },
            "methods": {
                "CreateSubscription": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "GetSubscription": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "UpdateSubscription": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListSubscriptions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "DeleteSubscription": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ModifyAckDeadline": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "Acknowledge": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "messaging"
                },
                "Pull": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "pull",
                    "retry_params_name": "messaging"
                },
                "StreamingPull": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "pull",
                    "retry_params_name": "streaming_messaging"
                },
                "ModifyPushConfig": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "ListSnapshots": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "CreateSnapshot": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "UpdateSnapshot": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "DeleteSnapshot": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "Seek": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "SetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "GetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "TestIamPermissions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
