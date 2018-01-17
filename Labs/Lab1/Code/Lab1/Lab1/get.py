import request

#Get request
def get(host: str, path: str, header: str = '') -> str:
    #Append header to message if any
    if header != '':
        header = '\r\n' + header
    message = f'GET {path} HTTP/1.0\r\nHost: {host}{header}\r\n\r\n'
    return request.req(host, 80, message)
