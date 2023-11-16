from mongoengine import StringField, SequenceField, EmbeddedDocument, ListField, IntField


class Item(EmbeddedDocument):
    id = SequenceField(primary_key=True)
    name = StringField(required=True, max_length=100)
    price = IntField(required=True)
    description = StringField(required=False)
    image = StringField(required=False)
    tags = ListField(StringField(max_length=30))  # list of tags this item belongs to

    def __repr__(self):
        return f'<Item(id={self.id}, name={self.name})>'
