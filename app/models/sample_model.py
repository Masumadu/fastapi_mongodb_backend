from datetime import datetime

from mongoengine import DateTimeField, Document, StringField


class ResourceModel(Document):
    title: str
    content: str
    created: datetime
    modified: datetime

    meta = {"collection": "resource"}
    title = StringField()
    content = StringField()
    created = DateTimeField(default=datetime.now)
    modified = DateTimeField(default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created": self.created,
            "modified": self.modified,
        }
