import request

def get(host: str, path: str) -> str:
    message = f'GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n'
    return request.req(host, 80, message)
