from fastapi import FastAPI

from .endpoints import resource_router, resource_router_base_url


def init_api_v1(app: FastAPI):
    app.include_router(
        router=resource_router, tags=["SampleRoute"], prefix=resource_router_base_url
    )
