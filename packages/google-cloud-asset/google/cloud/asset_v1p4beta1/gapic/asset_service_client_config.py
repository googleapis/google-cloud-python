config = {
    "interfaces": {
        "google.cloud.asset.v1p4beta1.AssetService": {
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
                "ExportIamPolicyAnalysis": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "AnalyzeIamPolicy": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
