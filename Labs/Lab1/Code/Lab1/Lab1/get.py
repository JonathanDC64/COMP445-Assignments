import request
import message

#Get request
def get(host: str, path: str, header: str = '') -> message:
    #Append header to message if any
    if header != '':
        header = '\r\n' + header
    msg = f'GET {path} HTTP/1.0\r\nHost: {host}{header}\r\n\r\n'
    return request.req(host, 80, msg)
