import random
from exert.indexer import Indexer
from exert.vgg16 import VGG16Extractor

indexer = Indexer('exert')
extractor = VGG16Extractor()
try:
    indexer.init(True)
    v = extractor.extract('asset/test.jpg')
    ids = indexer.index([v])
    print('{} => {}'.format(len(v), ids))
    indexer.flush()
    c = indexer.search([v])
    print(c)
    indexer.unindex([i.id for i in c[0]])
    indexer.close()
except Exception as e:
    print(e)