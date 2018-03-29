import threading
from urllib.parse import urlencode
from urllib.request import Request, urlopen


CONNECTIONS = 10    
    
LARGE_DATA = urlencode({'data': "8f1c812e-c49c-4463-a08d-5c528cd02"}).encode()
    
def http_write():
    request = Request("http://127.0.0.1:8080/ThreadFile2.txt",  data=LARGE_DATA, method="POST")
    response = urlopen(request)
    print("write: " + response.read().decode())
    response.close()
    
    
def http_read():
    request = Request("http://127.0.0.1:8080/ThreadFile2.txt")
    response = urlopen(request)
    print("read: " + response.read().decode())
    response.close()

print("Writing...")
#Multiple writes
for i in range(CONNECTIONS):
    threading.Thread(target=http_write, args=()).start()

print("Reading...")
#Multiple reads
for i in range(CONNECTIONS):
    threading.Thread(target=http_read, args=()).start()
    
print("Writing and Reading...")
#Multiple Read/Writes
for i in range(CONNECTIONS):
    threading.Thread(target=http_write, args=()).start()
    threading.Thread(target=http_read, args=()).start()