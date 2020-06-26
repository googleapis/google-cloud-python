config = {
    "interfaces": {
        "google.cloud.automl.v1.AutoMl": {
            "retry_codes": {
                "retry_policy_1_codes": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "no_retry_codes": [],
                "no_retry_1_codes": [],
            },
            "retry_params": {
                "retry_policy_1_params": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 5000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 5000,
                    "total_timeout_millis": 5000,
                },
                "no_retry_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 0.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 0,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 0,
                    "total_timeout_millis": 0,
                },
                "no_retry_1_params": {
                    "initial_retry_delay_millis": 0,
                    "retry_delay_multiplier": 0.0,
                    "max_retry_delay_millis": 0,
                    "initial_rpc_timeout_millis": 5000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 5000,
                    "total_timeout_millis": 5000,
                },
            },
            "methods": {
                "CreateDataset": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "GetDataset": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ListDatasets": {
                    "timeout_millis": 50000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "UpdateDataset": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "DeleteDataset": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ImportData": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "ExportData": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "GetAnnotationSpec": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "CreateModel": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "GetModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ListModels": {
                    "timeout_millis": 50000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "DeleteModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "UpdateModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "DeployModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "UndeployModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "ExportModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_1_codes",
                    "retry_params_name": "no_retry_1_params",
                },
                "GetModelEvaluation": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ListModelEvaluations": {
                    "timeout_millis": 50000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
            },
        }
    }
}
