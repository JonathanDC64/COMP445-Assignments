import socket

def req(host: str, port: str, msg: str) -> str:
    BUFFER = 2048
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
        request = msg.encode("utf-8")
        conn.sendall(request)
        response = b''
        # Keep receiving packets until the EOF is reached
        while  True:
            packet = conn.recv(BUFFER)
            # EOF
            if not packet:
                break
            else:
                response += packet
    finally:
        conn.close()
    return response.decode("utf-8")
