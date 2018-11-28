config = {
    "interfaces": {
        "google.container.v1.ClusterManager": {
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
                "ListClusters": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetCluster": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateCluster": {
                    "timeout_millis": 45000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateCluster": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateNodePool": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetNodePoolAutoscaling": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetLoggingService": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetMonitoringService": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetAddonsConfig": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetLocations": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "UpdateMaster": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetMasterAuth": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "DeleteCluster": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListOperations": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetOperation": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CancelOperation": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "GetServerConfig": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "ListNodePools": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "GetNodePool": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "CreateNodePool": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "DeleteNodePool": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default",
                },
                "RollbackNodePoolUpgrade": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetNodePoolManagement": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetLabels": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetLegacyAbac": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "StartIPRotation": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "CompleteIPRotation": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetNodePoolSize": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetNetworkPolicy": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
                "SetMaintenancePolicy": {
                    "timeout_millis": 20000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default",
                },
            },
        }
    }
}
