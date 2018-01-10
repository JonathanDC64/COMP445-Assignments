import argparse
import get
import post
import urlparser

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("action", help="", choices=['get', 'post'])
parser.add_argument("-v", help="", action='store_true')
parser.add_argument("-h", help="")
parser.add_argument("-d", help="")
parser.add_argument("-f", help="")
parser.add_argument("URL", help="")
args = parser.parse_args()

url = args.URL
action = args.action

host = urlparser.get_host(url)

response = ''

if action == 'get':
    response = get.get(host, urlparser.get_path(url))
elif action == 'post':
    response = post.post(host, urlparser.get_path(url), {})

if args.v:
    print(response.get_header())

print(response.get_body())
    