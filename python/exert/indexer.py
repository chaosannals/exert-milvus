from milvus import Milvus, MetricType, IndexType
from . import ExertMilvusException


class Indexer:
    '''
    索引器。
    '''

    def __init__(self, name, host='127.0.0.1', port='19530'):
        '''
        初始化。
        '''
        self.client = Milvus(host=host, port=port)
        self.collection = name

    def init(self, lenient=False):
        '''
        创建集合。
        '''
        if lenient:
            status, result = self.client.has_collection(
                collection_name=self.collection
            )
            if status.code != 0:
                raise ExertMilvusException(status)
            if result:
                return

        status = self.client.create_collection({
            'collection_name': self.collection,
            'dimension': 512,
            'index_file_size': 1024,
            'metric_type': MetricType.L2
        })
        if status.code != 0 and not (lenient and status.code == 9):
            raise ExertMilvusException(status)

        # 创建索引。
        status = self.client.create_index(
            collection_name=self.collection,
            index_type=IndexType.IVF_FLAT,
            params={
                'nlist': 16384
            }
        )
        if status.code != 0:
            raise ExertMilvusException(status)

        return status

    def drop(self):
        '''
        删除集合。
        '''
        status = self.client.drop_collection(
            collection_name=self.collection
        )
        if status.code != 0:
            raise ExertMilvusException(status)

    def flush(self):
        '''
        写入到硬盘。
        '''
        status = self.client.flush([self.collection])
        if status.code != 0:
            raise ExertMilvusException(status)

    def compact(self):
        '''
        压缩集合。
        '''
        status = self.client.compact(
            collection_name=self.collection
        )
        if status.code != 0:
            raise ExertMilvusException(status)

    def close(self):
        '''
        关闭链接。
        '''
        self.client.close()

    def new_tag(self, tag):
        '''
        建分块标签。
        '''
        status = self.client.create_partition(
            collection_name=self.collection,
            partition_tag=tag
        )
        if status.code != 0:
            raise ExertMilvusException(status)

    def list_tag(self):
        '''
        列举分块标签。
        '''
        status, result = self.client.list_partitions(
            collection_name=self.collection
        )
        if status.code != 0:
            raise ExertMilvusException(status)
        return result

    def drop_tag(self, tag):
        '''
        删除分块标签。
        '''
        status = self.client.drop_partition(
            collection_name=self.collection,
            partition_tag=tag
        )
        if status.code != 0:
            raise ExertMilvusException(status)

    def index(self, vectors, tag=None, ids=None):
        '''
        添加索引
        '''
        params = {}
        if tag != None:
            params['tag'] = tag
        if ids != None:
            params['ids'] = ids
        status, result = self.client.insert(
            collection_name=self.collection,
            records=vectors,
            params=params
        )
        if status.code != 0:
            raise ExertMilvusException(status)

        return result

    def listing(self, ids):
        '''
        列举信息。
        '''
        status, result = self.client.get_entity_by_id(
            collection_name=self.collection,
            ids=ids
        )
        if status.code != 0:
            raise ExertMilvusException(status)
        return result

    def counting(self):
        '''
        计算索引数。
        '''
        status, result = self.client.count_entities(
            collection_name=self.collection
        )
        if status.code != 0:
            raise ExertMilvusException(status)
        return result

    def unindex(self, ids):
        '''
        去掉索引。
        '''
        status = self.client.delete_entity_by_id(
            collection_name=self.collection,
            id_array=ids
        )
        if status.code != 0:
            raise ExertMilvusException(status)

    def search(self, vectors, top_count=100):
        params= {'nprobe': 16}
        status, results = self.client.search(
            collection_name=self.collection,
            query_records=vectors,
            top_k=top_count,
            params=params
        )
        if status.code != 0:
            raise ExertMilvusException(status)
        return results