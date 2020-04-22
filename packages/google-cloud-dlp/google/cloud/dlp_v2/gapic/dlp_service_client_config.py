config = {
    "interfaces": {
        "google.privacy.dlp.v2.DlpService": {
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
                "InspectContent": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "RedactImage": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeidentifyContent": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ReidentifyContent": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListInfoTypes": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateInspectTemplate": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateInspectTemplate": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetInspectTemplate": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListInspectTemplates": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteInspectTemplate": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateDeidentifyTemplate": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateDeidentifyTemplate": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetDeidentifyTemplate": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListDeidentifyTemplates": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteDeidentifyTemplate": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateDlpJob": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "ListDlpJobs": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetDlpJob": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteDlpJob": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CancelDlpJob": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "FinishDlpJob": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "HybridInspectDlpJob": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "ListJobTriggers": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetJobTrigger": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteJobTrigger": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "HybridInspectJobTrigger": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateJobTrigger": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "CreateJobTrigger": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "CreateStoredInfoType": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateStoredInfoType": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetStoredInfoType": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListStoredInfoTypes": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "DeleteStoredInfoType": {
                    "timeout_millis": 300000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
