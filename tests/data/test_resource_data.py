class ResourceTestData:
    @property
    def exiting_resource(self):
        return {
            "title": "resource_title",
            "content": "resource_content",
        }

    @property
    def create_resource(self):
        return {
            "title": "new_title",
            "content": "new_content",
        }

    @property
    def update_resource(self):
        return {
            "content": "updated_content",
        }
