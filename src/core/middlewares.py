import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class StatisticsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

        self.request_count = 0
        self.request_time = 0.0

    @property
    def request_time_average(self):
        return 0.0 if not self.request_count else self.request_time / self.request_count

    def add_metrics(self, perf_metrics: float):
        self.request_count += 1
        self.request_time += perf_metrics

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if not hasattr(request.state, "request_time_average"):
            request.state.request_time_average = self.request_time_average

        request.state.request_count = self.request_count

        start = time.perf_counter()
        response = await call_next(request)
        self.add_metrics(time.perf_counter() - start)

        return response
