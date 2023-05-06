import json
from typing import Any

from bson import ObjectId as BsonObjectId

# from bson.objectid import ObjectId as BsonObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, BsonObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


# class ObjectIdStr(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, v):
#         try:
#             ObjectId(str(v))
#         except InvalidId:
#             raise ValuerError("Not a valid ObjectId")
#         return str(v)
#
#
# class MongoObjectId(BsonObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, v):
#         if isinstance(v, BsonObjectId):
#             return str(v)
#         elif isinstance(v, str):
#             try:
#                 return BsonObjectId(v)
#             except Exception:
#                 raise TypeError("BsonObjectId required")


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            try:
                BsonObjectId(v)
            except Exception:
                raise ValueError("Not a valid ObjectId")
        return str(v)
