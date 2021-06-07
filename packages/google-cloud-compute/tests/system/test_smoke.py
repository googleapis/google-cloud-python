# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import time
import google.api_core.exceptions

from google.cloud.compute_v1.services.instances.client import InstancesClient
from google.cloud.compute_v1.types import (
    InsertInstanceRequest,
    Instance,
    AttachedDisk,
    NetworkInterface,
    AttachedDiskInitializeParams,
    ShieldedInstanceConfig,
)
from tests.system.base import TestBase


class TestComputeSmoke(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.client = InstancesClient(transport="rest")
        self.name = self.get_unique_name("instance")
        self.instances = []

    def tearDown(self) -> None:
        for instance in self.instances:
            self.client.delete(
                project=self.DEFAULT_PROJECT, zone=self.DEFAULT_ZONE, instance=instance
            )

    def test_insert_instance(self):
        self.insert_instance()
        self.assert_instance()

    def insert_instance(self):
        disk = AttachedDisk()
        initialize_params = AttachedDiskInitializeParams()
        initialize_params.source_image = self.DISK_IMAGE
        disk.initialize_params = initialize_params
        disk.auto_delete = True
        disk.boot = True
        disk.type_ = AttachedDisk.Type.PERSISTENT

        network_interface = NetworkInterface()
        network_interface.name = "default"

        instance = Instance()
        instance.name = self.name
        instance.disks = [disk]
        instance.machine_type = self.MACHINE_TYPE
        instance.network_interfaces = [network_interface]

        request = InsertInstanceRequest()
        request.zone = self.DEFAULT_ZONE
        request.project = self.DEFAULT_PROJECT
        request.instance_resource = instance
        operation = self.client.insert(request=request)
        self.wait_for_zonal_operation(operation.name)
        self.instances.append(self.name)

    def test_aggregated_list(self):
        presented = False
        self.insert_instance()
        result = self.client.aggregated_list(project=self.DEFAULT_PROJECT)
        instances = getattr(result.get("zones/" + self.DEFAULT_ZONE), "instances")
        for item in instances:
            if getattr(item, "name") == self.name:
                presented = True
                break
        self.assertTrue(presented)

    def test_client_error(self):
        with self.assertRaises(
            expected_exception=google.api_core.exceptions.BadRequest
        ):
            self.client.get(instance=self.name, zone=self.DEFAULT_ZONE)

    def test_api_error(self):
        with self.assertRaises(expected_exception=google.api_core.exceptions.NotFound):
            self.client.get(
                project=self.DEFAULT_PROJECT,
                zone=self.DEFAULT_ZONE,
                instance="nonexistent9999123412314",
            )

    def test_zero_values(self):
        with self.assertRaises(expected_exception=TypeError) as ex:
            self.client.get(instance=self.name, zone=0)
        self.assertIn(
            "0 has type int, but expected one of: bytes, unicode",
            str(ex.exception.args),
        )

    def get_instance(self):
        return self.client.get(
            project=self.DEFAULT_PROJECT, zone=self.DEFAULT_ZONE, instance=self.name
        )

    def assert_instance(self):
        instance = self.get_instance()
        self.assertEqual(getattr(instance, "name"), self.name)
        self.assertEqual(len(getattr(instance, "network_interfaces")), 1)
        self.assertEqual(len(getattr(instance, "disks")), 1)

    def test_patch(self):
        self.insert_instance()
        instance = self.get_instance()
        self.assertEqual(instance.shielded_instance_config.enable_secure_boot, False)
        op = self.client.stop(
            project=self.DEFAULT_PROJECT, zone=self.DEFAULT_ZONE, instance=self.name
        )
        self.wait_for_zonal_operation(op.name)

        timeout = time.time() + 120  # it takes some time for instance to stop
        while True:
            if time.time() > timeout:
                self.fail("Instance was not stopped")
            instance = self.get_instance()
            if instance.status == Instance.Status.TERMINATED:
                break
            else:
                time.sleep(10)

        resource = ShieldedInstanceConfig()
        resource.enable_secure_boot = True
        op = self.client.update_shielded_instance_config(
            project=self.DEFAULT_PROJECT,
            zone=self.DEFAULT_ZONE,
            instance=self.name,
            shielded_instance_config_resource=resource,
        )
        self.wait_for_zonal_operation(op.name)
        patched_instance = self.get_instance()
        self.assertEqual(
            patched_instance.shielded_instance_config.enable_secure_boot, True
        )

    def test_list(self):
        presented = False
        self.insert_instance()
        result = self.client.list(project=self.DEFAULT_PROJECT, zone=self.DEFAULT_ZONE)
        for item in result:
            if getattr(item, "name") == self.name:
                presented = True
                break
        self.assertTrue(presented)
