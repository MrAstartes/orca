import os

from fastapi import FastAPI

import cloud
import monitoring
from core.cloud_service import CloudEnvironmentService
from core.middlewares import StatisticsMiddleware

app = FastAPI()


@app.on_event("startup")
async def load_input_file():
    CloudEnvironmentService.load(os.environ.get("CLOUD_ENVIRONMENT_FILE_PATH"))


app.add_middleware(StatisticsMiddleware)

app.include_router(cloud.router, prefix="/api/v1")
app.include_router(monitoring.router, prefix="/api/v1")
