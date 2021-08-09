import sys
from exert.indexer import Indexer
from exert.vgg16 import VGG16Extractor
from exert.dbase import DBase

dbase = DBase()
indexer = Indexer('exert')
extractor = VGG16Extractor()

try:
    dbase.init()
    indexer.init(True)
    v = extractor.extract(sys.argv[1])
    c = indexer.search([v])
    ids = [i.id for i in c[0]]
    print(f'id count: {len(ids)}')
    r = dbase.get_by_ids(ids)
    for i in r:
        print(f'{i[0]} : {i[1]}')
    indexer.close()
except Exception as e:
    print(e)