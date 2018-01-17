import argparse
import get
import post
from urllib.parse import urlparse

HELP = """
httpc is a curl-like application but supports HTTP protocol only.
Usage:
    httpc command [arguments]
The commands are:
    -get executes a HTTP GET request and prints the response.
    -post executes a HTTP POST request and prints the response.
    -help prints this screen."""
    
GET_HELP = """
Usage: httpc get [-v] [-h key:value] URL
Get executes a HTTP GET request for a given URL.
    -v Prints the detail of the response such as protocol,
status, and headers.
    -h key:value Associates headers to HTTP Request with the format 'key:value'.
"""

POST_HELP = """
Usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL
Post executes a HTTP POST request for a given URL with inline data or
from file.
    -v Prints the detail of the response such as protocol, status, and headers.
    -h key:value Associates headers to HTTP Request with the format 'key:value'.
    -d string Associates an inline data to the body HTTP POST request.
    -f file Associates the content of a file to the body HTTP POST request.
    
Either [-d] or [-f] can be used but not both.
"""

parser = argparse.ArgumentParser(add_help=False, usage='httpc.py (-get|-post) [-v] (-h "k:v")* [-d inline-data] [-f file] URL')

#parser.add_argument("action", help="Executes a HTTP GET or POST request and prints the response.", choices=['get', 'post', 'none'], default='none')
parser.add_argument("-get", help="Executes a HTTP GET  request and prints the response.", action="store_true")
parser.add_argument("-post", help="Executes a HTTP POST request and prints the response.", action="store_true")
parser.add_argument("-help", help="Prints this screen.", action="store_true")
parser.add_argument("-v", help="Prints all the status, and its headers, then the contents of the response", action='store_true')
parser.add_argument("-h", help="Passes the headers value to your HTTP operation", action='append')
parser.add_argument("-d", help="Gives the user the possibility to associate the body of the HTTP Request with the inline data,")
parser.add_argument("-f", help="Send body data from file.")
parser.add_argument("URL", help="Determines the targeted HTTP server. It could contain parameters of the HTTP operation.", default='', nargs='?')

#args = parser.parse_args(['post', '-v', 'httpbin.org/post', '-d', 'a=8'])
#args = parser.parse_args(['get','-help'])
args = parser.parse_args()
#print(args)

url = args.URL

#action = args.action

data = ''
if args.d:
    data = args.d

parsedurl = urlparse(url)
scheme = parsedurl.scheme
host = parsedurl.netloc
path = parsedurl.path
query = parsedurl.query


if query:
    path = path + '?' + query

header = ''
if args.h:
    header = '\r\n'.join(map(str,args.h))
    
help = args.help

response = ''

#print(args)
#print(parsedurl)

if help == False and (scheme != 'http' and scheme != 'https'):
    parser.print_usage()
    print("URL must contain either http or https protocol")
else:
    if args.get:
        if help:
            print(GET_HELP)
        else:
            response = get.get(host, path, header)
    elif args.post:
        if help:
            print(POST_HELP)
        else:
            response = post.post(host, path, data, header)
    elif help:
        print(HELP)
    
    if not help:
        if args.v:
            print(response.get_header())
        print(response.get_body())
    