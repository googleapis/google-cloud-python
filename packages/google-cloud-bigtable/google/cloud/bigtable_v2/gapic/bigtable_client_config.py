config = {
    "interfaces": {
        "google.bigtable.v2.Bigtable": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "idempotent_params": {
                    "initial_retry_delay_millis": 10,
                    "retry_delay_multiplier": 2.0,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 20000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 20000,
                    "total_timeout_millis": 600000,
                },
                "non_idempotent_params": {
                    "initial_retry_delay_millis": 10,
                    "retry_delay_multiplier": 2.0,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 20000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 20000,
                    "total_timeout_millis": 20000,
                },
                "read_rows_params": {
                    "initial_retry_delay_millis": 10,
                    "retry_delay_multiplier": 2.0,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 300000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 300000,
                    "total_timeout_millis": 43200000,
                },
                "mutate_rows_params": {
                    "initial_retry_delay_millis": 10,
                    "retry_delay_multiplier": 2.0,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 600000,
                },
            },
            "methods": {
                "ReadRows": {
                    "timeout_millis": 43200000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "read_rows_params",
                },
                "SampleRowKeys": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "MutateRow": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "idempotent_params",
                },
                "MutateRows": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "mutate_rows_params",
                },
                "CheckAndMutateRow": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
                "ReadModifyWriteRow": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "non_idempotent_params",
                },
            },
        }
    }
}
