config = {
    "interfaces": {
        "google.cloud.automl.v1beta1.AutoMl": {
            "retry_codes": {
                "retry_policy_1_codes": ["UNAVAILABLE", "DEADLINE_EXCEEDED"],
                "no_retry_2_codes": [],
                "no_retry_codes": [],
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
                "no_retry_2_params": {
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
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
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
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "DeleteDataset": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ImportData": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "ExportData": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "GetAnnotationSpec": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "GetTableSpec": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ListTableSpecs": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "UpdateTableSpec": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "GetColumnSpec": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ListColumnSpecs": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "UpdateColumnSpec": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "CreateModel": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
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
                "DeployModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "UndeployModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "ExportModel": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "ExportEvaluatedExamples": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
                "GetModelEvaluation": {
                    "timeout_millis": 5000,
                    "retry_codes_name": "retry_policy_1_codes",
                    "retry_params_name": "retry_policy_1_params",
                },
                "ListModelEvaluations": {
                    "timeout_millis": 50000,
                    "retry_codes_name": "no_retry_2_codes",
                    "retry_params_name": "no_retry_2_params",
                },
            },
        }
    }
}
