import socket
import message

#General/Raw web request
def req(host: str, port: str, msg: str) -> message:
    #Read a buffer of 2KB at a time
    BUFFER = 2048
    #Create a socket
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #Connect  to the host
        conn.connect((host, port))
        #Encode the message in unicode
        request = msg.encode("utf-8")
        #Send request to server
        conn.sendall(request)
        response = b''
        #Keep receiving packets until the EOF is reached
        while  True:
            packet = conn.recv(BUFFER)
            #EOF
            if not packet:
                break
            else:
                response += packet
    finally:
        conn.close()
        
    #Seperate header and body in the response (delimited by \r\n\r\n)
    resp = response.decode("utf-8")
    seperator = resp.find('\r\n\r\n')
    header = resp[:seperator]
    body = resp[seperator+4:]
    
    #Create and return HTTP response message
    respmsg = message.message(header, body);
    return respmsg
