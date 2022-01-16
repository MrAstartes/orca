from fastapi import APIRouter, Request

from core.cloud_service import CloudEnvironmentService
from core.models import StatsResponse

router = APIRouter(tags=["monitoring"])


@router.get("/stats/", response_model=StatsResponse)
async def stats(request: Request):
    return {
        "vm_count": CloudEnvironmentService.get_vm_count(),
        "request_count": request.state.request_count,
        "average_request_time": request.state.request_time_average,
    }
