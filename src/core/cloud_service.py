import json
from collections import defaultdict

from core.models import (
    CloudEnvironment,
    FirewallRule,
    TagName,
    VirtualMachine,
    VirtualMachineID,
)


class InputFileReadException(Exception):
    pass


class CloudEnvironmentService:
    _vm_access_map: dict[VirtualMachineID, set[VirtualMachineID]] = {}
    _vm_count: int = 0

    @classmethod
    def get_vm_vulnerabilities(cls, vm_id: VirtualMachineID) -> list[VirtualMachineID]:
        return list(cls._vm_access_map.get(vm_id, []))

    @classmethod
    def get_vm_count(cls) -> int:
        return cls._vm_count

    @classmethod
    def load(cls, path: str) -> None:
        try:
            with open(path, "r") as f:
                try:
                    input_data = json.load(f)
                except json.JSONDecodeError as e:
                    raise InputFileReadException("Invalid JSON provided") from e
        except FileNotFoundError:
            raise InputFileReadException("Error while read input file")

        cls._process_data(CloudEnvironment(**input_data))

    @classmethod
    def _process_data(cls, data: CloudEnvironment) -> None:
        source_by_destination = cls._get_source_by_destination_map(data.fw_rules)
        virtual_machine_by_tag = cls._get_virtual_machine_by_tag_map(data.vms)
        vm_access_map = cls._get_virtual_machine_access_map(data.vms, source_by_destination, virtual_machine_by_tag)

        cls._vm_access_map = vm_access_map
        cls._vm_count = len(data.vms)

    @staticmethod
    def _get_source_by_destination_map(fw_rules: list[FirewallRule]) -> dict[TagName, set[TagName]]:
        """
        Return a map with source tags grouped by destination tag.
        """
        result = defaultdict(set)
        for fw_rule in fw_rules:
            result[fw_rule.dest_tag].add(fw_rule.source_tag)

        return result

    @staticmethod
    def _get_virtual_machine_by_tag_map(vms: list[VirtualMachine]) -> dict[TagName, set[VirtualMachineID]]:
        """
        Return a map with virtual machine grouped by firewall tags attached to them.
        """
        result = defaultdict(set)
        for vm in vms:
            for tag in vm.tags:
                result[tag].add(vm.vm_id)

        return result

    @staticmethod
    def _get_virtual_machine_access_map(
        vms: list[VirtualMachine],
        source_by_destination: dict[TagName, set[TagName]],
        virtual_machine_by_tag: dict[TagName, set[VirtualMachineID]],
    ) -> dict[VirtualMachineID, VirtualMachineID]:
        """
        Return a map with virtual machines ids grouped virtual machines to which they have access
        """

        result = defaultdict(set)
        for vm in vms:
            tags_have_access = set()
            for tag in vm.tags:
                tags_have_access.update(source_by_destination[tag])

            for tag in tags_have_access:
                result[vm.vm_id].update(virtual_machine_by_tag[tag])

        return result


def foo():
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
    print("100")
