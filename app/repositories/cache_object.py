from app.core.database import mongoengine_connection as me
from app.models import ResourceModel
from app.schema import ResourceSchema, ResourceSchemaCollection
from app.services import RedisService


def obj_serializer(
    obj_data: ResourceModel, cache_key: str, redis_instance: RedisService
) -> ResourceModel:
    schema_object = ResourceSchema.parse_obj(obj_data.to_dict())
    redis_instance.set(cache_key, schema_object.json())
    return obj_data


def objs_serializer(
    obj_data: me.queryset.QuerySet, cache_key: str, redis_instance: RedisService
) -> [ResourceSchema]:
    resource_collection = ResourceSchemaCollection(obj_data)
    redis_instance.set(cache_key, resource_collection.json())
    return obj_data


def obj_deserializer(obj_data: dict, obj_model: me.Document) -> ResourceModel:
    return obj_model(**obj_data)


def objs_deserializer(obj_data: list) -> [ResourceSchema]:
    return ResourceSchemaCollection(obj_data)
