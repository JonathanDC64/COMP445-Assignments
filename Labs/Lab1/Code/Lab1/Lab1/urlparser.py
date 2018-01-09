
def get_query_parameters(url: str) -> str:
    startpos = url.find("?") 
    if startpos < 0:
        return ''
    else:
        startpos += 1
        return url[startpos :  startpos + (len(url) - startpos)]

def get_path(url: str) -> str:
    endpos = url.find('?')
    if endpos < 0:
        return url
    else:
        return url[0:endpos]
