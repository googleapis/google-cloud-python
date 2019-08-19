config = {
    "interfaces": {
        "google.cloud.kms.v1.KeyManagementService": {
            "retry_codes": {
                "retryable": ["DEADLINE_EXCEEDED", "INTERNAL", "UNAVAILABLE"],
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
                "non_retryable": [],
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
                "ListKeyRings": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "ListImportJobs": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "ListCryptoKeys": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "ListCryptoKeyVersions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "GetKeyRing": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "GetImportJob": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "GetCryptoKey": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "GetCryptoKeyVersion": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "CreateKeyRing": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "CreateImportJob": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "CreateCryptoKey": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "CreateCryptoKeyVersion": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_retryable",
                    "retry_params_name": "default",
                },
                "ImportCryptoKeyVersion": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_retryable",
                    "retry_params_name": "default",
                },
                "UpdateCryptoKey": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "UpdateCryptoKeyVersion": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "Encrypt": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "Decrypt": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "UpdateCryptoKeyPrimaryVersion": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "DestroyCryptoKeyVersion": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "RestoreCryptoKeyVersion": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "GetPublicKey": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "AsymmetricDecrypt": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "AsymmetricSign": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "SetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "GetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
                "TestIamPermissions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "retryable",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
