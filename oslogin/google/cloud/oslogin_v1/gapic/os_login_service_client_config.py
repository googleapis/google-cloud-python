config = {
    "interfaces": {
        "google.cloud.oslogin.v1.OsLoginService": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 10000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 10000,
                    "total_timeout_millis": 600000,
                }
            },
            "methods": {
                "DeletePosixAccount": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteSshPublicKey": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetLoginProfile": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetSshPublicKey": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ImportSshPublicKey": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "UpdateSshPublicKey": {
                    "timeout_millis": 10000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
