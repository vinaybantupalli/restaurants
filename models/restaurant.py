from datetime import datetime

from mongoengine import Document, StringField, SequenceField, EmbeddedDocumentField, ListField, DictField, DateTimeField

from models.item import Item
from models.menu_layout import MenuLayout


class Restaurant(Document):
    id = SequenceField(primary_key=True)
    name = StringField(required=True, max_length=100)
    metadata = DictField()
    items = ListField(EmbeddedDocumentField(Item))
    # menu_layout will have 2 fields.
    # sort_order which will contain a list of categories at this level, to be shown in that order in the UI
    # layout map of these categories as keys with values being menu_layout type dictionaries, or None for last layer
    # these categories would be referenced in the items.tags list
    menu_layout = EmbeddedDocumentField(MenuLayout)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())

    def __repr__(self):
        return f'<Restaurant(id={self.id}, name={self.name})>'
