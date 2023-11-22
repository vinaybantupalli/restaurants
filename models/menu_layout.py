from mongoengine import EmbeddedDocument, StringField, ListField, EmbeddedDocumentField, DictField


class MenuLayout(EmbeddedDocument):
    # Field to store the order of categories at this level
    sort_order = ListField(StringField())
    # Field to store the layout map of categories to nested MenuLayout dictionaries or None
    layout = DictField(EmbeddedDocumentField('self'), default={})
