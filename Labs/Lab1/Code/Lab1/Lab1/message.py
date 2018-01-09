class message:
    __header = ''
    __body = ''
    
    def __init__(self, header: str, body: str) -> None:
        self.__header = header
        self.__body = body
        
    def get_header(self):
        return self.__header
    
    def get_body(self):
        return self.__body