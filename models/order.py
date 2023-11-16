from flask_mongoengine import Document
from mongoengine import IntField, ListField, SequenceField, EmbeddedDocumentField

from models.order_item import OrderItem


class Order(Document):
    restaurant_id = IntField(required=True)
    table_id = ListField(IntField(), required=True)
    order_id = SequenceField(primary_key=True)
    items = ListField(EmbeddedDocumentField(OrderItem))
