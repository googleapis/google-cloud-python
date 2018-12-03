config = {
    "interfaces": {
        "google.cloud.automl.v1beta1.AutoMl": {
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
                "CreateDataset": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetDataset": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListDatasets": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteDataset": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ImportData": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "ExportData": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "CreateModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListModels": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeployModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UndeployModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetModelEvaluation": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListModelEvaluations": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
