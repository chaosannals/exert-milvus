from exert.indexer import Indexer

indexer = Indexer('exert')
try:
    indexer.init(True)
    
except Exception as e:
    print(e)