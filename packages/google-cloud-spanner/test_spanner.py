from google.cloud.spanner_admin_instance_v1.types import spanner_instance_admin
request = spanner_instance_admin.UpdateInstanceRequest(
    instance=spanner_instance_admin.Instance(
        name="projects/my-project/instances/my-instance",
        edition=spanner_instance_admin.Instance.Edition.ENTERPRISE,
    ),
    field_mask={"paths": ["edition"]},
)
print("SUCCESS")
