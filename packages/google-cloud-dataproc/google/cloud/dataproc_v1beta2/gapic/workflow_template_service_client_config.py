config = {
    "interfaces": {
        "google.cloud.dataproc.v1beta2.WorkflowTemplateService": {
            "retry_codes": {
                "retry_policy_6_codes": ["UNAVAILABLE"],
                "no_retry_codes": [],
                "retry_policy_7_codes": [
                    "DEADLINE_EXCEEDED",
                    "INTERNAL",
                    "UNAVAILABLE",
                ],
            },
            "retry_params": {
                "retry_policy_6_params": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 600000,
                    "total_timeout_millis": 600000,
                },
                "retry_policy_7_params": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 600000,
                    "total_timeout_millis": 600000,
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
            },
            "methods": {
                "InstantiateWorkflowTemplate": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "retry_policy_6_codes",
                    "retry_params_name": "retry_policy_6_params",
                },
                "InstantiateInlineWorkflowTemplate": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "retry_policy_6_codes",
                    "retry_params_name": "retry_policy_6_params",
                },
                "CreateWorkflowTemplate": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "retry_policy_6_codes",
                    "retry_params_name": "retry_policy_6_params",
                },
                "GetWorkflowTemplate": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "retry_policy_7_codes",
                    "retry_params_name": "retry_policy_7_params",
                },
                "UpdateWorkflowTemplate": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "retry_policy_6_codes",
                    "retry_params_name": "retry_policy_6_params",
                },
                "ListWorkflowTemplates": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "retry_policy_7_codes",
                    "retry_params_name": "retry_policy_7_params",
                },
                "DeleteWorkflowTemplate": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "retry_policy_6_codes",
                    "retry_params_name": "retry_policy_6_params",
                },
            },
        }
    }
}
