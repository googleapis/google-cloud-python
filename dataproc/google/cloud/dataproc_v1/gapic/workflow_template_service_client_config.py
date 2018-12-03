config = {
    "interfaces": {
        "google.cloud.dataproc.v1.WorkflowTemplateService": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "INTERNAL", "UNAVAILABLE"],
                "non_idempotent": ["UNAVAILABLE"],
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
                "CreateWorkflowTemplate": {
                    "timeout_millis": 30000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetWorkflowTemplate": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "InstantiateWorkflowTemplate": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "InstantiateInlineWorkflowTemplate": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateWorkflowTemplate": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "ListWorkflowTemplates": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteWorkflowTemplate": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
