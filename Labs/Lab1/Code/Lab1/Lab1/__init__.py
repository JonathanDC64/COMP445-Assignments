import request

host = 'httpbin.org'
print(request.req(host, 80, f'GET /ip HTTP/1.0\r\nHost: {host}\r\n\r\n'))