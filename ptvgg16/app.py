import json
from wsgiref.simple_server import make_server
import action

def dispatch(environ, start_response):
    '''
    调度请求。
    '''

    url_path = environ.get('PATH_INFO')
    n = url_path.strip('/')

    # 没有匹配的功能。
    if not hasattr(action, n):
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
    d = getattr(action, n)
    r = d()
    start_response('400 Bad Request' if r['code'] > 0 else '200 OK', [
        ('Content-Type', 'application/json; charset=utf-8'),
    ])
    return [json.dumps(r, ensure_ascii=False).encode('utf-8')]

server = make_server('', 9530, dispatch)
server.serve_forever()