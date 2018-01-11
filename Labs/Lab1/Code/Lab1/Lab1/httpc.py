import argparse
import get
import post
import urlparser

parser = argparse.ArgumentParser(add_help=False, usage='httpc.py (get|post) [-v] (-h "k:v")* [-d inline-data] [-f file] URL')

parser.add_argument("action", help="Executes a HTTP GET or POST request and prints the response.", choices=['get', 'post'])
parser.add_argument("-help", help="Prints this screen.", action="help")
parser.add_argument("-v", help="Prints all the status, and its headers, then the contents of the response", action='store_true')
parser.add_argument("-h", help="Passes the headers value to your HTTP operation", action='append')
parser.add_argument("-d", help="Gives the user the possibility to associate the body of the HTTP Request with the inline data,")
parser.add_argument("-f", help="Send body data from file.")
parser.add_argument("URL", help="Determines the targeted HTTP server. It could contain parameters of the HTTP operation. ")

args = parser.parse_args(['get', '-v', 'httpbin.org/ip'])

print(args)

url = args.URL

action = args.action

data = ''
if args.d:
	data = args.d

host = urlparser.get_host(url)

header = ''
if args.h:
	header = '\r\n'.join(map(str,args.h))
	
response = ''

if action == 'get':
    response = get.get(host, urlparser.get_path(url), header)
elif action == 'post':
    response = post.post(host, urlparser.get_path(url), data, header)

if args.v:
    print(response.get_header())

print(response.get_body())
    