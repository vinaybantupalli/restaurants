from mongoengine import Document, StringField, SequenceField


class Restaurant(Document):
    id = SequenceField(primary_key=True)
    name = StringField(required=True, max_length=100)

    def __repr__(self):
        return f'<Restaurant(id={self.id}, name={self.name})>'
