import re
import mime
import sys
from importlib import reload


def insert_image(environ):
    '''
    '''
    return { 
        'code': 0,
        '2343': 324
    }

def remove_image(environ):
    '''
    '''

    return {
        'code': 0,
        'asdf' : 123
    }

def search_image(environ):
    '''
    '''

    ctype = environ.get('CONTENT_TYPE')
    m = re.match(r'.+?boundary=(.+?)\s*$', ctype)
    b = m.group(1)

    try:
        body_length = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError as e:
        print(e)
        body_length = 0
    body = environ['wsgi.input']
    d = body.read(body_length)
    reload(mime)
    mr = mime.parse_mime(d, b)

    return {
        'code': 0,
        'text': 12321,
        'asdfasd': 234324,
        'mr': mr
    }