import argparse
import get
import post
import urlparser
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("action", help="", choices=['get', 'post'])
parser.add_argument("-v", help="", action='store_true')
parser.add_argument("-h", help="", action='append')
parser.add_argument("-d", help="")
parser.add_argument("-f", help="")
parser.add_argument("URL", help="")
args = parser.parse_args()

print(args)



url = args.URL
action = args.action
data = args.d
host = urlparser.get_host(url)
header = '\r\n'.join(map(str,args.h))
response = ''

if action == 'get':
    response = get.get(host, urlparser.get_path(url))
elif action == 'post':
    response = post.post(host, urlparser.get_path(url), data, header)

if args.v:
    print(response.get_header())

print(response.get_body())
    