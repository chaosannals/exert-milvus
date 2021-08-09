from pymilvus_orm import connections, Collection, FieldSchema, CollectionSchema
from pymilvus_orm.types import DataType

class Indexer:
    def __init__(self, name):
        connections.add_connection(default={
            'host': '127.0.0.1',
            'port': '19530',
        })
        connections.connect(alias=name)
        id_field = FieldSchema(name='id', is_primary=True, dtype=DataType.INT64, description='id')
        image_field = FieldSchema(name='image', dtype=DataType.FLOAT_VECTOR, dim=512, description='image')
        
        schema = CollectionSchema(fields=[id_field, image_field], primary_field='id')
        collection = Collection(name=name, schema=schema)