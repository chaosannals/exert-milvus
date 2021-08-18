import json
import re
import action
import time
import os
import mime
from wsgiref.simple_server import make_server
from types import FunctionType
from importlib import reload
from urllib.parse import parse_qs

class Dispatcher:
    '''
    '''

    def __init__(self):
        '''
        '''

        self.action_mtime = time.time_ns()

    def get_action(self, name):
        '''
        '''

        amt = os.stat(action.__file__).st_mtime_ns

        if amt > self.action_mtime:
            print(f'重载 action')
            reload(action)
            self.action_mtime = amt

        if not hasattr(action, name):
            return None
        r = getattr(action, name)
        if not isinstance(r, FunctionType):
            return None
        return r

    def dispatch(self, environ, start_response):
        '''
        调度请求。
        '''

        url_path = environ.get('PATH_INFO')
        n = url_path.strip('/')

        print(action.__file__)

        # 没有匹配的功能。
        d = self.get_action(n)
        if d == None:
            start_response('404 NOT FOUND', [
                ('Content-Type', 'application/json; charset=utf-8'),
            ])
            return [
                json.dumps({
                    'code': -1,
                    'message': f'无效路径： {url_path}'
                }, ensure_ascii=False).encode('utf-8')
            ]
        
        # 请求调度
        body = environ['wsgi.input']
        ctype = environ.get('CONTENT_TYPE')
        if re.search(r'json', ctype, re.I):
            c = str(body, encoding='utf8')
        elif re.search(r'boundary=', ctype, re.I):
            pass
            #c = mime.parse_mime(body, 'aa')
        print(f'boyd: {ctype}')
        r = d(environ)
        start_response('400 Bad Request' if r['code'] > 0 else '200 OK', [
            ('Content-Type', 'application/json; charset=utf-8'),
        ])
        return [json.dumps(r, ensure_ascii=False).encode('utf-8')]

def main():
    '''
    '''
    dispatcher = Dispatcher()
    with make_server('', 9535, dispatcher.dispatch) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    main()