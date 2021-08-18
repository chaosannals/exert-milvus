class MimeItem:
    '''
    '''

    def __init__(self) -> None:
        pass

def parse_mime(data, boundary):
    '''
    '''

    rs = data.split(bytes(f'--{boundary}', encoding='utf8'))
    rs = filter(lambda i: len(i) > 0 and i != b'--', map(lambda i: i.strip(b'\r\n'), rs))
    result = []
    for r in rs:
        hs = r.split(b'\r\n')
        info = {}
        for h in hs:
            if len(h) == 0:
                break
            hn, hc = [j.strip().decode('utf8') for j in h.split(b':', 1)]
            info[hn.lower()] = hc
        result.append(info)
    return result