import request
import message

#POST request
def post(host: str, path: str, body: str, header: str = '') -> message:
    #Append header to message if any
    if header != '':
        header = '\r\n' + header
    if path == '':
        path = '/'
    msg = f'POST {path} HTTP/1.0\r\nHost: {host}\r\nContent-Length: {len(body)}{header}\r\n\r\n{body}'
    return request.req(host, 80, msg)
