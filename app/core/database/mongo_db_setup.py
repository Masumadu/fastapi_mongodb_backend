import mongoengine
import mongomock

from app import constants
from config import settings

# reminder: establishing a connection to mongodb
if settings.fastapi_config == constants.TESTING_ENVIRONMENT:
    mongoengine_connection = mongoengine.connect(
        settings.db_name,
        hosnt="mongodb://localhost",
        mongo_client_class=mongomock.MongoClient,
    )
else:
    mongoengine_connection = mongoengine.connect(
        host=settings.db_host,
        db=settings.db_name,
        username=settings.db_user,
        password=settings.db_password,
        authentication_source="admin",
    )
