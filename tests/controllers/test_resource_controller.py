from unittest import mock

import pytest
from bson.objectid import ObjectId

from app.core.exceptions import AppException
from app.enums import TokenTypeEnum
from app.models import ResourceModel
from tests.base_test_case import BaseTestCase


class TestResourceController(BaseTestCase):
    @pytest.mark.controller
    def test_get_resource(self, test_app, caplog):
        result = self.resource_controller.get_resource(query_params={})

        assert result
        assert isinstance(result, list)
        assert all([isinstance(obj, ResourceModel) for obj in result])
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.resource_controller.get_resource(
                query_params={"resource_id": ObjectId()}
            )
        assert not_found.value.status_code == 404
        assert "does not exist" in not_found.value.error_message
        assert len(caplog.messages) == 1

    @pytest.mark.controller
    def test_create_resource(self, test_app):
        result = self.resource_controller.create_resource(
            obj_data=self.resource_test_data.create_resource
        )

        assert result
        assert isinstance(result, ResourceModel)
        assert ResourceModel.objects.count() == 2

    @pytest.mark.controller
    def test_update_resource(self, test_app):
        result = self.resource_controller.update_resource(
            obj_id=self.resource_model.id,
            obj_data=self.resource_test_data.update_resource,
        )

        assert result
        assert isinstance(result, ResourceModel)
        assert result.content == self.resource_test_data.update_resource.get("content")

    @pytest.mark.controller
    def test_delete_resource(self, test_app, caplog):
        result = self.resource_controller.delete(obj_id=self.resource_model.id)

        assert ResourceModel.objects.count() == 0
        assert result is None
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.resource_controller.delete(ObjectId())
        assert not_found.value.status_code == 404
        assert "does not exist" in not_found.value.error_message
        assert len(caplog.messages) == 1

    @pytest.mark.controller
    def test_get_token(self, test_app):
        result = self.resource_controller.get_token()

        assert result
        assert isinstance(result, dict)

    @pytest.mark.controller
    @mock.patch("app.utils.auth.jwt.decode")
    def test_refresh_token(self, mock_jwt_decode, test_app):
        mock_jwt_decode.return_value = self.mock_decode_token(
            TokenTypeEnum.refresh_token.value
        )
        result = self.resource_controller.refresh_token(
            obj_data={"refresh_token": self.refresh_token}
        )

        assert result
        assert isinstance(result, dict)
