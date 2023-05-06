import uuid

from app.core.exceptions import AppException
from app.repositories import ResourceRepository
from app.utils import JwtAuthentication


class ResourceController:
    def __init__(
        self,
        resource_repository: ResourceRepository,
        jwt_authentication: JwtAuthentication,
    ):
        self.resource_repository = resource_repository
        self.jwt_authentication = jwt_authentication

    def get_resource(self, query_params: dict):
        resource_id: str = query_params.get("resource_id")
        if resource_id:
            try:
                result = self.resource_repository.get_by_id(resource_id)
            except AppException.NotFoundException:
                raise AppException.NotFoundException(
                    error_message="resource does not exist"
                )
        else:
            result = self.resource_repository.index()
        return result

    def create_resource(self, obj_data: dict):
        data = self.resource_repository.create(obj_data)
        return data

    def update_resource(self, obj_id, obj_data: dict):
        obj_data = {key: value for key, value in obj_data.items() if value}
        data = self.resource_repository.update_by_id(obj_id, obj_data)
        return data

    def delete(self, obj_id):
        try:
            self.resource_repository.delete_by_id(obj_id)
        except AppException.NotFoundException:
            raise AppException.NotFoundException(
                error_message="resource does not exist"
            )
        return None

    def get_token(self):
        token: dict = self.jwt_authentication.get_token(user_id=str(uuid.uuid4()))

        return token

    def refresh_token(self, obj_data: dict):
        refresh_token = obj_data.get("refresh_token")
        token: dict = self.jwt_authentication.refresh_token(refresh_token)

        return token
