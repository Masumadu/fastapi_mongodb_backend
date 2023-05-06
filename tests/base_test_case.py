import fakeredis
import pytest
from fastapi.testclient import TestClient

from app import constants
from app.controllers import ResourceController
from app.enums import TokenTypeEnum
from app.models import ResourceModel
from app.repositories import ResourceRepository
from app.utils import JwtAuthentication
from config import settings
from tests.data import ResourceTestData
from tests.utils import MockSideEffects


@pytest.mark.usefixtures("app")
class BaseTestCase(MockSideEffects):
    @pytest.fixture
    def test_app(self, app, mocker):
        assert (
            settings.fastapi_config == constants.TESTING_ENVIRONMENT
        ), constants.ENV_ERROR.format(settings.fastapi_config)
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # noqa: E501
        self.refresh_token = self.access_token
        self.token_type = TokenTypeEnum.access_token.value
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        test_client = TestClient(app)
        self.setup_test_data()
        self.setup_patches(mocker, token_type=self.token_type)
        self.instantiate_classes()
        yield test_client

    def setup_test_data(self):
        ResourceModel.objects.delete()
        self.resource_test_data = ResourceTestData()
        self.resource_model = ResourceModel(**self.resource_test_data.exiting_resource)
        self.resource_model.save()

    def instantiate_classes(self):
        self.jwt_authentication = JwtAuthentication()
        self.resource_repository = ResourceRepository(redis_service=self.redis)
        self.resource_controller = ResourceController(
            resource_repository=self.resource_repository,
            jwt_authentication=self.jwt_authentication,
        )

    def setup_patches(self, mocker, **kwargs):
        self.redis = mocker.patch(
            "app.services.redis_service.redis_conn", fakeredis.FakeStrictRedis()
        )
        self.jwt_decode = mocker.patch(
            "app.utils.auth.jwt.decode",
            return_value=self.mock_decode_token(self.token_type),
        )
