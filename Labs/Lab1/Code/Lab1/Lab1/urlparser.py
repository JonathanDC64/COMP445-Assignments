from typing import Dict

def get_query_parameters(url: str) -> Dict:
    startpos = url.index("?") + 1
    params = url[startpos :  startpos + (len(url) - startpos)]
    return params