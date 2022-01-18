import os
from tempfile import NamedTemporaryFile

import pytest

from core.cloud_service import CloudEnvironmentService, InputFileReadException
from core.models import CloudEnvironment, FirewallRule, VirtualMachine
from tests.conftest import FIXTURES_DIR


class TestCloudService:
    test_cloud = {
        "vms": [
            {"vm_id": "vm-1", "name": "vm1 name", "tags": ["tag1"]},
            {"vm_id": "vm-2", "name": "vm2 name", "tags": ["tag3", "tag2"]},
            {"vm_id": "vm-3", "name": "vm3 name", "tags": ["tag3"]},
            {"vm_id": "vm-4", "name": "vm4 name", "tags": ["tag4"]},
            {"vm_id": "vm-5", "name": "vm5 name", "tags": []},
        ],
        "fw_rules": [
            {"fw_id": "fw-1", "source_tag": "tag1", "dest_tag": "tag2"},
            {"fw_id": "fw-2", "source_tag": "tag2", "dest_tag": "tag3"},
            {"fw_id": "fw-3", "source_tag": "tag3", "dest_tag": "tag1"},
            {"fw_id": "fw-4", "source_tag": "tag4", "dest_tag": "tag4"},
        ],
    }

    source_by_destination_result = {"tag2": {"tag1"}, "tag3": {"tag2"}, "tag1": {"tag3"}, "tag4": {"tag4"}}
    virtual_machine_by_tag_result = {"tag1": {"vm-1"}, "tag3": {"vm-2", "vm-3"}, "tag2": {"vm-2"}, "tag4": {"vm-4"}}
    vm_access_map_result = {"vm-1": {"vm-3", "vm-2"}, "vm-2": {"vm-1", "vm-2"}, "vm-3": {"vm-2"}, "vm-4": {"vm-4"}}

    @pytest.mark.parametrize(
        "vm_id, expected",
        [("vm-1", ["vm-1", "vm-2"]), ("vm-2", ["vm-1"]), ("vm-non-exist", [])],
    )
    def test_get_vm_vulnerabilities(self, vm_id, expected):
        CloudEnvironmentService._vm_access_map = {"vm-1": {"vm-1", "vm-2"}, "vm-2": {"vm-1"}}
        result = CloudEnvironmentService.get_vm_vulnerabilities(vm_id)
        assert sorted(result) == sorted(expected)

    def test_get_vm_count(self):
        CloudEnvironmentService._vm_count = 10
        assert CloudEnvironmentService.get_vm_count() == 10

    def test_load_success(self, mocker):
        CloudEnvironmentService._vm_count = 0
        CloudEnvironmentService._vm_access_map = {}

        spy = mocker.spy(CloudEnvironmentService, "_process_data")

        file_path = os.path.join(os.path.join(FIXTURES_DIR, "cloud.json"))
        CloudEnvironmentService.load(file_path)

        spy.assert_called_once()

    def test_load_file_not_found(self):
        with pytest.raises(InputFileReadException, match="Error while read input file"):
            CloudEnvironmentService.load("/some/invalid/file/path")

    def test_load_invalid_json(self):
        with NamedTemporaryFile(mode="w") as f:
            f.write("{some-invalid-json}")
            f.seek(0)

            with pytest.raises(InputFileReadException, match="Invalid JSON provided"):
                CloudEnvironmentService.load(f.name)

    def test__process_data(self):
        CloudEnvironmentService._vm_count = 0
        CloudEnvironmentService._vm_access_map = {}

        CloudEnvironmentService._process_data(CloudEnvironment(**self.test_cloud))

        assert CloudEnvironmentService._vm_count == 5
        assert CloudEnvironmentService._vm_access_map == self.vm_access_map_result

    def test__process_data_spy(self, mocker):
        must_be_called = [
            mocker.spy(CloudEnvironmentService, "_get_source_by_destination_map"),
            mocker.spy(CloudEnvironmentService, "_get_virtual_machine_by_tag_map"),
            mocker.spy(CloudEnvironmentService, "_get_virtual_machine_access_map"),
        ]

        CloudEnvironmentService._process_data(CloudEnvironment(**self.test_cloud))

        for spy in must_be_called:
            spy.assert_called_once()

    def test__get_source_by_destination_map_success(self):
        test_data = [FirewallRule(**item) for item in self.test_cloud["fw_rules"]]
        result = CloudEnvironmentService._get_source_by_destination_map(test_data)

        assert result == self.source_by_destination_result

    def test__get_virtual_machine_by_tag_map_success(self):
        test_data = [VirtualMachine(**item) for item in self.test_cloud["vms"]]
        result = CloudEnvironmentService._get_virtual_machine_by_tag_map(test_data)

        assert result == self.virtual_machine_by_tag_result

    def test_get_virtual_machine_access_map_success(self):
        vms = [VirtualMachine(**item) for item in self.test_cloud["vms"]]
        result = CloudEnvironmentService._get_virtual_machine_access_map(
            vms, self.source_by_destination_result, self.virtual_machine_by_tag_result
        )

        assert result == self.vm_access_map_result
