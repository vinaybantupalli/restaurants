from datetime import datetime

from mongoengine import Document, IntField, ListField, SequenceField, EmbeddedDocumentField, BooleanField, DateTimeField

from models.order_item import OrderItem


class Order(Document):
    restaurant_id = IntField(required=True)
    table_id = IntField(required=True)
    order_id = SequenceField(primary_key=True)
    items = ListField(EmbeddedDocumentField(OrderItem))
    active = BooleanField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
