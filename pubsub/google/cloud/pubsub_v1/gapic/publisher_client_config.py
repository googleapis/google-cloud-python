config = {
    "interfaces": {
        "google.pubsub.v1.Publisher": {
            "retry_codes": {
                "idempotent": ["ABORTED", "UNAVAILABLE", "UNKNOWN"],
                "non_idempotent": ["UNAVAILABLE"],
                "none": [],
                "publish": [
                    "ABORTED",
                    "CANCELLED",
                    "DEADLINE_EXCEEDED",
                    "INTERNAL",
                    "RESOURCE_EXHAUSTED",
                    "UNAVAILABLE",
                    "UNKNOWN",
                ],
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 600000,
                },
                "messaging": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 5000,
                    "rpc_timeout_multiplier": 1.3,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 60000,
                },
            },
            "methods": {
                "CreateTopic": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateTopic": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "Publish": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "publish",
                    "retry_params_name": "messaging",
                    "bundling": {
                        "element_count_threshold": 100,
                        "element_count_limit": 1000,
                        "request_byte_threshold": 1048576,
                        "request_byte_limit": 10485760,
                        "delay_threshold_millis": 10,
                    },
                },
                "GetTopic": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListTopics": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListTopicSubscriptions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteTopic": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "TestIamPermissions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
