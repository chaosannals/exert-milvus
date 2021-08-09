class ExertException(Exception):
    '''
    异常基础类。
    '''

    def __init__(self, message, *args):
        super().__init__(*args)
        self.message = message

    def __str__(self):
        return self.message
        
class ExertMilvusException(ExertException):
    '''
    Milvus 相关异常。
    '''

    def __init__(self, status):
        super().__init__(status.message)
        self.code = status.code

    def __str__(self):
        return '[{}] {}'.format(self.code, self.message)
        
        