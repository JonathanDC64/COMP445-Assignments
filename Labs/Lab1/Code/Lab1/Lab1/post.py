import request
from typing import Dict

def post(host: str, path: str, params: Dict) -> str:
    body = ''
    for key in params:
        body += key + '=' + params[key] + '&'
    body = body[:-1]
    message = f'POST {path} HTTP/1.0\r\nHost: {host}\r\n\r\n{body}'
    print(message)
    return request.req(host, 80, message)
