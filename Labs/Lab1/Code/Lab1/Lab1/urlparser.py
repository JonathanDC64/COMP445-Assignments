
def get_query_parameters(url: str) -> str:
    startpos = url.find("?") 
    if startpos < 0:
        return ''
    else:
        startpos += 1
        return url[startpos :  startpos + (len(url) - startpos)]

def get_host(url: str) -> str:
    path = url.find('/')
    query = url.find('?')
    if path < 0 and query < 0:
        return url  
    endpos = 0    
    if path < 0:
        endpos = query
    else:
        endpos = path
    return url[0:endpos]


def get_path_no_params(url: str) -> str:
    startpos = url.find('/')
    endpos = url.find('?')
    if startpos < 0:
        return '/'
    if endpos < 0:
        return url[startpos:]
    else:
        return url[startpos:endpos]


def get_path(url: str) -> str:
    startpos = url.find('/')
    if startpos < 0:
        return '/'
    else:
        return url[startpos:]