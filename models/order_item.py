from mongoengine import EmbeddedDocument, IntField, StringField, DateTimeField


class OrderItem(EmbeddedDocument):
    item_id = IntField(required=True)  # unique item id from Item Model
    batch_id = IntField(required=True)  # if items are ordered in batches, this is incremented
    name = StringField(required=True)  # item name from Item Model
    price = IntField(required=True)
    quantity = IntField(required=True)
    instructions = StringField(required=False)  # cooking instructions for this item
    timestamp = DateTimeField(required=True)  # timestamp at which this item is added to the order
