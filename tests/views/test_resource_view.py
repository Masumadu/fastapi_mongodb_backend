from unittest import mock

import pytest

from app.api.api_v1.endpoints import resource_router_base_url
from app.enums import TokenTypeEnum
from tests.base_test_case import BaseTestCase


class TestResourceView(BaseTestCase):
    @pytest.mark.view
    def test_get_resource(self, test_app):
        response = test_app.get(
            f"{resource_router_base_url}/",
            params={"resource_id": self.resource_model.id},
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_create_resource(self, test_app):
        response = test_app.post(
            f"{resource_router_base_url}/", json=self.resource_test_data.create_resource
        )
        response_data = response.json()
        assert response.status_code == 201
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_update_resource(self, test_app):
        response = test_app.patch(
            f"{resource_router_base_url}/{self.resource_model.id}",
            json=self.resource_test_data.update_resource,
            headers=self.headers,
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_delete_resource(self, test_app):
        response = test_app.delete(
            f"{resource_router_base_url}/{self.resource_model.id}", headers=self.headers
        )
        assert response.status_code == 204

    @pytest.mark.view
    def test_get_token(self, test_app):
        response = test_app.get(f"{resource_router_base_url}/get-token/")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    @mock.patch("app.utils.auth.jwt.decode")
    def test_fresh_token(self, mock_decode_token, test_app):
        mock_decode_token.return_value = self.mock_decode_token(
            TokenTypeEnum.refresh_token.value
        )
        response = test_app.post(
            f"{resource_router_base_url}/refresh-token/",
            json={"refresh_token": self.refresh_token},
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)
