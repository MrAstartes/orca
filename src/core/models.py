from pydantic import BaseModel, confloat, conint, constr

TagName = constr(strip_whitespace=True)
VirtualMachineID = constr(strip_whitespace=True, regex=r"vm-\w+")
FirewallRuleID = constr(strip_whitespace=True, regex=r"fw-\w+")


class VirtualMachine(BaseModel):
    vm_id: VirtualMachineID
    name: constr(strip_whitespace=True)
    tags: list[constr(strip_whitespace=True)]


class FirewallRule(BaseModel):
    fw_id: FirewallRuleID
    source_tag: TagName
    dest_tag: TagName


class CloudEnvironment(BaseModel):
    vms: list[VirtualMachine]
    fw_rules: list[FirewallRule]


class StatsResponse(BaseModel):
    vm_count: conint(ge=0)
    request_count: conint(ge=0)
    average_request_time: confloat(ge=0)
