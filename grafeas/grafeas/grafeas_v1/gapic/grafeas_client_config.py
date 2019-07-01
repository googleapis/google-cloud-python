config = {
    "interfaces": {
        "grafeas.v1.Grafeas": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 20000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 20000,
                    "total_timeout_millis": 600000,
                }
            },
            "methods": {
                "GetOccurrence": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListOccurrences": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteOccurrence": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateOccurrence": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "BatchCreateOccurrences": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateOccurrence": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetOccurrenceNote": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetNote": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListNotes": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteNote": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateNote": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "BatchCreateNotes": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateNote": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "ListNoteOccurrences": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
