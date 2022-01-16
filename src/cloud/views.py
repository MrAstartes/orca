from typing import List

from fastapi import APIRouter

from core.cloud_service import CloudEnvironmentService
from core.models import VirtualMachineID

router = APIRouter(tags=["cloud"])


@router.get("/attack/", response_model=List[VirtualMachineID])
async def attack(vm_id: VirtualMachineID):
    return CloudEnvironmentService.get_vm_vulnerabilities(vm_id)
