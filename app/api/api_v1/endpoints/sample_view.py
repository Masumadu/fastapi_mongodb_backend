from typing import List, Union

import pinject
from fastapi import APIRouter, Depends, status

from app.controllers import ResourceController
from app.repositories import ResourceRepository
from app.schema import (
    CreateResourceSchema,
    RefreshTokenSchema,
    ResourceSchema,
    TokenSchema,
    UpdateResourceSchema,
)
from app.services import RedisService
from app.utils import JwtAuthentication

resource_router = APIRouter()
resource_router_base_url = "/api/v1/sample-prefix"

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[ResourceController, ResourceRepository, RedisService, JwtAuthentication],
)
resource_controller: ResourceController = obj_graph.provide(ResourceController)


@resource_router.get("/", response_model=Union[List[ResourceSchema], ResourceSchema])
def get_resource(resource_id: str = None):
    query_params = {"resource_id": resource_id}
    result = resource_controller.get_resource(query_params)
    return result


@resource_router.post(
    "/", response_model=ResourceSchema, status_code=status.HTTP_201_CREATED
)
def create_resource(obj_data: CreateResourceSchema):
    result = resource_controller.create_resource(obj_data.dict())
    return result


@resource_router.patch("/{resource_id}", response_model=ResourceSchema)
def update_resource(
    resource_id: str,
    obj_data: UpdateResourceSchema,
    current_user=Depends(JwtAuthentication()),  # noqa
):
    result = resource_controller.update_resource(resource_id, obj_data.dict())
    return result


@resource_router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: str, current_user=Depends(JwtAuthentication())  # noqa
):
    result = resource_controller.delete(resource_id)
    return result


@resource_router.get("/get-token/", response_model=TokenSchema)
def get_token():
    result = resource_controller.get_token()
    return result


@resource_router.post("/refresh-token/", response_model=TokenSchema)
def refresh_token(obj_data: RefreshTokenSchema):
    result = resource_controller.refresh_token(obj_data.dict())
    return result
