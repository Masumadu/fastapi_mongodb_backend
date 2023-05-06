import pytest

from app.models import ResourceModel
from tests.base_test_case import BaseTestCase


class TestResourceModels(BaseTestCase):
    @pytest.mark.model
    def test_resource_model(self, test_app):
        result = ResourceModel.objects.get(pk=self.resource_model.id)
        assert result
        assert hasattr(result, "id")
        assert hasattr(result, "title")
        assert hasattr(result, "content")
        assert hasattr(result, "created")
        assert hasattr(result, "modified")
        assert result.id is not None
        assert result.created is not None
        assert result.modified is not None
