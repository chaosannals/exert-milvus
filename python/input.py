import glob
from exert.indexer import Indexer
from exert.vgg16 import VGG16Extractor
from exert.dbase import DBase

dbase = DBase()
indexer = Indexer('exert')
extractor = VGG16Extractor()

try:
    dbase.init()
    indexer.init(True)
    for p in glob.glob('asset/photo/*.jpg'):
        print(p)
        v = extractor.extract(p)
        ids = indexer.index([v])
        dbase.insert(ids[0], p)
    indexer.close()
except Exception as e:
    print(e)